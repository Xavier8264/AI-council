"""
Debate Engine - Orchestrates multiple LLMs in a debate format.
"""

import asyncio
from typing import List, Dict, Any
from llm_clients import call_openai, call_anthropic, call_gemini, call_grok


class DebateEngine:
    """
    Manages debate rounds between multiple LLM models.
    """
    
    def __init__(self):
        """Initialize the debate engine with available models."""
        self.models = {
            "openai": call_openai,
            "anthropic": call_anthropic,
            "gemini": call_gemini,
            "grok": call_grok
        }
    
    async def run_debate(
        self, 
        question: str, 
        selected_models: List[str], 
        rounds: int = 2
    ) -> Dict[str, Any]:
        """
        Run a debate with selected models for a given number of rounds.
        
        Args:
            question: The question to debate
            selected_models: List of model names to participate
            rounds: Number of debate rounds (default: 2)
            
        Returns:
            Dictionary containing the debate history and final answer
        """
        debate_history = []
        
        # Validate selected models
        valid_models = [m for m in selected_models if m in self.models]
        if not valid_models:
            return {
                "error": "No valid models selected",
                "debate_history": [],
                "final_answer": ""
            }
        
        # Initial round - each model answers the question independently
        initial_prompt = f"Question: {question}\n\nProvide your answer and reasoning."
        
        round_data = {
            "round": 0,
            "type": "initial",
            "responses": []
        }
        
        # Get initial responses from all models concurrently
        tasks = []
        for model_name in valid_models:
            tasks.append(self._get_model_response(model_name, initial_prompt))
        
        responses = await asyncio.gather(*tasks)
        
        for model_name, response in zip(valid_models, responses):
            round_data["responses"].append({
                "model": model_name,
                "response": response
            })
        
        debate_history.append(round_data)
        
        # Debate rounds - models respond to each other
        for round_num in range(1, rounds + 1):
            # Build context from previous responses
            context = self._build_context(question, debate_history)
            
            debate_prompt = (
                f"{context}\n\n"
                f"Based on the arguments above, provide your response. "
                f"You may agree, disagree, or present a different perspective. "
                f"Be specific and cite reasoning."
            )
            
            round_data = {
                "round": round_num,
                "type": "debate",
                "responses": []
            }
            
            # Get debate responses from all models concurrently
            tasks = []
            for model_name in valid_models:
                tasks.append(self._get_model_response(model_name, debate_prompt))
            
            responses = await asyncio.gather(*tasks)
            
            for model_name, response in zip(valid_models, responses):
                round_data["responses"].append({
                    "model": model_name,
                    "response": response
                })
            
            debate_history.append(round_data)
        
        # Generate final synthesis
        final_answer = await self._generate_final_answer(question, debate_history)
        
        return {
            "question": question,
            "debate_history": debate_history,
            "final_answer": final_answer
        }
    
    async def _get_model_response(self, model_name: str, prompt: str) -> str:
        """
        Get response from a specific model.
        
        Args:
            model_name: Name of the model to query
            prompt: The prompt to send
            
        Returns:
            The model's response
        """
        model_func = self.models.get(model_name)
        if not model_func:
            return f"Error: Model {model_name} not found"
        
        try:
            response = await model_func(prompt)
            return response
        except Exception as e:
            return f"Error calling {model_name}: {str(e)}"
    
    def _build_context(self, question: str, debate_history: List[Dict]) -> str:
        """
        Build context string from debate history.
        
        Args:
            question: The original question
            debate_history: List of previous rounds
            
        Returns:
            Formatted context string
        """
        context = f"Question: {question}\n\n"
        context += "Previous responses:\n\n"
        
        for round_data in debate_history:
            round_num = round_data["round"]
            round_type = round_data["type"]
            
            context += f"--- Round {round_num} ({round_type}) ---\n"
            
            for resp in round_data["responses"]:
                model = resp["model"]
                response = resp["response"]
                context += f"\n{model.upper()}:\n{response}\n"
            
            context += "\n"
        
        return context
    
    async def _generate_final_answer(
        self, 
        question: str, 
        debate_history: List[Dict]
    ) -> str:
        """
        Generate a final synthesized answer based on the debate.
        
        Args:
            question: The original question
            debate_history: Complete debate history
            
        Returns:
            Final synthesized answer
        """
        # Use the first available model to synthesize
        synthesis_model = None
        for model_name in ["openai", "anthropic", "gemini", "grok"]:
            if model_name in self.models:
                synthesis_model = model_name
                break
        
        if not synthesis_model:
            return "Error: No model available for synthesis"
        
        context = self._build_context(question, debate_history)
        
        synthesis_prompt = (
            f"{context}\n\n"
            f"Based on all the arguments and perspectives presented above, "
            f"provide a final, synthesized answer to the original question. "
            f"Consider all viewpoints and provide a balanced, well-reasoned conclusion."
        )
        
        final_answer = await self._get_model_response(synthesis_model, synthesis_prompt)
        
        return final_answer
