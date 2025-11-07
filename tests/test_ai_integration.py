from model.bug_predictor import predict_severity

def test_predict_severity_runs():
    result = predict_severity("App crashes when emoji in input")
    assert result in ["Critical", "Major", "Minor"]
