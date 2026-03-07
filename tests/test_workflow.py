from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest
import yaml


WORKFLOW_PATH = Path(".github/workflows/daily-email.yml")
EXPECTED_SECRET_KEYS = {
    "EMAIL_SENDER",
    "EMAIL_PASSWORD",
    "EMAIL_RECIPIENT",
    "SENDER_NAME",
    "RECIPIENT_NAME",
    "WEATHER_API_KEY",
    "LOVE_START_DATE",
    "CITY",
    "ANNIVERSARIES",
    "CARD_BACKGROUND_TYPE",
    "CARD_BACKGROUND_VALUE",
    "ICON_URL",
}


def _load_workflow():
    assert WORKFLOW_PATH.exists(), "daily-email.yml workflow file should exist"
    parsed = yaml.safe_load(WORKFLOW_PATH.read_text(encoding="utf-8"))
    assert parsed is not None
    return parsed


def _get_triggers(content):
    # PyYAML may parse top-level "on" as boolean True in YAML 1.1 mode.
    return content.get("on") or content.get(True) or {}


def _find_send_step(content):
    steps = content["jobs"]["send-email"]["steps"]
    for step in steps:
        if step.get("run", "").strip() == "python src/main.py":
            return step
    raise AssertionError("Send love email step not found")


def _parse_basic_cron(expr):
    """
    Minimal parser for 5-field cron of the form:
    minute hour day month weekday
    where this workflow expects fixed minute/hour and wildcard day/month/weekday.
    """
    if not isinstance(expr, str) or not expr.strip():
        raise ValueError("Cron expression must be a non-empty string")

    parts = expr.split()
    if len(parts) != 5:
        raise ValueError("Cron expression must contain exactly 5 fields")

    minute, hour, day, month, weekday = parts
    if day != "*" or month != "*" or weekday != "*":
        raise ValueError("Day/month/weekday must be '*' for this workflow")

    if not minute.isdigit() or not hour.isdigit():
        raise ValueError("Minute and hour must be numeric")

    minute_value = int(minute)
    hour_value = int(hour)

    if not (0 <= minute_value <= 59):
        raise ValueError("Minute out of range")
    if not (0 <= hour_value <= 23):
        raise ValueError("Hour out of range")

    return minute_value, hour_value


class TestWorkflowYaml:
    def test_daily_email_workflow_valid_yaml(self):
        parsed = _load_workflow()
        assert "name" in parsed
        assert True in parsed or "on" in parsed
        assert "jobs" in parsed

    def test_daily_email_workflow_required_sections(self):
        content = _load_workflow()

        assert content["name"] == "Daily Love Email"

        triggers = _get_triggers(content)
        assert "schedule" in triggers or "workflow_dispatch" in triggers

        jobs = content["jobs"]
        assert "send-email" in jobs

        job = jobs["send-email"]
        assert job["runs-on"] == "ubuntu-latest"

        steps = job["steps"]
        assert len(steps) >= 1

        step_names = [step.get("name", "") for step in steps]
        assert any("Checkout" in name or "checkout" in name.lower() for name in step_names)

    def test_daily_email_workflow_has_python_setup(self):
        content = _load_workflow()
        steps = content["jobs"]["send-email"]["steps"]

        python_steps = [
            step
            for step in steps
            if "python" in step.get("uses", "").lower()
            or "python" in step.get("name", "").lower()
        ]
        assert len(python_steps) > 0, "Should have Python setup step"

    def test_daily_email_workflow_has_secrets(self):
        content = _load_workflow()
        env = _find_send_step(content).get("env", {})
        assert any("secrets." in str(v) for v in env.values()), "Should use GitHub secrets"

    def test_daily_email_workflow_install_dependencies(self):
        content = _load_workflow()
        steps = content["jobs"]["send-email"]["steps"]

        install_step = None
        for step in steps:
            run = step.get("run", "")
            if "pip install" in run or "pip install" in str(step.get("uses", "")):
                install_step = step
                break

        assert install_step is not None, "Should have dependencies installation step"

    def test_cron_expression_is_valid_and_expected(self):
        content = _load_workflow()
        schedule = _get_triggers(content)["schedule"]

        assert isinstance(schedule, list) and len(schedule) == 1
        cron_expr = schedule[0]["cron"]

        minute, hour = _parse_basic_cron(cron_expr)
        assert cron_expr == "0 8 * * *"
        assert minute == 0
        assert hour == 8

    @pytest.mark.parametrize(
        "expr",
        [
            "",
            "0 8 * *",
            "0 8 * * * *",
            "-1 8 * * *",
            "60 8 * * *",
            "0 -1 * * *",
            "0 24 * * *",
            "x 8 * * *",
            "0 y * * *",
            "0 8 1 * *",
        ],
    )
    def test_cron_expression_parser_invalid_inputs(self, expr):
        with pytest.raises(ValueError):
            _parse_basic_cron(expr)

    @pytest.mark.parametrize(
        "expr, expected",
        [
            ("0 0 * * *", (0, 0)),
            ("59 23 * * *", (59, 23)),
        ],
    )
    def test_cron_expression_parser_boundary_values(self, expr, expected):
        assert _parse_basic_cron(expr) == expected

    def test_schedule_time_conversion_utc_to_beijing(self):
        content = _load_workflow()
        cron_expr = _get_triggers(content)["schedule"][0]["cron"]
        minute, hour = _parse_basic_cron(cron_expr)

        utc_time = datetime(2026, 1, 1, hour, minute, tzinfo=timezone.utc)
        beijing_time = utc_time.astimezone(timezone(timedelta(hours=8)))

        assert beijing_time.hour == 16
        assert beijing_time.minute == 0

    def test_workflow_dispatch_dry_run_input_configuration(self):
        content = _load_workflow()
        dispatch = _get_triggers(content)["workflow_dispatch"]

        assert "inputs" in dispatch
        assert "dry_run" in dispatch["inputs"]

        dry_run = dispatch["inputs"]["dry_run"]
        assert dry_run["required"] is False
        assert dry_run["default"] == "false"
        assert dry_run["type"] == "choice"
        assert dry_run["options"] == ["false", "true"]

    def test_secrets_references_are_complete(self):
        content = _load_workflow()
        env = _find_send_step(content)["env"]

        actual_secret_keys = {k for k, v in env.items() if "secrets." in str(v)}
        assert actual_secret_keys == EXPECTED_SECRET_KEYS

        for key in EXPECTED_SECRET_KEYS:
            assert env[key] == f"${{{{ secrets.{key} }}}}", f"Secret {key} should use correct syntax"

    def test_environment_variables_passed_to_send_step(self):
        content = _load_workflow()
        env = _find_send_step(content)["env"]

        assert env["DRY_RUN"] == "${{ github.event.inputs.dry_run }}"
        assert env["GITHUB_REPO_URL"] == "${{ github.server_url }}/${{ github.repository }}"
        assert env["GITHUB_BRANCH"] == "${{ github.ref_name }}"
        assert env["USE_IMAGE_URL"] == "true"

    def test_dry_run_has_safe_default_for_manual_trigger(self):
        content = _load_workflow()
        dry_run = _get_triggers(content)["workflow_dispatch"]["inputs"]["dry_run"]
        assert dry_run["default"] == "false"
        assert "false" in dry_run["options"]
