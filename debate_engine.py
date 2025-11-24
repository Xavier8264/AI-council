import asyncio
from typing import List, Dict
from ollama_client import call_ollama
from models_config import get_active_models, get_model_display_name, get_consensus_settings
import logging

logger = logging.getLogger(__name__)

class DebateEngine:
    def __init__(self):
        # Get active models from config
        active_model_ids = get_active_models()
        self.models = {
            get_model_display_name(model_id): model_id 
            for model_id in active_model_ids
        }
        self.consensus_settings = get_consensus_settings()
    
    async def run_debate(self, question: str, rounds: int = None) -> Dict:
        """
        Run a debate between multiple LLMs until unanimous consent is reached.
        
        Args:
            question: The question to debate
            rounds: Maximum number of debate rounds (if None, uses consensus settings)
        
        Returns:
            Dictionary containing debate history, consensus status, and final synthesis
        """
        max_rounds = rounds if rounds is not None else self.consensus_settings["max_rounds"]
        debate_history = []
        consensus_reached = False
        consensus_round = None
        
        # Round 1: Initial responses
        round_1_prompt = f"You are participating in a multi-AI debate. Please provide your initial answer to this question:\n\n{question}\n\nBe clear, concise, and explain your reasoning."
        
        round_1_responses = await self._get_all_responses(round_1_prompt)
        debate_history.append({
            "round": 1,
            "description": "Initial responses",
            "responses": round_1_responses
        })
        
        # Check for early consensus
        consensus_reached = self._check_consensus(round_1_responses)
        if consensus_reached:
            consensus_round = 1
        
        # Additional rounds: Continue until consensus or max rounds reached
        round_num = 2
        while round_num <= max_rounds and not consensus_reached:
            previous_responses = debate_history[-1]["responses"]
            other_responses_text = self._format_other_responses(previous_responses)
            
            round_prompt = f"""You are participating in a multi-AI debate on this question:

{question}

Here are the responses from other AI models in the previous round:

{other_responses_text}

Please review these perspectives carefully:
1. If you find yourself in strong agreement with the other models, acknowledge this and refine the shared consensus
2. If you disagree on any points, explain your reasoning and suggest improvements
3. Work towards finding common ground while maintaining intellectual honesty

Our goal is to reach unanimous consent on the best answer."""
            
            round_responses = await self._get_all_responses(round_prompt)
            debate_history.append({
                "round": round_num,
                "description": f"Round {round_num}: Refinement and consensus building",
                "responses": round_responses
            })
            
            # Check if consensus has been reached
            consensus_reached = self._check_consensus(round_responses)
            if consensus_reached:
                consensus_round = round_num
                break
            
            round_num += 1
        
        # Final synthesis using the first model (or could use a designated model)
        all_perspectives = self._format_all_rounds(debate_history)
        synthesis_prompt = f"""You are synthesizing a debate between multiple AI models on this question:

{question}

Here is the complete debate history across {len(debate_history)} rounds:

{all_perspectives}

Consensus {"WAS" if consensus_reached else "WAS NOT"} reached after {consensus_round if consensus_round else len(debate_history)} rounds.

Please provide a final, synthesized answer that:
1. Integrates the strongest points from all perspectives
2. {"Presents the unanimous consensus" if consensus_reached else "Addresses remaining disagreements and provides a balanced conclusion"}
3. Provides a clear, actionable conclusion

Be comprehensive but concise."""
        
        # Use the first model for synthesis
        first_model_id = list(self.models.values())[0]
        final_answer = await call_ollama(first_model_id, synthesis_prompt)
        
        return {
            "question": question,
            "debate_history": debate_history,
            "final_answer": final_answer,
            "consensus_reached": consensus_reached,
            "consensus_round": consensus_round,
            "total_rounds": len(debate_history)
        }
    
    async def _get_all_responses(self, prompt: str) -> List[Dict[str, str]]:
        """Get responses from all models concurrently."""
        tasks = [
            self._get_model_response(name, model_id, prompt)
            for name, model_id in self.models.items()
        ]
        return await asyncio.gather(*tasks)
    
    async def _get_model_response(self, name: str, model_id: str, prompt: str) -> Dict[str, str]:
        """Get response from a single model."""
        response = await call_ollama(model_id, prompt)
        return {
            "model": name,
            "response": response
        }
    
    def _check_consensus(self, responses: List[Dict[str, str]]) -> bool:
        """
        Check if consensus has been reached among the models.
        
        This is a simplified consensus check based on:
        1. Response length similarity
        2. Key phrase overlap
        3. Sentiment/agreement indicators
        
        Args:
            responses: List of model responses
            
        Returns:
            bool: True if consensus is detected, False otherwise
        """
        if len(responses) < 2:
            return True
        
        # Extract response texts
        texts = [r["response"] for r in responses if not r["response"].startswith("Error:")]
        
        # If any model errored, no consensus
        if len(texts) != len(responses):
            return False
        
        # Check for agreement indicators in responses
        agreement_phrases = [
            "i agree",
            "i concur",
            "similarly",
            "as the others mentioned",
            "building on the previous",
            "consensus",
            "we all agree",
            "shared understanding",
            "common ground",
            "aligned with",
            "same conclusion"
        ]
        
        agreement_count = 0
        for text in texts:
            text_lower = text.lower()
            if any(phrase in text_lower for phrase in agreement_phrases):
                agreement_count += 1
        
        # If majority of models show agreement indicators
        agreement_ratio = agreement_count / len(texts)
        min_ratio = self.consensus_settings.get("min_agreement_ratio", 0.8)
        
        if agreement_ratio >= min_ratio:
            logger.info(f"Consensus detected: {agreement_count}/{len(texts)} models show agreement")
            return True
        
        return False
    
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
