"""
Tests for Coding Agent Connectors.

Tests:
- Agent profile registration (Kimi, Kimi Claw, Genspark, free backup agents)
- Connector initialization
- Emergency fallback routing
- FreeBackupManager provider detection
"""

import pytest
from unittest.mock import patch, MagicMock

from agentx.orchestrator.agent_profiles import AgentRegistry, AgentCapability
from agentx.orchestrator.task_router import (
    TaskRouter,
    PRIMARY_ROUTING_TABLE,
    EMERGENCY_FALLBACK_CHAIN,
)
from agentx.integrations.coding_agents import (
    ManusConnector,
    KimiConnector,
    KimiClawConnector,
    GensparkConnector,
    FreeBackupManager,
    AgentResponse,
)


class TestNewAgentProfiles:
    """Test new agent profiles are properly registered."""

    def test_kimi_profile_exists(self):
        """Kimi profile should be registered."""
        registry = AgentRegistry()
        profile = registry.get("kimi")
        assert profile is not None
        assert profile.name == "Kimi 2.5"
        assert profile.provider == "Moonshot AI"
        assert AgentCapability.CODE_GENERATION in profile.capabilities

    def test_kimi_claw_profile_exists(self):
        """Kimi Claw profile should be registered."""
        registry = AgentRegistry()
        profile = registry.get("kimi_claw")
        assert profile is not None
        assert profile.name == "Kimi Claw"
        assert profile.supports_sandbox is True

    def test_genspark_profile_exists(self):
        """Genspark profile should be registered."""
        registry = AgentRegistry()
        profile = registry.get("genspark")
        assert profile is not None
        assert AgentCapability.WORKFLOW_AUTOMATION in profile.capabilities

    def test_free_backup_profiles_exist(self):
        """All free backup agent profiles should be registered."""
        registry = AgentRegistry()

        groq = registry.get("groq")
        assert groq is not None
        assert groq.cost_tier == "budget"

        gemini = registry.get("gemini_free")
        assert gemini is not None
        assert gemini.cost_tier == "budget"

        cloudflare = registry.get("cloudflare_workers_ai")
        assert cloudflare is not None
        assert cloudflare.cost_tier == "budget"

        deepseek = registry.get("deepseek")
        assert deepseek is not None
        assert deepseek.cost_tier == "budget"


class TestTaskRouterFallback:
    """Test task router emergency fallback functionality."""

    def test_emergency_fallback_chain_defined(self):
        """Emergency fallback chain should be defined."""
        assert len(EMERGENCY_FALLBACK_CHAIN) > 0
        assert "groq" in EMERGENCY_FALLBACK_CHAIN
        assert "gemini_free" in EMERGENCY_FALLBACK_CHAIN

    def test_kimi_in_coding_routing(self):
        """Kimi should be in coding routing table."""
        assert "kimi" in PRIMARY_ROUTING_TABLE["coding"]

    def test_kimi_claw_in_automation_routing(self):
        """Kimi Claw should be in automation routing table."""
        assert "kimi_claw" in PRIMARY_ROUTING_TABLE["automation"]

    def test_genspark_in_integration_routing(self):
        """Genspark should be in integration routing table."""
        assert "genspark" in PRIMARY_ROUTING_TABLE["integration"]

    def test_route_with_fallback_includes_free_apis(self):
        """route_with_fallback should include emergency free APIs."""
        router = TaskRouter()
        candidates = router.route_with_fallback("coding")
        # Should include at least one free backup agent
        free_agents = [a for a in candidates if a in EMERGENCY_FALLBACK_CHAIN]
        assert len(free_agents) > 0

    def test_get_emergency_fallbacks(self):
        """get_emergency_fallbacks should return available free agents."""
        router = TaskRouter()
        fallbacks = router.get_emergency_fallbacks()
        # Should return at least deepseek (most likely to be enabled)
        assert isinstance(fallbacks, list)

    def test_is_free_tier(self):
        """is_free_tier should correctly identify budget agents."""
        router = TaskRouter()
        assert router.is_free_tier("groq") is True
        assert router.is_free_tier("gemini_free") is True
        assert router.is_free_tier("openai_codex") is False


class TestConnectorInitialization:
    """Test connector classes initialize correctly."""

    def test_manus_connector_init(self):
        """ManusConnector should initialize without API key."""
        connector = ManusConnector()
        assert connector.api_key is None

    def test_manus_connector_with_key(self):
        """ManusConnector should accept API key."""
        connector = ManusConnector(api_key="test-key")
        assert connector.api_key == "test-key"

    def test_kimi_connector_init(self):
        """KimiConnector should initialize."""
        connector = KimiConnector()
        assert connector.api_key is None

    def test_kimi_claw_connector_init(self):
        """KimiClawConnector should initialize with Kimi backend."""
        connector = KimiClawConnector()
        assert connector.kimi is not None
        assert connector.max_agents == 1500

    def test_kimi_claw_spawn_agents(self):
        """KimiClawConnector should spawn agent instances."""
        connector = KimiClawConnector()
        agents = connector.spawn_agents(10)
        assert len(agents) == 10
        assert connector.get_active_count() == 10

    def test_genspark_connector_init(self):
        """GensparkConnector should initialize."""
        connector = GensparkConnector()
        assert connector.api_key is None


class TestFreeBackupManager:
    """Test FreeBackupManager functionality."""

    def test_free_backup_manager_init(self):
        """FreeBackupManager should initialize."""
        manager = FreeBackupManager()
        assert manager.fallback_order == ["groq", "gemini", "deepseek", "cloudflare"]

    def test_get_available_providers_empty(self):
        """get_available_providers should return empty when no keys set."""
        manager = FreeBackupManager()
        # Clear any env vars that might be set
        manager.groq_key = None
        manager.gemini_key = None
        manager.deepseek_key = None
        manager.cloudflare_token = None
        available = manager.get_available_providers()
        assert available == []

    @patch.dict("os.environ", {"GROQ_API_KEY": "test-groq-key"})
    def test_get_available_providers_with_groq(self):
        """get_available_providers should detect Groq when key is set."""
        manager = FreeBackupManager()
        manager.groq_key = "test-groq-key"
        available = manager.get_available_providers()
        assert "groq" in available


class TestAgentResponse:
    """Test AgentResponse model."""

    def test_agent_response_success(self):
        """AgentResponse should handle success case."""
        response = AgentResponse(
            success=True,
            content="Generated code",
            code="print('hello')",
            model="test-model",
            agent_id="test-agent",
        )
        assert response.success is True
        assert response.content == "Generated code"

    def test_agent_response_failure(self):
        """AgentResponse should handle failure case."""
        response = AgentResponse(
            success=False,
            error="API rate limited",
            agent_id="test-agent",
        )
        assert response.success is False
        assert response.error == "API rate limited"
