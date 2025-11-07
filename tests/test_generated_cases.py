import os
import textwrap

def generate_test_case(description: str, severity: str = "critical", requirement_id: str = "REQ-001"):
    """
    Generates multiple auto test cases aligned with ISTQB concepts.
    Tests vary based on severity level and follow structured design:
    - Critical: crash & exception handling
    - Major: functional behavior
    - Minor: boundary or smoke test
    """
    os.makedirs("tests", exist_ok=True)
    test_file = os.path.join("tests", "test_generated_cases.py")

    with open(test_file, "w", encoding="utf-8") as f:
        f.write("# Auto-generated test file (ISTQB-aligned, multi-case)\n")
        f.write("import pytest\n")
        f.write("from app import sample_app as app\n\n")

        f.write(f"# Requirement: {requirement_id}\n")
        f.write(f"# Description: {description}\n\n")

        if severity.lower() == "critical":
            f.write(textwrap.dedent(f"""
            @pytest.mark.severity("critical")
            @pytest.mark.type("crash")
            @pytest.mark.req("{requirement_id}")
            def test_crash_case():
                # {requirement_id}: Ensure app handles invalid inputs (crash proof)
                try:
                    app.run_test_case("crash_input")
                except Exception:
                    assert True
                else:
                    assert False, "Expected crash not triggered"
            """))

            f.write(textwrap.dedent("""
            @pytest.mark.severity("critical")
            @pytest.mark.type("negative")
            def test_invalid_data():
                # Validate handling of corrupted data input
                with pytest.raises(ValueError):
                    app.run_test_case("invalid_data")
            """))

        elif severity.lower() == "major":
            f.write(textwrap.dedent(f"""
            @pytest.mark.severity("major")
            @pytest.mark.type("functional")
            def test_feature_behavior():
                # {requirement_id}: Verify core feature executes correctly
                result = app.run_test_case("normal_input")
                assert result is True
            """))

            f.write(textwrap.dedent("""
            @pytest.mark.severity("major")
            @pytest.mark.type("boundary")
            def test_boundary_values():
                # Validate boundary behavior for edge inputs
                result = app.run_test_case("edge_input")
                assert result in [True, False]
            """))

        else:
            f.write(textwrap.dedent(f"""
            @pytest.mark.severity("minor")
            @pytest.mark.type("smoke")
            def test_smoke():
                # {requirement_id}: Basic sanity check
                result = app.run_test_case("basic_input")
                assert result is not None
            """))

    print(f"✅ Multi-case test file generated at {test_file}")
    return test_file
