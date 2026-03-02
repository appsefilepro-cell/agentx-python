"""
AgentX5 Advanced Edition
========================

Permanent multi-environment AI orchestration system with 1500+ agent fleet.
Includes Abacus AI CLI integration, legal drafting, and forensic analysis.
ClawBot fleet with Kimi Claw, OpenAI Codex, Manus, GenSpark, and more.

Environments Supported:
- Cloud (Vercel, Google Cloud Run)
- iPhone/Mobile
- Laptop/Desktop
- Docker containers
- Sandbox environments
- Linux Ubuntu

Document Date: February 2, 2026
APPS Holdings WY, Inc.
"""

from agentx5_advanced.orchestrator import (
    AgentX5Orchestrator,
    AbacusAgent,
    SilentPartnerConfig,
)
from agentx5_advanced.config.settings import (
    AGENTX5_CONFIG,
    ABACUS_CONFIG,
    DEPLOYMENT_TARGETS,
)
from agentx5_advanced.agents.clawbot_manager import ClawBotManager
from agentx5_advanced.agents.task_manager import TaskScreenManager

__all__ = [
    "AgentX5Orchestrator",
    "AbacusAgent",
    "SilentPartnerConfig",
    "AGENTX5_CONFIG",
    "ABACUS_CONFIG",
    "DEPLOYMENT_TARGETS",
    "ClawBotManager",
    "TaskScreenManager",
]

__version__ = "1.0.0"
__author__ = "APPS Holdings WY, Inc."
__document_date__ = "February 2, 2026"
