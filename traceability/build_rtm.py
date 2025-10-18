from pathlib import Path
import subprocess, re
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "traceability" / "rtm.csv"

def collect_nodeids():
    r = subprocess.run(["pytest", "--collect-only", "-q"], cwd=ROOT, capture_output=True, text=True)
    r.check_returncode()
    return [ln.strip() for ln in r.stdout.splitlines() if "::" in ln]

def inspect_markers(nodeid: str):
    file_path = ROOT / nodeid.split("::")[0]
    text = file_path.read_text(encoding="utf-8", errors="ignore")
    msev = re.search(r'@pytest\.mark\.severity\("([^"]+)"\)', text)
    mtyp = re.search(r'@pytest\.mark\.type\("([^"]+)"\)', text)
    mreq = re.search(r'@pytest\.mark\.req\("([^"]+)"\)', text)
    return {
        "severity": msev.group(1) if msev else "",
        "type": mtyp.group(1) if mtyp else "",
        "req_id": mreq.group(1) if mreq else "",
    }

def main():
    nodeids = collect_nodeids()
    rows = []
    for nid in nodeids:
        meta = inspect_markers(nid)
        rows.append({"test_name": nid, **meta})

    df = pd.DataFrame(rows)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT, index=False)
    print(f"✅ wrote {OUT}")
    print(df.head())

if __name__ == "__main__":
    main()
