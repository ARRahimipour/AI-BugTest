# Auto-generated test file
from app import sample_app as app

def test_crash_case():
    try:
        app.run_test_case("crash_input")
    except Exception:
        assert True
    else:
        assert False, "Expected crash not triggered"
