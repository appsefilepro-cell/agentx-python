"""
Coding Agent Connectors for AgentX5 Multi-Agent Pipeline.

Provides API connectors for:
- Manus (autonomous sandbox execution)
- Kimi / Kimi Claw (Moonshot AI coding assistants)
- Genspark (agent orchestration)
- Free Backup APIs (Groq, Gemini, Cloudflare, DeepSeek)

All connectors follow a unified interface for the pipeline orchestrator.
"""

import os
import json
import logging
from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class AgentResponse(BaseModel):
    """Standardized response from any coding agent."""

    success: bool
    content: str = ""
    code: Optional[str] = None
    error: Optional[str] = None
    tokens_used: int = 0
    model: str = ""
    agent_id: str = ""


class ManusConnector:
    """
    Manus Autonomous Agent Connector.

    Provides:
    - Sandbox code execution
    - Terminal command execution
    - File system operations
    - Package installation
    - Live progress streaming
    """

    BASE_URL = "https://api.manus.ai/v1"

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("MANUS_API_KEY")
        if not self.api_key:
            logger.warning("Manus API key not configured")

    def _headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def execute_code(
        self,
        code: str,
        language: str = "python",
        timeout: int = 300,
    ) -> AgentResponse:
        """Execute code in Manus sandbox."""
        import requests

        response = requests.post(
            f"{self.BASE_URL}/sandbox/execute",
            headers=self._headers(),
            json={
                "code": code,
                "language": language,
                "timeout": timeout,
            },
        )
        if response.status_code == 200:
            data = response.json()
            return AgentResponse(
                success=True,
                content=data.get("output", ""),
                code=code,
                model="manus-sandbox",
                agent_id="manus",
            )
        return AgentResponse(
            success=False,
            error=f"Manus execution failed: {response.status_code}",
            agent_id="manus",
        )

    def run_terminal(self, command: str, timeout: int = 120) -> AgentResponse:
        """Run terminal command in Manus sandbox."""
        import requests

        response = requests.post(
            f"{self.BASE_URL}/sandbox/terminal",
            headers=self._headers(),
            json={"command": command, "timeout": timeout},
        )
        if response.status_code == 200:
            data = response.json()
            return AgentResponse(
                success=True,
                content=data.get("output", ""),
                model="manus-terminal",
                agent_id="manus",
            )
        return AgentResponse(
            success=False,
            error=f"Terminal execution failed: {response.status_code}",
            agent_id="manus",
        )

    def create_session(self) -> str:
        """Create a new Manus sandbox session."""
        import requests

        response = requests.post(
            f"{self.BASE_URL}/sandbox/session",
            headers=self._headers(),
        )
        if response.status_code == 200:
            return response.json().get("session_id", "")
        raise Exception(f"Failed to create session: {response.status_code}")


class KimiConnector:
    """
    Moonshot Kimi API Connector.

    Provides:
    - Code generation with Kimi 2.5
    - Long-context code understanding
    - Multilingual code support
    """

    BASE_URL = "https://api.moonshot.cn/v1"

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("KIMI_API_KEY")
        if not self.api_key:
            logger.warning("Kimi API key not configured")

    def _headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def generate_code(
        self,
        prompt: str,
        system_prompt: str = "You are an expert programmer.",
        max_tokens: int = 4096,
    ) -> AgentResponse:
        """Generate code using Kimi 2.5."""
        import requests

        response = requests.post(
            f"{self.BASE_URL}/chat/completions",
            headers=self._headers(),
            json={
                "model": "moonshot-v1-128k",
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt},
                ],
                "max_tokens": max_tokens,
                "temperature": 0.2,
            },
        )
        if response.status_code == 200:
            data = response.json()
            content = data["choices"][0]["message"]["content"]
            return AgentResponse(
                success=True,
                content=content,
                tokens_used=data.get("usage", {}).get("total_tokens", 0),
                model="kimi-2.5",
                agent_id="kimi",
            )
        return AgentResponse(
            success=False,
            error=f"Kimi generation failed: {response.status_code}",
            agent_id="kimi",
        )

    def review_code(self, code: str, language: str = "python") -> AgentResponse:
        """Review code using Kimi."""
        prompt = f"Review this {language} code for bugs, security issues, and improvements:\n\n```{language}\n{code}\n```"
        return self.generate_code(
            prompt,
            system_prompt="You are a senior code reviewer. Identify issues and suggest improvements.",
        )


