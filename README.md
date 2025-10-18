# 🧠 AI-BugTest  
**AI-driven Adaptive Test Case Generation and Prioritization System (ISTQB®-Aligned)**  

This project implements an **AI-powered software testing assistant** that predicts the severity of software defects, automatically generates test cases based on defect descriptions, and prioritizes them using **risk-based testing principles** defined by **ISTQB®**.  
It integrates NLP, test automation, and DevOps-style execution — ideal for graduate-level research or advanced software testing coursework.

---

## 🚀 Key Features

- 🧠 **AI-driven defect severity prediction** using NLP (TF-IDF + Logistic Regression)
- 🧩 **Automatic test generation** (Crash, API, Performance, Validation, UI)
- ⚖️ **Risk-based test prioritization** (Impact × Likelihood)
- ▶️ **Automated test execution** directly from Streamlit UI (via `pytest`)
- 📈 **Coverage reporting** and regression-ready test pipeline
- 💡 **Fully compliant with ISTQB® concepts** — Defect Severity, Risk-Based Testing, Test Design, Automation, Regression Testing

---

## 📂 Project Structure

```
AI-BugTest/
├── app/
│   └── sample_app.py               # Sample app for generated tests
├── data/
│   └── bugs.csv                    # Sample bug dataset
├── model/
│   ├── train_model_advanced.py     # Model training (AI severity predictor)
│   └── bug_severity_model.pkl      # Saved trained model
├── testgen/
│   └── generate_test.py            # AI + rule-based test generation logic
├── prioritizer/
│   └── prioritize.py               # Risk-based test prioritization
├── tests/
│   ├── __init__.py
│   └── test_generated_cases.py     # Auto-generated test cases
├── ui_streamlit.py                 # Streamlit UI (Predict → Generate → Run)
├── run_pipeline.py                 # CLI pipeline version
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup Instructions

### 1️⃣ Environment Setup
```bash
git clone https://github.com/arrahimipour/AI-BugTest.git
cd AI-BugTest
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

If missing:
```bash
pip install streamlit pytest pytest-cov scikit-learn pandas joblib requests
```

---

### 2️⃣ Train the Model
```bash
python model/train_model_advanced.py
```
Trains the NLP model on `data/bugs.csv` and stores it at `model/bug_severity_model.pkl`.

---

### 3️⃣ Launch the Streamlit UI
```bash
streamlit run ui_streamlit.py
```

Then in the browser:
1. Enter a bug description (e.g., *"App crashes when uploading file larger than 10MB"*).  
2. Click **🔮 Predict** to view predicted severity and probability.  
3. Click **🧪 Generate & Run** to generate and execute a test file.  
4. Click **⚖️ Prioritize & Run Top-50%** to execute risk-prioritized tests.

---

### 4️⃣ Run Everything via CLI (Optional)
```bash
python run_pipeline.py
```
Runs training → prediction → test generation → pytest pipeline in one go.

---

## 🧪 Testing & Coverage
```bash
pytest -q
pytest --cov=app --cov-report=term-missing
```

---

## 📘 ISTQB® Alignment

| ISTQB® Concept | Implementation in AI-BugTest |
|----------------|-------------------------------|
| **Defect Severity & Priority** | AI predicts severity based on textual description |
| **Risk-Based Testing** | `Risk = Impact × Likelihood` computed from model probabilities |
| **Test Design Techniques** | Rule-based AI test generation (Crash/API/Perf/Validation/UI) |
| **Test Automation Framework** | Fully automated via pytest + Streamlit pipeline |
| **Regression Testing** | Every new bug generates a test that joins the regression suite |

---

## 🧩 Future Improvements (Graduate-Level Extensions)
- 🧬 Replace TF-IDF with **Sentence-BERT embeddings** for semantic understanding
- 🔁 Implement **Active Learning** to continuously improve defect classification
- 🧮 Integrate **coverage-based prioritization** via `pytest-cov`
- 🌐 Deploy as **FastAPI microservice** + frontend via **Next.js**
- ⚙️ Integrate CI/CD workflow (GitHub Actions / Jenkins)
- 📊 Include dashboards for test effectiveness and risk metrics

---

## 🧑‍💻 Author
Developed by **Alireza Rahimipour Anaraki**  
MSc Software Engineering — *AI and Software Testing Research*
