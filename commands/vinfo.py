def run(form_data):
    user = form_data.get("user_name", "사용자")
    return {
        "response_type": "in_channel",
        "text": f":robot_face: 안녕하세요 {user}님! 현재 시스템은 정상 작동 중입니다."
    }
