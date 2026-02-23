"""
Repository Management and GitHub Sync for AgentX5.

Provides:
- GitHub repository creation and management
- GitLab repository sync
- Multi-repo orchestration for corporate ownership
- Automated PR creation and management
- Repository health checks and compliance
- Corporate ownership verification
"""

import os
import json
import logging
import subprocess
from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class RepoConfig(BaseModel):
    """Repository configuration."""

    name: str
    description: str = ""
    private: bool = True
    owner: str = ""  # GitHub org or user
    default_branch: str = "main"
    topics: List[str] = Field(default_factory=list)
    has_issues: bool = True
    has_wiki: bool = False
    auto_init: bool = True
    license_template: str = "mit"


class RepoStatus(BaseModel):
    """Repository status information."""

    name: str
    full_name: str
    url: str
    default_branch: str
    is_private: bool
    last_push: Optional[str] = None
    open_prs: int = 0
    open_issues: int = 0
    topics: List[str] = Field(default_factory=list)


class RepoManager:
    """
    Multi-repository management for AgentX5 corporate infrastructure.

    Manages GitHub and GitLab repositories, ensuring all code is
    properly owned and organized under the corporate account.

    Uses GitHub CLI (gh) and GitLab CLI (glab) for operations.
    """

    def __init__(
        self,
        github_token: Optional[str] = None,
        gitlab_token: Optional[str] = None,
        owner: str = "",
    ):
        self.github_token = github_token or os.getenv("GITHUB_TOKEN")
        self.gitlab_token = gitlab_token or os.getenv("GITLAB_TOKEN")
        self.owner = owner

    def _run_gh(self, args: List[str]) -> Dict[str, Any]:
        """Run a GitHub CLI command."""
        env = os.environ.copy()
        if self.github_token:
            env["GH_TOKEN"] = self.github_token

        cmd = ["gh"] + args
        result = subprocess.run(
            cmd, capture_output=True, text=True, env=env
        )
        if result.returncode != 0:
            raise Exception(f"gh command failed: {result.stderr}")
        try:
            return json.loads(result.stdout) if result.stdout.strip() else {}
        except json.JSONDecodeError:
            return {"output": result.stdout}

    def create_repo(self, config: RepoConfig) -> Dict[str, Any]:
        """Create a new GitHub repository."""
        args = [
            "repo",
            "create",
            f"{config.owner}/{config.name}" if config.owner else config.name,
            f"--description={config.description}",
            f"--license={config.license_template}",
        ]
        if config.private:
            args.append("--private")
        else:
            args.append("--public")
        if config.auto_init:
            args.append("--add-readme")

        result = self._run_gh(args)
        logger.info(f"Repository created: {config.name}")

        # Add topics if specified
        if config.topics:
            self._set_topics(
                f"{config.owner}/{config.name}" if config.owner else config.name,
                config.topics,
            )

        return result

    def list_repos(self, owner: Optional[str] = None, limit: int = 100) -> List[Dict[str, Any]]:
        """List repositories for an owner."""
        target = owner or self.owner
        args = [
            "repo",
            "list",
            target,
            "--json=name,description,url,isPrivate,defaultBranchRef,pushedAt",
            f"--limit={limit}",
        ]
        return self._run_gh(args)

    def get_repo_status(self, repo: str) -> RepoStatus:
        """Get status of a specific repository."""
        args = [
            "repo",
            "view",
            repo,
            "--json=name,nameWithOwner,url,defaultBranchRef,isPrivate,pushedAt,repositoryTopics",
        ]
        data = self._run_gh(args)
        return RepoStatus(
            name=data.get("name", ""),
            full_name=data.get("nameWithOwner", ""),
            url=data.get("url", ""),
            default_branch=data.get("defaultBranchRef", {}).get("name", "main"),
            is_private=data.get("isPrivate", True),
            last_push=data.get("pushedAt"),
            topics=[
                t.get("name", "")
                for t in data.get("repositoryTopics", [])
            ],
        )

    def clone_repo(self, repo: str, target_dir: Optional[str] = None) -> str:
        """Clone a repository to local."""
        args = ["repo", "clone", repo]
        if target_dir:
            args.append(target_dir)
        self._run_gh(args)
        return target_dir or repo.split("/")[-1]

    def fork_repo(self, repo: str, org: Optional[str] = None) -> Dict[str, Any]:
        """Fork a repository."""
        args = ["repo", "fork", repo, "--clone=false"]
        if org:
            args.extend(["--org", org])
        return self._run_gh(args)

    def create_pr(
        self,
        repo: str,
        title: str,
        body: str,
        base: str = "main",
        head: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Create a pull request."""
        args = [
            "pr",
            "create",
            f"--repo={repo}",
            f"--title={title}",
            f"--body={body}",
            f"--base={base}",
        ]
        if head:
            args.append(f"--head={head}")
        return self._run_gh(args)

    def list_prs(
        self, repo: str, state: str = "open"
    ) -> List[Dict[str, Any]]:
        """List pull requests for a repository."""
        args = [
            "pr",
            "list",
            f"--repo={repo}",
            f"--state={state}",
            "--json=number,title,state,author,createdAt,url",
        ]
        return self._run_gh(args)

    def _set_topics(self, repo: str, topics: List[str]):
        """Set repository topics."""
        args = [
            "api",
            f"repos/{repo}/topics",
            "-X",
            "PUT",
            "-f",
            f"names={json.dumps(topics)}",
        ]
        try:
            self._run_gh(args)
        except Exception as e:
            logger.warning(f"Failed to set topics for {repo}: {e}")

    def sync_to_github(
        self, local_path: str, repo_name: str, branch: str = "main"
    ) -> bool:
        """
        Sync a local directory to a GitHub repository.

        Creates the repo if it doesn't exist, then pushes.
        """
        try:
            # Check if repo exists
            self.get_repo_status(f"{self.owner}/{repo_name}")
        except Exception:
            # Create if it doesn't exist
            self.create_repo(
                RepoConfig(
                    name=repo_name,
                    owner=self.owner,
                    description=f"Synced from AgentX5 Pipeline - {repo_name}",
                    private=True,
                    topics=["agentx5", "auto-synced"],
                )
            )

        # Git operations
        remote_url = f"https://github.com/{self.owner}/{repo_name}.git"
        cmds = [
            ["git", "-C", local_path, "init"],
            ["git", "-C", local_path, "remote", "add", "origin", remote_url],
            ["git", "-C", local_path, "add", "-A"],
            [
                "git",
                "-C",
                local_path,
                "commit",
                "-m",
                "AgentX5 Pipeline Sync",
            ],
            ["git", "-C", local_path, "push", "-u", "origin", branch],
        ]

        for cmd in cmds:
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                # Allow failures for already-existing remotes etc.
                logger.warning(f"Git command warning: {' '.join(cmd)} - {result.stderr}")

        logger.info(f"Synced {local_path} -> {self.owner}/{repo_name}")
        return True

    def run_health_check(self, repo: str) -> Dict[str, Any]:
        """Run a health check on a repository."""
        checks = {
            "repo": repo,
            "has_readme": False,
            "has_license": False,
            "has_ci": False,
            "has_security_policy": False,
            "branch_protection": False,
            "open_issues": 0,
            "open_prs": 0,
        }

        try:
            # Check repo contents
            args = [
                "api",
                f"repos/{repo}/contents",
                "--jq",
                ".[].name",
            ]
            result = self._run_gh(args)
            files = result.get("output", "").strip().split("\n")
            checks["has_readme"] = any(
                f.lower().startswith("readme") for f in files
            )
            checks["has_license"] = any(
                f.lower().startswith("license") for f in files
            )
            checks["has_ci"] = any(
                f in [".github", ".gitlab-ci.yml"] for f in files
            )
            checks["has_security_policy"] = any(
                f.upper() == "SECURITY.MD" for f in files
            )

            # Count open issues and PRs
            prs = self.list_prs(repo, "open")
            checks["open_prs"] = len(prs) if isinstance(prs, list) else 0

        except Exception as e:
            logger.warning(f"Health check partial failure for {repo}: {e}")

        return checks

    def transfer_ownership(
        self, repo: str, new_owner: str
    ) -> Dict[str, Any]:
        """Transfer repository ownership."""
        args = [
            "api",
            f"repos/{repo}/transfer",
            "-X",
            "POST",
            "-f",
            f"new_owner={new_owner}",
        ]
        return self._run_gh(args)
