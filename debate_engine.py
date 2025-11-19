"""
Debate engine that orchestrates multiple LLM rounds to discuss a question.
"""

import asyncio
from typing import List, Dict, Callable, Any
from llm_clients import call_openai, call_anthropic, call_gemini, call_grok


class DebateEngine:
    """
    Manages the debate process between multiple LLMs.
    """
    
    def __init__(self):
        # Map of model names to their respective async functions
        self.models = {
            "OpenAI (GPT-4)": call_openai,
            "Anthropic (Claude)": call_anthropic,
            "Google (Gemini)": call_gemini,
            "xAI (Grok)": call_grok
        }
    
    async def run_debate(
        self, 
        question: str, 
        selected_models: List[str], 
        rounds: int = 2
    ) -> Dict[str, Any]:
        """
        Run a debate between selected models.
        
        Args:
            question: The question to debate
            selected_models: List of model names to participate
            rounds: Number of debate rounds (default: 2)
            
        Returns:
            Dictionary containing the debate history and final answer
        """
        if not selected_models:
            return {
                "error": "No models selected",
                "debate_history": [],
                "final_answer": ""
            }
        
        debate_history = []
        context = ""
        
        # Run debate rounds
        for round_num in range(1, rounds + 1):
            round_responses = []
            
            # Build the prompt for this round
            if round_num == 1:
                prompt = f"Question: {question}\n\nPlease provide your answer and reasoning."
            else:
                prompt = (
                    f"Question: {question}\n\n"
                    f"Previous responses from other models:\n{context}\n\n"
                    f"Based on the above discussion, provide your updated answer and reasoning. "
                    f"You may agree, disagree, or refine your position."
                )
            
            # Get responses from all selected models in parallel
            tasks = []
            for model_name in selected_models:
                if model_name in self.models:
                    tasks.append(self._call_model(model_name, prompt))
            
            responses = await asyncio.gather(*tasks)
            
            # Collect responses for this round
            for model_name, response in zip(selected_models, responses):
                round_responses.append({
                    "model": model_name,
                    "response": response
                })
            
            debate_history.append({
                "round": round_num,
                "responses": round_responses
            })
            
            # Update context for next round
            context = self._build_context(round_responses)
        
        # Generate final synthesized answer
        final_answer = await self._generate_final_answer(question, debate_history)
        
        return {
            "question": question,
            "debate_history": debate_history,
            "final_answer": final_answer
        }
    
    async def _call_model(self, model_name: str, prompt: str) -> str:
        """
        Call a specific model with error handling.
        
        Args:
            model_name: Name of the model to call
            prompt: The prompt to send
            
        Returns:
            The model's response
        """
        try:
            model_func = self.models.get(model_name)
            if model_func:
                return await model_func(prompt)
            else:
                return f"Error: Unknown model {model_name}"
        except Exception as e:
            return f"Error calling {model_name}: {str(e)}"
    
    def _build_context(self, responses: List[Dict[str, str]]) -> str:
        """
        Build context string from previous responses.
        
        Args:
            responses: List of response dictionaries
            
        Returns:
            Formatted context string
        """
        context_parts = []
        for resp in responses:
            context_parts.append(f"{resp['model']}: {resp['response']}")
        return "\n\n".join(context_parts)
    
    async def _generate_final_answer(
        self, 
        question: str, 
        debate_history: List[Dict[str, Any]]
    ) -> str:
        """
        Generate a final synthesized answer based on the debate.
        
        Args:
            question: The original question
            debate_history: Full history of the debate
            
        Returns:
            Final synthesized answer
        """
        # Build summary of the debate
        summary_parts = [f"Question: {question}\n\nDebate Summary:"]
        
        for round_data in debate_history:
            round_num = round_data["round"]
            summary_parts.append(f"\nRound {round_num}:")
            for resp in round_data["responses"]:
                summary_parts.append(f"- {resp['model']}: {resp['response'][:200]}...")
        
        debate_summary = "\n".join(summary_parts)
        
        # Use the first available model to synthesize
        synthesis_prompt = (
            f"{debate_summary}\n\n"
            f"Based on all the perspectives shared above, provide a final, "
            f"synthesized answer to the question: {question}\n\n"
            f"Your response should integrate the key insights from all viewpoints."
        )
        
        # Try to use OpenAI for synthesis, fallback to first available model
        try:
            final = await call_openai(synthesis_prompt)
            return final
        except:
            # Fallback to first available model
            for model_func in self.models.values():
                try:
                    final = await model_func(synthesis_prompt)
                    return final
                except:
                    continue
            
            return "Unable to generate final synthesis. Please review the debate history above."
