import streamlit as st
import subprocess
from pathlib import Path
from model import bug_predictor
from testgen import generate_test
from prioritizer import run_and_log, apfd
from traceability import build_rtm

st.set_page_config(page_title="AI-BugTest Dashboard", layout="wide")

st.title("🤖 AI-BugTest System")

ROOT = Path(__file__).resolve().parents[0]
MODEL = ROOT / "model" / "bug_severity_model.pkl"

description = st.text_area("🧩 Bug Description:", placeholder="Describe the bug here...")
col1, col2 = st.columns(2)

if col1.button("🧠 Predict Severity"):
    if not description.strip():
        st.warning("⚠️ Please enter a bug description.")
    else:
        try:
            severity = bug_predictor.predict_severity(description)
            st.success(f"Predicted Severity: **{severity}**")
        except Exception as e:
            st.error(f"Model error: {e}")

if col2.button("🧪 Generate Test Case"):
    if not description.strip():
        st.warning("⚠️ Please enter a description first.")
    else:
        try:
            generate_test.generate_test_code(description, "critical")
            st.success("✅ Test case generated successfully!")
            st.code(open("tests/test_generated_cases.py").read(), language="python")
        except Exception as e:
            st.error(f"Error generating test: {e}")

st.divider()
st.header("🔍 Automated Validation & Reporting")

col3, col4, col5 = st.columns(3)

# Pytest + Coverage
if col3.button("▶️ Run Quality Gate"):
    with st.spinner("Running tests and coverage..."):
        res = subprocess.run(
            ["python3", "scripts/quality_gate.py"],
            capture_output=True, text=True
        )
        st.text(res.stdout)
        if "✅" in res.stdout:
            st.success("Quality Gate Passed ✅")
        else:
            st.error("Quality Gate Failed ❌")

# Prioritizer
if col4.button("📊 Run Prioritization"):
    with st.spinner("Prioritizing test cases..."):
        run_and_log.main()
        apfd.main()
        st.success("✅ Prioritization complete")
        st.dataframe(
            open("prioritizer/results.csv").read().splitlines(),
            use_container_width=True
        )

# RTM
if col5.button("🧾 Build RTM Matrix"):
    with st.spinner("Building RTM..."):
        build_rtm.build_rtm()
        st.success("✅ RTM built successfully")
        rtm_file = Path("traceability/rtm.csv")
        if rtm_file.exists():
            st.download_button(
                "📥 Download RTM CSV",
                data=rtm_file.read_text(),
                file_name="rtm.csv",
                mime="text/csv"
            )

st.divider()
st.caption("© 2025 | AI-BugTest (ISTQB-aligned Intelligent Testing Platform)")
