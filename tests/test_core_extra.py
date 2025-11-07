"""
Extended coverage tests (AI-BugTest)
Ensures all main modules run at least once.
"""

from model import train_model_advanced
from traceability import build_rtm
from prioritizer import apfd, run_and_log
from testgen import generate_test
import pytest, os

def test_train_model_executes(monkeypatch):
    """Run training pipeline end-to-end."""
    monkeypatch.setattr("pandas.read_csv", lambda _: 
        __import__("pandas").DataFrame({
            "description": ["sample bug", "input crash", "ui freeze"],
            "severity": ["Critical", "Major", "Minor"],
        })
    )
    train_model_advanced.main()
    assert (train_model_advanced.OUT).exists()

def test_build_rtm_runs(tmp_path):
    """Generate RTM file."""
    build_rtm.RTM_FILE = tmp_path / "rtm.csv"
    build_rtm.build_rtm()
    assert build_rtm.RTM_FILE.exists()

def test_prioritizer_scripts_run():
    """Run prioritizer components end-to-end."""
    run_and_log.main()
    assert os.path.exists("prioritizer/results.csv")
    apfd.main()

def test_generate_test_code():
    """Generate and validate test code."""
    generate_test.generate_test_code("App fails on invalid input", "critical")
    assert os.path.exists("tests/test_generated_cases.py")
