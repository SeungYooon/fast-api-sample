from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_create_comment():
    response = client.post(
        "/comments/",
        json={
            "post_id": 1,
            "content": "Test comment",
        },
        headers={"Authorization": "Bearer <token>"},
    )
    assert response.status_code == 200


def test_get_comments():
    response = client.get("/comments/?post_id=1")
    assert response.status_code == 200


def test_delete_comment():
    response = client.delete(
        "/comments/1",
        headers={"Authorization": "Bearer <token>"},
    )
    assert response.status_code == 200
