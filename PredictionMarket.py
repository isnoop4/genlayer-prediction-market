# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }
from genlayer import *

class AIPredictionMarket(gl.Contract):
    question: str
    is_resolved: bool
    outcome: str

    def __init__(self, question: str):
        self.question = question
        self.is_resolved = False
        self.outcome = "PENDING"

    @gl.public.write
    def resolve_market(self, news_summary: str) -> str:
        if self.is_resolved:
            return f"Market already resolved as: {self.outcome}"

        q = self.question

        # Call the nondeterministic LLM directly inside the consensus block
        def call_llm() -> str:
            prompt = (
                f"Analyze the following verifiable news evidence strictly:\n"
                f"News Evidence: \"{news_summary}\"\n\n"
                f"Question: \"{q}\"\n\n"
                f"Based ONLY on the provided news evidence, has the event happened?\n"
                f"Respond with EXACTLY one word: YES or NO. Do not add any other text."
            )
            return gl.nondet.exec_prompt(prompt)

        # Apply Comparative Consensus on the LLM output
        llm_decision = gl.eq_principle.ComparativeEq(call_llm)
        clean_result = str(llm_decision).strip().upper()

        if "YES" in clean_result:
            self.outcome = "YES"
            self.is_resolved = True
            return "RESOLVED: YES"
        elif "NO" in clean_result:
            self.outcome = "NO"
            self.is_resolved = True
            return "RESOLVED: NO"
        else:
            return f"UNCLEAR: {clean_result}"
