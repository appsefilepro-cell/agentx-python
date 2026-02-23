"""
Cloud Service Integrations for AgentX5.

Provides connectors for:
- Dropbox (file storage and sync)
- Box (enterprise content management)
- Google Cloud Platform (infrastructure and services)
- Sandbox environments (M1/M2, cloud containers)

All connectors follow a unified interface for the pipeline orchestrator.
"""

import os
import json
import logging
from typing import List, Dict, Optional, Any, BinaryIO
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class CloudFile(BaseModel):
    """Represents a file in cloud storage."""

    name: str
    path: str
    size: int = 0
    modified: Optional[str] = None
    content_hash: Optional[str] = None
    download_url: Optional[str] = None


class SyncResult(BaseModel):
    """Result from a file sync operation."""

    uploaded: int = 0
    downloaded: int = 0
    skipped: int = 0
    errors: List[str] = Field(default_factory=list)


class DropboxConnector:
    """
    Dropbox integration for file storage and synchronization.

    Provides:
    - File upload/download
    - Folder listing and management
    - Sync with local directories
    - Shared link generation
    """

    BASE_URL = "https://api.dropboxapi.com/2"
    CONTENT_URL = "https://content.dropboxapi.com/2"

    def __init__(self, access_token: Optional[str] = None):
        self.access_token = access_token or os.getenv("DROPBOX_ACCESS_TOKEN")
        if not self.access_token:
            logger.warning("Dropbox access token not configured")

    def _headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }

    def list_folder(self, path: str = "") -> List[CloudFile]:
        """List files in a Dropbox folder."""
        import requests

        response = requests.post(
            f"{self.BASE_URL}/files/list_folder",
            headers=self._headers(),
            json={"path": path or "", "recursive": False, "limit": 2000},
        )
        if response.status_code == 200:
            entries = response.json().get("entries", [])
            return [
                CloudFile(
                    name=e.get("name", ""),
                    path=e.get("path_display", ""),
                    size=e.get("size", 0),
                    modified=e.get("server_modified"),
                    content_hash=e.get("content_hash"),
                )
                for e in entries
                if e.get(".tag") == "file"
            ]
        raise Exception(f"Dropbox list_folder failed: {response.status_code}")

    def upload_file(self, local_path: str, dropbox_path: str) -> CloudFile:
        """Upload a file to Dropbox."""
        import requests

        with open(local_path, "rb") as f:
            response = requests.post(
                f"{self.CONTENT_URL}/files/upload",
                headers={
                    "Authorization": f"Bearer {self.access_token}",
                    "Content-Type": "application/octet-stream",
                    "Dropbox-API-Arg": json.dumps(
                        {"path": dropbox_path, "mode": "overwrite", "autorename": True}
                    ),
                },
                data=f,
            )
        if response.status_code == 200:
            data = response.json()
            return CloudFile(
                name=data.get("name", ""),
                path=data.get("path_display", ""),
                size=data.get("size", 0),
                modified=data.get("server_modified"),
                content_hash=data.get("content_hash"),
            )
        raise Exception(f"Dropbox upload failed: {response.status_code}")

    def download_file(self, dropbox_path: str, local_path: str) -> str:
        """Download a file from Dropbox to local path."""
        import requests

        response = requests.post(
            f"{self.CONTENT_URL}/files/download",
            headers={
                "Authorization": f"Bearer {self.access_token}",
                "Dropbox-API-Arg": json.dumps({"path": dropbox_path}),
            },
        )
        if response.status_code == 200:
            with open(local_path, "wb") as f:
                f.write(response.content)
            return local_path
        raise Exception(f"Dropbox download failed: {response.status_code}")

    def create_shared_link(self, path: str) -> str:
        """Create a shared link for a Dropbox file."""
        import requests

        response = requests.post(
            f"{self.BASE_URL}/sharing/create_shared_link_with_settings",
            headers=self._headers(),
            json={"path": path, "settings": {"requested_visibility": "public"}},
        )
        if response.status_code == 200:
            return response.json().get("url", "")
        raise Exception(f"Dropbox shared link failed: {response.status_code}")


