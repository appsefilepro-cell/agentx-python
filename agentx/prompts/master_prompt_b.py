"""
MASTER EXECUTION PROMPT - PART B
For Genetic Autonomous AI Agents, Manus, Genspark AgentX5, and All Connected Systems.

Target: Apps Holdings WY Inc - Complete System Deployment & Automation
Execution Mode: Fully Autonomous with Zero Manual Intervention
Data Mode: LOW DATA / MINIMUM USAGE

This prompt governs Phase 2: Deployment, Automation, Testing, and Continuous Operations.
"""

from datetime import datetime


MASTER_PROMPT_B = """
# MASTER EXECUTION PROMPT - PART B: DEPLOYMENT, AUTOMATION & CONTINUOUS OPERATIONS

## DIRECTIVE
Continue from Part A. All systems initialized. All agents active. All errors remediated.
Now execute full deployment, configure automation workflows, and establish continuous
operation protocols. The system must be self-sustaining with minimal manual intervention.

## EXECUTION CONTEXT
- **Corporation:** Apps Holdings WY Inc
- **Date:** {date}
- **Phase:** Deployment & Automation (Part B)
- **Prerequisite:** Part A completed successfully
- **Target State:** Fully deployed, automated, self-healing

---

## PHASE 5: FULL DEPLOYMENT PIPELINE

### 5.1 Pre-Deployment Checklist
Before any deployment:
- [ ] All tests passing (unit, integration, e2e)
- [ ] No critical or high severity security findings
- [ ] All merge conflicts resolved
- [ ] All dependencies up to date and pinned
- [ ] Version bumped appropriately (semver)
- [ ] Changelog updated
- [ ] Documentation current

### 5.2 Staging Deployment
```
Deploy to staging:
  1. Build package: python -m build
  2. Run full test suite: pytest tests/ -v
  3. Security scan: bandit -r agentx/ -f json
  4. Type check: mypy agentx/ --ignore-missing-imports
  5. Lint: ruff check agentx/
  6. Deploy to staging environment
  7. Run smoke tests against staging
  8. Verify all integrations functional
```

### 5.3 Production Deployment
```
Deploy to production (only after staging passes):
  1. Create release branch: release/vX.Y.Z
  2. Final review: Claude Code reviews all changes
  3. Merge to main
  4. CI/CD auto-publishes to PyPI
  5. GitHub Release created automatically
  6. Notify all connected systems
  7. Post-deployment health check
```

### 5.4 Copilot CLI Deployment Integration
```bash
# GitHub Copilot CLI commands for deployment verification
gh copilot suggest "deploy agentx-python to PyPI"
gh copilot explain "the CI/CD workflow in .github/workflows/release.yml"
gh copilot suggest "verify the latest PyPI package version"
```

---

## PHASE 6: AUTOMATION WORKFLOWS

### 6.1 Priority Automation (Highest Manual Task Reduction)
These are the tasks that require the most manual effort, automated first:

**1. Error Detection & Auto-Fix (saves ~10 hrs/week)**
```yaml
Trigger: On push to any branch
Actions:
  - Run linter (ruff)
  - Run type checker (mypy)
  - If errors found:
    - Create fix branch
    - Apply automated fixes
    - Create PR with fix description
    - Auto-merge if tests pass
```

**2. Dependency Updates (saves ~5 hrs/week)**
```yaml
Trigger: Weekly schedule (Monday 6 AM UTC)
Actions:
  - Check for outdated dependencies
  - Create update branch
  - Update requirements.txt and setup.py
  - Run tests
  - Create PR if tests pass
```

**3. Repository Sync (saves ~3 hrs/week)**
```yaml
Trigger: On push to main, or daily schedule
Actions:
  - Sync all local repos to GitHub
  - Verify corporate ownership
  - Update topics and descriptions
  - Run health checks
  - Report any issues
```

**4. Legal Document Generation (saves ~8 hrs/week)**
```yaml
Trigger: On request, or scheduled
Actions:
  - Generate compliance reports
  - Update forensic omnibus
  - Sync to corporate data vault
  - Export to Dropbox/Box
```

**5. PR/MR Management (saves ~4 hrs/week)**
```yaml
Trigger: Daily schedule
Actions:
  - Review all open PRs
  - Auto-merge passing PRs older than 24 hours
  - Close stale PRs (no activity > 14 days)
  - Delete merged branches
  - Send summary report
```

### 6.2 Zapier Workflow Integrations
```
Zap 1: GitHub PR -> Slack/Email Notification
Zap 2: New legal document -> Dropbox upload
Zap 3: CI/CD failure -> Alert + Auto-remediation trigger
Zap 4: New repository -> Auto-configure settings + branch protection
Zap 5: Weekly -> Generate system health report
```

### 6.3 Proactive Agent Behavior
The AgentX5 super agent must think ahead:
- Predict potential failures before they occur
- Pre-emptively update dependencies before vulnerabilities are published
- Monitor API rate limits and adjust usage patterns
- Cache frequently accessed data to reduce API calls
- Schedule resource-intensive tasks during off-peak hours

---

## PHASE 7: TESTING FRAMEWORK

### 7.1 Test Pyramid
```
Level 1 - Unit Tests (fast, many):
  - Test each module independently
  - Mock external APIs
  - Target: 90%+ code coverage

Level 2 - Integration Tests (medium, moderate):
  - Test module interactions
  - Test API connectivity (with test keys)
  - Test pipeline orchestration flow

Level 3 - End-to-End Tests (slow, few):
  - Test full pipeline execution
  - Test deployment flow
  - Test automation workflows
```

### 7.2 Front-End Testing (if applicable)
```
- Component rendering tests
- User interaction tests
- Accessibility compliance
- Cross-browser compatibility
```

### 7.3 Back-End Testing
```
- API endpoint validation
- Authentication and authorization
- Rate limiting and throttling
- Error handling and recovery
- Data integrity and consistency
```

### 7.4 Security Testing
```
- SAST (Static Application Security Testing)
- DAST (Dynamic Application Security Testing)
- Dependency vulnerability scanning
- Secret detection in codebase
- API security audit
```

---

## PHASE 8: MOBILE & TERMINAL ACCESS

### 8.1 iPhone Terminal Integration
For accessing AgentX5 from iPhone via Tmux/iSH apps:
```
- SSH into server running AgentX5
- Tmux session management for persistent connections
- Lightweight CLI interface for mobile access
- Push notifications for task completion
```

### 8.2 Free-Tier Service Configuration
Ensure all services use free-tier plans:
```
GitHub: Free (unlimited public repos, private with limits)
GitLab: Free tier (400 CI/CD minutes/month)
Google Cloud: Free tier ($300 credit + always-free products)
Zapier: Free tier (100 tasks/month, 5 Zaps)
Dropbox: Basic free (2 GB)
Box: Personal free (10 GB)
DeepSeek: Free API tier
Llama: Open source (self-hosted, free)
Grok: Free tier via X platform
Firecrawl: Free tier (500 pages/month)
```

### 8.3 LLM Chat Integration (Free Tier)
```
Free LLMs available:
  - DeepSeek: Open-weight, free API access
  - Llama (Meta): Open source, self-hostable
  - Grok (xAI): Free via X platform
  - Gemini: Free tier via Google AI Studio
  - Mistral: Free tier available
```

---

## PHASE 9: CONTINUOUS OPERATIONS

### 9.1 Self-Healing Protocol
When errors are detected in production:
1. Alert: Log and notify
2. Diagnose: Identify root cause automatically
3. Fix: Apply automated fix if confidence > 90%
4. Test: Validate fix doesn't break other systems
5. Deploy: Push fix through expedited pipeline
6. Report: Document the incident and resolution

### 9.2 Monitoring Dashboard
Track these metrics:
- Pipeline success rate (target: 99%+)
- Average task completion time
- Agent utilization rates
- Error detection and resolution times
- API cost per operation
- Free-tier usage vs. limits

### 9.3 Rollback Protocol
If deployment fails:
1. Automatic rollback to last known good version
2. Alert all connected systems
3. Root cause analysis by Claude Code
4. Fix by OpenAI Codex
5. Re-deploy through full pipeline

---

## PHASE 10: FINAL VERIFICATION

### 10.1 Completion Criteria
The system is 100% complete when:
- [ ] All 10 agents active and configured
- [ ] All pipelines executing without errors
- [ ] All repositories synced to GitHub under corporate ownership
- [ ] All automation workflows running
- [ ] All free-tier services configured
- [ ] All tests passing
- [ ] All documentation current
- [ ] All security scans clean
- [ ] Mobile access configured
- [ ] Self-healing protocol active

### 10.2 Handoff
Once complete, the system should:
- Run autonomously with minimal intervention
- Auto-fix detected errors
- Auto-update dependencies
- Auto-generate compliance documents
- Auto-sync repositories
- Provide status reports on request

---

## EXECUTION RULES (CONTINUED FROM PART A)
11. DEPLOY to staging first, production second. Never skip staging.
12. AUTOMATE the highest-manual-effort tasks first.
13. USE free-tier services wherever possible.
14. THINK proactively - anticipate needs before they arise.
15. SELF-HEAL when errors are detected in production.
16. REPORT all actions taken for full transparency.
17. NEVER break existing functionality when adding new features.
18. ALWAYS maintain backward compatibility.
19. PARALLELIZE execution within stages for maximum throughput.
20. COMPLETE 100% of all tasks. No exceptions. No partial completions.
"""


def get_prompt_b(**kwargs) -> str:
    """Get Master Prompt B with dynamic values substituted."""
    return MASTER_PROMPT_B.format(
        date=kwargs.get("date", datetime.utcnow().strftime("%B %d, %Y")),
        **{k: v for k, v in kwargs.items() if k != "date"},
    )
