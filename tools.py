import subprocess
import json
import platform
import re
import logging
import time
from datetime import datetime
from typing import Dict, Any, Optional
from abc import ABC, abstractmethod

# Set up logging for tool calls
def setup_tool_logger():
    """Set up logger for tool calls with both console and file output."""
    logger = logging.getLogger('tool_calls')
    logger.setLevel(logging.INFO)

    # Clear existing handlers
    logger.handlers.clear()

    # Create formatter
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File handler (append mode)
    try:
        file_handler = logging.FileHandler('tool_calls.log', mode='a', encoding='utf-8')
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    except Exception:
        # If file logging fails, continue with console logging only
        pass

    return logger

# Initialize the logger
tool_logger = setup_tool_logger()

class Tool(ABC):
    """Abstract base class for agent tools."""

    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

    @abstractmethod
    def execute(self, args: Dict[str, Any]) -> str:
        """Execute the tool with given arguments."""
        pass

    def execute_with_logging(self, args: Dict[str, Any]) -> str:
        """Execute the tool with logging."""
        start_time = time.time()
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Log tool call start
        tool_logger.info(f"🚀 CALLING TOOL: {self.name}")
        tool_logger.info(f"📋 Arguments: {args}")
        tool_logger.info(f"⏰ Started at: {timestamp}")

        try:
            # Execute the tool
            result = self.execute(args)

            # Calculate execution time
            execution_time = time.time() - start_time

            # Log successful completion
            tool_logger.info(f"✅ TOOL COMPLETED: {self.name}")
            tool_logger.info(f"⏱️  Execution time: {execution_time:.2f}s")
            tool_logger.info(f"📊 Result: {result[:100]}{'...' if len(result) > 100 else ''}")
            tool_logger.info("-" * 60)

            return result

        except Exception as e:
            # Calculate execution time even for failures
            execution_time = time.time() - start_time

            # Log error
            tool_logger.error(f"❌ TOOL FAILED: {self.name}")
            tool_logger.error(f"⏱️  Failed after: {execution_time:.2f}s")
            tool_logger.error(f"🚨 Error: {str(e)}")
            tool_logger.info("-" * 60)

            # Re-raise the exception
            raise

    @property
    @abstractmethod
    def parameters(self) -> Dict[str, Any]:
        """Return JSON schema for tool parameters."""
        pass

class PingTool(Tool):
    """Ping tool for checking network connectivity."""

    def __init__(self):
        super().__init__(
            name="ping",
            description="Ping a host to check network connectivity. Returns ping statistics including packet loss, latency, and response time."
        )

    def execute(self, args: Dict[str, Any]) -> str:
        """Execute ping command."""
        host = args.get("host", "")
        count = args.get("count", 4)
        timeout = args.get("timeout", 3)

        if not host:
            return "Error: Host is required for ping command"

        try:
            # Build ping command based on platform
            system = platform.system().lower()
            if system == "windows":
                cmd = ["ping", "-n", str(count), "-w", str(timeout * 1000), host]
            else:
                cmd = ["ping", "-c", str(count), "-W", str(timeout), host]

            # Execute ping command
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout + 10
            )

            if result.returncode == 0:
                return self._parse_ping_output(result.stdout, host)
            else:
                return f"Ping failed for {host}: {result.stderr.strip()}"

        except subprocess.TimeoutExpired:
            return f"Ping timeout for {host} after {timeout + 10} seconds"
        except Exception as e:
            return f"Error pinging {host}: {str(e)}"

    def _parse_ping_output(self, output: str, host: str) -> str:
        """Parse ping command output into a readable format."""
        lines = output.split('\n')

        # Extract key information
        packet_info = ""
        rtt_info = ""

        for line in lines:
            # Look for packet statistics
            if "packets transmitted" in line.lower() or "packets transmitted" in line:
                packet_info = line.strip()
            # Look for round-trip time statistics
            if "rtt min/avg/max" in line.lower() or "round-trip" in line.lower():
                rtt_info = line.strip()
            # Look for individual ping responses
            if "bytes from" in line.lower() and "ttl=" in line.lower():
                # Extract time from ping response
                time_match = re.search(r'time[=<](\d+\.?\d*)\s*ms', line)
                if time_match:
                    response_time = time_match.group(1)
                    return f"✅ {host} is reachable - Response time: {response_time}ms"

        # If we couldn't parse individual responses, use summary stats
        if packet_info:
            return f"✅ {host} is reachable - {packet_info}"
        elif rtt_info:
            return f"✅ {host} is reachable - {rtt_info}"
        else:
            return f"✅ {host} is reachable - Ping successful"

    @property
    def parameters(self) -> Dict[str, Any]:
        """Return JSON schema for ping parameters."""
        return {
            "type": "object",
            "properties": {
                "host": {
                    "type": "string",
                    "description": "The hostname or IP address to ping"
                },
                "count": {
                    "type": "integer",
                    "description": "Number of ping packets to send (default: 4)",
                    "default": 4,
                    "minimum": 1,
                    "maximum": 10
                },
                "timeout": {
                    "type": "integer",
                    "description": "Timeout in seconds for each ping (default: 3)",
                    "default": 3,
                    "minimum": 1,
                    "maximum": 30
                }
            },
            "required": ["host"]
        }

