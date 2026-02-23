"""
Agent Profiles Registry for AgentX5 Multi-Agent Orchestration.

Defines the strengths, weaknesses, and capabilities of each coding AI agent
in the pipeline. Used by the TaskRouter to assign work optimally.

Agents:
1. Claude Code (Anthropic) - Primary structural framework / coder
2. OpenAI Codex 5.1 (Kodex) - Genetic autonomous coding agent
3. GitHub Copilot CLI - IDE-integrated code completion & deployment
4. Google Cloud CLI (Gemini) - Cloud infrastructure & services
5. VS Code AI Extensions - IDE automation & workspace management
6. GitHub/GitLab Duo - Repository management & CI/CD
7. Zapier Duo - Workflow automation & cross-platform integration
8. Manus - Autonomous sandbox execution agent
9. Abacus AI - Legal drafting & financial analysis
10. Firecrawl - Web crawling & data extraction
"""

from typing import List, Dict, Optional
from pydantic import BaseModel, Field
from enum import Enum


class AgentCapability(str, Enum):
    CODE_GENERATION = "code_generation"
    CODE_REVIEW = "code_review"
    DEBUGGING = "debugging"
    TESTING = "testing"
    DEPLOYMENT = "deployment"
    CI_CD = "ci_cd"
    CLOUD_INFRA = "cloud_infrastructure"
    IDE_AUTOMATION = "ide_automation"
    WORKFLOW_AUTOMATION = "workflow_automation"
    REPO_MANAGEMENT = "repo_management"
    LEGAL_DRAFTING = "legal_drafting"
    FINANCIAL_ANALYSIS = "financial_analysis"
    WEB_CRAWLING = "web_crawling"
    DATA_EXTRACTION = "data_extraction"
    SANDBOX_EXECUTION = "sandbox_execution"
    DOCUMENTATION = "documentation"
    SECURITY_AUDIT = "security_audit"
    REFACTORING = "refactoring"
    ARCHITECTURE = "architecture"
    API_INTEGRATION = "api_integration"


class AgentProfile(BaseModel):
    """Profile defining an agent's capabilities, strengths, and weaknesses."""

    id: str
    name: str
    provider: str
    description: str
    version: Optional[str] = None
    api_env_var: str  # Environment variable for the API key
    strengths: List[str] = Field(default_factory=list)
    weaknesses: List[str] = Field(default_factory=list)
    capabilities: List[AgentCapability] = Field(default_factory=list)
    max_context_tokens: int = 0
    supports_streaming: bool = False
    supports_sandbox: bool = False
    cost_tier: str = "standard"  # budget, standard, premium
    priority_rank: int = 5  # 1 = highest priority
    enabled: bool = True

    class Config:
        use_enum_values = True


# ============================================================
# AGENT REGISTRY - All Coding Agents with Strengths & Weaknesses
# ============================================================

