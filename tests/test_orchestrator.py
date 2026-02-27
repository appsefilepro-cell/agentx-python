"""Tests for the orchestrator module."""
import pytest


class TestAgentProfiles:
    """Test agent profile configurations."""

    def test_all_agents_have_strengths(self):
        """Each agent should have at least 5 strengths."""
        from agentx.orchestrator.agent_profiles import AGENT_PROFILES
        for agent_id, profile in AGENT_PROFILES.items():
            assert len(profile.strengths) >= 5, f"{agent_id} needs 5+ strengths"

    def test_all_agents_have_weaknesses(self):
        """Each agent should have 3-5 weaknesses documented."""
        from agentx.orchestrator.agent_profiles import AGENT_PROFILES
        for agent_id, profile in AGENT_PROFILES.items():
            assert 3 <= len(profile.weaknesses) <= 5, f"{agent_id} needs 3-5 weaknesses"

    def test_agent_registry_lookup(self):
        """Registry should find agents by ID."""
        from agentx.orchestrator.agent_profiles import AgentRegistry
        registry = AgentRegistry()
        codex = registry.get("openai_codex")
        assert codex is not None
        assert codex.name == "OpenAI Codex"


class TestTaskRouter:
    """Test task routing logic."""

    def test_route_coding_task(self):
        """Coding tasks should route to Codex first."""
        from agentx.orchestrator.task_router import TaskRouter
        router = TaskRouter()
        agent_id = router.route("coding")
        assert agent_id == "openai_codex"

    def test_route_legal_task(self):
        """Legal tasks should route to Abacus."""
        from agentx.orchestrator.task_router import TaskRouter
        router = TaskRouter()
        agent_id = router.route("legal")
        assert agent_id == "abacus_ai"

    def test_fallback_chain(self):
        """Should return fallback chain for categories."""
        from agentx.orchestrator.task_router import TaskRouter
        router = TaskRouter()
        chain = router.get_fallback_chain("coding")
        assert "openai_codex" in chain
        assert "claude_code" in chain


class TestPipeline:
    """Test pipeline execution."""

    def test_pipeline_init(self):
        """Pipeline should initialize with default config."""
        from agentx.orchestrator.pipeline import Pipeline, PipelineConfig
        config = PipelineConfig(name="test")
        pipeline = Pipeline(config)
        assert pipeline.config.name == "test"

    def test_add_stage(self):
        """Should add stages to pipeline."""
        from agentx.orchestrator.pipeline import Pipeline, PipelineConfig, PipelineStage
        config = PipelineConfig(name="test")
        pipeline = Pipeline(config)
        stage = PipelineStage(name="build", task_category="coding")
        pipeline.add_stage(stage)
        assert len(pipeline.stages) == 1
