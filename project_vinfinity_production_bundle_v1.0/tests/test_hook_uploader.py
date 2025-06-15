from hook_uploader import upload_to_wordpress


def test_upload_to_wordpress():
    status, resp = upload_to_wordpress("title", "content", "slug", "token")
    assert status == 201
    assert resp["url"].endswith("slug")
