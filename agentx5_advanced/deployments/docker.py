"""
AgentX5 Advanced Edition - Docker Deployment Configuration

Supports deployment to Docker containers across all environments.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any


DOCKERFILE_CONTENT = '''# AgentX5 Advanced Edition
# Multi-environment AI Orchestration System
FROM python:3.11-slim

LABEL maintainer="APPS Holdings WY, Inc."
LABEL version="1.0.0"
LABEL description="AgentX5 Advanced Edition with Abacus AI CLI Integration"

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV AGENTX5_ENV=production

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \\
    curl \\
    git \\
    nodejs \\
    npm \\
    && rm -rf /var/lib/apt/lists/*

# Install Abacus AI CLI globally
RUN npm install -g @abacus-ai/cli

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Install the package
RUN pip install -e .

# Expose ports
EXPOSE 8080 443

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \\
    CMD curl -f http://localhost:8080/health || exit 1

# Run the orchestrator
CMD ["python", "-m", "agentx5_advanced"]
'''

DOCKER_COMPOSE_CONTENT = '''version: "3.9"

services:
  agentx5:
    build:
      context: .
      dockerfile: Dockerfile
    image: agentx5-advanced:latest
    container_name: agentx5-orchestrator
    restart: unless-stopped
    ports:
      - "8080:8080"
      - "443:443"
    environment:
      - AGENTX5_ENV=production
      - ABACUS_API_KEY=${ABACUS_API_KEY}
      - ABACUS_API_ENDPOINT=${ABACUS_API_ENDPOINT}
      - AGENTX_API_KEY=${AGENTX_API_KEY}
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
    networks:
      - agentx5-network
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 10s

  redis:
    image: redis:7-alpine
    container_name: agentx5-redis
    restart: unless-stopped
    ports:
      - "6379:6379"
    volumes:
      - redis-data:/data
    networks:
      - agentx5-network

networks:
  agentx5-network:
    driver: bridge

volumes:
  redis-data:
'''


@dataclass
class DockerDeployment:
    """Docker deployment configuration for AgentX5 Advanced Edition."""

    image_name: str = "agentx5-advanced"
    image_tag: str = "latest"
    container_name: str = "agentx5-orchestrator"
    ports: List[int] = field(default_factory=lambda: [8080, 443])
    environment: Dict[str, str] = field(default_factory=dict)
    volumes: List[str] = field(default_factory=lambda: ["./data:/app/data", "./logs:/app/logs"])
    restart_policy: str = "unless-stopped"

    def get_dockerfile(self) -> str:
        """Get Dockerfile content."""
        return DOCKERFILE_CONTENT

    def get_docker_compose(self) -> str:
        """Get docker-compose.yml content."""
        return DOCKER_COMPOSE_CONTENT

    def get_build_command(self) -> str:
        """Get docker build command."""
        return f"docker build -t {self.image_name}:{self.image_tag} ."

    def get_run_command(self) -> str:
        """Get docker run command."""
        port_mappings = " ".join([f"-p {p}:{p}" for p in self.ports])
        return f"docker run -d --name {self.container_name} {port_mappings} {self.image_name}:{self.image_tag}"

    def get_compose_up_command(self) -> str:
        """Get docker-compose up command."""
        return "docker-compose up -d"

    def get_config(self) -> Dict[str, Any]:
        """Get deployment configuration as dictionary."""
        return {
            "image": f"{self.image_name}:{self.image_tag}",
            "container": self.container_name,
            "ports": self.ports,
            "volumes": self.volumes,
            "restart_policy": self.restart_policy,
            "commands": {
                "build": self.get_build_command(),
                "run": self.get_run_command(),
                "compose_up": self.get_compose_up_command(),
            },
        }
