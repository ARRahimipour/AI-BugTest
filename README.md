# 🧠 AI-BugTest  
### Intelligent Test Generation and Prioritization System (ISTQB® Aligned)

---

## 🎯 Overview
**AI-BugTest** is a research-driven, intelligent testing framework that combines  
machine learning and ISTQB® principles to **predict defect severity**,  
**generate test cases automatically**, and **prioritize test execution** based on risk.

It is part of an **MSc-level project** for the *Advanced Software Testing* course,  
demonstrating the integration of **AI**, **Risk-Based Testing (RBT)**,  
and **Quality Gates** within a reproducible test pipeline.

---

## 🧩 Key Features

| Category | Description |
|-----------|-------------|
| **AI-Driven Severity Prediction** | Uses NLP (TF-IDF + Logistic Regression) to classify bug descriptions into *Critical, Major, Minor*. |
| **Automated Test Generation** | Dynamically generates pytest test cases (Crash, API, Performance, Validation, UI). |
| **Risk-Based Prioritization** | Orders tests by predicted risk (Impact × Likelihood × Speed). |
| **Requirements Traceability (RTM)** | Automatically maps test cases to requirement IDs (REQ-001 ...). |
| **Quality Gates** | Enforces minimum coverage and zero-failure thresholds before release. |
| **APFD Metric Calculation** | Computes the Average Percentage of Fault Detection for prioritization analysis. |
| **ISTQB® Alignment** | Fully implements concepts from *Advanced Level Test Manager & Analyst*. |

---

## 🏗️ Project Structure
```
AI-BugTest/
│
├── app/                  # Sample app under test
├── model/                # ML training scripts (TF-IDF + LR)
├── testgen/              # Automatic test generator
├── prioritizer/          # Risk prioritization + APFD calculator
├── traceability/         # RTM builder (requirements to tests)
├── scripts/              # Quality gates & CI integration
├── tests/                # All generated & manual test cases
├── requirements.txt
├── README.md
└── .gitignore
```

---

## ⚙️ Installation

```bash
git clone https://github.com/arrahimipour/AI-BugTest.git
cd AI-BugTest
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

---

## 🚀 Usage Workflow

### 1️⃣ Train the Model
```bash
python model\train_model_advanced.py
```

### 2️⃣ Generate and Run Tests
```bash
pytest -q
```

### 3️⃣ Build Requirements Traceability Matrix (RTM)
```bash
python -m traceability.build_rtm
```

### 4️⃣ Check Quality Gates
```bash
python scripts\quality_gate.py
```

### 5️⃣ Run Prioritization and Compute APFD
```bash
python -m prioritizer.run_and_log
python -m prioritizer.apfd
```

---

## 📊 Example Outputs

✅ **Quality Gate Passed**
```
Coverage: 80.00%
✅ Quality gates passed.
```

📈 **APFD Metric**
```
APFD: 1.000
```

📋 **Generated RTM (traceability/rtm.csv)**
| test_name | severity | type | req_id |
|------------|-----------|------|--------|
| tests/test_generated_cases.py::test_crash_case | critical | crash | REQ-001 |
| tests/test_ui_alignment.py::test_ui_alignment | minor | ui | REQ-003 |

---

## 🎓 Academic Context

This project aligns with the **Advanced Software Testing (MSc)** curriculum  
and ISTQB® Advanced Level modules:
- **Test Manager** → Risk-Based Test Strategy, Entry/Exit Criteria  
- **Test Analyst** → Test Design Techniques, Coverage Analysis  
- **Technical Test Analyst** → Automation, Non-functional Testing, APFD

---

## 🧱 Next Steps (Planned)
- REST API via **FastAPI** (`/predict`, `/generate`, `/prioritize`)
- Web Dashboard via **Next.js** for visualization
- Integration with CI/CD (GitHub Actions Quality Gate)
- Paper submission to IEEE/Elsevier on *AI-driven Risk-Based Testing*

---

## 🧑‍💻 Author
**Alireza Rahimipour Anaraki**  
MSc Student, University of Tehran  
📘 Course: *Advanced Software Testing (ISTQB® Aligned)*  
📎 GitHub: [github.com/arrahimipour/AI-BugTest](https://github.com/arrahimipour/AI-BugTest)
