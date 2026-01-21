"""
Consensus models for LLM abstraction
"""
from abc import ABC, abstractmethod

class SimpleLLMModel(ABC):
    """Base class for LLM clients used in consensus engine"""
    
    @abstractmethod
    async def ask(self, prompt: str) -> str:
        """Ask the LLM a question and return response"""
        pass