class BoxConnector:
    """
    Box integration for enterprise content management.

    Provides:
    - File upload/download
    - Folder management
    - Enterprise-grade security and compliance
    - Metadata and classification
    """

    BASE_URL = "https://api.box.com/2.0"
    UPLOAD_URL = "https://upload.box.com/api/2.0"

    def __init__(self, access_token: Optional[str] = None):
        self.access_token = access_token or os.getenv("BOX_ACCESS_TOKEN")
        if not self.access_token:
            logger.warning("Box access token not configured")

    def _headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }

    def list_folder(self, folder_id: str = "0") -> List[CloudFile]:
        """List items in a Box folder (0 = root)."""
        import requests

        response = requests.get(
            f"{self.BASE_URL}/folders/{folder_id}/items",
            headers=self._headers(),
            params={"limit": 1000, "fields": "name,size,modified_at,sha1"},
        )
        if response.status_code == 200:
            entries = response.json().get("entries", [])
            return [
                CloudFile(
                    name=e.get("name", ""),
                    path=f"/{e.get('name', '')}",
                    size=e.get("size", 0),
                    modified=e.get("modified_at"),
                    content_hash=e.get("sha1"),
                )
                for e in entries
                if e.get("type") == "file"
            ]
        raise Exception(f"Box list_folder failed: {response.status_code}")

    def upload_file(
        self, local_path: str, folder_id: str = "0", filename: Optional[str] = None
    ) -> CloudFile:
        """Upload a file to Box."""
        import requests

        fname = filename or os.path.basename(local_path)
        with open(local_path, "rb") as f:
            response = requests.post(
                f"{self.UPLOAD_URL}/files/content",
                headers={"Authorization": f"Bearer {self.access_token}"},
                data={
                    "attributes": json.dumps(
                        {"name": fname, "parent": {"id": folder_id}}
                    )
                },
                files={"file": (fname, f)},
            )
        if response.status_code in (200, 201):
            entries = response.json().get("entries", [{}])
            data = entries[0] if entries else {}
            return CloudFile(
                name=data.get("name", fname),
                path=f"/{data.get('name', fname)}",
                size=data.get("size", 0),
                modified=data.get("modified_at"),
            )
        raise Exception(f"Box upload failed: {response.status_code}")

    def download_file(self, file_id: str, local_path: str) -> str:
        """Download a file from Box."""
        import requests

        response = requests.get(
            f"{self.BASE_URL}/files/{file_id}/content",
            headers={"Authorization": f"Bearer {self.access_token}"},
            allow_redirects=True,
        )
        if response.status_code == 200:
            with open(local_path, "wb") as f:
                f.write(response.content)
            return local_path
        raise Exception(f"Box download failed: {response.status_code}")


