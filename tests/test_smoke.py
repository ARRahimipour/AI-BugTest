from app import sample_app
from model import train_model_advanced
from prioritizer import run_and_log

def test_imports_and_basic_runs():
    assert sample_app is not None
    assert train_model_advanced is not None
    assert run_and_log is not None
