"""Contract tests for the OFW MCP server tool surface.

These assert the *interface* holds — every tool declared in SPEC.md exists and
behaves per its capability state. The Testing/Debugging agents extend these with
behavioral tests as each capability is implemented.
"""
import importlib


def test_package_imports():
    mod = importlib.import_module("ofw_mcp")
    assert mod.__version__


def test_server_imports_and_registers_tools():
    server = importlib.import_module("ofw_mcp.server")
    assert server.mcp is not None
    # every scaffolded tool is a real callable on the module
    for name in server._SCAFFOLD:
        assert hasattr(server, name), f"missing tool: {name}"
        assert callable(getattr(server, name))


def test_config_loads_with_safe_defaults():
    from ofw_mcp.config import CONFIG
    assert CONFIG.ofw_base_url.startswith("https://")
    # default sync mode must be the safe one
    assert CONFIG.sync_mode in ("dry_run", "live")


def test_calendar_sync_status_handles_missing_state(tmp_path, monkeypatch):
    import importlib
    monkeypatch.setenv("SYNC_STATE_FILE", str(tmp_path / "nope.json"))
    cfg = importlib.reload(importlib.import_module("ofw_mcp.config"))
    server = importlib.reload(importlib.import_module("ofw_mcp.server"))
    assert cfg.CONFIG.sync_state_file.endswith("nope.json")
    out = server.calendar_sync_status()
    assert out["status"] == "no_state"