AGENT_PROFILES: Dict[str, AgentProfile] = {
    # --------------------------------------------------------
    # 1. CLAUDE CODE (Anthropic) - Primary Structural Framework
    # --------------------------------------------------------
    "claude_code": AgentProfile(
        id="claude_code",
        name="Claude Code",
        provider="Anthropic",
        description="Primary structural framework and code architect. Top 90th percentile for code structure, planning, and multi-file refactoring.",
        version="opus-4.5",
        api_env_var="ANTHROPIC_API_KEY",
        strengths=[
            "Exceptional code architecture and structural design",
            "Multi-file refactoring with full context awareness",
            "Detailed chain-of-thought reasoning for complex problems",
            "Strong natural language understanding for requirements analysis",
            "Excellent documentation and code explanation generation",
            "Superior error analysis and debugging with root cause identification",
            "Git operations and version control workflow management",
            "Cross-language code translation and migration",
            "Security vulnerability detection (OWASP top 10)",
            "Long-context window for large codebase comprehension",
        ],
        weaknesses=[
            "Not designed for direct sandbox execution environments",
            "Cannot directly execute or test code in isolated containers",
            "Limited real-time web browsing for live data",
            "No direct IDE plugin for inline completions",
            "Cannot autonomously deploy to production without CI/CD wrapper",
        ],
        capabilities=[
            AgentCapability.CODE_GENERATION,
            AgentCapability.CODE_REVIEW,
            AgentCapability.DEBUGGING,
            AgentCapability.DOCUMENTATION,
            AgentCapability.REFACTORING,
            AgentCapability.ARCHITECTURE,
            AgentCapability.SECURITY_AUDIT,
            AgentCapability.API_INTEGRATION,
        ],
        max_context_tokens=200000,
        supports_streaming=True,
        supports_sandbox=False,
        cost_tier="premium",
        priority_rank=2,
    ),
    # --------------------------------------------------------
    # 2. OPENAI CODEX 5.1 (Kodex) - Genetic Autonomous Coder
    # --------------------------------------------------------
    "openai_codex": AgentProfile(
        id="openai_codex",
        name="OpenAI Codex 5.1 (Kodex)",
        provider="OpenAI",
        description="Genetic autonomous coding AI agent. The primary coder for superagent-level autonomous task execution. Best coder in the pipeline.",
        version="codex-5.1",
        api_env_var="OPENAI_API_KEY",
        strengths=[
            "Superior autonomous code generation across all languages",
            "Genetic algorithm-based code optimization and evolution",
            "Full sandbox execution with container isolation",
            "Real-time code testing and validation in runtime",
            "Autonomous multi-step task completion without human intervention",
            "Strong API integration and endpoint generation",
            "Excellent at rapid prototyping and MVP creation",
            "Native tool-use for file operations, git, and terminal commands",
            "Post-human super-tier autonomous execution capability",
            "Parallel task execution across multiple workstreams",
        ],
        weaknesses=[
            "Higher API cost for extended autonomous sessions",
            "Context window smaller than Claude for very large codebases",
            "May over-engineer solutions when simpler approaches exist",
            "Less transparent chain-of-thought compared to Claude",
            "Requires careful prompt engineering for precise outputs",
        ],
        capabilities=[
            AgentCapability.CODE_GENERATION,
            AgentCapability.DEBUGGING,
            AgentCapability.TESTING,
            AgentCapability.SANDBOX_EXECUTION,
            AgentCapability.API_INTEGRATION,
            AgentCapability.DEPLOYMENT,
            AgentCapability.REFACTORING,
        ],
        max_context_tokens=128000,
        supports_streaming=True,
        supports_sandbox=True,
        cost_tier="premium",
        priority_rank=1,
    ),
    # --------------------------------------------------------
    # 3. GITHUB COPILOT CLI - IDE Code Completion & Deployment
    # --------------------------------------------------------
    "github_copilot": AgentProfile(
        id="github_copilot",
        name="GitHub Copilot CLI",
        provider="GitHub / Microsoft",
        description="IDE-integrated code completion, deployment pipeline, and Copilot CLI for terminal-based AI coding.",
        version="copilot-cli-latest",
        api_env_var="GITHUB_TOKEN",
        strengths=[
            "Best-in-class inline code completion in VS Code / IDEs",
            "Native GitHub integration for PRs, issues, and actions",
            "Copilot CLI for terminal command generation and explanation",
            "Excellent at boilerplate generation and pattern completion",
            "Strong TypeScript/JavaScript ecosystem support",
            "Context-aware suggestions from open editor files",
            "Pull request summarization and review assistance",
            "GitHub Actions workflow generation and debugging",
        ],
        weaknesses=[
            "Limited to suggestion-based interaction (not autonomous execution)",
            "Smaller context window than dedicated LLM agents",
            "Cannot independently create and manage full projects",
            "Requires IDE or CLI environment to function",
            "Less effective for architectural decisions and complex refactoring",
        ],
        capabilities=[
            AgentCapability.CODE_GENERATION,
            AgentCapability.CODE_REVIEW,
            AgentCapability.CI_CD,
            AgentCapability.REPO_MANAGEMENT,
            AgentCapability.DEPLOYMENT,
            AgentCapability.IDE_AUTOMATION,
        ],
        max_context_tokens=8000,
        supports_streaming=True,
        supports_sandbox=False,
        cost_tier="standard",
        priority_rank=3,
    ),
    # --------------------------------------------------------
    # 4. GOOGLE CLOUD CLI (Gemini) - Cloud Infrastructure
    # --------------------------------------------------------
    "google_cloud_cli": AgentProfile(
        id="google_cloud_cli",
        name="Google Cloud CLI (Gemini)",
        provider="Google",
        description="Google Cloud SDK with Gemini AI integration for cloud infrastructure management, deployment, and GCP services.",
        version="gcloud-cli-latest",
        api_env_var="GOOGLE_APPLICATION_CREDENTIALS",
        strengths=[
            "Native Google Cloud Platform infrastructure management",
            "Kubernetes (GKE) cluster provisioning and management",
            "Cloud Functions and Cloud Run serverless deployment",
            "BigQuery data analytics and pipeline orchestration",
            "Firebase integration for frontend and mobile backends",
            "Gemini AI for cloud architecture recommendations",
            "IAM and security policy management",
            "Cloud Storage and database service management",
        ],
        weaknesses=[
            "Vendor-locked to Google Cloud Platform ecosystem",
            "Not designed for general-purpose code generation",
            "Complex authentication setup with service accounts",
            "Limited usefulness outside cloud infrastructure tasks",
            "Steep learning curve for multi-service orchestration",
        ],
        capabilities=[
            AgentCapability.CLOUD_INFRA,
            AgentCapability.DEPLOYMENT,
            AgentCapability.SECURITY_AUDIT,
            AgentCapability.DATA_EXTRACTION,
        ],
        max_context_tokens=32000,
        supports_streaming=False,
        supports_sandbox=True,
        cost_tier="standard",
        priority_rank=5,
    ),
    # --------------------------------------------------------
    # 5. VS CODE AI EXTENSIONS - IDE Automation
    # --------------------------------------------------------
    "vscode_ai": AgentProfile(
        id="vscode_ai",
        name="VS Code AI Extensions",
        provider="Microsoft",
        description="VS Code integrated AI extensions for workspace automation, debugging, and intelligent code navigation.",
        version="vscode-latest",
        api_env_var="GITHUB_TOKEN",
        strengths=[
            "Deep IDE integration for real-time code assistance",
            "Integrated terminal and debugging automation",
            "Workspace configuration and settings management",
            "Extension ecosystem for specialized tool integration",
            "Multi-language IntelliSense and code navigation",
            "Live Share for collaborative coding sessions",
            "Integrated Git GUI for version control operations",
        ],
        weaknesses=[
            "Requires desktop or codespaces environment",
            "Extension conflicts can degrade performance",
            "Limited autonomous capability without human interaction",
            "Cannot operate headlessly for CI/CD pipelines",
        ],
        capabilities=[
            AgentCapability.IDE_AUTOMATION,
            AgentCapability.DEBUGGING,
            AgentCapability.CODE_GENERATION,
            AgentCapability.REPO_MANAGEMENT,
        ],
        max_context_tokens=8000,
        supports_streaming=True,
        supports_sandbox=False,
        cost_tier="budget",
        priority_rank=6,
    ),
    # --------------------------------------------------------
    # 6. GITHUB / GITLAB DUO - Repository & CI/CD Management
    # --------------------------------------------------------
    "gitlab_duo": AgentProfile(
        id="gitlab_duo",
        name="GitHub / GitLab Duo",
        provider="GitLab",
        description="Combined GitHub and GitLab Duo for repository management, CI/CD pipelines, merge requests, and DevSecOps.",
        version="duo-latest",
        api_env_var="GITLAB_TOKEN",
        strengths=[
            "Full CI/CD pipeline creation, management, and debugging",
            "Merge request analysis and automated code review",
            "Container registry and artifact management",
            "DevSecOps scanning (SAST, DAST, dependency scanning)",
            "Environment management (staging, production, review apps)",
            "Auto-DevOps for automatic pipeline configuration",
            "Issue tracking and project management integration",
            "Infrastructure as Code (IaC) integration with Terraform",
        ],
        weaknesses=[
            "Primarily focused on DevOps, not code generation",
            "Complex YAML configuration for advanced pipelines",
            "Limited natural language understanding for code tasks",
            "Duo AI features still maturing compared to standalone LLMs",
            "Requires self-hosted runners for private infrastructure",
        ],
        capabilities=[
            AgentCapability.CI_CD,
            AgentCapability.DEPLOYMENT,
            AgentCapability.REPO_MANAGEMENT,
            AgentCapability.SECURITY_AUDIT,
            AgentCapability.TESTING,
        ],
        max_context_tokens=16000,
        supports_streaming=False,
        supports_sandbox=True,
        cost_tier="standard",
        priority_rank=4,
    ),
    # --------------------------------------------------------
    # 7. ZAPIER DUO - Workflow Automation
    # --------------------------------------------------------
    "zapier_duo": AgentProfile(
        id="zapier_duo",
        name="Zapier Duo",
        provider="Zapier",
        description="AI-powered workflow automation for cross-platform integration, data sync, and event-driven task orchestration.",
        version="zapier-ai-latest",
        api_env_var="ZAPIER_API_KEY",
        strengths=[
            "Cross-platform workflow automation (6000+ app integrations)",
            "Event-driven trigger and action pipelines",
            "No-code/low-code automation for business processes",
            "Data transformation and mapping between services",
            "Scheduled task execution and monitoring",
            "Webhook-based real-time integration",
            "Multi-step workflow (Zap) creation and management",
        ],
        weaknesses=[
            "Not designed for code generation or review",
            "Limited to API-level integration (no deep code access)",
            "Execution delays on free/lower tier plans",
            "Complex data transformations require custom code steps",
            "Rate limits on high-volume automation workflows",
        ],
        capabilities=[
            AgentCapability.WORKFLOW_AUTOMATION,
            AgentCapability.API_INTEGRATION,
            AgentCapability.DATA_EXTRACTION,
        ],
        max_context_tokens=4000,
        supports_streaming=False,
        supports_sandbox=False,
        cost_tier="standard",
        priority_rank=7,
    ),
    # --------------------------------------------------------
    # 8. MANUS - Autonomous Sandbox Execution Agent
    # --------------------------------------------------------
    "manus": AgentProfile(
        id="manus",
        name="Manus Autonomous Agent",
        provider="Manus AI",
        description="Fully autonomous sandbox execution agent. Runs Python scripts, installs SDKs, manages files, and executes multi-step terminal operations in isolated environments.",
        version="manus-latest",
        api_env_var="MANUS_API_KEY",
        strengths=[
            "Full autonomous sandbox execution (Ubuntu environment)",
            "Direct terminal command execution without human intervention",
            "SDK and package installation in real-time",
            "File system operations (create, read, write, delete)",
            "Multi-step autonomous task orchestration with live monitoring",
            "Google Cloud SDK installation and configuration",
            "Python script execution with real-time output",
            "Web browsing and data extraction capabilities",
            "Integration with external tools (curl, wget, git)",
            "Live progress streaming for long-running operations",
        ],
        weaknesses=[
            "Sandbox environment resets between sessions",
            "Limited persistent storage without external integration",
            "Network restrictions in some sandbox configurations",
            "Higher latency for complex multi-step operations",
            "Session-based (no always-on daemon capability)",
        ],
        capabilities=[
            AgentCapability.SANDBOX_EXECUTION,
            AgentCapability.DEPLOYMENT,
            AgentCapability.TESTING,
            AgentCapability.CODE_GENERATION,
            AgentCapability.CLOUD_INFRA,
            AgentCapability.WEB_CRAWLING,
        ],
        max_context_tokens=128000,
        supports_streaming=True,
        supports_sandbox=True,
        cost_tier="premium",
        priority_rank=2,
    ),
    # --------------------------------------------------------
    # 9. ABACUS AI - Legal Drafting & Financial Analysis
    # --------------------------------------------------------
    "abacus_ai": AgentProfile(
        id="abacus_ai",
        name="Abacus AI",
        provider="Abacus.AI",
        description="AI platform for legal drafting, forensic analysis, financial modeling, and audit-ready document generation. Integrated with Apps Holdings corporate systems.",
        version="abacus-cli-59ea",
        api_env_var="ABACUS_API_KEY",
        strengths=[
            "Legal document drafting with Ivy League standards",
            "Master Forensic Omnibus generation (audit-proof, enforcement-ready)",
            "Financial analysis and fraud detection modeling",
            "Corporate compliance and regulatory document generation",
            "Data vault management for sensitive corporate records",
            "Integration with legal filing and court systems",
            "Automated police report and incident documentation",
            "Chain-of-custody evidence management",
        ],
        weaknesses=[
            "Not designed for general software development",
            "Requires domain-specific configuration for legal jurisdictions",
            "Limited code generation capability",
            "Specialized vocabulary may not generalize to other domains",
            "Dependent on external data sources for current legal standards",
        ],
        capabilities=[
            AgentCapability.LEGAL_DRAFTING,
            AgentCapability.FINANCIAL_ANALYSIS,
            AgentCapability.DOCUMENTATION,
            AgentCapability.DATA_EXTRACTION,
            AgentCapability.SECURITY_AUDIT,
        ],
        max_context_tokens=64000,
        supports_streaming=True,
        supports_sandbox=False,
        cost_tier="premium",
        priority_rank=3,
    ),
    # --------------------------------------------------------
    # 10. FIRECRAWL - Web Crawling & Data Extraction
    # --------------------------------------------------------
    "firecrawl": AgentProfile(
        id="firecrawl",
        name="Firecrawl",
        provider="Firecrawl",
        description="Web crawling and data extraction engine. Provides search and crawl capabilities for AI agents to access live web data.",
        version="firecrawl-latest",
        api_env_var="FIRECRAWL_API_KEY",
        strengths=[
            "High-performance web crawling and scraping",
            "Structured data extraction from web pages",
            "JavaScript-rendered page support (headless browser)",
            "API endpoint discovery and documentation extraction",
            "Rate-limited crawling with politeness policies",
            "Output in structured JSON/markdown format",
        ],
        weaknesses=[
            "Read-only (cannot modify web resources)",
            "Subject to website terms of service and robots.txt",
            "Rate limits on high-volume crawling",
            "Cannot interact with authenticated web applications without credentials",
        ],
        capabilities=[
            AgentCapability.WEB_CRAWLING,
            AgentCapability.DATA_EXTRACTION,
        ],
        max_context_tokens=16000,
        supports_streaming=False,
        supports_sandbox=False,
        cost_tier="standard",
        priority_rank=8,
    ),
}


