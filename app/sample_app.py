def run_test_case(kind: str):
    if kind == "crash_input":
        raise RuntimeError("Simulated crash for emoji/large input")
    return True

def check_ui_alignment():
    return True

def generic_check():
    return True
