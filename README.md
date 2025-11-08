# 🏓 Ping Agent - 网络诊断智能助手

基于 Fly.io 博客文章 ["Everyone Write an Agent"](https://fly.io/blog/everyone-write-an-agent/) 构建的智能网络诊断代理。

> **核心理念**: 一个能够使用工具的 LLM 循环，简单而强大的智能代理架构。

## 🎯 项目概述

Ping Agent 是一个使用 OpenAI API 的智能网络诊断助手，它可以通过多种网络工具来检查连接性、诊断网络问题并提供专业的网络分析。

### 核心特性

- 🔍 **智能网络诊断**: 使用 ping、traceroute、DNS 查询等工具
- 🤖 **对话式交互**: 自然语言界面，无需记忆复杂命令
- 🧠 **上下文感知**: 维护对话历史，支持连续对话
- 🛠️ **多工具集成**: 四种核心网络诊断工具
- 📊 **结果解析**: 智能解析网络命令输出，提供可读性强的结果
- ⚡ **等待动画**: 处理请求时显示动态等待动画
- 📝 **工具调用日志**: 详细记录每个工具的执行过程和结果

## 🏗️ 架构设计

基于 Fly.io 文章的简洁架构理念：

```
Agent = LLM + Tools + Context + Loop
```

### 核心组件

1. **Agent (agent.py)**: 主代理循环和上下文管理
2. **Tools (tools.py)**: 可执行的网络工具集合
3. **Config (config.py)**: 配置管理
4. **Context**: 对话上下文（简单的字符串列表）

## 🚀 快速开始

### 1. 环境准备

```bash
# 克隆或下载项目
cd ping-agent

# 安装依赖
pip install -r requirements.txt
```

### 2. 配置 OpenAI API

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑 .env 文件，添加你的 OpenAI API Key
# OPENAI_API_KEY=your-openai-api-key-here
```

### 3. 运行代理

```bash
python agent.py
```

### 4. 开始对话

```
🏓 Ping Agent - Network Diagnostics Assistant
Based on Fly.io 'Everyone Write an Agent'
Type 'quit' to exit, 'reset' to clear context
--------------------------------------------------

You: ping google.com
Agent: ✅ google.com is reachable - Response time: 12.3ms

You: 为什么有些网站访问很慢？
Agent: 让我帮你检查一下网络连接情况。请问你想检查哪个网站的连接状态？

You: check github.com
Agent: I'll check the connectivity to github.com for you.
[自动调用 ping 工具]
✅ github.com is reachable - Response time: 45.7ms

The connection to github.com looks good with a reasonable response time. If you're experiencing slow access to GitHub, it might be due to other factors like server load, your geographic location, or intermediate network routing.
```

## 🛠️ 可用工具

### 1. Ping 工具
检查网络连接性和响应时间。

**功能**:
- 测试主机可达性
- 测量响应时间
- 检测丢包率

**使用示例**:
```
"请检查 google.com 的连接状态"
"ping 8.8.8.8 5次"
```

### 2. Traceroute 工具
追踪到目标主机的网络路径。

**功能**:
- 显示网络跳转路径
- 识别网络瓶颈
- 诊断路由问题

**使用示例**:
```
"追踪到 github.com 的路径"
"看看访问 stackoverflow.com 经过了哪些路由器"
```

### 3. DNS 查询工具
解析域名并获取 DNS 信息。

**功能**:
- 域名解析
- 查询不同类型的 DNS 记录
- DNS 问题诊断

**使用示例**:
```
"查询 github.com 的 IP 地址"
"DNS lookup google.com"
```

### 4. 网络信息工具
获取本地网络配置信息。

**功能**:
- 显示本机 IP 地址
- 获取公网 IP
- 列出网络接口

**使用示例**:
```
"显示我的网络信息"
"我的 IP 地址是什么？"
"检查本地网络配置"
```

## 🧠 代理人格 (Personas)

### 1. helpful_assistant (默认)
友好通用的助手人格，适合一般网络检查需求。

### 2. network_specialist (推荐)
网络专家人格，提供专业的网络诊断建议。

### 3. minimal
极简人格，只在必要时使用工具。

## ⚙️ 配置详解

### 环境变量

在 `.env` 文件中配置以下选项：

```bash
# 必需配置
OPENAI_API_KEY=your-openai-api-key-here

# 模型配置
OPENAI_MODEL=gpt-4              # 可选: gpt-3.5-turbo, gpt-4-turbo, gpt-4o, gpt-4o-mini
AGENT_PERSONA=network_specialist # 可选: helpful_assistant, minimal

# 高级配置
MAX_CONTEXT_LENGTH=10           # 对话上下文保留的消息数量
MAX_TOOL_TIMEOUT=60            # 工具执行超时时间（秒）

# 工具默认设置
DEFAULT_PING_COUNT=4           # 默认 ping 次数
DEFAULT_PING_TIMEOUT=3         # 默认 ping 超时（秒）
DEFAULT_TRACEROUTE_HOPS=15     # 默认 traceroute 跳数
```

### 支持的 OpenAI 模型

- `gpt-4`: 最佳性能，推荐用于复杂任务
- `gpt-4-turbo`: 更快的响应速度
- `gpt-3.5-turbo`: 经济实惠的选择
- `gpt-4o`: 最新的多模态模型
- `gpt-4o-mini`: 轻量级版本

## 🎮 使用技巧

### 对话命令

- `quit`: 退出程序
- `reset`: 清除对话上下文
- `context`: 查看当前对话历史

### 最佳实践

1. **明确的请求**: 使用具体的域名或 IP 地址
2. **中文友好**: 支持中文对话和指令
3. **连续对话**: 可以基于之前的回答继续提问
4. **问题诊断**: 描述具体的网络问题，获得针对性建议

### 示例对话

```
You: 我的网站访问很慢，能帮我检查一下吗？
Agent: 当然可以帮你检查网络连接情况。请告诉我你想检查的网站域名或IP地址？

You: example.com
Agent: 我来检查一下 example.com 的连接状态。
[调用 ping 工具]
✅ example.com is reachable - Response time: 156.2ms

example.com 是可以访问的，但响应时间 156.2ms 确实有点慢。让我再检查一下网络路径情况。
[调用 traceroute 工具]

根据检查结果，example.com 的延迟较高可能是由于：
1. 地理距离较远
2. 中间网络节点拥堵
3. 服务器负载较高

建议你：
1. 尝试使用 CDN 加速
2. 检查服务器性能
3. 考虑使用更近的服务器节点
```

## ✨ 新功能特色

### ⚡ 智能等待动画

当代理执行网络诊断工具时，会显示动态等待动画：

```
🔍 Pinging...     (网络探测中)
📡 Scanning...    (扫描网络)
⌚ Analyzing...   (分析结果)
🚀 Processing... (处理中)
```

动画特点：
- 🎯 **网络主题**: 显示网络相关的活动状态
- 🔄 **流畅切换**: 每 150ms 更新一次，10 个动作循环
- ⏱️ **智能时长**: 根据实际处理时间自动调整
- 🎨 **视觉友好**: 使用表情符号和旋转指示器

### 📝 详细工具调用日志

每次工具调用都会生成详细日志，包含：

**控制台输出示例**:
```
2025-11-08 22:13:06,969 - INFO - 🚀 CALLING TOOL: ping
2025-11-08 22:13:06,969 - INFO - 📋 Arguments: {'host': 'baidu.com', 'count': 4}
2025-11-08 22:13:06,969 - INFO - ⏰ Started at: 2025-11-08 22:13:06
2025-11-08 22:13:08,042 - INFO - ✅ TOOL COMPLETED: ping
2025-11-08 22:13:08,043 - INFO - ⏱️  Execution time: 1.07s
2025-11-08 22:13:08,043 - INFO - 📊 Result: ✅ baidu.com is reachable - 4 packets transmitted...
2025-11-08 22:13:08,043 - INFO - ------------------------------------------------------------
```

**日志特点**:
- 📊 **双输出**: 同时显示在控制台和保存到 `tool_calls.log` 文件
- ⏱️ **执行时间**: 精确记录每个工具的执行耗时
- 📋 **参数记录**: 完整记录传入的工具参数
- 🎯 **结果预览**: 显示执行结果的前 100 字符
- ❌ **错误追踪**: 工具执行失败时的详细错误信息

**日志文件位置**: `tool_calls.log` (项目根目录)
- 📝 **追加模式**: 不会覆盖历史日志
- 🔍 **可检索**: 支持文本搜索和分析
- 📊 **长期记录**: 适合性能分析和问题排查

## 🔧 进阶开发

### 添加新工具

1. 在 `tools.py` 中创建新的工具类：

```python
class YourCustomTool(Tool):
    def __init__(self):
        super().__init__(
            name="your_tool",
            description="Your tool description"
        )

    def execute(self, args: Dict[str, Any]) -> str:
        # 实现工具逻辑
        return "Tool result"

    @property
    def parameters(self) -> Dict[str, Any]:
        # 定义参数模式
        return {
            "type": "object",
            "properties": {
                "param1": {"type": "string", "description": "Parameter description"}
            },
            "required": ["param1"]
        }
```

2. 在 `get_tools()` 函数中添加新工具：

```python
def get_tools() -> list[Tool]:
    return [
        PingTool(),
        TracerouteTool(),
        DNSLookupTool(),
        NetworkInfoTool(),
        YourCustomTool()  # 添加新工具
    ]
```

### 自定义人格

在 `config.py` 的 `get_available_personas()` 方法中添加新人格：

```python
def get_available_personas(cls) -> dict[str, str]:
    return {
        "helpful_assistant": "...",
        "network_specialist": "...",
        "minimal": "...",
        "your_custom_persona": "自定义人格描述"
    }
```

在 `agent.py` 的 `_get_persona()` 方法中添加对应的描述。

### 扩展上下文管理

当前的上下文管理使用简单的字符串列表。你可以扩展为：

1. **持久化存储**: 将对话保存到数据库
2. **智能总结**: 长对话自动总结关键信息
3. **分类存储**: 按主题分类存储对话历史
4. **云端同步**: 多设备间同步对话状态

### 集成外部服务

```python
# 示例：集成 Slack 通知
def send_slack_notification(message: str):
    import requests
    webhook_url = os.getenv("SLACK_WEBHOOK_URL")
    requests.post(webhook_url, json={"text": message})

# 在工具执行后发送通知
def execute(self, args: Dict[str, Any]) -> str:
    result = super().execute(args)
    send_slack_notification(f"Network check completed: {result}")
    return result
```

## 🧪 测试与调试

### 单元测试

```bash
# 创建测试文件 test_agent.py
python -m pytest test_agent.py -v
```

### 调试模式

在 `agent.py` 中添加调试输出：

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# 在关键位置添加调试信息
logging.debug(f"Current context: {self.context}")
logging.debug(f"Tool call: {tool_name} with args {tool_args}")
```

### 性能监控

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

# 应用到关键函数
@monitor_performance
def run(self, user_input: str) -> str:
    # ... 原有逻辑
```

## 🚀 部署选项

### 1. 本地部署

直接运行 `python agent.py`

### 2. Docker 容器化

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

### 3. 云服务部署

可以部署到：
- **Fly.io**: 与文章主题呼应
- **Heroku**: 简单的 PaaS 部署
- **AWS Lambda**: 无服务器架构
- **Google Cloud Run**: 容器化部署

### 4. API 服务

修改为 FastAPI 或 Flask 应用：

```python
from fastapi import FastAPI

app = FastAPI()
agent = Agent()

@app.post("/chat")
async def chat(message: str):
    response = agent.run(message)
    return {"response": response}
```

## 🔒 安全注意事项

1. **API 密钥保护**: 永远不要在代码中硬编码 API 密钥
2. **输入验证**: 验证用户输入，防止命令注入
3. **权限控制**: 限制工具可以执行的操作
4. **日志审计**: 记录所有工具调用和用户请求

## 🤝 贡献指南

1. Fork 项目
2. 创建功能分支: `git checkout -b feature/amazing-feature`
3. 提交更改: `git commit -m 'Add amazing feature'`
4. 推送分支: `git push origin feature/amazing-feature`
5. 提交 Pull Request

## 📄 许可证

本项目基于 MIT 许可证开源。

## 🙏 致谢

- [Fly.io - "Everyone Write an Agent"](https://fly.io/blog/everyone-write-an-agent/): 提供了核心架构理念
- OpenAI: 提供强大的语言模型能力
- 开源社区: 各种网络工具和库的支持

## 📚 相关资源

- [OpenAI API 文档](https://platform.openai.com/docs)
- [Python subprocess 模块](https://docs.python.org/3/library/subprocess.html)
- [JSON Schema 规范](https://json-schema.org/)
- [网络诊断工具指南](https://en.wikipedia.org/wiki/Ping_(networking_utility))

---

**开始构建你自己的智能代理吧！** 🚀