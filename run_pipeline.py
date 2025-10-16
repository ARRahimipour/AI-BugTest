import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def run(cmd: list[str], cwd: Path = None):
    print(">>", " ".join(cmd))
    res = subprocess.run(cmd, cwd=cwd or ROOT)
    if res.returncode != 0:
        sys.exit(res.returncode)

def main():
    # 1) Train
    run([sys.executable, "model/train_model.py"])

    # 2) Predict & Generate test for a sample bug
    sample_desc = "App crashes when input contains emoji"
    run([sys.executable, "main.py", sample_desc])

    # 3) Run tests
    run([sys.executable, "-m", "pytest", "-q"])

if __name__ == "__main__":
    main()
