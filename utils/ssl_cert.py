import os
import ssl
import httpx
from typing import Optional

def get_ssl_client() -> Optional[httpx.Client]:
    """Get HTTP client with SSL configuration if needed"""
    if os.getenv('USE_SSL', 'false').lower() != 'true':
        return None
    
    ca_bundle_path = os.getenv('CA_BUNDLE_PATH')
    if not ca_bundle_path or not os.path.exists(ca_bundle_path):
        print(f"Warning: SSL enabled but CA bundle not found at {ca_bundle_path}")
        return None
    
    ssl_context = ssl.create_default_context(cafile=ca_bundle_path)
    return httpx.Client(verify=ssl_context)