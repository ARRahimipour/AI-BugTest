import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report
import joblib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "bugs.csv"
OUT = ROOT / "model" / "bug_severity_model.pkl"

def main():
    df = pd.read_csv(DATA)
    X = df["description"].astype(str)
    y = df["severity"].astype(str)

    pipe = Pipeline([
        ("tfidf", TfidfVectorizer(ngram_range=(1,2), min_df=1)),
        ("clf", MultinomialNB())
    ])

    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)
    pipe.fit(Xtr, ytr)
    preds = pipe.predict(Xte)
    print("=== Evaluation ===")
    print(classification_report(yte, preds))

    OUT.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipe, OUT)
    print(f"✅ Model saved to {OUT}")

if __name__ == "__main__":
    main()
