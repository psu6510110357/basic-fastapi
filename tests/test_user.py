import pytest


@pytest.fixture
def user_data():
    return {
        "username": "johndoe",
        "email": "john@example.com",
        "firstName": "John",
        "lastName": "Doe",
        "password": "securepassword123",
    }


@pytest.mark.asyncio
async def test_create_user(client, user_data):
    response = await client.post("/api/v1/users/", json=user_data)

    assert response.status_code == 201
    data = response.json()
    assert data["username"] == user_data["username"]
    assert data["email"] == user_data["email"]
    assert data["firstName"] == user_data["firstName"]
    assert data["lastName"] == user_data["lastName"]
    assert "id" in data


@pytest.mark.asyncio
async def test_get_users(client):
    response = await client.get("/api/v1/users/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "users" in data
    assert "total_count" in data
    assert "has_more" in data

    users = data["users"]
    assert isinstance(users, list)
    for user in users:
        assert "id" in user
        assert "username" in user
        assert "email" in user


@pytest.mark.asyncio
async def test_get_user_by_id(client, user_data):
    # Create a user first
    create_resp = await client.post("/api/v1/users/", json=user_data)
    user_id = create_resp.json()["id"]

    # Retrieve the user
    response = await client.get(f"/api/v1/users/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == user_id

    import uuid

    non_existent_id = str(uuid.uuid4())
    response = await client.get(f"/api/v1/users/{non_existent_id}")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_update_user(client, user_data):
    # Create a user first
    create_resp = await client.post("/api/v1/users/", json=user_data)
    user_id = create_resp.json()["id"]

    updated_data = user_data.copy()
    updated_data["username"] = "Jane Doe"

    response = await client.put(f"/api/v1/users/{user_id}", json=updated_data)
    assert response.status_code == 200
    assert response.json()["username"] == "Jane Doe"

    # Attempt to update with invalid data
    invalid_data = {"username": ""}  # Empty username
    response = await client.put(f"/api/v1/users/{user_id}", json=invalid_data)
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_delete_user(client, user_data):
    # Create a user first
    create_resp = await client.post("/api/v1/users/", json=user_data)
    user_id = create_resp.json()["id"]

    response = await client.delete(f"/api/v1/users/{user_id}")
    assert response.status_code == 204

    # Attempt to delete a non-existent user
    response = await client.delete(f"/api/v1/users/{user_id}")
    assert response.status_code == 404
