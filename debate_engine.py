import asyncio
from typing import List, Dict
from llm_clients import call_openai, call_anthropic, call_gemini, call_grok

class DebateEngine:
    def __init__(self):
        self.models = {
            "OpenAI GPT": call_openai,
            "Anthropic Claude": call_anthropic,
            "Google Gemini": call_gemini,
            "xAI Grok": call_grok
        }
    
    async def run_debate(self, question: str, rounds: int = 2) -> Dict:
        """
        Run a debate between multiple LLMs.
        
        Args:
            question: The question to debate
            rounds: Number of debate rounds (default 2)
        
        Returns:
            Dictionary containing debate history and final synthesis
        """
        debate_history = []
        
        # Round 1: Initial responses
        round_1_prompt = f"You are participating in a multi-AI debate. Please provide your initial answer to this question:\n\n{question}\n\nBe clear, concise, and explain your reasoning."
        
        debate_history.append({
            "round": 1,
            "description": "Initial responses",
            "responses": await self._get_all_responses(round_1_prompt)
        })
        
        # Additional rounds: Critique and refine
        for round_num in range(2, rounds + 1):
            previous_responses = debate_history[-1]["responses"]
            other_responses_text = self._format_other_responses(previous_responses)
            
            round_prompt = f"""You are participating in a multi-AI debate on this question:

{question}

Here are the responses from other AI models in the previous round:

{other_responses_text}

Please review these perspectives, critique any weaknesses you see, and refine your own answer. Be respectful but candid."""
            
            debate_history.append({
                "round": round_num,
                "description": f"Round {round_num}: Critique and refinement",
                "responses": await self._get_all_responses(round_prompt)
            })
        
        # Final synthesis
        all_perspectives = self._format_all_rounds(debate_history)
        synthesis_prompt = f"""You are synthesizing a debate between multiple AI models on this question:

{question}

Here is the complete debate history:

{all_perspectives}

Please provide a final, synthesized answer that:
1. Integrates the strongest points from all perspectives
2. Addresses any disagreements or conflicts
3. Provides a clear, actionable conclusion

Be comprehensive but concise."""
        
        final_answer = await call_anthropic(synthesis_prompt)
        
        return {
            "question": question,
            "debate_history": debate_history,
            "final_answer": final_answer
        }
    
    async def _get_all_responses(self, prompt: str) -> List[Dict[str, str]]:
        """Get responses from all models concurrently."""
        tasks = [
            self._get_model_response(name, func, prompt)
            for name, func in self.models.items()
        ]
        return await asyncio.gather(*tasks)
    
    async def _get_model_response(self, name: str, func, prompt: str) -> Dict[str, str]:
        """Get response from a single model."""
        response = await func(prompt)
        return {
            "model": name,
            "response": response
        }
    
    def _format_other_responses(self, responses: List[Dict[str, str]]) -> str:
        """Format other models' responses for the next round."""
        formatted = []
        for resp in responses:
            formatted.append(f"**{resp['model']}:**\n{resp['response']}\n")
        return "\n".join(formatted)
    
    def _format_all_rounds(self, debate_history: List[Dict]) -> str:
        """Format all debate rounds for final synthesis."""
        formatted = []
        for round_data in debate_history:
            formatted.append(f"\n=== Round {round_data['round']}: {round_data['description']} ===\n")
            for resp in round_data["responses"]:
                formatted.append(f"**{resp['model']}:**\n{resp['response']}\n")
        return "\n".join(formatted)
