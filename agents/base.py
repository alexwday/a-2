from abc import ABC, abstractmethod
from typing import List, Dict, Any
from connectors.openai import OpenAIConnector

class BaseAgent(ABC):
    """Base class for all agents in the system"""
    
    def __init__(self, name: str, prompt_file: str = None):
        self.name = name
        self.prompt_file = prompt_file
        self.llm = OpenAIConnector()
    
    @abstractmethod
    def process(self, messages: List[Dict[str, str]]) -> Dict[str, Any]:
        """Process incoming messages and return response"""
        pass
    
    def load_prompt(self) -> str:
        """Load prompt template from YAML file"""
        if not self.prompt_file:
            return ""
        # TODO: Implement YAML loading
        pass