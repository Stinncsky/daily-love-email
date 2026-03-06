import json
import os
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from config import _cast_leaf, _override_env, load_config


class TestCastLeaf:
    def test_cast_leaf_bool_true(self):
        assert _cast_leaf(False, "true") is True
        assert _cast_leaf(False, "1") is True
        assert _cast_leaf(False, "yes") is True
        assert _cast_leaf(False, "on") is True

    def test_cast_leaf_bool_false(self):
        assert _cast_leaf(True, "false") is False
        assert _cast_leaf(True, "0") is False
        assert _cast_leaf(True, "no") is False
        assert _cast_leaf(True, "off") is False

    def test_cast_leaf_bool_invalid(self):
        assert _cast_leaf(True, "invalid") is True
        assert _cast_leaf(False, "maybe") is False

    def test_cast_leaf_int_success(self):
        assert _cast_leaf(0, "42") == 42
        assert _cast_leaf(0, "-10") == -10

    def test_cast_leaf_int_failure(self):
        assert _cast_leaf(100, "not_a_number") == 100
        assert _cast_leaf(0, "3.14") == 0

    def test_cast_leaf_float_success(self):
        assert _cast_leaf(0.0, "3.14") == 3.14

    def test_cast_leaf_float_failure(self):
        assert _cast_leaf(1.5, "invalid") == 1.5

    def test_cast_leaf_string(self):
        assert _cast_leaf("default", "new_value") == "new_value"


class TestOverrideEnv:
    def test_override_simple_string(self, monkeypatch):
        monkeypatch.setenv("EMAIL_SENDER", "test@example.com")
        config = {"email": {"sender": "old@example.com"}}
        result = _override_env(config)
        assert result["email"]["sender"] == "test@example.com"

    def test_override_nested_dict(self, monkeypatch):
        monkeypatch.setenv("EMAIL_SENDER", "nested@example.com")
        config = {
            "email": {
                "sender": "original@example.com",
                "password": "secret"
            }
        }
        result = _override_env(config)
        assert result["email"]["sender"] == "nested@example.com"
        assert result["email"]["password"] == "secret"

    def test_anniversaries_json_parse_success(self, monkeypatch):
        anniversaries_json = '[{"name": "Test Day", "date": "12-25"}]'
        monkeypatch.setenv("ANNIVERSARIES", anniversaries_json)
        config = {"anniversaries": [{"name": "Original", "date": "01-01"}]}
        result = _override_env(config)
        assert isinstance(result["anniversaries"], list)
        assert len(result["anniversaries"]) == 1
        assert result["anniversaries"][0]["name"] == "Test Day"
        assert result["anniversaries"][0]["date"] == "12-25"

    def test_anniversaries_json_parse_failure_fallback(self, monkeypatch):
        monkeypatch.setenv("ANNIVERSARIES", "not valid json")
        original_list = [{"name": "Original", "date": "01-01"}]
        config = {"anniversaries": original_list}
        result = _override_env(config)
        assert result["anniversaries"] == original_list

    def test_anniversaries_complex_json(self, monkeypatch):
        anniversaries_json = json.dumps([
            {"name": "First Date", "date": "01-01"},
            {"name": "Wedding", "date": "06-15"},
            {"name": "Anniversary", "date": "12-31"}
        ])
        monkeypatch.setenv("ANNIVERSARIES", anniversaries_json)
        config = {"anniversaries": []}
        result = _override_env(config)
        assert len(result["anniversaries"]) == 3
        assert result["anniversaries"][1]["name"] == "Wedding"

    def test_anniversaries_empty_json_array(self, monkeypatch):
        monkeypatch.setenv("ANNIVERSARIES", "[]")
        config = {"anniversaries": [{"name": "Keep", "date": "01-01"}]}
        result = _override_env(config)
        assert result["anniversaries"] == []

    def test_override_bool_conversion(self, monkeypatch):
        monkeypatch.setenv("DEBUG", "true")
        config = {"debug": False}
        result = _override_env(config)
        assert result["debug"] is True

    def test_override_int_conversion(self, monkeypatch):
        monkeypatch.setenv("SMTP_PORT", "587")
        config = {"smtp_port": 465}
        result = _override_env(config)
        assert result["smtp_port"] == 587

    def test_no_env_no_change(self):
        config = {"email": {"sender": "test@example.com"}}
        result = _override_env(config)
        assert result == config

    def test_dict_json_parse(self, monkeypatch):
        dict_json = '{"key1": "value1", "key2": "value2"}'
        monkeypatch.setenv("SETTINGS", dict_json)
        config = {"settings": {"old": "value"}}
        result = _override_env(config)
        assert result["settings"] == {"old": "value"}

    def test_dict_json_parse_failure_fallback(self, monkeypatch):
        monkeypatch.setenv("SETTINGS", "not json")
        original_dict = {"old": "value"}
        config = {"settings": original_dict}
        result = _override_env(config)
        assert result["settings"] == original_dict


class TestLoadConfig:
    def test_config_file_not_exist(self):
        result = load_config("nonexistent_config.yaml")
        assert result == {}

    def test_empty_config_file(self, tmp_path, monkeypatch):
        config_file = tmp_path / "empty_config.yaml"
        config_file.write_text("")
        result = load_config(str(config_file))
        assert result == {}

    def test_invalid_yaml(self, tmp_path, monkeypatch):
        config_file = tmp_path / "invalid.yaml"
        config_file.write_text("invalid: yaml: content: [")
        result = load_config(str(config_file))
        assert result == {}

    def test_load_with_env_override(self, tmp_path, monkeypatch):
        monkeypatch.setenv("EMAIL_SENDER", "env@example.com")
        config_file = tmp_path / "config.yaml"
        config_file.write_text("email:\n  sender: file@example.com\n  password: secret")
        result = load_config(str(config_file))
        assert result["email"]["sender"] == "env@example.com"
        assert result["email"]["password"] == "secret"

    def test_yaml_not_dict(self, tmp_path, monkeypatch):
        config_file = tmp_path / "list_config.yaml"
        config_file.write_text("- item1\n- item2")
        result = load_config(str(config_file))
        assert result == {}

    def test_anniversaries_from_env(self, tmp_path, monkeypatch):
        anniversaries_json = '[{"name": "Test", "date": "05-20"}]'
        monkeypatch.setenv("ANNIVERSARIES", anniversaries_json)
        config_file = tmp_path / "config.yaml"
        config_file.write_text("anniversaries:\n  - name: Original\n    date: 01-01")
        result = load_config(str(config_file))
        assert len(result["anniversaries"]) == 1
        assert result["anniversaries"][0]["name"] == "Test"
