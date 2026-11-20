from uuid import uuid4


def test_register_user(client):
    email = f"test_{uuid4().hex[:8]}@example.com"

    response = client.post(
        "/api/v1/auth/register",
        json={
            "name": "Test User",
            "email": email,
            "password": "TestPassword123"
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert data["name"] == "Test User"
    assert data["email"] == email
    assert data["is_active"] is True
    assert "password" not in data
    assert "password_hash" not in data




def test_duplicate_registration(client):
    user_data = {
        "name": "Test User",
        "email": "duplicate@example.com",
        "password": "TestPassword123"
    }

    first_response = client.post(
        "/api/v1/auth/register",
        json=user_data
    )

    second_response = client.post(
        "/api/v1/auth/register",
        json=user_data
    )

    assert first_response.status_code == 201
    assert second_response.status_code == 409    




def test_login_user(client):
    email = "login_test@example.com"
    password = "TestPassword123"

    client.post(
        "/api/v1/auth/register",
        json={
            "name": "Login Test",
            "email": email,
            "password": password
        }
    )

    response = client.post(
        "/api/v1/auth/login",
        data={
            "username": email,
            "password": password
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"    




def test_login_invalid_password(client):
    email = "invalid_login@example.com"
    password = "CorrectPassword123"

    client.post(
        "/api/v1/auth/register",
        json={
            "name": "Invalid Login Test",
            "email": email,
            "password": password
        }
    )

    response = client.post(
        "/api/v1/auth/login",
        data={
            "username": email,
            "password": "WrongPassword123"
        }
    )

    assert response.status_code == 401
    assert "access_token" not in response.json()    



def test_get_current_user(client):
    email = "profile_test@example.com"
    password = "TestPassword123"

    client.post(
        "/api/v1/auth/register",
        json={
            "name": "Profile Test",
            "email": email,
            "password": password
        }
    )

    login_response = client.post(
        "/api/v1/auth/login",
        data={
            "username": email,
            "password": password
        }
    )

    access_token = login_response.json()["access_token"]

    response = client.get(
        "/api/v1/auth/me",
        headers={
            "Authorization": f"Bearer {access_token}"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "Profile Test"
    assert data["email"] == email
    assert "password_hash" not in data 




def test_get_current_user_without_token(client):
    response = client.get("/api/v1/auth/me")
    
    assert response.status_code == 401    