"""
AgentX5 Advanced Edition - Multi-Platform Deployment Configurations

Supports: Cloud, iPhone, Laptop, Docker, Sandbox, Linux Ubuntu
"""

from typing import Dict, Any, List
from dataclasses import dataclass


SUPPORTED_PLATFORMS = [
    "cloud_vercel",
    "cloud_google",
    "cloud_github_actions",
    "mobile_iphone",
    "desktop_laptop",
    "container_docker",
    "container_sandbox",
    "server_linux_ubuntu",
]


@dataclass
class PlatformConfig:
    """Base configuration for a deployment platform."""
    name: str
    platform_type: str
    status: str = "ready"
    config: Dict[str, Any] = None

    def __post_init__(self):
        if self.config is None:
            self.config = {}


# ============================================================================
# PLATFORM CONFIGURATIONS
# ============================================================================

PLATFORM_CONFIGS: Dict[str, Dict[str, Any]] = {
    # Cloud Platforms
    "cloud_vercel": {
        "name": "Vercel AI Gateway",
        "platform_type": "cloud",
        "project_id": "prj_SeXMgdDSfCo4wdltc9fGv0HNd8Ww",
        "deployment_url": "https://agentx5.vercel.app",
        "features": ["serverless", "edge_functions", "ai_gateway"],
        "status": "connected",
        "setup_commands": [
            "npm i -g vercel",
            "vercel login",
            "vercel --prod",
        ],
    },
    "cloud_google": {
        "name": "Google Cloud Run",
        "platform_type": "cloud",
        "region": "us-central1",
        "memory": "1024Mi",
        "cpu": "1",
        "features": ["auto_scaling", "https", "custom_domains"],
        "status": "ready",
        "setup_commands": [
            "gcloud auth login",
            "gcloud config set project YOUR_PROJECT_ID",
            "gcloud run deploy agentx5 --source . --region us-central1",
        ],
    },
    "cloud_github_actions": {
        "name": "GitHub Actions CI/CD",
        "platform_type": "cloud",
        "repository": "private-claude",
        "workflows": ["ci-cd.yml", "release.yml", "test.yml"],
        "features": ["automated_testing", "deployment", "secrets_management"],
        "status": "active",
        "setup_commands": [
            "# Add secrets in GitHub Settings > Secrets",
            "# ABACUS_API_KEY",
            "# AGENTX_API_KEY",
        ],
    },

    # Mobile Platforms
    "mobile_iphone": {
        "name": "iPhone/iOS",
        "platform_type": "mobile",
        "api_access": True,
        "push_notifications": True,
        "features": ["api_client", "notifications", "shortcuts"],
        "status": "configured",
        "setup_commands": [
            "# Use REST API endpoints from any HTTP client",
            "# Configure Shortcuts app for quick commands",
        ],
    },

    # Desktop Platforms
    "desktop_laptop": {
        "name": "Desktop/Laptop",
        "platform_type": "desktop",
        "supported_os": ["macOS", "Windows", "Linux"],
        "cli_available": True,
        "features": ["full_cli", "local_development", "testing"],
        "status": "ready",
        "setup_commands": {
            "all": [
                "pip install agentx-python",
                "npm install -g @abacus-ai/cli",
            ],
            "macos_linux": [
                'export ABACUS_API_KEY="YOUR_KEY"',
                'export AGENTX_API_KEY="YOUR_KEY"',
            ],
            "windows_powershell": [
                '$env:ABACUS_API_KEY="YOUR_KEY"',
                '$env:AGENTX_API_KEY="YOUR_KEY"',
            ],
            "windows_cmd": [
                'set ABACUS_API_KEY=YOUR_KEY',
                'set AGENTX_API_KEY=YOUR_KEY',
            ],
        },
    },

    # Container Platforms
    "container_docker": {
        "name": "Docker",
        "platform_type": "container",
        "image": "agentx5-advanced:latest",
        "ports": [8080, 443],
        "features": ["isolation", "portability", "scaling"],
        "status": "buildable",
        "setup_commands": [
            "docker build -t agentx5-advanced:latest .",
            "docker-compose up -d",
        ],
    },
    "container_sandbox": {
        "name": "Sandbox Environment",
        "platform_type": "container",
        "runtime": "python3.11",
        "isolation": "full",
        "features": ["isolated_testing", "safe_execution", "reproducible"],
        "status": "ready",
        "setup_commands": [
            "python -m venv sandbox_env",
            "source sandbox_env/bin/activate",  # or sandbox_env\\Scripts\\activate on Windows
            "pip install -e .",
        ],
    },

    # Server Platforms
    "server_linux_ubuntu": {
        "name": "Linux Ubuntu Server",
        "platform_type": "server",
        "ubuntu_version": "22.04 LTS",
        "python_version": "3.11",
        "features": ["production_ready", "systemd_service", "nginx_proxy"],
        "status": "supported",
        "setup_commands": [
            "sudo apt update && sudo apt upgrade -y",
            "sudo apt install python3.11 python3.11-venv python3-pip nodejs npm -y",
            "npm install -g @abacus-ai/cli",
            "python3.11 -m pip install agentx-python",
            "# Configure systemd service for auto-start",
        ],
        "systemd_service": '''[Unit]
Description=AgentX5 Advanced Edition Orchestrator
After=network.target

[Service]
Type=simple
User=agentx5
WorkingDirectory=/opt/agentx5
Environment="ABACUS_API_KEY=YOUR_KEY"
Environment="AGENTX_API_KEY=YOUR_KEY"
ExecStart=/usr/bin/python3.11 -m agentx5_advanced
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
''',
    },
}


def get_deployment_config(platform: str) -> Dict[str, Any]:
    """Get deployment configuration for a specific platform."""
    if platform not in PLATFORM_CONFIGS:
        available = ", ".join(PLATFORM_CONFIGS.keys())
        raise ValueError(f"Unknown platform: {platform}. Available: {available}")
    return PLATFORM_CONFIGS[platform]


def get_all_deployment_configs() -> Dict[str, Dict[str, Any]]:
    """Get all deployment configurations."""
    return PLATFORM_CONFIGS.copy()


def get_setup_commands(platform: str) -> List[str]:
    """Get setup commands for a specific platform."""
    config = get_deployment_config(platform)
    commands = config.get("setup_commands", [])
    if isinstance(commands, dict):
        # Flatten nested command dicts
        all_commands = []
        for key, cmds in commands.items():
            all_commands.extend(cmds)
        return all_commands
    return commands
