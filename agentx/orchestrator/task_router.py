"""
Task Router for AgentX5 Multi-Agent Pipeline.

Routes incoming tasks to the most appropriate agent based on:
- Task category and type
- Agent capabilities and strengths
- Agent priority ranking
- Current availability and load
- Fallback chain for failure recovery
"""

import logging
from typing import List, Optional, Dict
from agentx.orchestrator.agent_profiles import (
    AgentProfile,
    AgentRegistry,
    AgentCapability,
    AGENT_PROFILES,
)

logger = logging.getLogger(__name__)

# Mapping from task categories to required capabilities
CATEGORY_CAPABILITY_MAP: Dict[str, List[AgentCapability]] = {
    "coding": [AgentCapability.CODE_GENERATION, AgentCapability.DEBUGGING],
    "testing": [AgentCapability.TESTING, AgentCapability.SANDBOX_EXECUTION],
    "deployment": [AgentCapability.DEPLOYMENT, AgentCapability.CI_CD],
    "legal": [AgentCapability.LEGAL_DRAFTING, AgentCapability.DOCUMENTATION],
    "documentation": [AgentCapability.DOCUMENTATION, AgentCapability.CODE_REVIEW],
    "integration": [AgentCapability.API_INTEGRATION, AgentCapability.WORKFLOW_AUTOMATION],
    "remediation": [AgentCapability.DEBUGGING, AgentCapability.SECURITY_AUDIT],
    "automation": [AgentCapability.WORKFLOW_AUTOMATION, AgentCapability.IDE_AUTOMATION],
    "security": [AgentCapability.SECURITY_AUDIT, AgentCapability.CODE_REVIEW],
    "review": [AgentCapability.CODE_REVIEW, AgentCapability.DOCUMENTATION],
}

# Primary agent assignment for each category (ordered by preference)
PRIMARY_ROUTING_TABLE: Dict[str, List[str]] = {
    "coding": ["openai_codex", "claude_code", "kimi", "github_copilot", "manus"],
    "testing": ["openai_codex", "manus", "kimi_claw", "gitlab_duo", "claude_code"],
    "deployment": ["gitlab_duo", "github_copilot", "google_cloud_cli", "manus", "genspark"],
    "legal": ["abacus_ai", "claude_code"],
    "documentation": ["claude_code", "kimi", "abacus_ai", "github_copilot"],
    "integration": ["zapier_duo", "genspark", "openai_codex", "claude_code", "manus"],
    "remediation": ["claude_code", "openai_codex", "kimi_claw", "gitlab_duo"],
    "automation": ["zapier_duo", "kimi_claw", "manus", "genspark", "vscode_ai", "github_copilot"],
    "security": ["gitlab_duo", "claude_code", "openai_codex"],
    "review": ["claude_code", "kimi", "github_copilot", "gitlab_duo"],
}

# Emergency fallback chain - free APIs for when paid agents fail
EMERGENCY_FALLBACK_CHAIN: List[str] = [
    "deepseek",      # Best free coder
    "groq",          # Fast inference
    "gemini_free",   # Google free tier
    "cloudflare_workers_ai",  # Edge deployment
]


class TaskRouter:
    """
    Intelligent task router that assigns work to the best available agent.
    """

    def __init__(self, registry: Optional[AgentRegistry] = None):
        self.registry = registry or AgentRegistry()
        self._load_tracker: Dict[str, int] = {}

    def route(self, category: str, priority: str = "medium") -> str:
        """
        Route a task to the best agent for the given category.

        Args:
            category: Task category (coding, testing, deployment, etc.)
            priority: Task priority level

        Returns:
            Agent ID of the best available agent
        """
        candidates = PRIMARY_ROUTING_TABLE.get(category, [])

        for agent_id in candidates:
            profile = self.registry.get(agent_id)
            if profile and profile.enabled:
                self._track_assignment(agent_id)
                logger.info(
                    f"Routed {category} task (priority={priority}) -> {profile.name}"
                )
                return agent_id

        # Fallback: pick the highest-ranked enabled agent
        ranked = self.registry.get_ranked()
        if ranked:
            fallback = ranked[0]
            self._track_assignment(fallback.id)
            logger.warning(
                f"No primary agent for {category}, falling back to {fallback.name}"
            )
            return fallback.id

        raise ValueError(f"No available agent for category: {category}")

    def get_fallback_chain(self, category: str) -> List[str]:
        """Get the ordered fallback chain for a task category."""
        return PRIMARY_ROUTING_TABLE.get(category, [])

    def get_best_for_capability(
        self, capability: AgentCapability
    ) -> Optional[str]:
        """Find the best agent for a specific capability."""
        agents = self.registry.find_by_capability(capability)
        if agents:
            # Sort by priority rank
            agents.sort(key=lambda a: a.priority_rank)
            return agents[0].id
        return None

    def _track_assignment(self, agent_id: str):
        """Track how many tasks have been assigned to each agent."""
        self._load_tracker[agent_id] = self._load_tracker.get(agent_id, 0) + 1

    def get_load_distribution(self) -> Dict[str, int]:
        """Get the current load distribution across agents."""
        return dict(self._load_tracker)

    def get_routing_table(self) -> Dict[str, List[str]]:
        """Get the full routing table with agent names resolved."""
        resolved: Dict[str, List[str]] = {}
        for category, agent_ids in PRIMARY_ROUTING_TABLE.items():
            names = []
            for aid in agent_ids:
                profile = self.registry.get(aid)
                if profile:
                    names.append(f"{profile.name} ({profile.provider})")
            resolved[category] = names
        return resolved

    def route_with_fallback(
        self, category: str, priority: str = "medium"
    ) -> List[str]:
        """
        Route a task with full fallback chain including emergency free APIs.

        Returns ordered list of agent IDs to try.
        """
        # Start with primary routing
        candidates = list(PRIMARY_ROUTING_TABLE.get(category, []))

        # Add emergency fallback chain for free APIs
        for fallback_agent in EMERGENCY_FALLBACK_CHAIN:
            if fallback_agent not in candidates:
                profile = self.registry.get(fallback_agent)
                if profile and profile.enabled:
                    candidates.append(fallback_agent)

        return candidates

    def get_emergency_fallbacks(self) -> List[str]:
        """Get list of emergency fallback agents (free tier)."""
        available = []
        for agent_id in EMERGENCY_FALLBACK_CHAIN:
            profile = self.registry.get(agent_id)
            if profile and profile.enabled:
                available.append(agent_id)
        return available

    def is_free_tier(self, agent_id: str) -> bool:
        """Check if an agent is on the free tier."""
        profile = self.registry.get(agent_id)
        return profile is not None and profile.cost_tier == "budget"
