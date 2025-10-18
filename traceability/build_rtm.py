import os
import csv
import re

TESTS_DIR = "tests"
RTM_FILE = "traceability/rtm.csv"

REQ_PATTERN = re.compile(r"REQ-[A-Z0-9]+")

def extract_requirements_from_test(test_file):
    with open(test_file, encoding="utf-8") as f:
        content = f.read()
    return list(set(REQ_PATTERN.findall(content)))

def build_rtm():
    rows = []
    for root, _, files in os.walk(TESTS_DIR):
        for file in files:
            if file.startswith("test_") and file.endswith(".py"):
                path = os.path.join(root, file)
                reqs = extract_requirements_from_test(path)
                if reqs:
                    for r in reqs:
                        rows.append({"requirement_id": r, "test_file": file})
                else:
                    rows.append({"requirement_id": "UNKNOWN", "test_file": file})

    os.makedirs(os.path.dirname(RTM_FILE), exist_ok=True)
    with open(RTM_FILE, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["requirement_id", "test_file"])
        writer.writeheader()
        writer.writerows(rows)

    print(f"RTM built successfully at: {RTM_FILE}")
    print(f"📄 Total test mappings: {len(rows)}")

if __name__ == "__main__":
    build_rtm()
