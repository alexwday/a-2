# Multi-Agent Finance Assistant

A flexible LLM connector that supports both OpenAI API and internal OAuth-based endpoints with SSL certificates.

## Quick Start

```bash
# Clone and setup
git clone https://github.com/alexwday/a-2.git
cd a-2
./setup.sh

# Configure environment
# Edit .env with your settings (see Configuration below)

# Test connection
python main.py
```

## Manual Setup

If you prefer manual setup or are on Windows:

```bash
# 1. Create virtual environment
python3 -m venv venv

# 2. Activate virtual environment
source venv/bin/activate  # macOS/Linux
# OR
venv\Scripts\activate     # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create configuration
cp .env.example .env
# Edit .env with your settings

# 5. Test
python main.py
```

## Configuration

The `.env` file controls all settings. See `.env.example` for full documentation.

### Local Development (OpenAI)
```env
BASE_URL=https://api.openai.com/v1
USE_OAUTH=false
API_KEY=sk-...your-api-key...
USE_SSL=false
MODEL=gpt-4.1-2025-04-14
```

### Work Environment (Internal)
```env
BASE_URL=https://internal-llm.company.com/v1
USE_OAUTH=true
OAUTH_URL=https://auth.company.com/oauth2/token
CLIENT_ID=your-client-id
CLIENT_SECRET=your-client-secret
USE_SSL=true
CA_BUNDLE_PATH=./rbc-ca-bundle.cer
MODEL=gpt-4.1-2025-04-14
```

## Project Structure

```
/
├── .env.example      # Configuration template
├── .env             # Your configuration (git ignored)
├── main.py          # Entry point
├── setup.sh         # Quick setup script
├── utils/           # Authentication utilities
│   ├── oauth_token.py
│   └── ssl_cert.py
├── connectors/      # LLM connectors
│   └── openai.py
└── config/          # Configuration management
    └── settings.py
```

## Features

- **Dual Environment Support**: Seamlessly switch between OpenAI and internal endpoints
- **OAuth Authentication**: Automatic token generation and refresh
- **SSL Certificate Support**: Custom CA bundle for internal endpoints
- **Environment-based Configuration**: Single `.env` file controls everything

## Testing

After setup, run:
```bash
python main.py
```

This will:
1. Validate your configuration
2. Test the LLM connection
3. Send a sample query
4. Display the response

## Troubleshooting

### OpenAI Issues
- Verify your API key is valid
- Check internet connection
- Ensure API key has proper permissions

### Internal/OAuth Issues
- Verify OAuth endpoint is accessible
- Check CLIENT_ID and CLIENT_SECRET are correct
- Ensure CA bundle file exists (if USE_SSL=true)
- Test OAuth endpoint separately if needed

### Common Errors
- `ModuleNotFoundError`: Run `pip install -r requirements.txt`
- `API key not found`: Check `.env` file exists and has API_KEY set
- `SSL Error`: Verify CA bundle path is correct