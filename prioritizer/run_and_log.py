from pathlib import Path
import subprocess
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
ORDERED = ROOT / "prioritizer" / "ordered_tests.csv"
RESULTS = ROOT / "prioritizer" / "results.csv"

def collect_order():
    if not ORDERED.exists():
        subprocess.run(["python", "-m", "prioritizer.prioritize"], cwd=ROOT, check=True, text=True)
    df = pd.read_csv(ORDERED)
    return df["test_name"].tolist()

def run_one(nodeid: str) -> int:
    r = subprocess.run(["pytest", "-q", nodeid], cwd=ROOT, capture_output=True, text=True)
    return r.returncode

def main():
    order = collect_order()
    rows = []
    for i, nid in enumerate(order, start=1):
        rc = run_one(nid)
        rows.append({"test_name": nid, "failed": 1 if rc != 0 else 0, "order_index": i})

    df = pd.DataFrame(rows)
    RESULTS.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(RESULTS, index=False)
    print(f"✅ wrote {RESULTS}")
    print(df.head())

if __name__ == "__main__":
    main()
