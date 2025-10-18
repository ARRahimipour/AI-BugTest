from pathlib import Path
import re
from textwrap import dedent

HEADER = """# Auto-generated test file (ISTQB-aligned)
import pytest
from app import sample_app as app
"""

def wrap_with_metadata(body: str, severity: str, ttype: str, req: str):
    meta = dedent(f'''
    @pytest.mark.severity("{severity.lower()}")
    @pytest.mark.type("{ttype.lower()}")
    @pytest.mark.req("{req}")
    ''')
    return meta + body

def gen_crash_test():
    return dedent("""
    def test_crash_case():
        """ "REQ-001: app shall handle invalid inputs / crash proof" """
        try:
            app.run_test_case("crash_input")
        except Exception:
            assert True
        else:
            assert False, "Expected crash not triggered"
    """)

def gen_ui_test():
    return dedent("""
    def test_ui_alignment():
        """ "REQ-003: UI layout remains aligned on settings page" """
        assert app.check_ui_alignment() is True
    """)

def gen_perf_test():
    return dedent("""
    def test_performance_under_load():
        """ "REQ-005: acceptable latency under synthetic load" """
        import time
        start = time.perf_counter()
        for _ in range(10000):
            app.generic_check()
        assert (time.perf_counter() - start) < 0.5, "Too slow under synthetic load"
    """)

def gen_validation_test():
    return dedent("""
    def test_input_validation_boundaries():
        """ "REQ-001: input validation for empty/emoji/large" """
        try:
            app.run_test_case("invalid_input")
        except Exception:
            assert True
        else:
            assert False, "Expected validation error not triggered"
    """)

def gen_api_test(url: str, method: str = "GET"):
    return dedent(f"""
    def test_api_endpoint_reachable():
        \"\"\" REQ-002: API endpoint shall not return 5xx \"\"\"
        import requests
        resp = requests.request("{method.upper()}", "{url}", timeout=10)
        assert resp.status_code < 500, f"Server error: {{resp.status_code}}"
    """)

def generate_test_code(description: str, severity: str) -> str:
    desc = (description or "").lower()
    sev = (severity or "").lower()
    req = "REQ-004"

    api_url = None
    m = re.search(r'(https?://\\S+|/api/\\S+)', desc)
    if m:
        api_url = m.group(1)
        if api_url.startswith("/"):
            api_url = f"http://localhost:8000{api_url}"

    if any(k in desc for k in ["crash", "exception", "error 500", "fatal"]) or sev == "critical":
        body = gen_crash_test(); ttype = "crash"; req = "REQ-001"
    elif api_url:
        body = gen_api_test(api_url); ttype = "api"; req = "REQ-002"
    elif any(k in desc for k in ["slow", "latency", "timeout", "performance"]) or sev == "major":
        body = gen_perf_test(); ttype = "performance"; req = "REQ-005"
    elif any(k in desc for k in ["ui", "align", "overlap", "typo", "cosmetic"]) or sev == "minor":
        body = gen_ui_test(); ttype = "ui"; req = "REQ-003"
    elif any(k in desc for k in ["empty", "invalid", "emoji", "large", "boundary"]):
        body = gen_validation_test(); ttype = "validation"; req = "REQ-001"
    else:
        body = dedent("""
        def test_generic_behavior():
            \"\"\" REQ-004: generic behavior shall hold \"\"\"
            assert app.generic_check() is True
        """); ttype = "generic"; req = "REQ-004"

    test_code = HEADER + wrap_with_metadata(body, severity=sev, ttype=ttype, req=req)
    return test_code

def write_test_file(code: str, out_path: Path):
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(code, encoding="utf-8")
