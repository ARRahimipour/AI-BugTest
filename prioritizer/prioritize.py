from pathlib import Path
import subprocess, time
import joblib
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
MODEL = ROOT / "model" / "bug_severity_model.pkl"
TESTS_DIR = ROOT / "tests"
OUT = ROOT / "prioritizer" / "ordered_tests.csv"

IMPACT = {"Critical": 1.0, "Major": 0.6, "Minor": 0.3}

def collect_nodeids():
    r = subprocess.run(["pytest", "--collect-only", "-q"], cwd=ROOT, capture_output=True, text=True)
    r.check_returncode()
    return [ln.strip() for ln in r.stdout.splitlines() if "::" in ln]

def time_single_test(nodeid: str) -> float:
    t0 = time.perf_counter()
    subprocess.run(["pytest", "-q", nodeid], cwd=ROOT, capture_output=True, text=True)
    return time.perf_counter() - t0

def predict_probs(descriptions: list[str]) -> pd.DataFrame:
    payload = joblib.load(MODEL)
    pipe, classes_ = payload["pipe"], payload["classes_"]
    proba = pipe.predict_proba(descriptions)
    df = pd.DataFrame(proba, columns=classes_)
    return df

def main():
    gen_file = ROOT / "tests" / "test_generated_cases.py"
    if not gen_file.exists():
        raise SystemExit("No generated test found. Generate one from UI first.")

    bug_desc = "App crashes when input contains emoji"

    # Likelihood per severity
    probs = predict_probs([bug_desc]).iloc[0]
    likelihood = {k: float(v) for k, v in probs.items()}

    # Risk score (ISTQB: Impact × Likelihood)
    risk = sum(IMPACT.get(sev, 0) * likelihood.get(sev, 0) for sev in ["Critical", "Major", "Minor"])

    nodeids = collect_nodeids()
    rows = []
    for nid in nodeids:
        rt = time_single_test(nid)
        rows.append({"test_name": nid, "runtime_sec": rt})

    df = pd.DataFrame(rows)
    df["risk_score"] = risk
    df["speed_score"] = 1.0 / df["runtime_sec"].clip(lower=1e-3)

    # ترکیب: بیشتر وزن به ریسک
    alpha, beta = 0.7, 0.3
    df["priority"] = alpha * df["risk_score"] + beta * df["speed_score"]

    OUT.parent.mkdir(parents=True, exist_ok=True)
    df.sort_values("priority", ascending=False).to_csv(OUT, index=False)
    print(f"✅ wrote {OUT}")
    print(df.sort_values("priority", ascending=False).head())

if __name__ == "__main__":
    main()
