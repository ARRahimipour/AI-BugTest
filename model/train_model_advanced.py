from pathlib import Path
import numpy as np
import pandas as pd
import joblib
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, f1_score, log_loss
from sklearn.model_selection import StratifiedKFold, train_test_split

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "bugs.csv"
OUT  = ROOT / "model" / "bug_severity_model.pkl"

def build_pipe():
    clf = LogisticRegression(
        max_iter=1000,
        class_weight="balanced",
        solver="lbfgs",
        multi_class="auto",
    )
    return Pipeline([
        ("tfidf", TfidfVectorizer(ngram_range=(1, 2), min_df=1)),
        ("clf", clf),
    ])

def main():
    df = pd.read_csv(DATA)
    X = df["description"].astype(str).values
    y = df["severity"].astype(str).values

    pipe = build_pipe()

    vc = pd.Series(y).value_counts()
    min_class = int(vc.min())
    total = len(y)

    y_true, y_pred, y_proba = [], [], []

    if min_class >= 2 and total >= 4:
        n_splits = int(max(2, min(5, min_class)))
        skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=42)
        for tr, te in skf.split(X, y):
            pipe.fit(X[tr], y[tr])
            yp = pipe.predict(X[te])
            y_pred.extend(yp)
            y_true.extend(y[te])
            y_proba.extend(list(pipe.predict_proba(X[te])))
    else:
        Xtr, Xte, ytr, yte = train_test_split(
            X, y, test_size=0.5 if total >= 4 else 0.33, random_state=42,
            stratify=y if min_class >= 2 else None
        )
        pipe.fit(Xtr, ytr)
        y_pred.extend(pipe.predict(Xte))
        y_true.extend(yte)
        y_proba.extend(list(pipe.predict_proba(Xte)))

    print("=== Evaluation ===")
    print(classification_report(y_true, y_pred, zero_division=0))
    try:
        print(f"Macro-F1: {f1_score(y_true, y_pred, average='macro', zero_division=0):.3f} | "
              f"LogLoss: {log_loss(y_true, np.array(y_proba), labels=np.unique(y)):.3f}")
    except Exception:
        pass

    pipe.fit(X, y)
    payload = {"pipe": pipe, "classes_": list(pipe.classes_)}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(payload, OUT)
    print(f"✅ Advanced model saved to {OUT}")

if __name__ == "__main__":
    main()
