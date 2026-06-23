"""
日记 API 集成测试
"""
import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.fixture
async def client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac


@pytest.fixture
async def auth_headers(client):
    username = "testuser_py"
    password = "testpass123"
    reg = await client.post("/api/auth/register", json={
        "username": username,
        "password": password,
        "nickname": "测试用户",
    })
    if reg.status_code == 201:
        token = reg.json()["access_token"]
    else:
        login = await client.post("/api/auth/login", json={
            "username": username,
            "password": password,
        })
        token = login.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.mark.asyncio
async def test_health_check(client):
    response = await client.get("/api/system/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


@pytest.mark.asyncio
async def test_register_and_login(client):
    resp = await client.post("/api/auth/register", json={
        "username": "user_auth_test",
        "password": "password123",
    })
    assert resp.status_code in (201, 400)

    login = await client.post("/api/auth/login", json={
        "username": "user_auth_test",
        "password": "password123",
    })
    assert login.status_code == 200
    data = login.json()
    assert "access_token" in data
    assert data["user"]["username"] == "user_auth_test"


@pytest.mark.asyncio
async def test_create_diary_requires_auth(client):
    response = await client.post("/api/diary", json={
        "title": "测试",
        "content": "内容",
    })
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_create_diary(client, auth_headers):
    response = await client.post("/api/diary", json={
        "title": "测试日记",
        "content": "今天天气很好，心情不错，和朋友一起去了公园散步。",
        "mood_label": "开心",
    }, headers=auth_headers)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "测试日记"
    assert data["id"] is not None


@pytest.mark.asyncio
async def test_list_diaries(client, auth_headers):
    response = await client.get("/api/diary", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert "total" in data
    assert "items" in data


@pytest.mark.asyncio
async def test_get_diary_not_found(client, auth_headers):
    response = await client.get("/api/diary/99999", headers=auth_headers)
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_diary(client, auth_headers):
    create_resp = await client.post("/api/diary", json={
        "title": "待删除日记",
        "content": "这篇日记会被删除。",
    }, headers=auth_headers)
    diary_id = create_resp.json()["id"]

    delete_resp = await client.delete(f"/api/diary/{diary_id}", headers=auth_headers)
    assert delete_resp.status_code == 200

    get_resp = await client.get(f"/api/diary/{diary_id}", headers=auth_headers)
    assert get_resp.status_code == 404
