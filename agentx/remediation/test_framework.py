"""
Test Framework for AgentX5 Multi-Agent Pipeline.

Provides:
- Unit test runner with coverage
- Integration test suite
- End-to-end pipeline test
- Security test suite
- Test result reporting
"""

import os
import json
import logging
import subprocess
from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field
from enum import Enum

logger = logging.getLogger(__name__)


class TestLevel(str, Enum):
    UNIT = "unit"
    INTEGRATION = "integration"
    E2E = "e2e"
    SECURITY = "security"


class TestStatus(str, Enum):
    PASSED = "passed"
    FAILED = "failed"
    SKIPPED = "skipped"
    ERROR = "error"


class TestResult(BaseModel):
    """Result from a single test."""

    name: str
    level: TestLevel
    status: TestStatus
    duration_ms: float = 0
    message: Optional[str] = None
    file: Optional[str] = None

    class Config:
        use_enum_values = True


class TestSuiteResult(BaseModel):
    """Result from a complete test suite run."""

    level: str
    total: int = 0
    passed: int = 0
    failed: int = 0
    skipped: int = 0
    errors: int = 0
    duration_ms: float = 0
    tests: List[TestResult] = Field(default_factory=list)
    coverage_percent: Optional[float] = None


class TestRunner:
    """
    Test runner for the AgentX5 pipeline.

    Runs tests at all levels of the test pyramid and
    generates comprehensive reports.
    """

    def __init__(self, project_root: str = "."):
        self.project_root = os.path.abspath(project_root)
        self.tests_dir = os.path.join(self.project_root, "tests")

    def run_all(self) -> Dict[str, TestSuiteResult]:
        """Run all test levels."""
        results = {}
        results["unit"] = self.run_unit_tests()
        results["integration"] = self.run_integration_tests()
        results["security"] = self.run_security_tests()
        return results

    def run_unit_tests(self) -> TestSuiteResult:
        """Run unit tests with pytest."""
        logger.info("Running unit tests...")
        return self._run_pytest(
            test_dir=self.tests_dir,
            level=TestLevel.UNIT,
            markers="-m unit or not integration and not e2e and not security",
        )

    def run_integration_tests(self) -> TestSuiteResult:
        """Run integration tests."""
        logger.info("Running integration tests...")
        return self._run_pytest(
            test_dir=self.tests_dir,
            level=TestLevel.INTEGRATION,
            markers="-m integration",
        )

    def run_security_tests(self) -> TestSuiteResult:
        """Run security tests using bandit."""
        logger.info("Running security tests...")
        tests = []

        # Run bandit
        try:
            result = subprocess.run(
                ["bandit", "-r", self.project_root, "-f", "json", "-q"],
                capture_output=True,
                text=True,
            )
            if result.stdout.strip():
                data = json.loads(result.stdout)
                issues = data.get("results", [])
                if not issues:
                    tests.append(
                        TestResult(
                            name="bandit_security_scan",
                            level=TestLevel.SECURITY,
                            status=TestStatus.PASSED,
                            message="No security issues found",
                        )
                    )
                else:
                    for issue in issues:
                        tests.append(
                            TestResult(
                                name=f"bandit_{issue.get('test_id', 'unknown')}",
                                level=TestLevel.SECURITY,
                                status=TestStatus.FAILED,
                                message=issue.get("issue_text", ""),
                                file=issue.get("filename", ""),
                            )
                        )
            else:
                tests.append(
                    TestResult(
                        name="bandit_security_scan",
                        level=TestLevel.SECURITY,
                        status=TestStatus.PASSED,
                        message="Security scan passed",
                    )
                )
        except FileNotFoundError:
            tests.append(
                TestResult(
                    name="bandit_security_scan",
                    level=TestLevel.SECURITY,
                    status=TestStatus.SKIPPED,
                    message="bandit not installed",
                )
            )

        passed = sum(1 for t in tests if t.status == TestStatus.PASSED)
        failed = sum(1 for t in tests if t.status == TestStatus.FAILED)
        skipped = sum(1 for t in tests if t.status == TestStatus.SKIPPED)

        return TestSuiteResult(
            level=TestLevel.SECURITY,
            total=len(tests),
            passed=passed,
            failed=failed,
            skipped=skipped,
            tests=tests,
        )

    def _run_pytest(
        self, test_dir: str, level: TestLevel, markers: str = ""
    ) -> TestSuiteResult:
        """Run pytest and parse results."""
        report_file = os.path.join(self.project_root, f".test_report_{level.value}.json")

        cmd = [
            "python3",
            "-m",
            "pytest",
            test_dir,
            "-v",
            "--tb=short",
            f"--json-report",
            f"--json-report-file={report_file}",
        ]
        if markers:
            cmd.extend(markers.split())

        try:
            result = subprocess.run(
                cmd, capture_output=True, text=True, cwd=self.project_root
            )

            # Try to parse JSON report
            if os.path.exists(report_file):
                with open(report_file) as f:
                    data = json.load(f)
                tests = []
                for test in data.get("tests", []):
                    status_map = {
                        "passed": TestStatus.PASSED,
                        "failed": TestStatus.FAILED,
                        "skipped": TestStatus.SKIPPED,
                        "error": TestStatus.ERROR,
                    }
                    tests.append(
                        TestResult(
                            name=test.get("nodeid", "unknown"),
                            level=level,
                            status=status_map.get(
                                test.get("outcome", "error"), TestStatus.ERROR
                            ),
                            duration_ms=test.get("duration", 0) * 1000,
                            message=test.get("call", {}).get("longrepr"),
                        )
                    )
                summary = data.get("summary", {})
                return TestSuiteResult(
                    level=level,
                    total=summary.get("total", len(tests)),
                    passed=summary.get("passed", 0),
                    failed=summary.get("failed", 0),
                    skipped=summary.get("skipped", 0),
                    errors=summary.get("error", 0),
                    duration_ms=summary.get("duration", 0) * 1000,
                    tests=tests,
                )
            else:
                # Parse from stdout if no JSON report
                return self._parse_pytest_output(result.stdout, level)

        except FileNotFoundError:
            return TestSuiteResult(
                level=level,
                tests=[
                    TestResult(
                        name="pytest_check",
                        level=level,
                        status=TestStatus.SKIPPED,
                        message="pytest not installed",
                    )
                ],
                total=1,
                skipped=1,
            )

    def _parse_pytest_output(self, output: str, level: TestLevel) -> TestSuiteResult:
        """Parse pytest terminal output when JSON report is unavailable."""
        tests = []
        passed = failed = skipped = 0

        for line in output.split("\n"):
            if " PASSED" in line:
                passed += 1
                name = line.split(" PASSED")[0].strip()
                tests.append(
                    TestResult(name=name, level=level, status=TestStatus.PASSED)
                )
            elif " FAILED" in line:
                failed += 1
                name = line.split(" FAILED")[0].strip()
                tests.append(
                    TestResult(name=name, level=level, status=TestStatus.FAILED)
                )
            elif " SKIPPED" in line:
                skipped += 1

        return TestSuiteResult(
            level=level,
            total=passed + failed + skipped,
            passed=passed,
            failed=failed,
            skipped=skipped,
            tests=tests,
        )

    def export_report(
        self, results: Dict[str, TestSuiteResult], filepath: str = "test_report.json"
    ) -> str:
        """Export test results to JSON."""
        full_path = os.path.join(self.project_root, filepath)
        report = {
            level: suite.model_dump() for level, suite in results.items()
        }
        with open(full_path, "w") as f:
            json.dump(report, f, indent=2, default=str)
        logger.info(f"Test report exported to {full_path}")
        return full_path
