"""Tests for integration modules."""
import pytest


class TestCloudServices:
    """Test cloud service integrations."""

    def test_dropbox_client_init(self):
        """DropboxClient should initialize."""
        from agentx.integrations.cloud_services import DropboxClient
        client = DropboxClient()
        assert client is not None

    def test_box_client_init(self):
        """BoxClient should initialize."""
        from agentx.integrations.cloud_services import BoxClient
        client = BoxClient()
        assert client is not None

    def test_google_cloud_client_init(self):
        """GoogleCloudClient should initialize."""
        from agentx.integrations.cloud_services import GoogleCloudClient
        client = GoogleCloudClient()
        assert client is not None


class TestIDEIntegration:
    """Test IDE integration module."""

    def test_vscode_manager_init(self):
        """VSCodeManager should initialize."""
        from agentx.integrations.ide import VSCodeManager
        manager = VSCodeManager()
        assert manager is not None

    def test_get_recommended_extensions(self):
        """Should return recommended extensions."""
        from agentx.integrations.ide import VSCodeManager
        manager = VSCodeManager()
        extensions = manager.get_recommended_extensions()
        assert len(extensions) > 0


class TestLegalIntegration:
    """Test legal/Abacus integration."""

    def test_abacus_client_init(self):
        """AbacusClient should initialize."""
        from agentx.integrations.legal import AbacusClient
        client = AbacusClient()
        assert client is not None


class TestRepoManager:
    """Test repository management."""

    def test_repo_manager_init(self):
        """RepoManager should initialize."""
        from agentx.integrations.repo_manager import RepoManager
        manager = RepoManager(owner="test-org")
        assert manager.owner == "test-org"

    def test_repo_config_model(self):
        """RepoConfig should validate."""
        from agentx.integrations.repo_manager import RepoConfig
        config = RepoConfig(name="test-repo", description="Test")
        assert config.name == "test-repo"
        assert config.private == True
