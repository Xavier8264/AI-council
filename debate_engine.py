import asyncio
from typing import List, Dict, Optional
from model_registry import ModelRegistry, responses_consensus

class DebateEngine:
    def __init__(self, registry: Optional[ModelRegistry] = None):
        self.registry = registry or ModelRegistry()

    async def run_debate(self, question: str, rounds: int = 2) -> Dict:
        """Original fixed-round debate (backwards compatible)."""
        debate_history = []
        round_prompt_base = (
            "You are participating in a multi-AI debate. "
            "Provide your answer and reasoning concisely. Question:\n\n" + question
        )
        debate_history.append({
            "round": 1,
            "description": "Initial responses",
            "responses": await self.registry.generate_all(round_prompt_base)
        })
        for round_num in range(2, rounds + 1):
            prev = debate_history[-1]["responses"]
            other_text = self._format_other_responses(prev)
            prompt = (
                f"You are refining your perspective on the question:\n\n{question}\n\n"
                "Here are other models' previous responses:\n\n"
                f"{other_text}\n"
                "Critique weaknesses briefly then present an improved, clear answer."
            )
            debate_history.append({
                "round": round_num,
                "description": f"Round {round_num}: Critique and refinement",
                "responses": await self.registry.generate_all(prompt)
            })
        synthesis = await self._synthesize(question, debate_history)
        return {"question": question, "debate_history": debate_history, "final_answer": synthesis}

    async def run_until_consensus(self, question: str, max_rounds: int = 6, similarity_threshold: float = 0.85) -> Dict:
        """Iterate rounds until responses are in consensus or max rounds reached."""
        debate_history = []
        round_num = 1
        consensus = False
        while round_num <= max_rounds and not consensus:
            if round_num == 1:
                prompt = (
                    "You are part of an AI council. Provide a clear initial answer "
                    f"to the question and reasoning. Question:\n\n{question}"
                )
            else:
                prev = debate_history[-1]["responses"]
                other_text = self._format_other_responses(prev)
                prompt = (
                    f"We seek unanimous consent on: {question}\n\n"
                    "Previous round responses:\n\n"
                    f"{other_text}\n"
                    "Identify converging points. Adjust your answer to maximize shared agreement while remaining accurate."
                )
            responses = await self.registry.generate_all(prompt)
            debate_history.append({
                "round": round_num,
                "description": "Consensus iteration" if round_num > 1 else "Initial responses",
                "responses": responses
            })
            resp_texts = [r["response"] for r in responses]
            consensus = responses_consensus(resp_texts, threshold=similarity_threshold)
            round_num += 1
        synthesis = await self._synthesize(question, debate_history, consensus=consensus)
        return {
            "question": question,
            "debate_history": debate_history,
            "consensus_reached": consensus,
            "final_answer": synthesis
        }

    async def _synthesize(self, question: str, debate_history: List[Dict], consensus: bool = False) -> str:
        all_text = self._format_all_rounds(debate_history)
        mode_line = "Consensus achieved" if consensus else "Consensus not fully achieved"
        synth_prompt = (
            f"You are synthesizing an AI council debate. {mode_line}.\n\nQuestion:\n{question}\n\nDebate history:\n{all_text}\n\n"
            "Provide a final consolidated answer that captures strongest shared points, resolves conflicts, and is actionable."
        )
        # Offline-only synthesis using the first available local model
        first = self.registry.models[0] if self.registry.models else None
        if first:
            return await first.generate(synth_prompt)
        return "No models available for synthesis."

    def _format_other_responses(self, responses: List[Dict[str, str]]) -> str:
        formatted = []
        for r in responses:
            formatted.append(f"**{r['model']}:**\n{r['response']}\n")
        return "\n".join(formatted)

    def _format_all_rounds(self, history: List[Dict]) -> str:
        out = []
        for rd in history:
            out.append(f"\n=== Round {rd['round']} ({rd['description']}) ===\n")
            for resp in rd["responses"]:
                out.append(f"**{resp['model']}:**\n{resp['response']}\n")
        return "\n".join(out)
