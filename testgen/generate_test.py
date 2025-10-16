from pathlib import Path
import re

TEMPLATE_HEADER = """# Auto-generated test file
from app import sample_app as app
"""

def gen_crash_test():
    return """
def test_crash_case():
    try:
        app.run_test_case("crash_input")
    except Exception:
        assert True
    else:
        assert False, "Expected crash not triggered"
"""

def gen_ui_test():
    return """
def test_ui_alignment():
    assert app.check_ui_alignment() is True
"""

def gen_perf_test():
    return """
def test_performance_under_load():
    import time
    start = time.perf_counter()
    for _ in range(10000):
        app.generic_check()
    assert (time.perf_counter() - start) < 0.5, "Too slow under synthetic load"
"""

def gen_validation_test():
    return """
def test_input_validation_boundaries():
    # مثال: ورودی خالی/بسیار بزرگ/ایموچی
    try:
        app.run_test_case("invalid_input")
    except Exception:
        assert True
    else:
        assert False, "Expected validation error not triggered"
"""

def gen_api_test(url: str, method: str = "GET"):
    return f"""
def test_api_endpoint_reachable():
    import requests
    resp = requests.request("{method.upper()}", "{url}", timeout=10)
    assert resp.status_code < 500, f"Server error: {{resp.status_code}}"
"""

def generate_test_code(description: str, severity: str) -> str:
    desc = (description or "").lower()
    sev = (severity or "").lower()

    # API pattern detection
    api_url = None
    m = re.search(r'(https?://\\S+|/api/\\S+)', desc)
    if m:
        api_url = m.group(1)
        if api_url.startswith("/"):
            api_url = f"http://localhost:8000{api_url}"

    # rule-based routing
    if any(k in desc for k in ["crash", "exception", "error 500", "fatal"]) or sev == "critical":
        body = gen_crash_test()
    elif api_url:
        body = gen_api_test(api_url)
    elif any(k in desc for k in ["slow", "latency", "timeout", "performance"]) or sev == "major":
        body = gen_perf_test()
    elif any(k in desc for k in ["ui", "align", "overlap", "typo", "cosmetic"]) or sev == "minor":
        body = gen_ui_test()
    elif any(k in desc for k in ["empty", "invalid", "emoji", "large", "boundary"]):
        body = gen_validation_test()
    else:
        body = """
def test_generic_behavior():
    assert app.generic_check() is True
"""

    return TEMPLATE_HEADER + body

def write_test_file(code: str, out_path: Path):
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(code, encoding="utf-8")
