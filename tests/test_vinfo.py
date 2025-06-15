from commands import vinfo

def test_vinfo_response():
    form_data = {"user_name": "tester"}
    response = vinfo.run(form_data)
    assert response["text"].startswith(":robot_face:")
    assert "tester" in response["text"]
