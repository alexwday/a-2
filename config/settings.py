import os
from dotenv import load_dotenv
from typing import Tuple

def load_environment():
    """Load environment variables from .env file"""
    load_dotenv()

def validate_environment() -> Tuple[bool, list]:
    """
    Validate that required environment variables are set
    Returns: (is_valid, list_of_errors)
    """
    errors = []
    
    # Check base URL
    if not os.getenv('BASE_URL'):
        errors.append("BASE_URL is required")
    
    # Check authentication
    use_oauth = os.getenv('USE_OAUTH', 'false').lower() == 'true'
    if use_oauth:
        if not os.getenv('OAUTH_URL'):
            errors.append("OAUTH_URL is required when USE_OAUTH=true")
        if not os.getenv('CLIENT_ID'):
            errors.append("CLIENT_ID is required when USE_OAUTH=true")
        if not os.getenv('CLIENT_SECRET'):
            errors.append("CLIENT_SECRET is required when USE_OAUTH=true")
    else:
        if not os.getenv('API_KEY'):
            errors.append("API_KEY is required when USE_OAUTH=false")
    
    # Check SSL
    use_ssl = os.getenv('USE_SSL', 'false').lower() == 'true'
    if use_ssl:
        ca_bundle = os.getenv('CA_BUNDLE_PATH')
        if not ca_bundle:
            errors.append("CA_BUNDLE_PATH is required when USE_SSL=true")
        elif not os.path.exists(ca_bundle):
            errors.append(f"CA bundle file not found: {ca_bundle}")
    
    return len(errors) == 0, errors

def get_config():
    """Get configuration dictionary"""
    return {
        'base_url': os.getenv('BASE_URL'),
        'use_oauth': os.getenv('USE_OAUTH', 'false').lower() == 'true',
        'use_ssl': os.getenv('USE_SSL', 'false').lower() == 'true',
        'model': os.getenv('MODEL', 'gpt-4-turbo-preview'),
        'temperature': float(os.getenv('TEMPERATURE', '0.7')),
        'max_tokens': int(os.getenv('MAX_TOKENS', '2000'))
    }