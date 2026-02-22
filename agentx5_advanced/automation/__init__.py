"""
AgentX5 Advanced Edition - Automation Pipelines

Free-tier automation flows for enterprise-level operations:
- Google Gemini Pro (free)
- Manus (300 credits/day x 3 accounts = 900 credits/day)
- Box → Airtable automation
- Zapier free workflows
- Sandbox execution environment
"""

from agentx5_advanced.automation.pipelines import (
    AutomationPipeline,
    SandboxExecutor,
    TaskRouter,
)
from agentx5_advanced.automation.integrations import (
    GeminiIntegration,
    ManusIntegration,
    BoxAirtableSync,
    ZapierWorkflow,
)

__all__ = [
    "AutomationPipeline",
    "SandboxExecutor",
    "TaskRouter",
    "GeminiIntegration",
    "ManusIntegration",
    "BoxAirtableSync",
    "ZapierWorkflow",
]
