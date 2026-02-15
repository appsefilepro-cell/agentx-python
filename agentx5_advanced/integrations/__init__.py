"""
AgentX5 Advanced Edition - Integration Hub

FREE TIER INTEGRATIONS:
- GitHub / GitLab (version control)
- VS Code / Codespaces (development)
- Postman (API testing)
- E2B (code execution sandbox)
- Firecrawl (web scraping)
- Vercel (deployment)
- Telegram / Discord (messaging)
- Manus Sandbox (AI agents)

APPS HOLDINGS WY, INC.
"""

from agentx5_advanced.integrations.document_builder import DocumentBuilder, MemorySystem
from agentx5_advanced.integrations.github_sync import GitHubSync
from agentx5_advanced.integrations.messaging import TelegramBot, DiscordBot
from agentx5_advanced.integrations.sandbox import ManusSandbox, E2BSandbox

__all__ = [
    "DocumentBuilder",
    "MemorySystem",
    "GitHubSync",
    "TelegramBot",
    "DiscordBot",
    "ManusSandbox",
    "E2BSandbox",
]
