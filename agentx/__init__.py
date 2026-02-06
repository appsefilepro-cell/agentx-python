import logging

from agentx.agentx import AgentX
from agentx.version import VERSION
from agentx.integrations import (
    IntegrationManager,
    ToolCategory,
    PricingTier,
    get_free_alternative,
    get_all_free_tools,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S %Z",
)

__all__ = [
    "AgentX",
    "IntegrationManager",
    "ToolCategory",
    "PricingTier",
    "get_free_alternative",
    "get_all_free_tools",
]
__version__ = VERSION
