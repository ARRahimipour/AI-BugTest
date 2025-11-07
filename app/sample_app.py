"""
Sample Application Under Test (AUT)
Simulates a small system under test for AI-BugTest.
Aligned with ISTQB Test Levels (unit, integration, system).
"""

import random


class SampleApp:
    """A mock application for demonstrating automated testing."""

    def run_test_case(self, input_type: str):
        """
        Simulates app behavior based on input type.
        Returns True for success, raises or fails based on the input.
        """

        if input_type == "crash_input":
            # Simulate a critical crash scenario
            raise RuntimeError("Application crashed due to invalid emoji input 😭")

        elif input_type == "invalid_data":
            # Simulate invalid data causing a handled error
            raise ValueError("Corrupted input detected")

        elif input_type == "normal_input":
            # Simulate normal behavior
            return True

        elif input_type == "edge_input":
            # Edge case behavior (could randomly fail)
            return random.choice([True, False])

        elif input_type == "basic_input":
            # Simple smoke/sanity test case
            return "OK"

        else:
            # Unknown input, simulate unexpected behavior
            raise Exception(f"Unknown input type: {input_type}")


# Singleton instance for easy test imports
sample_app = SampleApp()