class TracerouteTool(Tool):
    """Traceroute tool for tracing network path."""

    def __init__(self):
        super().__init__(
            name="traceroute",
            description="Trace the network path to a host showing intermediate hops. Useful for diagnosing network routing issues."
        )

    def execute(self, args: Dict[str, Any]) -> str:
        """Execute traceroute command."""
        host = args.get("host", "")
        max_hops = args.get("max_hops", 15)

        if not host:
            return "Error: Host is required for traceroute command"

        try:
            system = platform.system().lower()
            if system == "windows":
                cmd = ["tracert", "-h", str(max_hops), host]
            else:
                cmd = ["traceroute", "-m", str(max_hops), host]

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60
            )

            if result.returncode == 0:
                return f"Traceroute to {host}:\n{result.stdout}"
            else:
                return f"Traceroute failed for {host}: {result.stderr.strip()}"

        except subprocess.TimeoutExpired:
            return f"Traceroute timeout for {host}"
        except FileNotFoundError:
            return "Traceroute command not found. This tool may not be available on your system."
        except Exception as e:
            return f"Error with traceroute to {host}: {str(e)}"

    @property
    def parameters(self) -> Dict[str, Any]:
        """Return JSON schema for traceroute parameters."""
        return {
            "type": "object",
            "properties": {
                "host": {
                    "type": "string",
                    "description": "The hostname or IP address to trace"
                },
                "max_hops": {
                    "type": "integer",
                    "description": "Maximum number of hops to trace (default: 15)",
                    "default": 15,
                    "minimum": 1,
                    "maximum": 30
                }
            },
            "required": ["host"]
        }

class DNSLookupTool(Tool):
    """DNS lookup tool for resolving domain names."""

    def __init__(self):
        super().__init__(
            name="dns_lookup",
            description="Perform DNS lookup to resolve domain names to IP addresses and get DNS information."
        )

    def execute(self, args: Dict[str, Any]) -> str:
        """Execute DNS lookup."""
        domain = args.get("domain", "")
        record_type = args.get("record_type", "A")

        if not domain:
            return "Error: Domain is required for DNS lookup"

        try:
            system = platform.system().lower()
            if system == "windows":
                cmd = ["nslookup", domain]
            else:
                cmd = ["dig", domain, record_type]

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30
            )

            if result.returncode == 0:
                return f"DNS lookup for {domain} ({record_type} record):\n{result.stdout}"
            else:
                return f"DNS lookup failed for {domain}: {result.stderr.strip()}"

        except subprocess.TimeoutExpired:
            return f"DNS lookup timeout for {domain}"
        except FileNotFoundError:
            # Fallback to simple socket-based lookup
            try:
                import socket
                ip = socket.gethostbyname(domain)
                return f"✅ {domain} resolves to {ip}"
            except Exception as e:
                return f"Could not resolve {domain}: {str(e)}"
        except Exception as e:
            return f"Error with DNS lookup for {domain}: {str(e)}"

    @property
    def parameters(self) -> Dict[str, Any]:
        """Return JSON schema for DNS lookup parameters."""
        return {
            "type": "object",
            "properties": {
                "domain": {
                    "type": "string",
                    "description": "The domain name to look up"
                },
                "record_type": {
                    "type": "string",
                    "description": "DNS record type (A, AAAA, MX, TXT, etc.)",
                    "enum": ["A", "AAAA", "MX", "TXT", "CNAME", "NS"],
                    "default": "A"
                }
            },
            "required": ["domain"]
        }

class NetworkInfoTool(Tool):
    """Network information tool for local network details."""

    def __init__(self):
        super().__init__(
            name="network_info",
            description="Get local network information including IP addresses, interfaces, and connection details."
        )

    def execute(self, args: Dict[str, Any]) -> str:
        """Get network information."""
        try:
            info = []

            # Get local IP addresses
            import socket
            hostname = socket.gethostname()
            local_ip = socket.gethostbyname(hostname)
            info.append(f"Local hostname: {hostname}")
            info.append(f"Local IP: {local_ip}")

            # Get public IP (simple HTTP request)
            try:
                import urllib.request
                public_ip = urllib.request.urlopen('https://api.ipify.org', timeout=5).read().decode()
                info.append(f"Public IP: {public_ip}")
            except:
                info.append("Public IP: Could not determine")

            # Platform-specific network info
            system = platform.system().lower()
            if system == "windows":
                result = subprocess.run(["ipconfig"], capture_output=True, text=True, timeout=10)
            else:
                result = subprocess.run(["ifconfig"], capture_output=True, text=True, timeout=10)

            if result.returncode == 0:
                info.append("\nNetwork interfaces:")
                # Add just the interface names and IPs
                for line in result.stdout.split('\n'):
                    if 'inet ' in line or 'IPv4' in line:
                        info.append(f"  {line.strip()}")

            return "\n".join(info)

        except Exception as e:
            return f"Error getting network info: {str(e)}"

    @property
    def parameters(self) -> Dict[str, Any]:
        """Return JSON schema for network info parameters."""
        return {
            "type": "object",
            "properties": {},
            "required": []
        }

def get_tools() -> list[Tool]:
    """Get all available tools."""
    return [
        PingTool(),
        TracerouteTool(),
        DNSLookupTool(),
        NetworkInfoTool()
    ]

def get_tool_by_name(name: str) -> Optional[Tool]:
    """Get a specific tool by name."""
    for tool in get_tools():
        if tool.name == name:
            return tool
    return None