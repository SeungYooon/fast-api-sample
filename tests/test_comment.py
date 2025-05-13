from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_comment():
    # 1. 회원가입
    client.post("/users/signup", json={
        "email": "commentuser@example.com",
        "password": "commentpassword"
    })

    # 2. 로그인 → 토큰 획득
    response = client.post("/users/login", json={
        "email": "commentuser@example.com",
        "password": "commentpassword"
    })
    assert response.status_code == 200
    token = response.json()["access_token"]

    # 3. 게시글 작성
    response = client.post("/posts/", json={
        "title": "댓글 테스트 게시글",
        "content": "댓글을 달기 위한 게시글입니다."
    }, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code in [200, 201]
    post_id = response.json()["id"]

    # 4. 댓글 작성
    response = client.post(f"/posts/{post_id}/comments", json={
        "content": "이것은 테스트 댓글입니다."
    }, headers={"Authorization": f"Bearer {token}"})

    print(response.text)  # 디버깅용

    assert response.status_code in [200, 201]
    assert response.json()["content"] == "이것은 테스트 댓글입니다."
    assert response.json()["post_id"] == post_id