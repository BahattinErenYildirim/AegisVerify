from pipelines.basic_pipeline import BasicAnalysisPipeline
from consensus.engine import ConsensusEngine
from consensus.geminiclient import GeminiClient

class AdvancedPipeline:

    def __init__(self):
        self.basic = BasicAnalysisPipeline()
        self.consensus = ConsensusEngine([
            GeminiClient(),
            # OpenAIClient(),
            # LlamaClient()
        ])

    async def run(self, text: str):
        basic = self.basic.run(text)

        responses = await self.consensus.ask_all(
            f"Analyze this claim:\n{text}"
        )

        consensus = self.consensus.compute_consensus(responses)

        return {
            "basic_analysis": basic,
            "consensus": consensus
        }
