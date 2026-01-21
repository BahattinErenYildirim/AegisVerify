class ConsensusEngine:

    def __init__(self, clients: list):
        self.clients = clients

    async def ask_all(self, prompt: str):
        responses = []

        for client in self.clients:
            try:
                res = await client.ask(prompt)
                responses.append(res)
            except:
                pass

        return responses

    def compute_consensus(self, responses):
        """
        Responses → string list
        """
        # Eğer numerical scoring varsa ortalama alınabilir.
        # Bu basit prototype consensus.
        joined = "\n---MODEL BREAK---\n".join(responses)

        return {
            "model_count": len(responses),
            "combined_output": joined
        }
