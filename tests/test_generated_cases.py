# Auto-generated test file (ISTQB-aligned)
import pytest
from app import sample_app as app

@pytest.mark.severity("critical")
@pytest.mark.type("crash")
@pytest.mark.req("REQ-001")

def test_crash_case():
    REQ-001: app shall handle invalid inputs / crash proof
    try:
        app.run_test_case("crash_input")
    except Exception:
        assert True
    else:
        assert False, "Expected crash not triggered"
