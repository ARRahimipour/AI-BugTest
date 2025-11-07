from pathlib import Path
import subprocess, time
import joblib
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
MODEL = ROOT / "model" / "bug_severity_model.pkl"
ORDERED = ROOT / "prioritizer" / "ordered_tests.csv"

IMPACT = {"Critical": 1.0, "Major": 0.6, "Minor": 0.3}

def collect_nodeids() -> list[str]:
    r = subprocess.run(["pytest", "--collect-only", "-q"], cwd=ROOT, capture_output=True, text=True)
    r.check_returncode()
    return [ln.strip() for ln in r.stdout.splitlines() if "::" in ln]

def time_single_test(nodeid: str) -> float:
    t0 = time.perf_counter()
    subprocess.run(["pytest", "-q", nodeid], cwd=ROOT, capture_output=True, text=True)
    return time.perf_counter() - t0

def predict_probs(desc: str) -> dict[str, float]:
    payload = joblib.load(MODEL)
    pipe, classes_ = payload["pipe"], payload["classes_"]
    proba = pipe.predict_proba([desc])[0]
    return {c: float(p) for c, p in zip(classes_, proba)}

def main():
    # برای نمونه، توضیح باگ اخیر را اینجا بده؛ در UI می‌توانیم از ورودی بگیریم
    bug_desc = "App crashes when input contains emoji"
    likelihood = predict_probs(bug_desc)
    risk = sum(IMPACT.get(sev, 0) * likelihood.get(sev, 0) for sev in IMPACT)

    nodeids = collect_nodeids()
    rows = []
    for nid in nodeids:
        rt = time_single_test(nid)
        rows.append({"test_name": nid, "runtime_sec": rt})

    df = pd.DataFrame(rows)
    df["risk_score"] = risk
    df["speed_score"] = 1.0 / df["runtime_sec"].clip(lower=1e-3)
    alpha, beta = 0.7, 0.3
    df["priority"] = alpha * df["risk_score"] + beta * df["speed_score"]

    ORDERED.parent.mkdir(parents=True, exist_ok=True)
    df.sort_values("priority", ascending=False).to_csv(ORDERED, index=False)
    print(f"✅ wrote {ORDERED}")
    print(df.sort_values("priority", ascending=False).head())

if __name__ == "__main__":
    main()
