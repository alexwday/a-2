from typing import List, Dict, Any
from dataclasses import dataclass

@dataclass
class Message:
    """OpenAI message format"""
    role: str  # system, user, assistant
    content: str

@dataclass
class Conversation:
    """Conversation container"""
    messages: List[Message]
    
    def to_openai_format(self) -> List[Dict[str, str]]:
        """Convert to OpenAI API format"""
        return [{"role": msg.role, "content": msg.content} for msg in self.messages]
    
    @classmethod
    def from_openai_format(cls, messages: List[Dict[str, str]]) -> 'Conversation':
        """Create from OpenAI API format"""
        return cls(messages=[Message(**msg) for msg in messages])