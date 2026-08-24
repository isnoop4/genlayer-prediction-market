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

    @gl.public.view
    def get_market_state(self) -> dict:
        """Fungsi pembacaan state langsung untuk Frontend."""
        return {
            "question": self.question,
            "is_resolved": self.is_resolved,
            "outcome": self.outcome
        }

    @gl.public.write
    def resolve_market(self, news_summary: str) -> str:
        """Memanggil konsensus AI untuk menyelesaikan prediksi pasar."""
        if self.is_resolved:
            return f"Market already resolved as: {self.outcome}"

        q = self.question

        # Memanggil konsensus AI dengan Lambda + Principle
        result = gl.eq_principle.prompt_comparative(
            lambda: f"Question: {q}\nNews Summary: {news_summary}\nAnalyze if the news summary confirms the question happens. Respond ONLY with 'YES' or 'NO'.",
            "The output must strictly evaluate if the news summary answers the prediction question with YES or NO."
        )

        res_str = str(result).upper()

        if "YES" in res_str:
            self.outcome = "YES"
            self.is_resolved = True
            return "RESOLVED: YES"
        elif "NO" in res_str:
            self.outcome = "NO"
            self.is_resolved = True
            return "RESOLVED: NO"
        else:
            return f"UNCLEAR: {result}"
