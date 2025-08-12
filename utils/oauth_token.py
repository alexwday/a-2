import os
import requests
from datetime import datetime, timedelta
from typing import Optional

class OAuthToken:
    def __init__(self):
        self.token: Optional[str] = None
        self.expires_at: Optional[datetime] = None
    
    def get_token(self) -> str:
        """Get OAuth token, refreshing if needed"""
        if os.getenv('USE_OAUTH', 'false').lower() != 'true':
            # Not using OAuth, return API key
            return os.getenv('API_KEY', '')
        
        # Check if token needs refresh
        if self.token and self.expires_at and datetime.now() < self.expires_at:
            return self.token
        
        # Request new token
        self._refresh_token()
        return self.token
    
    def _refresh_token(self):
        """Request new OAuth token"""
        oauth_url = os.getenv('OAUTH_URL')
        client_id = os.getenv('CLIENT_ID')
        client_secret = os.getenv('CLIENT_SECRET')
        
        print(f"Requesting OAuth token from {oauth_url}")
        
        # Check if SSL cert is needed
        verify = True
        if os.getenv('USE_SSL', 'false').lower() == 'true':
            ca_bundle = os.getenv('CA_BUNDLE_PATH')
            if ca_bundle and os.path.exists(ca_bundle):
                verify = ca_bundle
        
        response = requests.post(
            oauth_url,
            data={
                'grant_type': 'client_credentials',
                'client_id': client_id,
                'client_secret': client_secret
            },
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            verify=verify,
            timeout=30
        )
        response.raise_for_status()
        
        data = response.json()
        self.token = data['access_token']
        expires_in = data.get('expires_in', 3600)
        self.expires_at = datetime.now() + timedelta(seconds=expires_in - 60)