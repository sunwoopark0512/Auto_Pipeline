from utils.supabase_client import supabase

def run(form_data):
    user = form_data.get("user_name", "사용자")
    text = f":robot_face: 안녕하세요 {user}님! 현재 시스템은 정상 작동 중입니다."

    # Supabase에 기록
    supabase.table("command_logs").insert({
        "user_name": user,
        "command": "/vinfo",
        "text": text
    }).execute()

    return {
        "response_type": "in_channel",
        "text": text
    }
