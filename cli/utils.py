import questionary
from typing import List, Optional, Tuple, Dict
from rich.console import Console

from cli.models import AnalystType

console = Console()

ANALYST_ORDER = [
    ("Market Analyst", AnalystType.MARKET),
    ("Social Media Analyst", AnalystType.SOCIAL),
    ("News Analyst", AnalystType.NEWS),
    ("Fundamentals Analyst", AnalystType.FUNDAMENTALS),
]

# LLM Provider configurations
PROVIDER_CONFIGS = {
    "OpenAI": {
        "provider": "openai",
        "backend_url": "https://api.openai.com/v1",
        "models": ["o4-mini", "o3", "o3-mini", "gpt-4.1", "gpt-4.1-mini", 
                  "gpt-4.1-nano", "gpt-4o", "gpt-4o-mini", "o1", "o1-mini"],
        "description": "Industry-leading performance, good for production workloads",
        "requirements": "OPENAI_API_KEY environment variable"
    },
    "Anthropic": {
        "provider": "anthropic", 
        "backend_url": "https://api.anthropic.com/v1",
        "models": ["claude-3-5-sonnet-20241022", "claude-3-5-haiku-20241022", 
                  "claude-3-opus-20240229", "claude-3-sonnet-20240229", "claude-3-haiku-20240307"],
        "description": "Excellent reasoning capabilities, strong safety features",
        "requirements": "ANTHROPIC_API_KEY environment variable"
    },
    "Google": {
        "provider": "google",
        "backend_url": "https://generativelanguage.googleapis.com/v1",
        "models": ["gemini-2.5-flash", "gemini-2.0-flash", "gemini-1.5-pro", "gemini-1.5-flash", "gemini-1.0-pro"],
        "description": "Cost-effective, integrated with Google services",
        "requirements": "GOOGLE_API_KEY environment variable"
    },
    "Ollama": {
        "provider": "ollama",
        "backend_url": "http://localhost:11434/v1",
        "models": ["llama3.2", "llama3.1", "llama2", "codellama", "mistral", "phi"],
        "description": "Local/offline inference, privacy-focused, no API costs",
        "requirements": "Ollama server running locally on port 11434"
    },
    "OpenRouter": {
        "provider": "openrouter",
        "backend_url": "https://openrouter.ai/api/v1",
        "models": ["meta-llama/llama-3.2-3b-instruct", "meta-llama/llama-3.1-8b-instruct",
                  "anthropic/claude-3.5-sonnet", "openai/gpt-4o", "google/gemini-2.5-flash", "google/gemini-2.0-flash"],
        "description": "Access to multiple model providers through single API",
        "requirements": "OPENROUTER_API_KEY environment variable"
    }
}


def get_ticker() -> str:
    """Prompt the user to enter a ticker symbol."""
    ticker = questionary.text(
        "Enter the ticker symbol to analyze:",
        validate=lambda x: len(x.strip()) > 0 or "Please enter a valid ticker symbol.",
        style=questionary.Style(
            [
                ("text", "fg:green"),
                ("highlighted", "noinherit"),
            ]
        ),
    ).ask()

    if not ticker:
        console.print("\n[red]No ticker symbol provided. Exiting...[/red]")
        exit(1)

    return ticker.strip().upper()


def get_analysis_date() -> str:
    """Prompt the user to enter a date in YYYY-MM-DD format."""
    import re
    from datetime import datetime

    def validate_date(date_str: str) -> bool:
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", date_str):
            return False
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    date = questionary.text(
        "Enter the analysis date (YYYY-MM-DD):",
        validate=lambda x: validate_date(x.strip())
        or "Please enter a valid date in YYYY-MM-DD format.",
        style=questionary.Style(
            [
                ("text", "fg:green"),
                ("highlighted", "noinherit"),
            ]
        ),
    ).ask()

    if not date:
        console.print("\n[red]No date provided. Exiting...[/red]")
        exit(1)

    return date.strip()


def select_analysts() -> List[AnalystType]:
    """Select analysts using an interactive checkbox."""
    choices = questionary.checkbox(
        "Select Your [Analysts Team]:",
        choices=[
            questionary.Choice(display, value=value) for display, value in ANALYST_ORDER
        ],
        instruction="\n- Press Space to select/unselect analysts\n- Press 'a' to select/unselect all\n- Press Enter when done",
        validate=lambda x: len(x) > 0 or "You must select at least one analyst.",
        style=questionary.Style(
            [
                ("checkbox-selected", "fg:green"),
                ("selected", "fg:green noinherit"),
                ("highlighted", "noinherit"),
                ("pointer", "noinherit"),
            ]
        ),
    ).ask()

    if not choices:
        console.print("\n[red]No analysts selected. Exiting...[/red]")
        exit(1)

    return choices


