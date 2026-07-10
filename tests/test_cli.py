import subprocess
import sys
from pathlib import Path

from validate_lza.cli import build_schema_url, main

FIXTURES = Path(__file__).parent / "fixtures"


def test_build_schema_url():
    assert build_schema_url("v1.15.5", "global-config") == (
        "https://raw.githubusercontent.com/awslabs/landing-zone-accelerator-on-aws/"
        "v1.15.5/source/packages/@aws-accelerator/config/lib/schemas/global-config.json"
    )


def test_main_passes_through_check_jsonschema_exit_code(tmp_path, monkeypatch):
    captured = {}

    def fake_run(cmd, *args, **kwargs):
        captured["cmd"] = cmd
        return subprocess.CompletedProcess(cmd, returncode=7)

    monkeypatch.setattr("validate_lza.cli.subprocess.run", fake_run)

    config_file = tmp_path / "global-config.yaml"
    config_file.write_text("homeRegion: eu-west-1\n")

    exit_code = main(
        ["--lza-version", "v1.15.5", "--config-type", "global-config", str(config_file)]
    )

    assert exit_code == 7
    assert captured["cmd"][0] == "check-jsonschema"
    assert captured["cmd"][1] == "--schemafile"
    assert "global-config.json" in captured["cmd"][2]
    assert captured["cmd"][3] == str(config_file)


def test_end_to_end_valid_config_passes():
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "validate_lza.cli",
            "--lza-version",
            "v1.15.5",
            "--config-type",
            "global-config",
            str(FIXTURES / "global-config.valid.yaml"),
        ],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stdout + result.stderr


def test_end_to_end_stale_key_fails(tmp_path):
    stale_config = tmp_path / "global-config.yaml"
    valid_content = (FIXTURES / "global-config.valid.yaml").read_text()
    stale_config.write_text(valid_content + "iamRoleSsmParameters: []\n")

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "validate_lza.cli",
            "--lza-version",
            "v1.15.5",
            "--config-type",
            "global-config",
            str(stale_config),
        ],
        capture_output=True,
        text=True,
    )

    assert result.returncode != 0
    assert "iamRoleSsmParameters" in result.stdout + result.stderr
