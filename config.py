import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration management for the ping agent."""

    # OpenAI API Configuration
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_BASE_URL: str = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")

    # Default Model Configuration
    DEFAULT_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4")
    DEFAULT_PERSONA: str = os.getenv("AGENT_PERSONA", "network_specialist")

    # Agent Configuration
    MAX_CONTEXT_LENGTH: int = int(os.getenv("MAX_CONTEXT_LENGTH", "10"))
    MAX_TOOL_TIMEOUT: int = int(os.getenv("MAX_TOOL_TIMEOUT", "60"))

    # Tool Configuration
    DEFAULT_PING_COUNT: int = int(os.getenv("DEFAULT_PING_COUNT", "4"))
    DEFAULT_PING_TIMEOUT: int = int(os.getenv("DEFAULT_PING_TIMEOUT", "3"))
    DEFAULT_TRACEROUTE_HOPS: int = int(os.getenv("DEFAULT_TRACEROUTE_HOPS", "15"))

    @classmethod
    def validate(cls) -> bool:
        """Validate that required configuration is present."""
        if not cls.OPENAI_API_KEY:
            print("❌ Error: OPENAI_API_KEY environment variable is required")
            print("Please set it in your .env file or environment:")
            print("export OPENAI_API_KEY='your-api-key-here'")
            return False
        return True

    @classmethod
    def get_available_models(cls) -> list[str]:
        """Get list of available OpenAI models."""
        return [
            # OpenAI Models
            "gpt-4",
            "gpt-4-turbo",
            "gpt-3.5-turbo",
            "gpt-4o",
            "gpt-4o-mini",
            # OpenAI-Compatible Models (examples)
            "claude-3-5-sonnet-20241022",
            "gemini-pro",
            "mistral-large",
            "codellama-70b-instruct",
            "deepseek-coder",
            "qwen2-72b-instruct"
        ]

    @classmethod
    def get_available_personas(cls) -> dict[str, str]:
        """Get available agent personas."""
        return {
            "helpful_assistant": "A helpful assistant with network tools for general connectivity checks",
            "network_specialist": "A network diagnostics specialist for troubleshooting connectivity problems",
            "minimal": "A minimal AI assistant that uses tools when needed"
        }

    @classmethod
    def print_config(cls) -> None:
        """Print current configuration (excluding sensitive data)."""
        print("🔧 Ping Agent Configuration:")
        print(f"  Base URL: {cls.OPENAI_BASE_URL}")
        print(f"  Model: {cls.DEFAULT_MODEL}")
        print(f"  Persona: {cls.DEFAULT_PERSONA}")
        print(f"  Max Context Length: {cls.MAX_CONTEXT_LENGTH}")
        print(f"  Max Tool Timeout: {cls.MAX_TOOL_TIMEOUT}s")
        print(f"  Default Ping Count: {cls.DEFAULT_PING_COUNT}")
        print(f"  Default Ping Timeout: {cls.DEFAULT_PING_TIMEOUT}s")
        print(f"  Default Traceroute Hops: {cls.DEFAULT_TRACEROUTE_HOPS}")
        print(f"  OpenAI API Key: {'✅ Set' if cls.OPENAI_API_KEY else '❌ Not set'}")

    @classmethod
    def get_provider_info(cls) -> dict[str, str]:
        """Get information about common OpenAI-compatible providers."""
        return {
            # Official & Major Providers
            "OpenAI": "https://api.openai.com/v1 - Official OpenAI API",
            "Anthropic Claude": "https://api.anthropic.com - Requires Claude API proxy",
            "Google Gemini": "https://generativelanguage.googleapis.com - Requires OpenAI-compatible proxy",

            # AI Platform Providers
            "Mistral AI": "https://api.mistral.ai/v1 - Mistral's OpenAI-compatible endpoint",
            "Together AI": "https://api.together.xyz/v1 - OpenAI-compatible endpoint",
            "Groq": "https://api.groq.com/openai/v1 - Groq's OpenAI-compatible endpoint",
            "DeepSeek": "https://api.deepseek.com/v1 - DeepSeek's OpenAI-compatible endpoint",
            "Zhipu AI": "https://api.z.ai/api/coding/paas/v4 - Zhipu AI's OpenAI-compatible endpoint",
            "Moonshot AI": "https://api.moonshot.cn/v1 - Moonshot AI's OpenAI-compatible endpoint",
            "01.AI": "https://api.lingyiwanwu.com/v1 - 01.AI's OpenAI-compatible endpoint",
            "MiniMax": "https://api.minimax.chat/v1 - MiniMax's OpenAI-compatible endpoint",
            "StepFun": "https://api.stepfun.com/v1 - StepFun's OpenAI-compatible endpoint",

            # Chinese AI Providers
            "Baidu ERNIE": "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop - Baidu ERNIE models",
            "Alibaba Tongyi": "https://dashscope.aliyuncs.com/compatible-mode/v1 - Alibaba's Tongyi models",
            "Tencent Hunyuan": "https://hunyuan.tencentcloudapi.com - Tencent's Hunyuan models",

            # Local & Self-Hosted
            "Local Ollama": "http://localhost:11434/v1 - Local Ollama instance",
            "LM Studio": "http://localhost:1234/v1 - LM Studio local server",
            "Text Generation WebUI": "http://localhost:5000/v1 - Text Generation WebUI",
            "LocalAI": "http://localhost:8080/v1 - LocalAI server",
            "vLLM": "http://localhost:8000/v1 - vLLM inference server",

            # Other Providers
            "Perplexity": "https://api.perplexity.ai - Perplexity's OpenAI-compatible endpoint",
            "Fireworks AI": "https://api.fireworks.ai/inference/v1 - Fireworks AI endpoint",
            "Replicate": "https://api.replicate.com/v1 - Replicate's OpenAI-compatible endpoint",
            "Anyscale": "https://api.endpoints.anyscale.com/v1 - Anyscale's OpenAI-compatible endpoint",
            "Together Computer": "https://api.together.xyz/v1 - Together Computer endpoint"
        }