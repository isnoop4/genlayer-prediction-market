# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }
from genlayer import *
import json

class AIPredictionMarket(gl.Contract):
    question: str
    is_resolved: bool
    verdict_json: str

    def __init__(self, question: str):
        self.question = question
        self.is_resolved = False
        self.verdict_json = json.dumps({
            "verdict": "PENDING",
            "score": 0,
            "reasons": ["Market not resolved yet"],
            "confidence": "LOW"
        })

    @gl.public.write
    def resolve_market(self, news_summary: str) -> str:
        if self.is_resolved:
            return self.verdict_json

        q = self.question

        def call_llm() -> str:
            prompt = (
                f"You are an impartial GenLayer validator evaluating a prediction market.\n\n"
                f"Question: \"{q}\"\n"
                f"Evidence: \"{news_summary}\"\n\n"
                f"Rules:\n"
                f"- Return valid JSON only.\n"
                f"- Do not invent facts not present in the evidence.\n"
                f"- Set verdict to YES, NO, or NEEDS_MORE_EVIDENCE.\n\n"
                f"JSON schema:\n"
                f"{{\n"
                f'  "verdict": "YES" | "NO" | "NEEDS_MORE_EVIDENCE",\n'
                f'  "score": 0-100,\n'
                f'  "reasons": ["reason 1"],\n'
                f'  "confidence": "LOW" | "MEDIUM" | "HIGH"\n'
                f"}}"
            )
            return gl.nondet.exec_prompt(prompt)

        # Comparative consensus on LLM JSON output
        llm_decision = gl.eq_principle.ComparativeEq(call_llm)
        self.verdict_json = str(llm_decision)
        self.is_resolved = True
        return self.verdict_json

    @gl.public.view
    def get_verdict(self) -> str:
        return self.verdict_json

    @gl.public.view
    def get_question(self) -> str:
        return self.question

