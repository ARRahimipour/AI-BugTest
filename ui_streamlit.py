import streamlit as st
from pathlib import Path
import joblib
import subprocess
import pandas as pd
from testgen.generate_test import generate_test_code, write_test_file

ROOT = Path(__file__).resolve().parent
MODEL = ROOT / "model" / "bug_severity_model.pkl"
TEST_OUT = ROOT / "tests" / "test_generated_cases.py"
ORDERED = ROOT / "prioritizer" / "ordered_tests.csv"

st.set_page_config(page_title="AI Bug Severity & TestGen", page_icon="🧠", layout="centered")
st.title("AI-BugTest — AI Severity Prediction & Auto Test Generation")

desc = st.text_area("Bug description", "App crashes when input contains emoji", height=140)

c1, c2, c3 = st.columns([1,1,1])
with c1:
    predict_btn = st.button("Predict")
with c2:
    gen_btn = st.button("Generate & Run")
with c3:
    prio_btn = st.button("Prioritize & Run Top-50%")

@st.cache_resource
def load_payload():
    return joblib.load(MODEL)

def run_pytest(target: str | Path, with_cov=False):
    cmd = ["pytest", "-q", str(target)]
    if with_cov:
        cmd = ["pytest", "-q", "--cov=app", "--cov-report=term-missing", str(target)]
    return subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)

if predict_btn or gen_btn:
    try:
        payload = load_payload()
        pipe, classes_ = payload["pipe"], payload["classes_"]
    except Exception as e:
        st.error(f"Model not found. Train it first. {e}")
    else:
        proba = pipe.predict_proba([desc])[0]
        sev = pipe.classes_[proba.argmax()]
        st.success(f"Predicted severity: {sev}")
        st.caption("Class probabilities")
        st.dataframe(pd.DataFrame([proba], columns=classes_).T.rename(columns={0: "prob"}))

        code = generate_test_code(desc, sev)
        st.subheader("Generated test code")
        st.code(code, language="python")

        if gen_btn:
            write_test_file(code, TEST_OUT)
            with st.spinner("Running pytest with coverage..."):
                res = run_pytest(TEST_OUT, with_cov=True)
            st.subheader("Pytest Output")
            st.code(res.stdout or res.stderr or "No output", language="bash")
            if res.returncode == 0:
                st.success("All tests passed.")
            else:
                st.error("Some tests failed.")

if prio_btn:
    with st.spinner("Prioritizing tests (risk + speed)…"):
        res = subprocess.run(["python", "-m", "prioritizer.prioritize"], cwd=ROOT, capture_output=True, text=True)
    st.subheader("Prioritizer Log")
    st.code(res.stdout or res.stderr, language="bash")

    if ORDERED.exists():
        df = pd.read_csv(ORDERED)
        st.subheader("Ordered Tests")
        st.dataframe(df)

        k = max(1, len(df)//2)
        top = df.head(k)["test_name"].tolist()
        with st.spinner(f"Running Top-{k} tests…"):
            res2 = subprocess.run(["pytest", "-q", *top], cwd=ROOT, capture_output=True, text=True)
        st.subheader("Pytest Output (Top-50%)")
        st.code(res2.stdout or res2.stderr, language="bash")
        if res2.returncode == 0:
            st.success("Done.")
        else:
            st.error("Some tests failed.")
