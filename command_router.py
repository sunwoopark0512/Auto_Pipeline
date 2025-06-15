from commands import vinfo, vstart, vcheck


def handle_command(command_text, form_data):
    if command_text == "/vinfo":
        return vinfo.run(form_data)
    if command_text == "/vstart":
        return vstart.run(form_data)
    if command_text == "/vcheck":
        return vcheck.run(form_data)
    return {"response_type": "ephemeral", "text": "알 수 없는 명령어입니다."}
