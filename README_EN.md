# 🏓 Ping Agent - Network Diagnostics Assistant

An intelligent network diagnostics agent built based on the Fly.io blog post ["Everyone Write an Agent"](https://fly.io/blog/everyone-write-an-agent/).

> **Core Concept**: An LLM running in a loop that uses tools - simple yet powerful agent architecture.

## 🎯 Project Overview

Ping Agent is an intelligent network diagnostics assistant that uses OpenAI API (and OpenAI-compatible APIs) to check connectivity, diagnose network issues, and provide professional network analysis through multiple network tools.

### Key Features

- 🔍 **Intelligent Network Diagnostics**: Uses ping, traceroute, DNS lookup, and other tools
- 🤖 **Conversational Interface**: Natural language interaction, no need to memorize complex commands
- 🧠 **Context-Aware**: Maintains conversation history, supports continuous dialogue
- 🛠️ **Multi-Tool Integration**: Four core network diagnostic tools
- 📊 **Smart Result Parsing**: Intelligently parses network command outputs for readable results
- 🔧 **Multiple Provider Support**: Works with OpenAI and OpenAI-compatible APIs (Mistral, Groq, Ollama, etc.)
- ⚡ **Loading Animation**: Dynamic waiting animation during tool execution
- 📝 **Tool Call Logging**: Detailed logging of every tool execution with timing and results

## 🏗️ Architecture Design

Based on the simple architecture philosophy from the Fly.io article:

```
Agent = LLM + Tools + Context + Loop
```

### Core Components

1. **Agent (agent.py)**: Main agent loop and context management
2. **Tools (tools.py)**: Executable network tool collection
3. **Config (config.py)**: Configuration management with multi-provider support
4. **Context**: Conversation context (simple list of strings)

## 🚀 Quick Start

### 1. Environment Setup

```bash
# Clone or download the project
cd ping-agent

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure API

```bash
# Copy environment variables template
cp .env.example .env

# Edit .env file and add your API key
# For OpenAI:
# OPENAI_API_KEY=your-openai-api-key-here
# OPENAI_BASE_URL=https://api.openai.com/v1
# OPENAI_MODEL=gpt-4

# For other providers (see examples in .env.example)
```

### 3. Run the Agent

```bash
python agent.py
```

### 4. Start Conversation

```
🏓 Ping Agent - Network Diagnostics Assistant
Based on Fly.io 'Everyone Write an Agent'
Type 'quit' to exit, 'reset' to clear context
--------------------------------------------------

You: ping google.com
Agent: ✅ google.com is reachable - Response time: 12.3ms

You: Why are some websites loading slowly?
Agent: Let me help you check your network connection. Which website would you like me to test?

You: check github.com
Agent: I'll check the connectivity to github.com for you.
[Automatically calls ping tool]
✅ github.com is reachable - Response time: 45.7ms

The connection to github.com looks good with a reasonable response time. If you're experiencing slow access to GitHub, it might be due to other factors like server load, your geographic location, or intermediate network routing.
```

## 🛠️ Available Tools

### 1. Ping Tool
Check network connectivity and response time.

**Features**:
- Test host reachability
- Measure response time
- Detect packet loss

**Usage Examples**:
```
"Check connectivity to google.com"
"ping 8.8.8.8 5 times"
"Test network latency to baidu.com"
```

### 2. Traceroute Tool
Trace network path to destination host.

**Features**:
- Show network hop paths
- Identify network bottlenecks
- Diagnose routing issues

**Usage Examples**:
```
"Trace route to github.com"
"traceroute to baidu.com"
"Show which routers I go through to reach stackoverflow.com"
```

### 3. DNS Lookup Tool
Resolve domain names and get DNS information.

**Features**:
- Domain resolution
- Query different DNS record types
- DNS problem diagnosis

**Usage Examples**:
```
"Get IP address for github.com"
"DNS lookup google.com"
"Check MX records for baidu.com"
```

### 4. Network Info Tool
Get local network configuration information.

**Features**:
- Show local IP addresses
- Get public IP
- List network interfaces

**Usage Examples**:
```
"Show my network information"
"What's my IP address?"
"Check local network configuration"
```

## 🧠 Agent Personas

### 1. helpful_assistant (Default)
Friendly general-purpose assistant persona, suitable for general network checking needs.

### 2. network_specialist (Recommended)
Network expert persona that provides professional network diagnostics advice.

### 3. minimal
Minimal persona that only uses tools when necessary.

## 🔧 Supported Providers

The agent supports multiple OpenAI-compatible providers:

### 🚀 Major AI Platforms

#### Official OpenAI
```bash
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_MODEL=gpt-4  # or gpt-4-turbo, gpt-3.5-turbo, gpt-4o, gpt-4o-mini
```

#### Mistral AI
```bash
OPENAI_BASE_URL=https://api.mistral.ai/v1
OPENAI_MODEL=mistral-large  # or mistral-medium, mistral-small
```

#### Groq
```bash
OPENAI_BASE_URL=https://api.groq.com/openai/v1
OPENAI_MODEL=llama3-70b-8192  # or mixtral-8x7b-32768, gemma-7b-it
```

#### DeepSeek
```bash
OPENAI_BASE_URL=https://api.deepseek.com/v1
OPENAI_MODEL=deepseek-coder  # or deepseek-chat
```

#### Together AI
```bash
OPENAI_BASE_URL=https://api.together.xyz/v1
OPENAI_MODEL=meta-llama/Llama-3-70b-chat-hf
```

### 🇨🇳 Chinese AI Providers

#### Zhipu AI (智谱AI)
```bash
OPENAI_BASE_URL=https://api.z.ai/api/coding/paas/v4
OPENAI_MODEL=glm-4.6  # or glm-4, glm-3-turbo
```

#### Moonshot AI (月之暗面)
```bash
OPENAI_BASE_URL=https://api.moonshot.cn/v1
OPENAI_MODEL=moonshot-v1-8k  # or moonshot-v1-32k, moonshot-v1-128k
```

#### 01.AI (零一万物)
```bash
OPENAI_BASE_URL=https://api.lingyiwanwu.com/v1
OPENAI_MODEL=yi-large  # or yi-medium, yi-spark
```

#### MiniMax
```bash
OPENAI_BASE_URL=https://api.minimax.chat/v1
OPENAI_MODEL=abab6.5  # or abab6.5s, abab6.5-chat
```

#### StepFun (阶跃星辰)
```bash
OPENAI_BASE_URL=https://api.stepfun.com/v1
OPENAI_MODEL=step-1-8k  # or step-1-32k, step-1-256k
```

#### Alibaba Tongyi Qianwen (阿里通义千问)
```bash
OPENAI_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
OPENAI_MODEL=qwen-plus  # or qwen-turbo, qwen-max
```

### 🏠 Local & Self-Hosted

#### Local Ollama
```bash
OPENAI_BASE_URL=http://localhost:11434/v1
OPENAI_MODEL=llama3  # or any model you have in Ollama
```

#### LM Studio
```bash
OPENAI_BASE_URL=http://localhost:1234/v1
OPENAI_MODEL=local-model  # any model loaded in LM Studio
```

#### Text Generation WebUI
```bash
OPENAI_BASE_URL=http://localhost:5000/v1
OPENAI_MODEL=local-model
```

#### LocalAI
```bash
OPENAI_BASE_URL=http://localhost:8080/v1
OPENAI_MODEL=local-model
```

#### vLLM
```bash
OPENAI_BASE_URL=http://localhost:8000/v1
OPENAI_MODEL=local-model
```

### 🌟 Other Providers

#### Perplexity
```bash
OPENAI_BASE_URL=https://api.perplexity.ai
OPENAI_MODEL=llama-3-sonar-small-32k-online  # with real-time search
```

#### Fireworks AI
```bash
OPENAI_BASE_URL=https://api.fireworks.ai/inference/v1
OPENAI_MODEL=accounts/fireworks/models/llama-v3-70b-instruct
```

#### Anyscale
```bash
OPENAI_BASE_URL=https://api.endpoints.anyscale.com/v1
OPENAI_MODEL=meta-llama/Llama-2-70b-chat-hf
```

#### Replicate
```bash
OPENAI_BASE_URL=https://api.replicate.com/v1
OPENAI_MODEL=meta/meta-llama-3-70b-instruct
```

## ⚙️ Configuration Details

### Environment Variables

Configure the following options in your `.env` file:

```bash
# Required Configuration
OPENAI_API_KEY=your-api-key-here
OPENAI_BASE_URL=https://api.openai.com/v1  # Change for other providers

# Model Configuration
OPENAI_MODEL=gpt-4
AGENT_PERSONA=network_specialist

# Advanced Configuration
MAX_CONTEXT_LENGTH=10           # Number of messages to keep in context
MAX_TOOL_TIMEOUT=60            # Tool execution timeout (seconds)

# Tool Default Settings
DEFAULT_PING_COUNT=4           # Default ping count
DEFAULT_PING_TIMEOUT=3         # Default ping timeout (seconds)
DEFAULT_TRACEROUTE_HOPS=15     # Default traceroute hops
```

### Supported Models

**OpenAI Models**:
- `gpt-4`: Best performance, recommended for complex tasks
- `gpt-4-turbo`: Faster response speed
- `gpt-3.5-turbo`: Economical choice
- `gpt-4o`: Latest multimodal model
- `gpt-4o-mini`: Lightweight version

**Major Platform Models**:
- `mistral-large`: Mistral AI's flagship model
- `llama3-70b-8192`: Meta Llama 3 via Groq (ultra-fast)
- `deepseek-coder`: DeepSeek's coding specialist model
- `claude-3-5-sonnet-20241022`: Anthropic Claude (via proxy)
- `gemini-pro`: Google Gemini (via proxy)

**Chinese AI Models**:
- `glm-4.6`: Zhipu AI's latest model
- `moonshot-v1-8k`: Moonshot AI's conversational model
- `yi-large`: 01.AI's large language model
- `abab6.5`: MiniMax's advanced model
- `step-1-8k`: StepFun's reasoning model
- `qwen-plus`: Alibaba's Tongyi Qianwen model

**Open Source Models** (via various providers):
- `llama3`: Meta's Llama 3 family
- `mixtral-8x7b`: Mistral's MoE model
- `code-llama`: Meta's coding specialist
- `qwen2-72b-instruct`: Qwen 2 instruction model
- `phi-3`: Microsoft's small but capable model

**Local Models** (self-hosted):
- Any model loaded in Ollama
- Any model running in LM Studio
- Custom models in Text Generation WebUI
- Models served by LocalAI or vLLM

## 🎮 Usage Tips

### Conversation Commands

- `quit`: Exit the program
- `reset`: Clear conversation context
- `context`: View current conversation history
- `providers`: See supported OpenAI-compatible providers
- `config`: Show current configuration

### Best Practices

1. **Specific Requests**: Use specific domain names or IP addresses
2. **English & Chinese Support**: Supports both languages for dialogue and commands
3. **Continuous Dialogue**: Can continue asking follow-up questions based on previous answers
4. **Problem Diagnosis**: Describe specific network issues for targeted advice

### Example Conversations

```
You: My website is loading slowly, can you help check?
Agent: Of course! I can help check your network connection. Please tell me the website domain or IP address you'd like me to check.

You: example.com
Agent: I'll check the connection status for example.com.
[Calls ping tool]
✅ example.com is reachable - Response time: 156.2ms

example.com is accessible, but the response time of 156.2ms is indeed a bit slow. Let me check the network path as well.
[Calls traceroute tool]

Based on the check results, the high latency for example.com might be due to:
1. Long geographical distance
2. Congestion in intermediate network nodes
3. High server load

I recommend:
1. Try using CDN acceleration
2. Check server performance
3. Consider using closer server nodes
```

## ✨ New Features

### ⚡ Smart Loading Animation

When the agent executes network diagnostic tools, it displays a dynamic loading animation:

```
🔍 Pinging...     (Network probing)
📡 Scanning...    (Scanning network)
⚡ Analyzing...   (Analyzing results)
🚀 Processing... (Processing data)
```

**Animation Features**:
- 🎯 **Network Themed**: Shows network-related activity states
- 🔄 **Smooth Transitions**: Updates every 150ms with 10 rotating actions
- ⏱️ **Adaptive Duration**: Automatically adjusts based on actual processing time
- 🎨 **Visually Friendly**: Uses emojis and spinning indicators

### 📝 Detailed Tool Call Logging

Every tool execution generates comprehensive logs including:

**Console Output Example**:
```
2025-11-08 22:13:06,969 - INFO - 🚀 CALLING TOOL: ping
2025-11-08 22:13:06,969 - INFO - 📋 Arguments: {'host': 'baidu.com', 'count': 4}
2025-11-08 22:13:06,969 - INFO - ⏰ Started at: 2025-11-08 22:13:06
2025-11-08 22:13:08,042 - INFO - ✅ TOOL COMPLETED: ping
2025-11-08 22:13:08,043 - INFO - ⏱️  Execution time: 1.07s
2025-11-08 22:13:08,043 - INFO - 📊 Result: ✅ baidu.com is reachable - 4 packets transmitted...
2025-11-08 22:13:08,043 - INFO - ------------------------------------------------------------
```

**Logging Features**:
- 📊 **Dual Output**: Displays in console and saves to `tool_calls.log` file
- ⏱️ **Execution Timing**: Precise timing for each tool execution
- 📋 **Parameter Recording**: Complete record of input parameters
- 🎯 **Result Preview**: Shows first 100 characters of execution results
- ❌ **Error Tracking**: Detailed error information for failed executions

**Log File Location**: `tool_calls.log` (project root directory)
- 📝 **Append Mode**: Preserves historical logs
- 🔍 **Searchable**: Supports text search and analysis
- 📊 **Long-term Recording**: Suitable for performance analysis and troubleshooting

## 🔧 Advanced Development

### Adding New Tools

1. Create a new tool class in `tools.py`:

```python
class YourCustomTool(Tool):
    def __init__(self):
        super().__init__(
            name="your_tool",
            description="Your tool description"
        )

    def execute(self, args: Dict[str, Any]) -> str:
        # Implement tool logic
        return "Tool result"

    @property
    def parameters(self) -> Dict[str, Any]:
        # Define parameter schema
        return {
            "type": "object",
            "properties": {
                "param1": {"type": "string", "description": "Parameter description"}
            },
            "required": ["param1"]
        }
```

2. Add the new tool in the `get_tools()` function:

```python
def get_tools() -> list[Tool]:
    return [
        PingTool(),
        TracerouteTool(),
        DNSLookupTool(),
        NetworkInfoTool(),
        YourCustomTool()  # Add new tool
    ]
```

### Custom Personas

Add new personas in the `get_available_personas()` method in `config.py`:

```python
def get_available_personas(cls) -> dict[str, str]:
    return {
        "helpful_assistant": "...",
        "network_specialist": "...",
        "minimal": "...",
        "your_custom_persona": "Custom persona description"
    }
```

Add corresponding descriptions in the `_get_persona()` method in `agent.py`.

### Extending Context Management

The current context management uses a simple string list. You can extend it to:

1. **Persistent Storage**: Save conversations to database
2. **Smart Summarization**: Auto-summarize key information in long conversations
3. **Categorized Storage**: Store conversation history by topic
4. **Cloud Sync**: Sync conversation state across devices

### External Service Integration

```python
# Example: Slack notification integration
def send_slack_notification(message: str):
    import requests
    webhook_url = os.getenv("SLACK_WEBHOOK_URL")
    requests.post(webhook_url, json={"text": message})

# Send notification after tool execution
def execute(self, args: Dict[str, Any]) -> str:
    result = super().execute(args)
    send_slack_notification(f"Network check completed: {result}")
    return result
```

## 🧪 Testing and Debugging

### Unit Testing

```bash
# Create test file test_agent.py
python -m pytest test_agent.py -v
```

### Debug Mode

Add debug output in `agent.py`:

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Add debug information at key locations
logging.debug(f"Current context: {self.context}")
logging.debug(f"Tool call: {tool_name} with args {tool_args}")
```

### Performance Monitoring

```python
import time
import functools

def monitor_performance(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} took {end_time - start_time:.2f}s")
        return result
    return wrapper

# Apply to key functions
@monitor_performance
def run(self, user_input: str) -> str:
    # ... original logic
```

## 🚀 Deployment Options

### 1. Local Deployment

Simply run `python agent.py`

### 2. Docker Containerization

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["python", "agent.py"]
```

```bash
docker build -t ping-agent .
docker run -it --env-file .env ping-agent
```

### 3. Cloud Service Deployment

Can be deployed to:
- **Fly.io**: Echoes the article theme
- **Heroku**: Simple PaaS deployment
- **AWS Lambda**: Serverless architecture
- **Google Cloud Run**: Containerized deployment
- **Railway**: Modern deployment platform

### 4. API Service

Convert to FastAPI or Flask application:

```python
from fastapi import FastAPI

app = FastAPI()
agent = Agent()

@app.post("/chat")
async def chat(message: str):
    response = agent.run(message)
    return {"response": response}

@app.get("/health")
async def health():
    return {"status": "healthy"}
```

## 🔒 Security Considerations

1. **API Key Protection**: Never hardcode API keys in code
2. **Input Validation**: Validate user input to prevent command injection
3. **Access Control**: Limit operations that tools can execute
4. **Audit Logging**: Log all tool calls and user requests
5. **Network Security**: Ensure tool executions don't expose system vulnerabilities

## 📈 Monitoring and Observability

### Logging Configuration

```python
import logging

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Log tool usage
logger = logging.getLogger("ping_agent")
logger.info(f"Tool {tool_name} executed with args: {args}")
```

### Metrics Collection

```python
# Simple metrics tracking
class Metrics:
    def __init__(self):
        self.tool_calls = {}
        self.response_times = []

    def record_tool_call(self, tool_name: str, duration: float):
        if tool_name not in self.tool_calls:
            self.tool_calls[tool_name] = 0
        self.tool_calls[tool_name] += 1
        self.response_times.append(duration)
```

## 🤝 Contributing

1. Fork the project
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push branch: `git push origin feature/amazing-feature`
5. Submit Pull Request

## 📄 License

This project is open source under the MIT License.

## 🙏 Acknowledgments

- [Fly.io - "Everyone Write an Agent"](https://fly.io/blog/everyone-write-an-agent/): Provided the core architecture philosophy
- OpenAI: Provided powerful language model capabilities
- Open-source community: Support for various network tools and libraries
- Multiple AI providers: For offering OpenAI-compatible APIs

## 📚 Related Resources

- [OpenAI API Documentation](https://platform.openai.com/docs)
- [OpenAI-Compatible APIs](https://docs.anthropic.com/claude/reference/migrating-from-openai)
- [Python subprocess Module](https://docs.python.org/3/library/subprocess.html)
- [JSON Schema Specification](https://json-schema.org/)
- [Network Diagnostic Tools Guide](https://en.wikipedia.org/wiki/Ping_(networking_utility))

---

**Start building your own intelligent agent today!** 🚀