class AgentRegistry:
    """
    Central registry for all agent profiles.
    Provides lookup, filtering, and recommendation methods.
    """

    def __init__(self):
        self._profiles: Dict[str, AgentProfile] = dict(AGENT_PROFILES)

    def get(self, agent_id: str) -> Optional[AgentProfile]:
        """Get an agent profile by ID."""
        return self._profiles.get(agent_id)

    def list_all(self) -> List[AgentProfile]:
        """List all registered agent profiles."""
        return list(self._profiles.values())

    def list_enabled(self) -> List[AgentProfile]:
        """List only enabled agent profiles."""
        return [p for p in self._profiles.values() if p.enabled]

    def register(self, profile: AgentProfile):
        """Register a new agent profile."""
        self._profiles[profile.id] = profile

    def find_by_capability(
        self, capability: AgentCapability
    ) -> List[AgentProfile]:
        """Find all agents with a specific capability."""
        return [
            p
            for p in self._profiles.values()
            if capability in p.capabilities and p.enabled
        ]

    def find_by_provider(self, provider: str) -> List[AgentProfile]:
        """Find all agents from a specific provider."""
        return [
            p
            for p in self._profiles.values()
            if p.provider.lower() == provider.lower()
        ]

    def get_ranked(self) -> List[AgentProfile]:
        """Get all enabled agents sorted by priority rank (1=highest)."""
        enabled = self.list_enabled()
        return sorted(enabled, key=lambda p: p.priority_rank)

    def get_strengths_report(self) -> Dict[str, List[str]]:
        """Generate a report of all agent strengths."""
        return {p.name: p.strengths for p in self._profiles.values()}

    def get_weaknesses_report(self) -> Dict[str, List[str]]:
        """Generate a report of all agent weaknesses."""
        return {p.name: p.weaknesses for p in self._profiles.values()}

    def get_coverage_matrix(self) -> Dict[str, List[str]]:
        """Generate a capability coverage matrix showing which agents cover each capability."""
        matrix: Dict[str, List[str]] = {}
        for cap in AgentCapability:
            agents = self.find_by_capability(cap)
            matrix[cap.value] = [a.name for a in agents]
        return matrix

    def export_profiles(self) -> Dict[str, Any]:
        """Export all profiles as a dictionary."""
        return {
            agent_id: profile.model_dump()
            for agent_id, profile in self._profiles.items()
        }
