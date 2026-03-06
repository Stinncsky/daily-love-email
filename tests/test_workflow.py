import yaml
from pathlib import Path


class TestWorkflowYaml:
    def test_daily_email_workflow_valid_yaml(self):
        workflow_path = Path(".github/workflows/daily-email.yml")
        assert workflow_path.exists(), "daily-email.yml workflow file should exist"
        content = workflow_path.read_text(encoding="utf-8")
        parsed = yaml.safe_load(content)
        assert parsed is not None
        assert "name" in parsed
        assert True in parsed or "on" in parsed
        assert "jobs" in parsed

    def test_daily_email_workflow_required_sections(self):
        workflow_path = Path(".github/workflows/daily-email.yml")
        content = yaml.safe_load(workflow_path.read_text(encoding="utf-8"))

        assert "name" in content
        assert content["name"] == "Daily Love Email"

        triggers = content.get("on") or content.get(True)
        assert triggers is not None
        assert "schedule" in triggers or "workflow_dispatch" in triggers

        assert "jobs" in content
        jobs = content["jobs"]
        assert "send-email" in jobs

        job = jobs["send-email"]
        assert "runs-on" in job
        assert job["runs-on"] == "ubuntu-latest"

        assert "steps" in job
        steps = job["steps"]
        assert len(steps) >= 1

        step_names = [step.get("name", "") for step in steps]
        assert any("Checkout" in name or "checkout" in name.lower() for name in step_names)

    def test_daily_email_workflow_has_python_setup(self):
        workflow_path = Path(".github/workflows/daily-email.yml")
        content = yaml.safe_load(workflow_path.read_text(encoding="utf-8"))
        steps = content["jobs"]["send-email"]["steps"]

        python_steps = [
            step for step in steps
            if "python" in step.get("uses", "").lower()
            or "python" in step.get("name", "").lower()
        ]
        assert len(python_steps) > 0, "Should have Python setup step"

    def test_daily_email_workflow_has_secrets(self):
        workflow_path = Path(".github/workflows/daily-email.yml")
        content = yaml.safe_load(workflow_path.read_text(encoding="utf-8"))
        steps = content["jobs"]["send-email"]["steps"]

        secret_step = None
        for step in steps:
            if "env" in step:
                env = step["env"]
                if any("secrets." in str(v) for v in env.values()):
                    secret_step = step
                    break

        assert secret_step is not None, "Should have step using GitHub secrets"

    def test_daily_email_workflow_install_dependencies(self):
        workflow_path = Path(".github/workflows/daily-email.yml")
        content = yaml.safe_load(workflow_path.read_text(encoding="utf-8"))
        steps = content["jobs"]["send-email"]["steps"]

        install_step = None
        for step in steps:
            run = step.get("run", "")
            if "pip install" in run or "pip install" in str(step.get("uses", "")):
                install_step = step
                break

        assert install_step is not None, "Should have dependencies installation step"