class KimiClawConnector:
    """
    Kimi Claw Multi-Agent Coordinator.

    Orchestrates multiple agent instances for parallel task execution.
    Manages 1500 Clawbot instances.
    """

    def __init__(self, api_key: Optional[str] = None):
        self.kimi = KimiConnector(api_key)
        self.active_agents: Dict[str, bool] = {}
        self.max_agents = 1500

    def spawn_agents(self, count: int = 10) -> List[str]:
        """Spawn multiple Clawbot agent instances."""
        agent_ids = []
        for i in range(min(count, self.max_agents)):
            agent_id = f"clawbot_{i:04d}"
            self.active_agents[agent_id] = True
            agent_ids.append(agent_id)
        logger.info(f"Spawned {len(agent_ids)} Clawbot agents")
        return agent_ids

    def dispatch_task(
        self,
        agent_id: str,
        task: str,
        task_type: str = "coding",
    ) -> AgentResponse:
        """Dispatch a task to a specific Clawbot agent."""
        if agent_id not in self.active_agents:
            return AgentResponse(
                success=False,
                error=f"Agent {agent_id} not found",
                agent_id=agent_id,
            )

        return self.kimi.generate_code(
            prompt=f"[{task_type.upper()}] {task}",
            system_prompt=f"You are Clawbot agent {agent_id}. Execute the task efficiently.",
        )

    def get_active_count(self) -> int:
        """Get count of active agents."""
        return sum(1 for active in self.active_agents.values() if active)


