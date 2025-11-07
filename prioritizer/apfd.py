from __future__ import annotations
from pathlib import Path
import pandas as pd

"""
انتظار ورودی:
results.csv با ستون‌های:
test_name, failed(0/1), order_index(1..N)
"""

def apfd(results: pd.DataFrame) -> float:
    N = len(results)
    failing = results[results["failed"] == 1]
    if N == 0 or failing.empty:
        return 1.0
    m = len(failing)
    sum_TF = failing["order_index"].sum()
    return 1 - (sum_TF / (N * m)) + (1 / (2 * N))

def main():
    ROOT = Path(__file__).resolve().parents[1]
    csv = ROOT / "prioritizer" / "results.csv"
    if not csv.exists():
        print("No results.csv to compute APFD.")
        return
    df = pd.read_csv(csv)
    score = apfd(df)
    print(f"APFD: {score:.3f}")

if __name__ == "__main__":
    main()