class GoogleCloudConnector:
    """
    Google Cloud Platform integration.

    Provides:
    - Cloud Storage operations
    - Cloud Functions deployment
    - Cloud Run service management
    - BigQuery operations
    - IAM and security management
    """

    def __init__(self, credentials_path: Optional[str] = None):
        self.credentials_path = credentials_path or os.getenv(
            "GOOGLE_APPLICATION_CREDENTIALS"
        )
        self.project_id = os.getenv("GCP_PROJECT_ID")

    def get_storage_client(self):
        """Get Google Cloud Storage client."""
        try:
            from google.cloud import storage

            return storage.Client()
        except ImportError:
            raise ImportError(
                "google-cloud-storage is required. "
                "Install with: pip install google-cloud-storage"
            )

    def list_buckets(self) -> List[str]:
        """List all GCS buckets."""
        client = self.get_storage_client()
        return [bucket.name for bucket in client.list_buckets()]

    def upload_to_gcs(
        self, local_path: str, bucket_name: str, blob_name: str
    ) -> str:
        """Upload a file to Google Cloud Storage."""
        client = self.get_storage_client()
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(blob_name)
        blob.upload_from_filename(local_path)
        return f"gs://{bucket_name}/{blob_name}"

    def download_from_gcs(
        self, bucket_name: str, blob_name: str, local_path: str
    ) -> str:
        """Download a file from Google Cloud Storage."""
        client = self.get_storage_client()
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(blob_name)
        blob.download_to_filename(local_path)
        return local_path

    def deploy_cloud_function(
        self,
        function_name: str,
        source_dir: str,
        entry_point: str,
        runtime: str = "python311",
        region: str = "us-central1",
    ) -> Dict[str, Any]:
        """Deploy a Google Cloud Function."""
        import subprocess

        cmd = [
            "gcloud",
            "functions",
            "deploy",
            function_name,
            f"--source={source_dir}",
            f"--entry-point={entry_point}",
            f"--runtime={runtime}",
            f"--region={region}",
            "--trigger-http",
            "--allow-unauthenticated",
            "--format=json",
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            return json.loads(result.stdout)
        raise Exception(f"Cloud Function deploy failed: {result.stderr}")

    def deploy_cloud_run(
        self,
        service_name: str,
        image: str,
        region: str = "us-central1",
        env_vars: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        """Deploy a Cloud Run service."""
        import subprocess

        cmd = [
            "gcloud",
            "run",
            "deploy",
            service_name,
            f"--image={image}",
            f"--region={region}",
            "--platform=managed",
            "--allow-unauthenticated",
            "--format=json",
        ]
        if env_vars:
            env_str = ",".join(f"{k}={v}" for k, v in env_vars.items())
            cmd.append(f"--set-env-vars={env_str}")

        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            return json.loads(result.stdout)
        raise Exception(f"Cloud Run deploy failed: {result.stderr}")


class SandboxEnvironment:
    """
    Sandbox environment manager for isolated code execution.

    Supports:
    - M1/M2 local sandbox (Docker-based)
    - Cloud sandbox (GCP, AWS containers)
    - Manus remote sandbox integration
    """

    def __init__(self, sandbox_type: str = "docker"):
        self.sandbox_type = sandbox_type
        self.container_id: Optional[str] = None

    def create_sandbox(
        self,
        image: str = "python:3.11-slim",
        name: Optional[str] = None,
        env_vars: Optional[Dict[str, str]] = None,
        volumes: Optional[Dict[str, str]] = None,
    ) -> str:
        """Create an isolated sandbox container."""
        import subprocess

        cmd = ["docker", "run", "-d", "--rm"]
        if name:
            cmd.extend(["--name", name])
        if env_vars:
            for k, v in env_vars.items():
                cmd.extend(["-e", f"{k}={v}"])
        if volumes:
            for host_path, container_path in volumes.items():
                cmd.extend(["-v", f"{host_path}:{container_path}"])
        cmd.extend([image, "tail", "-f", "/dev/null"])

        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            self.container_id = result.stdout.strip()[:12]
            logger.info(f"Sandbox created: {self.container_id}")
            return self.container_id
        raise Exception(f"Sandbox creation failed: {result.stderr}")

    def execute_in_sandbox(
        self, command: str, container_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Execute a command inside the sandbox."""
        import subprocess

        cid = container_id or self.container_id
        if not cid:
            raise ValueError("No active sandbox container")

        result = subprocess.run(
            ["docker", "exec", cid, "bash", "-c", command],
            capture_output=True,
            text=True,
            timeout=300,
        )
        return {
            "exit_code": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
        }

    def install_package(
        self, package: str, container_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Install a Python package in the sandbox."""
        return self.execute_in_sandbox(
            f"pip install {package}", container_id
        )

    def copy_to_sandbox(
        self, local_path: str, container_path: str, container_id: Optional[str] = None
    ) -> bool:
        """Copy a file into the sandbox."""
        import subprocess

        cid = container_id or self.container_id
        if not cid:
            raise ValueError("No active sandbox container")

        result = subprocess.run(
            ["docker", "cp", local_path, f"{cid}:{container_path}"],
            capture_output=True,
            text=True,
        )
        return result.returncode == 0

    def copy_from_sandbox(
        self, container_path: str, local_path: str, container_id: Optional[str] = None
    ) -> bool:
        """Copy a file from the sandbox."""
        import subprocess

        cid = container_id or self.container_id
        if not cid:
            raise ValueError("No active sandbox container")

        result = subprocess.run(
            ["docker", "cp", f"{cid}:{container_path}", local_path],
            capture_output=True,
            text=True,
        )
        return result.returncode == 0

    def destroy_sandbox(self, container_id: Optional[str] = None) -> bool:
        """Destroy the sandbox container."""
        import subprocess

        cid = container_id or self.container_id
        if not cid:
            return True

        result = subprocess.run(
            ["docker", "stop", cid], capture_output=True, text=True
        )
        if result.returncode == 0:
            self.container_id = None
            logger.info(f"Sandbox destroyed: {cid}")
        return result.returncode == 0