class GensparkConnector:
    """
    Genspark Agent Orchestration Connector.

    Provides:
    - Multi-agent workflow coordination
    - Cross-platform agent integration
    - Workflow execution monitoring
    """

    BASE_URL = "https://api.genspark.ai/v1"

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("GENSPARK_API_KEY")
        if not self.api_key:
            logger.warning("Genspark API key not configured")

    def _headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def create_workflow(
        self,
        name: str,
        steps: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """Create a multi-agent workflow."""
        import requests

        response = requests.post(
            f"{self.BASE_URL}/workflows",
            headers=self._headers(),
            json={"name": name, "steps": steps},
        )
        if response.status_code in (200, 201):
            return response.json()
        raise Exception(f"Workflow creation failed: {response.status_code}")

    def execute_workflow(self, workflow_id: str) -> AgentResponse:
        """Execute a workflow."""
        import requests

        response = requests.post(
            f"{self.BASE_URL}/workflows/{workflow_id}/run",
            headers=self._headers(),
        )
        if response.status_code == 200:
            return AgentResponse(
                success=True,
                content=json.dumps(response.json()),
                model="genspark",
                agent_id="genspark",
            )
        return AgentResponse(
            success=False,
            error=f"Workflow execution failed: {response.status_code}",
            agent_id="genspark",
        )


class FreeBackupManager:
    """
    Unified manager for free-tier backup APIs.

    Provides automatic fallback across:
    - Groq (Llama/Mixtral)
    - Google Gemini (Free tier)
    - Cloudflare Workers AI
    - DeepSeek Coder

    Used when paid APIs are unavailable or rate-limited.
    """

    def __init__(self):
        self.groq_key = os.getenv("GROQ_API_KEY")
        self.gemini_key = os.getenv("GEMINI_API_KEY")
        self.cloudflare_token = os.getenv("CLOUDFLARE_API_TOKEN")
        self.cloudflare_account = os.getenv("CLOUDFLARE_ACCOUNT_ID")
        self.deepseek_key = os.getenv("DEEPSEEK_API_KEY")

        self.fallback_order = ["groq", "gemini", "deepseek", "cloudflare"]

    def generate_code(
        self,
        prompt: str,
        preferred_provider: Optional[str] = None,
    ) -> AgentResponse:
        """Generate code using free APIs with automatic fallback."""
        providers = (
            [preferred_provider] + self.fallback_order
            if preferred_provider
            else self.fallback_order
        )

        for provider in providers:
            try:
                if provider == "groq" and self.groq_key:
                    return self._groq_generate(prompt)
                elif provider == "gemini" and self.gemini_key:
                    return self._gemini_generate(prompt)
                elif provider == "deepseek" and self.deepseek_key:
                    return self._deepseek_generate(prompt)
                elif provider == "cloudflare" and self.cloudflare_token:
                    return self._cloudflare_generate(prompt)
            except Exception as e:
                logger.warning(f"Provider {provider} failed: {e}")
                continue

        return AgentResponse(
            success=False,
            error="All free backup APIs failed",
            agent_id="free_backup",
        )

    def _groq_generate(self, prompt: str) -> AgentResponse:
        """Generate using Groq API."""
        import requests

        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {self.groq_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": "llama-3.1-70b-versatile",
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 4096,
            },
        )
        if response.status_code == 200:
            data = response.json()
            return AgentResponse(
                success=True,
                content=data["choices"][0]["message"]["content"],
                tokens_used=data.get("usage", {}).get("total_tokens", 0),
                model="groq-llama-3.1-70b",
                agent_id="groq",
            )
        raise Exception(f"Groq failed: {response.status_code}")

    def _gemini_generate(self, prompt: str) -> AgentResponse:
        """Generate using Google Gemini API."""
        import requests

        response = requests.post(
            f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={self.gemini_key}",
            headers={"Content-Type": "application/json"},
            json={
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {"maxOutputTokens": 4096},
            },
        )
        if response.status_code == 200:
            data = response.json()
            content = data["candidates"][0]["content"]["parts"][0]["text"]
            return AgentResponse(
                success=True,
                content=content,
                model="gemini-1.5-flash",
                agent_id="gemini_free",
            )
        raise Exception(f"Gemini failed: {response.status_code}")

    def _deepseek_generate(self, prompt: str) -> AgentResponse:
        """Generate using DeepSeek API."""
        import requests

        response = requests.post(
            "https://api.deepseek.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {self.deepseek_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": "deepseek-coder",
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 4096,
            },
        )
        if response.status_code == 200:
            data = response.json()
            return AgentResponse(
                success=True,
                content=data["choices"][0]["message"]["content"],
                tokens_used=data.get("usage", {}).get("total_tokens", 0),
                model="deepseek-coder",
                agent_id="deepseek",
            )
        raise Exception(f"DeepSeek failed: {response.status_code}")

    def _cloudflare_generate(self, prompt: str) -> AgentResponse:
        """Generate using Cloudflare Workers AI."""
        import requests

        response = requests.post(
            f"https://api.cloudflare.com/client/v4/accounts/{self.cloudflare_account}/ai/run/@cf/meta/llama-3-8b-instruct",
            headers={
                "Authorization": f"Bearer {self.cloudflare_token}",
                "Content-Type": "application/json",
            },
            json={"prompt": prompt, "max_tokens": 2048},
        )
        if response.status_code == 200:
            data = response.json()
            return AgentResponse(
                success=True,
                content=data.get("result", {}).get("response", ""),
                model="cloudflare-llama-3-8b",
                agent_id="cloudflare_workers_ai",
            )
        raise Exception(f"Cloudflare failed: {response.status_code}")

    def get_available_providers(self) -> List[str]:
        """Get list of configured free providers."""
        available = []
        if self.groq_key:
            available.append("groq")
        if self.gemini_key:
            available.append("gemini")
        if self.deepseek_key:
            available.append("deepseek")
        if self.cloudflare_token and self.cloudflare_account:
            available.append("cloudflare")
        return available
