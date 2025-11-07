# Test Strategy (ISTQB®-Aligned)

## Objectives
- Risk-Based Testing: prioritize tests by Impact × Likelihood
- Automation-first for regression using pytest

## Test Design Techniques
- Crash/Exception handling (negative testing)
- API contract & status code validation
- Performance sanity checks under synthetic load
- Validation & boundary testing
- UI alignment/checks (logic-side in sample app)

## Prioritization
- Model-estimated likelihood × class impact
- Secondary factor: execution time (speed score)

## Entry/Exit Criteria
- Entry: Model trained, RTM built, environment ready
- Exit: All High-risk requirements covered; Quality gates passed
