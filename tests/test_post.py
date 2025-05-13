from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_post():
    # 1. 회원가입
    client.post("/users/signup", json={
        "email": "posttester@example.com",
        "password": "postpassword"
    })

    # 2. 로그인 → access_token 받기
    response = client.post("/users/login", json={
        "email": "posttester@example.com",
        "password": "postpassword"
    })
    assert response.status_code == 200
    token = response.json()["access_token"]

    # 3. 게시글 작성 요청 (Authorization 헤더 포함)
    response = client.post("/posts/", json={
        "title": "테스트 게시글",
        "content": "이것은 테스트 콘텐츠입니다."
    }, headers={"Authorization": f"Bearer {token}"})

    print(response.text)  # 디버깅용

    assert response.status_code in [200, 201]
    assert response.json()["title"] == "테스트 게시글"
    assert response.json()["content"] == "이것은 테스트 콘텐츠입니다."