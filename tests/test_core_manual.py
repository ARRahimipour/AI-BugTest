from app import sample_app as app
import pytest

def test_invalid_input_raises_value_error():
    with pytest.raises(ValueError):
        app.run_test_case("invalid_input")

def test_generic_check_returns_true():
    assert app.generic_check() is True