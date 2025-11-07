import subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def run(cmd):
    print(">>", " ".join(cmd))
    res = subprocess.run(cmd, cwd=ROOT)
    if res.returncode != 0:
        sys.exit(res.returncode)

if __name__ == "__main__":
    run([sys.executable, "model/train_model_advanced.py"])
    run([sys.executable, "ui_streamlit.py"])
