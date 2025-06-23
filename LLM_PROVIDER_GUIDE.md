# LLM Provider Selection Guide

## Overview
The TradingAgents GUI now supports selecting from multiple LLM providers through an intuitive interface. This allows users to leverage different AI models and services based on their preferences, budget, and requirements.

## Supported Providers

### 1. OpenAI
- **Models**: o4-mini, o3, o3-mini, gpt-4.1, gpt-4.1-mini, gpt-4.1-nano, gpt-4o, gpt-4o-mini, o1, o1-mini
- **Backend URL**: https://api.openai.com/v1
- **Requirements**: OPENAI_API_KEY environment variable
- **Use Case**: Industry-leading performance, good for production workloads

### 2. Anthropic
- **Models**: claude-3-5-sonnet-20241022, claude-3-5-haiku-20241022, claude-3-opus-20240229, claude-3-sonnet-20240229, claude-3-haiku-20240307
- **Backend URL**: https://api.anthropic.com/v1
- **Requirements**: ANTHROPIC_API_KEY environment variable
- **Use Case**: Excellent reasoning capabilities, strong safety features

### 3. Google
- **Models**: gemini-2.5-flash, gemini-2.0-flash, gemini-1.5-pro, gemini-1.5-flash, gemini-1.0-pro
- **Backend URL**: https://generativelanguage.googleapis.com/v1
- **Requirements**: GOOGLE_API_KEY environment variable
- **Use Case**: Cost-effective, integrated with Google services

### 4. Ollama
- **Models**: llama3.2, llama3.1, llama2, codellama, mistral, phi
- **Backend URL**: http://localhost:11434/v1
- **Requirements**: Ollama server running locally on port 11434
- **Use Case**: Local/offline inference, privacy-focused, no API costs

### 5. OpenRouter
- **Models**: meta-llama/llama-3.2-3b-instruct, meta-llama/llama-3.1-8b-instruct, anthropic/claude-3.5-sonnet, openai/gpt-4o, google/gemini-2.5-flash, google/gemini-2.0-flash
- **Backend URL**: https://openrouter.ai/api/v1
- **Requirements**: OPENROUTER_API_KEY environment variable
- **Use Case**: Access to multiple model providers through single API

## GUI Features

### Provider Selection
1. **LLM Provider Dropdown**: Choose from the five supported providers
2. **Dynamic Model Lists**: Available models update based on selected provider
3. **Provider-Specific Warnings**: Contextual help for each provider
4. **Custom Backend URL**: Override default URLs for custom endpoints

### Configuration Display
- **Current Configuration Panel**: Shows active provider, models, and backend URL
- **Real-time Updates**: Configuration changes reflected immediately
- **Historical Analysis**: Saved analyses include provider information

### Smart Reinitialization
- **Automatic Detection**: System detects when provider changes
- **Efficient Reuse**: Reuses agents when only models change within same provider
- **Clean Transitions**: Proper cleanup when switching providers

## Usage Instructions

### 1. Basic Setup
1. Open the TradingAgents GUI
2. In the sidebar, locate the "🤖 LLM Provider" section
3. Select your preferred provider from the dropdown
4. Choose appropriate models for deep and quick thinking

### 2. Provider-Specific Setup

#### OpenAI
```bash
export OPENAI_API_KEY="your-api-key-here"
```

#### Anthropic
```bash
export ANTHROPIC_API_KEY="your-api-key-here"
```

#### Google
```bash
export GOOGLE_API_KEY="your-api-key-here"
```

#### Ollama
```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Pull a model
ollama pull llama3.2

# Start server (usually runs automatically)
ollama serve
```

#### OpenRouter
```bash
export OPENROUTER_API_KEY="your-api-key-here"
```

### 3. Advanced Configuration
- **Custom URLs**: Enable "Use Custom Backend URL" for enterprise endpoints
- **Model Selection**: Choose different models for deep vs quick thinking
- **Cost Optimization**: Use smaller models for quick thinking to reduce costs

## Best Practices

### Model Selection
- **Deep Thinking**: Use larger, more capable models (o3, claude-3-5-sonnet, gemini-2.5-flash, gemini-1.5-pro)
- **Quick Thinking**: Use faster, efficient models (gpt-4o-mini, claude-3-5-haiku, gemini-2.0-flash)

### Cost Management
- **Tier Strategy**: Use premium providers for critical analysis, cost-effective ones for testing
- **Model Pairing**: Combine expensive deep models with cheaper quick models
- **Local Fallback**: Use Ollama for development and testing

### Performance Optimization
- **Provider Switching**: Minimal overhead when changing models within same provider
- **Batch Operations**: System reuses initialized agents when possible
- **Error Handling**: Automatic fallback suggestions on provider failures

## Troubleshooting

### Common Issues
1. **API Key Not Set**: Check environment variables
2. **Ollama Not Running**: Ensure server is started (`ollama serve`)
3. **Rate Limits**: Switch to different provider or adjust request frequency
4. **Model Not Available**: Verify model name and provider compatibility

### Error Messages
- **"Unsupported LLM provider"**: Check provider name in configuration
- **"Connection refused"**: Verify backend URL and network connectivity
- **"Authentication failed"**: Validate API keys and permissions

## Migration Guide

### From Previous Versions
1. Existing analyses remain compatible
2. Default provider is OpenAI (maintains compatibility)
3. New fields automatically added to future analyses
4. Historical analyses show "N/A" for missing provider info

### Configuration Updates
```python
# Old format (still supported)
config = {
    "deep_think_llm": "gpt-4o",
    "quick_think_llm": "gpt-4o-mini"
}

# New format (recommended)
config = {
    "llm_provider": "openai",
    "backend_url": "https://api.openai.com/v1",
    "deep_think_llm": "gpt-4o",
    "quick_think_llm": "gpt-4o-mini"
}
```

## Future Roadmap
- Additional provider support (Azure OpenAI, AWS Bedrock)
- Model performance benchmarking
- Cost tracking and optimization suggestions
- Provider failover and load balancing

---

For technical support or feature requests, please refer to the main project documentation or submit an issue on the project repository. 