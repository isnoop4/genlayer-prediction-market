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
        self.verdict_json = json.dumps({"verdict": "PENDING"})

    @gl.public.write
    def resolve_market(self, news_evidence: str) -> str:
        if self.is_resolved:
            return self.verdict_json

        q = self.question

        # Callback HANYA mengeksekusi LLM dan mengembalikan output murni LLM
        def call_nondet() -> str:
            prompt = (
                f"Analyze this news evidence for the prediction: '{q}'.\n"
                f"Evidence: '{news_evidence}'\n\n"
                f"Respond ONLY with a JSON object format:\n"
                f'{{"verdict": "YES" | "NO" | "NEEDS_MORE_EVIDENCE", "confidence": "HIGH" | "MEDIUM" | "LOW"}}'
            )
            return gl.nondet.exec_prompt(prompt)

        # Comparative Consensus mengevaluasi hasil eksekusi model nondeterministik
        raw_result = gl.eq_principle.ComparativeEq(call_nondet)
        
        self.verdict_json = str(raw_result)
        self.is_resolved = True
        return self.verdict_json

    @gl.public.view
    def get_verdict(self) -> str:
        return self.verdict_json
