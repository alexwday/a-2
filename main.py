#!/usr/bin/env python3

import os
import json
from typing import List, Dict, Any

from config.settings import load_environment, validate_environment, get_config
from connectors.openai import OpenAIConnector
from agents.coordinator import CoordinatorAgent
from utils.monitoring import ProcessMonitor

def process_conversation(messages: List[Dict[str, str]]) -> str:
    """
    Process a conversation through the LLM
    This is where the multi-agent logic will eventually go
    """
    llm = OpenAIConnector()
    
    # For now, just pass through to LLM
    # Later this will route to different agents based on the query
    response = llm.chat(messages=messages)
    
    if response.choices:
        return response.choices[0].message.content
    else:
        return "No response generated"

def main():
    print("=" * 60)
    print("Multi-Agent Finance Assistant")
    print("=" * 60)
    
    # Load and validate environment
    load_environment()
    is_valid, errors = validate_environment()
    if not is_valid:
        print("\nConfiguration errors:")
        for error in errors:
            print(f"  - {error}")
        print("\nPlease fix the configuration errors in .env file")
        return
    
    config = get_config()
    
    # Show configuration
    print("\nConfiguration:")
    print(f"  Base URL: {os.getenv('BASE_URL')}")
    print(f"  Auth Method: {'OAuth' if os.getenv('USE_OAUTH', 'false').lower() == 'true' else 'API Key'}")
    print(f"  SSL Enabled: {os.getenv('USE_SSL', 'false')}")
    print(f"  Model: {os.getenv('MODEL', 'gpt-4-turbo-preview')}")
    
    # Example conversation that would come from the user
    example_conversation = [
        {"role": "system", "content": "You are a financial assistant."},
        {"role": "user", "content": "What were the Q3 earnings highlights?"}
    ]
    
    print("\nProcessing conversation:")
    print(json.dumps(example_conversation, indent=2))
    
    try:
        response = process_conversation(example_conversation)
        print("\nResponse:")
        print(response)
        print("\n✅ Success!")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nTroubleshooting:")
        if os.getenv('USE_OAUTH', 'false').lower() == 'true':
            print("  - Check OAuth endpoint is accessible")
            print("  - Verify CLIENT_ID and CLIENT_SECRET")
        else:
            print("  - Verify API_KEY is valid")
        if os.getenv('USE_SSL', 'false').lower() == 'true':
            print("  - Check CA bundle file exists and is valid")

if __name__ == "__main__":
    main()