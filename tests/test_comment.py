import os
import sys

from fastapi.testclient import TestClient

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.main import app  # noqa: E402

client = TestClient(app)


def get_token():
    client.post("/users/signup", json={"email": "c@example.com", "password": "1234"})
    response = client.post(
        "/users/login",
        json={"email": "c@example.com", "password": "1234"},
    )
    return response.json()["access_token"]


def create_post(token):
    response = client.post(
        "/posts/",
        json={
            "title": "test title",
            "content": "test content",
        },
        headers={
            "Authorization": f"Bearer {token}",
        },
    )
    return response.json()["id"]


def test_create_comment():
    token = get_token()
    post_id = create_post(token)

    response = client.post(
        f"/posts/{post_id}/comments",
        json={"content": "Test comment"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200


def test_get_comments():
    token = get_token()
    post_id = create_post(token)

    response = client.get(f"/posts/{post_id}/comments")
    assert response.status_code == 200


def test_delete_comment():
    token = get_token()
    post_id = create_post(token)

    response = client.post(
        f"/posts/{post_id}/comments",
        json={"content": "Comment to delete"},
        headers={"Authorization": f"Bearer {token}"},
    )
    comment_id = response.json()["id"]

    response = client.delete(
        f"/posts/comments/{comment_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
