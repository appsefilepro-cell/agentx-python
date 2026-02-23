"""
IDE Automation and VS Code Integration for AgentX5.

Provides:
- VS Code workspace configuration generation
- Extension management and recommendations
- Task runner configuration
- Debug configuration generation
- Settings sync for multi-agent development environment
- Copilot CLI integration
"""

import os
import json
import logging
from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class IDEConfig(BaseModel):
    """IDE configuration model."""

    workspace_name: str = "AgentX5-MultiAgent-Workspace"
    python_path: str = "python3"
    default_formatter: str = "ms-python.black-formatter"
    line_length: int = 100
    enable_copilot: bool = True
    enable_pylance: bool = True
    auto_save: bool = True
    format_on_save: bool = True


class ExtensionRecommendation(BaseModel):
    """VS Code extension recommendation."""

    id: str
    name: str
    description: str
    required: bool = True


# Core extensions for multi-agent development
RECOMMENDED_EXTENSIONS: List[ExtensionRecommendation] = [
    ExtensionRecommendation(
        id="ms-python.python",
        name="Python",
        description="Python language support with IntelliSense and debugging",
    ),
    ExtensionRecommendation(
        id="ms-python.black-formatter",
        name="Black Formatter",
        description="Python code formatter using Black",
    ),
    ExtensionRecommendation(
        id="ms-python.pylint",
        name="Pylint",
        description="Python linting with Pylint",
    ),
    ExtensionRecommendation(
        id="ms-toolsai.jupyter",
        name="Jupyter",
        description="Jupyter notebook support for data analysis",
    ),
    ExtensionRecommendation(
        id="github.copilot",
        name="GitHub Copilot",
        description="AI-powered code completion and chat",
    ),
    ExtensionRecommendation(
        id="github.copilot-chat",
        name="GitHub Copilot Chat",
        description="AI chat for code explanation and generation",
    ),
    ExtensionRecommendation(
        id="ms-vscode.vscode-github-issue-notebooks",
        name="GitHub Issue Notebooks",
        description="GitHub issue and PR management in VS Code",
    ),
    ExtensionRecommendation(
        id="eamodio.gitlens",
        name="GitLens",
        description="Git supercharged with blame, history, and more",
    ),
    ExtensionRecommendation(
        id="ms-azuretools.vscode-docker",
        name="Docker",
        description="Docker container management and debugging",
    ),
    ExtensionRecommendation(
        id="redhat.vscode-yaml",
        name="YAML",
        description="YAML language support for CI/CD configs",
    ),
    ExtensionRecommendation(
        id="googlecloudtools.cloudcode",
        name="Google Cloud Code",
        description="Google Cloud development and deployment tools",
    ),
    ExtensionRecommendation(
        id="ms-python.mypy-type-checker",
        name="Mypy Type Checker",
        description="Static type checking for Python",
        required=False,
    ),
    ExtensionRecommendation(
        id="charliermarsh.ruff",
        name="Ruff",
        description="Fast Python linter and formatter",
        required=False,
    ),
]


