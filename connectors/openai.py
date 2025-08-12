import os
from typing import List, Dict, Any, Optional
from openai import OpenAI

from utils.oauth_token import OAuthToken
from utils.ssl_cert import get_ssl_client

class OpenAIConnector:
    def __init__(self):
        self.oauth_manager = OAuthToken()
        self.client = self._initialize_client()
    
    def _initialize_client(self) -> OpenAI:
        """Initialize OpenAI client with proper configuration"""
        # Get base URL from environment
        base_url = os.getenv('BASE_URL', 'https://api.openai.com/v1')
        
        # Get authentication token (API key or OAuth token)
        auth_token = self.oauth_manager.get_token()
        
        # Get SSL client if needed
        http_client = get_ssl_client()
        
        return OpenAI(
            api_key=auth_token,
            base_url=base_url,
            http_client=http_client
        )
    
    def chat(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> Any:
        """Send chat completion request"""
        # Refresh token if using OAuth
        if os.getenv('USE_OAUTH', 'false').lower() == 'true':
            self.client.api_key = self.oauth_manager.get_token()
        
        # Use defaults from environment if not specified
        model = model or os.getenv('MODEL', 'gpt-4-turbo-preview')
        temperature = temperature if temperature is not None else float(os.getenv('TEMPERATURE', '0.7'))
        max_tokens = max_tokens or int(os.getenv('MAX_TOKENS', '2000'))
        
        try:
            return self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                **kwargs
            )
        except Exception as e:
            if "401" in str(e) and os.getenv('USE_OAUTH', 'false').lower() == 'true':
                # Token might be expired, force refresh
                print("Auth failed, refreshing token...")
                self.oauth_manager.token = None
                self.client.api_key = self.oauth_manager.get_token()
                
                # Retry once
                return self.client.chat.completions.create(
                    model=model,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    **kwargs
                )
            raise