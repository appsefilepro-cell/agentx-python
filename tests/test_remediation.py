"""Tests for remediation engine."""
import pytest


class TestRemediationEngine:
    """Test the remediation engine."""

    def test_engine_init(self):
        """Engine should initialize with project root."""
        from agentx.remediation.engine import RemediationEngine
        engine = RemediationEngine()
        assert engine is not None

    def test_scan_python_syntax(self):
        """Should detect Python syntax errors."""
        from agentx.remediation.engine import RemediationEngine
        engine = RemediationEngine()
        # Scan current project (should have no syntax errors)
        errors = engine.scan_python_syntax()
        assert isinstance(errors, list)

    def test_error_categories(self):
        """Error categories should be defined."""
        from agentx.remediation.engine import ErrorCategory
        assert ErrorCategory.SYNTAX == "syntax"
        assert ErrorCategory.IMPORT == "import"
        assert ErrorCategory.SECURITY == "security"

    def test_error_severity(self):
        """Error severities should be defined."""
        from agentx.remediation.engine import ErrorSeverity
        assert ErrorSeverity.CRITICAL == "critical"
        assert ErrorSeverity.HIGH == "high"


class TestTestFramework:
    """Test the test framework module."""

    def test_runner_init(self):
        """TestRunner should initialize."""
        from agentx.remediation.test_framework import TestRunner
        runner = TestRunner()
        assert runner is not None

    def test_test_levels(self):
        """Test levels should be defined."""
        from agentx.remediation.test_framework import TestLevel
        assert TestLevel.UNIT == "unit"
        assert TestLevel.INTEGRATION == "integration"
        assert TestLevel.E2E == "e2e"
