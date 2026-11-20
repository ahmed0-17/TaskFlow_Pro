
from uuid import uuid4


def create_authenticated_user(client):
    """Register and login a user; return access token."""

    email = f"user_{uuid4().hex[:8]}@example.com"
    password = "TestPassword123"

    register_response = client.post(
        "/api/v1/auth/register",
        json={
            "name": "Test User",
            "email": email,
            "password": password
        }
    )

    assert register_response.status_code == 201

    login_response = client.post(
        "/api/v1/auth/login",
        data={
            "username": email,
            "password": password
        }
    )

    assert login_response.status_code == 200

    return login_response.json()["access_token"]


def create_test_task(client, token):
    """Create a task and return its response data."""

    response = client.post(
        "/api/v1/tasks/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "title": "Learn API Testing",
            "description": "Practice TaskFlow Pro endpoints",
            "priority": "High",
            "category": "Study"
        }
    )

    assert response.status_code == 201

    return response.json()


def test_create_task(client):
    token = create_authenticated_user(client)

    response = client.post(
        "/api/v1/tasks/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "title": "Learn API Testing",
            "description": "Practice TaskFlow Pro endpoints",
            "priority": "High",
            "category": "Study"
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert data["title"] == "Learn API Testing"
    assert data["priority"] == "High"
    assert data["category"] == "Study"
    assert data["is_completed"] is False
    assert "id" in data


def test_get_single_task(client):
    token = create_authenticated_user(client)
    task = create_test_task(client, token)

    response = client.get(
        f"/api/v1/tasks/{task['id']}",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert response.json()["id"] == task["id"]
    assert response.json()["title"] == task["title"]


def test_get_all_tasks(client):
    token = create_authenticated_user(client)
    task = create_test_task(client, token)

    response = client.get(
        "/api/v1/tasks/",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert any(item["id"] == task["id"] for item in data)


def test_update_task(client):
    token = create_authenticated_user(client)
    task = create_test_task(client, token)

    response = client.patch(
        f"/api/v1/tasks/{task['id']}",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "title": "Updated Task Title",
            "priority": "Low"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["title"] == "Updated Task Title"
    assert data["priority"] == "Low"


def test_delete_task(client):
    token = create_authenticated_user(client)
    task = create_test_task(client, token)

    response = client.delete(
        f"/api/v1/tasks/{task['id']}",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 204

    get_response = client.get(
        f"/api/v1/tasks/{task['id']}",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert get_response.status_code == 404


def test_get_nonexistent_task(client):
    token = create_authenticated_user(client)

    response = client.get(
        "/api/v1/tasks/2000000000",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 404


def test_access_task_without_token(client):
    response = client.get("/api/v1/tasks/")

    assert response.status_code == 401


def test_user_cannot_access_another_users_task(client):
    owner_token = create_authenticated_user(client)
    other_user_token = create_authenticated_user(client)

    task = create_test_task(client, owner_token)

    response = client.get(
        f"/api/v1/tasks/{task['id']}",
        headers={"Authorization": f"Bearer {other_user_token}"}
    )

    assert response.status_code == 404
