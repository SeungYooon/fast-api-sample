import os
import sys

from fastapi.testclient import TestClient

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.main import app  # noqa: E402

client = TestClient(app)


def test_signup_and_login():
    # 회원가입
    response = client.post(
        "/users/signup",
        json={
            "email": "testuser@example.com",
            "password": "testpassword",
        },
    )
    assert response.status_code in [200, 400]  # 이미 존재 or 성공

    # 로그인
    response = client.post(
        "/users/login",
        json={
            "email": "testuser@example.com",
            "password": "testpassword",
        },
    )

    print(response.text)  # 디버깅용

    assert response.status_code == 200
    assert "access_token" in response.json()
