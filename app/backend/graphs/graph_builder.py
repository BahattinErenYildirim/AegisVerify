import networkx as nx

class EvidenceGraph:

    def __init__(self):
        self.graph = nx.DiGraph()

    def add_claim(self, claim: str):
        self.graph.add_node(claim, type="claim")

    def add_evidence(self, claim: str, evidence: str, source: str, confidence: float):
        self.graph.add_node(evidence, type="evidence", source=source, confidence=confidence)
        self.graph.add_edge(evidence, claim, weight=confidence)

    def build_summary(self):
        summary = []

        for node, data in self.graph.nodes(data=True):
            if data.get("type") == "evidence":
                summary.append({
                    "evidence": node,
                    "source": data["source"],
                    "confidence": data["confidence"]
                })

        return summary


class GraphBuilder:
    """Builder for creating evidence graphs from claims and sources"""
    
    def __init__(self):
        self.graph = EvidenceGraph()
    
    def build(self, claim: str, evidence_list: list):
        """
        Build an evidence graph from a claim and list of evidence
        
        Args:
            claim: The main claim to verify
            evidence_list: List of dicts with 'evidence', 'source', 'confidence' keys
            
        Returns:
            dict: Summary of the evidence graph
        """
        self.graph.add_claim(claim)
        
        for evidence_item in evidence_list:
            evidence_text = evidence_item.get("evidence", "")
            source = evidence_item.get("source", "unknown")
            confidence = evidence_item.get("confidence", 0.5)
            
            self.graph.add_evidence(claim, evidence_text, source, confidence)
        
        return self.graph.build_summary()
    
    def get_graph(self):
        """Get the underlying EvidenceGraph instance"""
        return self.graph