class VSCodeAutomation:
    """
    VS Code workspace automation for AgentX5 multi-agent development.

    Generates and manages:
    - .vscode/settings.json
    - .vscode/extensions.json
    - .vscode/tasks.json
    - .vscode/launch.json
    - Workspace .code-workspace files
    """

    def __init__(self, workspace_root: str, config: Optional[IDEConfig] = None):
        self.workspace_root = workspace_root
        self.config = config or IDEConfig()
        self.vscode_dir = os.path.join(workspace_root, ".vscode")

    def setup_workspace(self) -> Dict[str, str]:
        """Set up the complete VS Code workspace configuration."""
        os.makedirs(self.vscode_dir, exist_ok=True)

        files_created = {}
        files_created["settings"] = self._generate_settings()
        files_created["extensions"] = self._generate_extensions()
        files_created["tasks"] = self._generate_tasks()
        files_created["launch"] = self._generate_launch()
        files_created["workspace"] = self._generate_workspace_file()

        logger.info(f"VS Code workspace configured at {self.workspace_root}")
        return files_created

    def _generate_settings(self) -> str:
        """Generate .vscode/settings.json."""
        settings = {
            "python.defaultInterpreterPath": self.config.python_path,
            "python.analysis.typeCheckingMode": "basic",
            "python.analysis.autoImportCompletions": True,
            "editor.formatOnSave": self.config.format_on_save,
            "editor.defaultFormatter": self.config.default_formatter,
            "[python]": {
                "editor.defaultFormatter": self.config.default_formatter,
                "editor.formatOnSave": True,
                "editor.codeActionsOnSave": {
                    "source.organizeImports": "explicit"
                },
            },
            "python.formatting.provider": "none",
            "black-formatter.args": [
                f"--line-length={self.config.line_length}"
            ],
            "files.autoSave": "afterDelay" if self.config.auto_save else "off",
            "files.autoSaveDelay": 1000,
            "git.autofetch": True,
            "git.enableSmartCommit": True,
            "github.copilot.enable": {
                "*": self.config.enable_copilot,
                "yaml": True,
                "markdown": True,
                "json": True,
            },
            "editor.inlineSuggest.enabled": self.config.enable_copilot,
            "editor.rulers": [self.config.line_length],
            "editor.tabSize": 4,
            "editor.insertSpaces": True,
            "files.trimTrailingWhitespace": True,
            "files.insertFinalNewline": True,
            "search.exclude": {
                "**/__pycache__": True,
                "**/.git": True,
                "**/node_modules": True,
                "**/*.egg-info": True,
                "**/dist": True,
                "**/build": True,
            },
        }

        filepath = os.path.join(self.vscode_dir, "settings.json")
        with open(filepath, "w") as f:
            json.dump(settings, f, indent=4)
        return filepath

    def _generate_extensions(self) -> str:
        """Generate .vscode/extensions.json."""
        extensions = {
            "recommendations": [ext.id for ext in RECOMMENDED_EXTENSIONS if ext.required],
            "unwantedRecommendations": [],
        }

        filepath = os.path.join(self.vscode_dir, "extensions.json")
        with open(filepath, "w") as f:
            json.dump(extensions, f, indent=4)
        return filepath

    def _generate_tasks(self) -> str:
        """Generate .vscode/tasks.json with pipeline tasks."""
        tasks = {
            "version": "2.0.0",
            "tasks": [
                {
                    "label": "AgentX5: Run Pipeline",
                    "type": "shell",
                    "command": "python -m agentx.orchestrator.pipeline",
                    "group": "build",
                    "problemMatcher": ["$python"],
                    "presentation": {"reveal": "always", "panel": "new"},
                },
                {
                    "label": "AgentX5: Run Tests",
                    "type": "shell",
                    "command": "python -m pytest tests/ -v --tb=short",
                    "group": "test",
                    "problemMatcher": ["$python"],
                },
                {
                    "label": "AgentX5: Run Remediation Engine",
                    "type": "shell",
                    "command": "python -m agentx.remediation.engine",
                    "group": "build",
                    "problemMatcher": ["$python"],
                },
                {
                    "label": "AgentX5: Lint (Ruff)",
                    "type": "shell",
                    "command": "ruff check agentx/ --fix",
                    "group": "build",
                    "problemMatcher": [],
                },
                {
                    "label": "AgentX5: Format (Black)",
                    "type": "shell",
                    "command": f"black agentx/ --line-length {self.config.line_length}",
                    "group": "build",
                    "problemMatcher": [],
                },
                {
                    "label": "AgentX5: Type Check (Mypy)",
                    "type": "shell",
                    "command": "mypy agentx/ --ignore-missing-imports",
                    "group": "build",
                    "problemMatcher": [],
                },
                {
                    "label": "AgentX5: Build Package",
                    "type": "shell",
                    "command": "python -m build",
                    "group": "build",
                    "problemMatcher": [],
                },
                {
                    "label": "AgentX5: Sync Repos to GitHub",
                    "type": "shell",
                    "command": "python -m agentx.integrations.repo_manager",
                    "group": "build",
                    "problemMatcher": [],
                },
            ],
        }

        filepath = os.path.join(self.vscode_dir, "tasks.json")
        with open(filepath, "w") as f:
            json.dump(tasks, f, indent=4)
        return filepath

    def _generate_launch(self) -> str:
        """Generate .vscode/launch.json for debugging."""
        launch = {
            "version": "0.2.0",
            "configurations": [
                {
                    "name": "AgentX5: Run Pipeline",
                    "type": "debugpy",
                    "request": "launch",
                    "module": "agentx.orchestrator.pipeline",
                    "console": "integratedTerminal",
                    "justMyCode": True,
                },
                {
                    "name": "AgentX5: Run Tests",
                    "type": "debugpy",
                    "request": "launch",
                    "module": "pytest",
                    "args": ["tests/", "-v", "--tb=short"],
                    "console": "integratedTerminal",
                },
                {
                    "name": "AgentX5: Remediation Engine",
                    "type": "debugpy",
                    "request": "launch",
                    "module": "agentx.remediation.engine",
                    "console": "integratedTerminal",
                },
                {
                    "name": "Python: Current File",
                    "type": "debugpy",
                    "request": "launch",
                    "program": "${file}",
                    "console": "integratedTerminal",
                },
            ],
        }

        filepath = os.path.join(self.vscode_dir, "launch.json")
        with open(filepath, "w") as f:
            json.dump(launch, f, indent=4)
        return filepath

    def _generate_workspace_file(self) -> str:
        """Generate the .code-workspace file."""
        workspace = {
            "folders": [{"path": "."}],
            "settings": {
                "python.defaultInterpreterPath": self.config.python_path,
                "editor.formatOnSave": True,
            },
            "extensions": {
                "recommendations": [ext.id for ext in RECOMMENDED_EXTENSIONS]
            },
            "tasks": {"version": "2.0.0", "tasks": []},
        }

        filepath = os.path.join(
            self.workspace_root, f"{self.config.workspace_name}.code-workspace"
        )
        with open(filepath, "w") as f:
            json.dump(workspace, f, indent=4)
        return filepath
