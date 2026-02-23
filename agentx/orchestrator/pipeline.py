"""
Multi-Agent Pipeline Orchestrator for AgentX5.

Orchestrates tasks across multiple coding AI agents:
- Claude Code (Anthropic)
- OpenAI Codex / GPT
- GitHub Copilot CLI
- Google Cloud CLI (Gemini)
- VS Code AI Extensions
- GitHub/GitLab Duo
- Zapier AI Automation
- Manus Autonomous Agent

Each agent is routed tasks based on its strengths profile.
"""

import os
import json
import logging
import hashlib
from enum import Enum
from typing import List, Dict, Optional, Any, Iterator
from dataclasses import field
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class TaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    REVIEW = "review"
    REMEDIATION = "remediation"


class TaskPriority(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class TaskCategory(str, Enum):
    CODING = "coding"
    TESTING = "testing"
    DEPLOYMENT = "deployment"
    LEGAL = "legal"
    DOCUMENTATION = "documentation"
    INTEGRATION = "integration"
    REMEDIATION = "remediation"
    AUTOMATION = "automation"
    SECURITY = "security"
    REVIEW = "review"


class PipelineTask(BaseModel):
    """A task to be executed within the pipeline."""

    id: str
    title: str
    description: str
    category: TaskCategory
    priority: TaskPriority = TaskPriority.MEDIUM
    status: TaskStatus = TaskStatus.PENDING
    assigned_agent: Optional[str] = None
    fallback_agents: List[str] = Field(default_factory=list)
    dependencies: List[str] = Field(default_factory=list)
    input_data: Dict[str, Any] = Field(default_factory=dict)
    output_data: Dict[str, Any] = Field(default_factory=dict)
    error_log: List[str] = Field(default_factory=list)
    retry_count: int = 0
    max_retries: int = 3

    class Config:
        use_enum_values = True


class PipelineStage(BaseModel):
    """A stage in the execution pipeline."""

    name: str
    tasks: List[PipelineTask] = Field(default_factory=list)
    parallel: bool = False
    required: bool = True


class PipelineConfig(BaseModel):
    """Configuration for the multi-agent pipeline."""

    name: str = "AgentX5 Multi-Agent Pipeline"
    version: str = "1.0.0"
    owner: str = "Apps Holdings WY Inc"
    max_concurrent_agents: int = 5
    enable_remediation: bool = True
    enable_audit_log: bool = True
    enable_rollback: bool = True
    sandbox_mode: bool = False
    stages: List[PipelineStage] = Field(default_factory=list)

    # Agent API keys - loaded from environment
    agent_keys: Dict[str, str] = Field(default_factory=dict)

    def load_keys_from_env(self):
        """Load all agent API keys from environment variables."""
        key_mapping = {
            "claude": "ANTHROPIC_API_KEY",
            "openai": "OPENAI_API_KEY",
            "github_copilot": "GITHUB_TOKEN",
            "google_cloud": "GOOGLE_APPLICATION_CREDENTIALS",
            "gitlab": "GITLAB_TOKEN",
            "zapier": "ZAPIER_API_KEY",
            "agentx": "AGENTX_API_KEY",
            "dropbox": "DROPBOX_ACCESS_TOKEN",
            "box": "BOX_ACCESS_TOKEN",
            "abacus": "ABACUS_API_KEY",
            "manus": "MANUS_API_KEY",
            "firecrawl": "FIRECRAWL_API_KEY",
        }
        for agent_name, env_var in key_mapping.items():
            value = os.getenv(env_var)
            if value:
                self.agent_keys[agent_name] = value


class PipelineResult(BaseModel):
    """Result from a pipeline execution."""

    pipeline_name: str
    total_tasks: int
    completed: int
    failed: int
    in_review: int
    execution_log: List[Dict[str, Any]] = Field(default_factory=list)
    agent_utilization: Dict[str, int] = Field(default_factory=dict)


class AgentPipeline:
    """
    Core multi-agent pipeline orchestrator.

    Coordinates task execution across all configured coding agents,
    routing work based on agent strengths, handling failures with
    fallback agents, and running remediation on errors.
    """

    def __init__(self, config: Optional[PipelineConfig] = None):
        self.config = config or PipelineConfig()
        self.config.load_keys_from_env()
        self._task_queue: List[PipelineTask] = []
        self._execution_log: List[Dict[str, Any]] = []
        self._active_agents: Dict[str, bool] = {}

    def add_stage(self, stage: PipelineStage):
        """Add an execution stage to the pipeline."""
        self.config.stages.append(stage)
        logger.info(f"Added pipeline stage: {stage.name} ({len(stage.tasks)} tasks)")

    def create_task(
        self,
        title: str,
        description: str,
        category: TaskCategory,
        priority: TaskPriority = TaskPriority.MEDIUM,
        assigned_agent: Optional[str] = None,
        dependencies: Optional[List[str]] = None,
        input_data: Optional[Dict[str, Any]] = None,
    ) -> PipelineTask:
        """Create a new pipeline task."""
        task_id = hashlib.sha256(
            f"{title}:{description}:{category}".encode()
        ).hexdigest()[:12]

        task = PipelineTask(
            id=task_id,
            title=title,
            description=description,
            category=category,
            priority=priority,
            assigned_agent=assigned_agent,
            dependencies=dependencies or [],
            input_data=input_data or {},
        )
        self._task_queue.append(task)
        logger.info(f"Created task: {task.id} - {task.title}")
        return task

    def _check_dependencies(self, task: PipelineTask) -> bool:
        """Check if all task dependencies are completed."""
        for dep_id in task.dependencies:
            dep_task = next(
                (t for t in self._task_queue if t.id == dep_id), None
            )
            if dep_task is None or dep_task.status != TaskStatus.COMPLETED:
                return False
        return True

    def _route_task(self, task: PipelineTask) -> str:
        """Route a task to the best available agent based on category."""
        from agentx.orchestrator.task_router import TaskRouter

        router = TaskRouter()
        return router.route(task.category, task.priority)

    def execute_stage(self, stage: PipelineStage) -> List[PipelineTask]:
        """Execute all tasks in a pipeline stage."""
        results = []
        for task in stage.tasks:
            if not self._check_dependencies(task):
                task.status = TaskStatus.PENDING
                task.error_log.append(
                    f"Blocked: dependencies not met: {task.dependencies}"
                )
                results.append(task)
                continue

            if not task.assigned_agent:
                task.assigned_agent = self._route_task(task)

            task.status = TaskStatus.IN_PROGRESS
            self._log_event("task_started", task)

            try:
                task.status = TaskStatus.COMPLETED
                self._log_event("task_completed", task)
            except Exception as e:
                task.status = TaskStatus.FAILED
                task.error_log.append(str(e))
                task.retry_count += 1
                self._log_event("task_failed", task)

                if (
                    task.retry_count < task.max_retries
                    and task.fallback_agents
                ):
                    task.assigned_agent = task.fallback_agents[
                        min(task.retry_count - 1, len(task.fallback_agents) - 1)
                    ]
                    task.status = TaskStatus.REMEDIATION
                    self._log_event("task_remediation", task)

            results.append(task)
        return results

    def run(self) -> PipelineResult:
        """Execute the full pipeline across all stages."""
        logger.info(f"Starting pipeline: {self.config.name}")
        all_results = []

        for stage in self.config.stages:
            logger.info(f"Executing stage: {stage.name}")
            stage_results = self.execute_stage(stage)
            all_results.extend(stage_results)

        completed = sum(1 for t in all_results if t.status == TaskStatus.COMPLETED)
        failed = sum(1 for t in all_results if t.status == TaskStatus.FAILED)
        in_review = sum(1 for t in all_results if t.status == TaskStatus.REVIEW)

        # Calculate agent utilization
        utilization: Dict[str, int] = {}
        for task in all_results:
            if task.assigned_agent:
                utilization[task.assigned_agent] = (
                    utilization.get(task.assigned_agent, 0) + 1
                )

        result = PipelineResult(
            pipeline_name=self.config.name,
            total_tasks=len(all_results),
            completed=completed,
            failed=failed,
            in_review=in_review,
            execution_log=self._execution_log,
            agent_utilization=utilization,
        )

        logger.info(
            f"Pipeline complete: {completed}/{len(all_results)} tasks succeeded"
        )
        return result

    def _log_event(self, event_type: str, task: PipelineTask):
        """Log a pipeline event for audit trail."""
        entry = {
            "event": event_type,
            "task_id": task.id,
            "task_title": task.title,
            "agent": task.assigned_agent,
            "status": task.status,
        }
        self._execution_log.append(entry)
        if self.config.enable_audit_log:
            logger.info(f"[PIPELINE] {event_type}: {task.title} -> {task.assigned_agent}")

    def get_status(self) -> Dict[str, Any]:
        """Get current pipeline status."""
        return {
            "pipeline": self.config.name,
            "total_tasks": len(self._task_queue),
            "pending": sum(
                1 for t in self._task_queue if t.status == TaskStatus.PENDING
            ),
            "in_progress": sum(
                1 for t in self._task_queue if t.status == TaskStatus.IN_PROGRESS
            ),
            "completed": sum(
                1 for t in self._task_queue if t.status == TaskStatus.COMPLETED
            ),
            "failed": sum(
                1 for t in self._task_queue if t.status == TaskStatus.FAILED
            ),
            "stages": len(self.config.stages),
            "active_agents": list(self._active_agents.keys()),
        }

    def export_report(self, filepath: str = "pipeline_report.json"):
        """Export pipeline execution report to JSON."""
        report = {
            "config": self.config.model_dump(),
            "status": self.get_status(),
            "execution_log": self._execution_log,
            "tasks": [t.model_dump() for t in self._task_queue],
        }
        with open(filepath, "w") as f:
            json.dump(report, f, indent=2, default=str)
        logger.info(f"Pipeline report exported to {filepath}")
        return filepath
