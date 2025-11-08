import json
import sys
import time
import threading
from typing import List, Dict, Any, Optional
from openai import OpenAI
from tools import get_tools
from config import Config

# Global variable for animation control
stop_animation = False

def show_loading_animation():
    """Show a loading animation while the agent is thinking."""
    animations = [
        "🔍 Pinging",
        "📡 Scanning",
        "🌐 Connecting",
        "⚡ Analyzing",
        "🔧 Configuring",
        "📊 Measuring",
        "🎯 Targeting",
        "🚀 Processing"
    ]

    spinners = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]

    idx = 0
    spinner_idx = 0

    while not stop_animation:
        # Combine spinner and action text
        current_action = animations[idx % len(animations)]
        current_spinner = spinners[spinner_idx % len(spinners)]

        sys.stdout.write(f"\r{current_spinner} {current_action}... ")
        sys.stdout.flush()

        time.sleep(0.15)

        # Change spinner every frame
        spinner_idx += 1

        # Change action text every 10 frames
        if spinner_idx % 10 == 0:
            idx += 1

class Agent:
    def __init__(self, model: str = None, persona: str = None):
        """
        Initialize the agent - Fly.io pattern

        Args:
            model: OpenAI model to use
            persona: Type of persona for the agent
        """
        self.client = OpenAI(
            api_key=Config.OPENAI_API_KEY,
            base_url=Config.OPENAI_BASE_URL
        )
        self.model = model or Config.DEFAULT_MODEL
        self.persona_name = persona or Config.DEFAULT_PERSONA
        self.tools = get_tools()
        self.context: List[Dict[str, Any]] = []

        # Add system message to context
        self.context.append({
            "role": "system",
            "content": self._get_persona(self.persona_name)
        })

    def _get_persona(self, persona_type: str) -> str:
        """Get the persona description based on type."""
        personas = {
            "helpful_assistant": "You are a helpful assistant with access to network tools. You help users check network connectivity and diagnose connection issues.",
            "network_specialist": "You are a network diagnostics specialist. You use ping and other network tools to help troubleshoot connectivity problems.",
            "minimal": "You are an AI assistant that can use tools when needed."
        }
        return personas.get(persona_type, personas["helpful_assistant"])

    def _get_tools_schema(self) -> List[Dict[str, Any]]:
        """Get OpenAI tool schema for all tools."""
        schemas = []
        for tool in self.tools:
            schemas.append({
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": tool.parameters
                }
            })
        return schemas

    def _execute_tool(self, tool_name: str, args: Dict[str, Any]) -> str:
        """Execute a tool and return the result."""
        for tool in self.tools:
            if tool.name == tool_name:
                try:
                    # Use the new logging method
                    result = tool.execute_with_logging(args)
                    return str(result)
                except Exception as e:
                    return f"Error executing {tool_name}: {str(e)}"

        return f"Unknown tool: {tool_name}"

    def _handle_tool_calls(self, response) -> bool:
        """
        Handle tool calls from OpenAI response.
        Returns True if more tool calls need to be made.
        """
        if not response.choices[0].message.tool_calls:
            return False

        message = response.choices[0].message

        # Add assistant message with tool calls to context
        self.context.append({
            "role": "assistant",
            "content": message.content or "",
            "tool_calls": [
                {
                    "id": tool_call.id,
                    "type": tool_call.type,
                    "function": {
                        "name": tool_call.function.name,
                        "arguments": tool_call.function.arguments
                    }
                }
                for tool_call in message.tool_calls
            ]
        })

        # Execute each tool call
        for tool_call in message.tool_calls:
            tool_name = tool_call.function.name
            try:
                tool_args = json.loads(tool_call.function.arguments)
            except json.JSONDecodeError:
                tool_args = {}

            tool_result = self._execute_tool(tool_name, tool_args)

            # Add tool result to context
            self.context.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "name": tool_name,
                "content": tool_result
            })

        return True  # More tool calls might be needed

    def process(self, user_input: str) -> str:
        """
        Process user input - Fly.io pattern

        Args:
            user_input: The user's message/input

        Returns:
            The agent's response
        """
        # Add user message to context
        self.context.append({
            "role": "user",
            "content": user_input
        })

        try:
            # Keep making calls until no more tool calls needed
            while True:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=self.context,
                    tools=self._get_tools_schema(),
                    tool_choice="auto"
                )

                # Handle tool calls if present
                if self._handle_tool_calls(response):
                    continue  # More tool calls needed

                # No more tool calls, we have our final response
                break

            # Get final response
            final_message = response.choices[0].message
            response_text = final_message.content or ""

            # Add assistant response to context
            self.context.append({
                "role": "assistant",
                "content": response_text
            })

            return response_text

        except Exception as e:
            error_msg = f"Error: {str(e)}"
            self.context.append({
                "role": "assistant",
                "content": error_msg
            })
            return error_msg

    def reset_context(self) -> None:
        """Reset the conversation context."""
        self.context = [{
            "role": "system",
            "content": self._get_persona(self.persona_name)
        }]

    def show_context(self) -> List[Dict[str, Any]]:
        """Show the current context."""
        return self.context.copy()

def main():
    """Main function - Fly.io pattern: input > process > output"""
    print("🏓 Ping Agent - Network Diagnostics Assistant")
    print("Based on Fly.io 'Everyone Write an Agent'")
    print("Commands: 'quit' to exit, 'reset' to clear context, 'context' to view history, 'providers' to see supported APIs")
    print("-" * 50)

    # Initialize agent
    agent = Agent()

    while True:
        try:
            user_input = input("\nYou: ").strip()

            if user_input.lower() == 'quit':
                print("Goodbye! 👋")
                break
            elif user_input.lower() == 'reset':
                agent.reset_context()
                print("Context reset. Starting fresh conversation.")
                continue
            elif user_input.lower() == 'context':
                print("\nCurrent context:")
                for i, msg in enumerate(agent.show_context(), 1):
                    role = msg.get("role", "unknown")
                    content = msg.get("content", "")[:100]
                    if len(content) == 100:
                        content += "..."
                    print(f"{i}. [{role}] {content}")
                continue
            elif user_input.lower() == 'providers':
                print("\n🌐 Supported OpenAI-Compatible Providers:")
                providers = Config.get_provider_info()
                for provider, info in list(providers.items())[:10]:  # Show first 10
                    print(f"  📍 {provider}: {info.split(' - ')[0]}")
                print(f"  ... and {len(providers) - 10} more providers")
                continue
            elif user_input.lower() == 'config':
                Config.print_config()
                continue

            if not user_input:
                continue

            # Process input using Fly.io pattern with animation
            global stop_animation
            stop_animation = False

            # Start animation in a separate thread
            animation_thread = threading.Thread(target=show_loading_animation)
            animation_thread.daemon = True
            animation_thread.start()

            # Get agent response
            response = agent.process(user_input)

            # Stop animation and clear line
            stop_animation = True
            time.sleep(0.1)  # Give animation time to stop
            sys.stdout.write("\r" + " " * 50 + "\r")  # Clear the animation line
            sys.stdout.flush()

            # Print response
            print(f"Agent: {response}")

        except KeyboardInterrupt:
            print("\n\nGoodbye! 👋")
            break
        except Exception as e:
            print(f"\nError: {str(e)}")

if __name__ == "__main__":
    main()