import sys, subprocess, json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

COVERAGE_MIN = 0.60
PASSRATE_MIN = 1.00

def run_pytest_cov():
    cmd = ["pytest", "--cov=app", "--cov-report=json:coverage.json", "-q"]
    r = subprocess.run(cmd, cwd=ROOT, text=True)
    return r.returncode

def parse_coverage():
    cov_file = ROOT / "coverage.json"
    if not cov_file.exists():
        return 0.0
    data = json.loads(cov_file.read_text(encoding="utf-8"))
    totals = data.get("totals", {})
    return float(totals.get("percent_covered", 0.0)) / 100.0

def main():
    rc = run_pytest_cov()
    if rc != 0 and PASSRATE_MIN >= 1.0:
        print("❌ Tests failed; quality gate not met.")
        sys.exit(1)

    cov = parse_coverage()
    print(f"Coverage: {cov:.2%}")
    if cov < COVERAGE_MIN:
        print(f"❌ Coverage below threshold ({COVERAGE_MIN:.0%}).")
        sys.exit(1)

    print("Quality gates passed.")
    sys.exit(0)

if __name__ == "__main__":
    main()
