from pathlib import Path
import subprocess
import joblib
import pandas as pd
import streamlit as st

# --- Paths
ROOT = Path(__file__).resolve().parent
MODEL_PATH = ROOT / "model" / "bug_severity_model.pkl"
TEST_OUT = ROOT / "tests" / "test_generated_cases.py"
ORDERED = ROOT / "prioritizer" / "ordered_tests.csv"
RTM_FILE = ROOT / "traceability" / "rtm.csv"

# --- Import test generator (we reuse your existing module)
from testgen.generate_test import generate_test_code, write_test_file

st.set_page_config(page_title="AI-BugTest", layout="centered")
st.title("AI-BugTest — ISTQB-aligned Testing Demo")

st.caption(
    "This UI demonstrates: Test Analysis (AI severity), Test Design (auto generation), "
    "Risk-Based Prioritization, Requirements Traceability (RTM), and Quality Gates."
)

# --- Input
desc = st.text_area("Bug description", "App crashes when input contains emoji", height=140)

colA, colB, colC = st.columns(3)
with colA:
    btn_predict = st.button("Predict")
with colB:
    btn_genrun = st.button("Generate & Run")
with colC:
    btn_prio = st.button("Prioritize & Run Top-50%")

colD, colE = st.columns(2)
with colD:
    btn_rtm = st.button("Build RTM")
with colE:
    btn_qgate = st.button("Run Quality Gate")


# --- Helpers
def run_cmd(cmd: list[str]):
    """Run a command in project root and return (rc, out)."""
    res = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    out = (res.stdout or "") + (("\n" + res.stderr) if res.stderr else "")
    return res.returncode, out.strip()


@st.cache_resource
def load_model():
    payload = joblib.load(MODEL_PATH)
    return payload["pipe"], payload["classes_"]


def predict(text: str):
    pipe, classes_ = load_model()
    proba = pipe.predict_proba([text])[0]
    idx = int(proba.argmax())
    label = classes_[idx]
    probs = pd.DataFrame([proba], columns=classes_).T.rename(columns={0: "probability"})
    return label, probs


# --- Actions
if btn_predict or btn_genrun:
    # Safety: ensure model exists
    if not MODEL_PATH.exists():
        st.error("Model not found. Train it first: python model/train_model_advanced.py")
    else:
        try:
            sev, probs_df = predict(desc)
            st.subheader("Prediction")
            st.write(f"Predicted severity: **{sev}**")
            st.dataframe(probs_df.style.format({"probability": "{:.3f}"}))
        except Exception as e:
            st.error(f"Prediction failed: {e}")

        if btn_genrun:
            # Generate test
            try:
                code = generate_test_code(desc, sev)
                write_test_file(code, TEST_OUT)
                st.subheader("Generated test code")
                st.code(code, language="python")
            except Exception as e:
                st.error(f"Test generation failed: {e}")
            else:
                # Run pytest with coverage
                with st.spinner("Running pytest (with coverage)..."):
                    rc, out = run_cmd(["pytest", "-q", "--cov=app", "--cov-report=term-missing", str(TEST_OUT)])
                st.subheader("Pytest output")
                st.code(out or "no output", language="bash")
                if rc == 0:
                    st.success("All tests passed.")
                else:
                    st.error("Some tests failed. See output above.")


if btn_prio:
    with st.spinner("Prioritizing tests (risk + speed) and running top-50%..."):
        rc1, out1 = run_cmd(["python", "-m", "prioritizer.prioritize"])
    st.subheader("Prioritizer log")
    st.code(out1 or "no output", language="bash")

    if ORDERED.exists():
        try:
            df = pd.read_csv(ORDERED)
            st.subheader("Ordered tests")
            st.dataframe(df)
            k = max(1, len(df) // 2)
            nodeids = df.head(k)["test_name"].tolist()
            with st.spinner(f"Running Top-{k} tests..."):
                rc2, out2 = run_cmd(["pytest", "-q", *nodeids])
            st.subheader("Pytest output (Top-50%)")
            st.code(out2 or "no output", language="bash")
            if rc2 == 0:
                st.success("Selected tests passed.")
            else:
                st.error("Some selected tests failed.")
        except Exception as e:
            st.error(f"Could not read or run ordered tests: {e}")
    else:
        st.warning("No ordered_tests.csv found. Run the prioritizer first.")


if btn_rtm:
    with st.spinner("Building RTM (traceability)..."):
        # run traceability builder if exists
        script = ROOT / "traceability" / "build_rtm.py"
        if script.exists():
            rc, out = run_cmd(["python", str(script)])
            st.subheader("RTM build output")
            st.code(out or "no output", language="bash")
        else:
            st.warning("traceability/build_rtm.py not found.")
    # show CSV if exists
    if RTM_FILE.exists():
        try:
            df = pd.read_csv(RTM_FILE)
            st.subheader("RTM (requirements to tests)")
            st.dataframe(df)
        except Exception as e:
            st.error(f"Could not read RTM CSV: {e}")
    else:
        st.info("RTM file not found yet.")


if btn_qgate:
    with st.spinner("Running Quality Gate..."):
        script = ROOT / "scripts" / "quality_gate.py"
        if script.exists():
            rc, out = run_cmd(["python", str(script)])
            st.subheader("Quality Gate output")
            st.code(out or "no output", language="bash")
            if rc == 0:
                st.success("Quality gates passed.")
            else:
                st.error("Quality gates failed.")
        else:
            st.warning("scripts/quality_gate.py not found.")
