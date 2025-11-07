from pathlib import Path
import joblib

MODEL_PATH = Path(__file__).resolve().parent / "bug_severity_model.pkl"

def predict_severity(description: str) -> str:
    """
    Load the trained ML model and predict the bug severity.
    """
    if not MODEL_PATH.exists():
        raise FileNotFoundError(f"Model not found at {MODEL_PATH}")

    data = joblib.load(MODEL_PATH)

    # Backward compatibility: handle both old and new formats
    if isinstance(data, dict) and "pipe" in data:
        model = data["pipe"]
    else:
        model = data

    pred = model.predict([description])[0]
    return str(pred)


if __name__ == "__main__":
    # Quick manual test
    print(predict_severity("App crashes when input contains emoji"))
