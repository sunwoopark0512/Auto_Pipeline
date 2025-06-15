from modules.hook_uploader import upload_to_wordpress


def upload_all(title, content, slug, token):
    status_wp, res_wp = upload_to_wordpress(title, content, slug, token)
    # TODO: extended platform uploads
    return {"wordpress": status_wp}
