import sys, subprocess, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# 💡 strict gate thresholds
COVERAGE_MIN = 0.60   # minimum 60% coverage required
PASSRATE_MIN = 1.00   # all tests must pass

def run_pytest_with_coverage():
    cmd = [
        "coverage", "run",
        "--source=app,model,testgen,traceability,prioritizer,app_under_test",
        "-m", "pytest", "-q"
    ]
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=ROOT, text=True)
    return result.returncode

def generate_coverage_report():
    subprocess.run(
        ["coverage", "json", "-o", "coverage.json"],
        cwd=ROOT,
        text=True
    )

def parse_coverage():
    cov_file = ROOT / "coverage.json"
    if not cov_file.exists():
        return 0.0
    data = json.loads(cov_file.read_text(encoding="utf-8"))
    totals = data.get("totals", {})
    return float(totals.get("percent_covered", 0.0)) / 100.0

def main():
    rc = run_pytest_with_coverage()
    generate_coverage_report()

    if rc != 0:
        print("❌ One or more tests failed; build halted by quality gate.")
        sys.exit(1)

    cov = parse_coverage()
    print(f"\nCoverage: {cov:.2%}")

    if cov < COVERAGE_MIN:
        print(f"❌ Coverage below required threshold ({COVERAGE_MIN:.0%}). Build rejected.")
        sys.exit(1)

    print("✅ All tests passed and coverage meets threshold.")
    print("✅ Quality gates passed. Safe to deploy or proceed.\n")
    sys.exit(0)

if __name__ == "__main__":
    main()