def select_research_depth() -> int:
    """Select research depth using an interactive selection."""

    # Define research depth options with their corresponding values
    DEPTH_OPTIONS = [
        ("Shallow - Quick research, few debate and strategy discussion rounds", 1),
        ("Medium - Middle ground, moderate debate rounds and strategy discussion", 3),
        ("Deep - Comprehensive research, in depth debate and strategy discussion", 5),
    ]

    choice = questionary.select(
        "Select Your [Research Depth]:",
        choices=[
            questionary.Choice(display, value=value) for display, value in DEPTH_OPTIONS
        ],
        instruction="\n- Use arrow keys to navigate\n- Press Enter to select",
        style=questionary.Style(
            [
                ("selected", "fg:yellow noinherit"),
                ("highlighted", "fg:yellow noinherit"),
                ("pointer", "fg:yellow noinherit"),
            ]
        ),
    ).ask()

    if choice is None:
        console.print("\n[red]No research depth selected. Exiting...[/red]")
        exit(1)

    return choice


def select_llm_provider() -> Dict[str, str]:
    """Select LLM provider using an interactive selection."""
    
    # Create choice options with provider descriptions
    provider_choices = []
    for name, config in PROVIDER_CONFIGS.items():
        display_text = f"{name} - {config['description']}"
        provider_choices.append(questionary.Choice(display_text, value=name))
    
    choice = questionary.select(
        "Select Your [LLM Provider]:",
        choices=provider_choices,
        instruction="\n- Use arrow keys to navigate\n- Press Enter to select",
        style=questionary.Style(
            [
                ("selected", "fg:cyan noinherit"),
                ("highlighted", "fg:cyan noinherit"),
                ("pointer", "fg:cyan noinherit"),
            ]
        ),
    ).ask()

    if choice is None:
        console.print("\n[red]No LLM provider selected. Exiting...[/red]")
        exit(1)

    selected_config = PROVIDER_CONFIGS[choice]
    
    # Display provider information
    console.print(f"\n[cyan]Selected Provider:[/cyan] {choice}")
    console.print(f"[dim]Requirements:[/dim] {selected_config['requirements']}")
    console.print(f"[dim]Backend URL:[/dim] {selected_config['backend_url']}")
    
    # Ask if user wants to use custom backend URL
    use_custom = questionary.confirm(
        "Would you like to use a custom backend URL?",
        default=False
    ).ask()
    
    backend_url = selected_config['backend_url']
    if use_custom:
        backend_url = questionary.text(
            "Enter custom backend URL:",
            default=selected_config['backend_url']
        ).ask()
        if not backend_url:
            backend_url = selected_config['backend_url']
    
    return {
        "provider": selected_config["provider"],
        "backend_url": backend_url,
        "models": selected_config["models"],
        "name": choice
    }


def select_shallow_thinking_agent(available_models: List[str]) -> str:
    """Select shallow thinking llm engine using an interactive selection."""
    
    # Create model options based on available models
    model_choices = []
    for model in available_models:
        # Add descriptions for common models
        if "mini" in model.lower() or "nano" in model.lower() or "flash" in model.lower():
            description = "Fast and efficient for quick tasks"
        elif "haiku" in model.lower():
            description = "Lightweight and fast model"
        else:
            description = "Standard model with good capabilities"
        
        display_text = f"{model} - {description}"
        model_choices.append(questionary.Choice(display_text, value=model))

    choice = questionary.select(
        "Select Your [Quick-Thinking LLM Engine]:",
        choices=model_choices,
        instruction="\n- Use arrow keys to navigate\n- Press Enter to select",
        style=questionary.Style(
            [
                ("selected", "fg:magenta noinherit"),
                ("highlighted", "fg:magenta noinherit"),
                ("pointer", "fg:magenta noinherit"),
            ]
        ),
    ).ask()

    if choice is None:
        console.print(
            "\n[red]No shallow thinking llm engine selected. Exiting...[/red]"
        )
        exit(1)

    return choice


def select_deep_thinking_agent(available_models: List[str]) -> str:
    """Select deep thinking llm engine using an interactive selection."""
    
    # Create model options based on available models
    model_choices = []
    for model in available_models:
        # Add descriptions for common models
        if "o3" in model.lower() or "o1" in model.lower():
            description = "Advanced reasoning model"
        elif "pro" in model.lower() or "opus" in model.lower():
            description = "High-performance model for complex tasks"
        elif "sonnet" in model.lower():
            description = "Balanced model with strong reasoning"
        elif "4o" in model.lower():
            description = "Standard model with solid capabilities"
        else:
            description = "Capable model for analysis tasks"
        
        display_text = f"{model} - {description}"
        model_choices.append(questionary.Choice(display_text, value=model))

    choice = questionary.select(
        "Select Your [Deep-Thinking LLM Engine]:",
        choices=model_choices,
        instruction="\n- Use arrow keys to navigate\n- Press Enter to select",
        style=questionary.Style(
            [
                ("selected", "fg:magenta noinherit"),
                ("highlighted", "fg:magenta noinherit"),
                ("pointer", "fg:magenta noinherit"),
            ]
        ),
    ).ask()

    if choice is None:
        console.print("\n[red]No deep thinking llm engine selected. Exiting...[/red]")
        exit(1)

    return choice
