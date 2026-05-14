import pytest


async def test_register_user(client):
    """Тестуємо ручку реєстрації"""
    response = await client.post("/register", json={
        "email": "test@example.com",
        "username": "testuser",
        "password": "secretpassword",
        "age": 25
    })
    assert response.status_code == 201
    data = response.json()
    assert data["message"] == "Успішна реєстрація"
    assert "id" in data


async def test_register_duplicate_user(client):
    """Тестуємо, що база не дасть створити двох однакових юзерів"""
    user_data = {
        "email": "test@example.com",
        "username": "testuser",
        "password": "secretpassword",
        "age": 25
    }
    # Створюємо першого
    await client.post("/register", json=user_data)
    # Пробуємо створити другого такого ж
    response2 = await client.post("/register", json=user_data)

    assert response2.status_code == 400
    assert response2.json()["detail"] == "User already exists"


async def test_login_and_protected_route(client):
    """Тестуємо логін і захищену ручку (перевірка кукі)"""
    # 1. Реєструємось
    await client.post("/register", json={
        "email": "auth@example.com",
        "username": "authuser",
        "password": "111",
        "age": 20
    })

    # 2. Логінимось
    login_response = await client.post("/login", json={
        "email": "auth@example.com",
        "password": "111"
    })
    assert login_response.status_code == 200
    assert "access_token" in login_response.cookies  # Перевіряємо чи кукі встановилось

    # 3. Смикаємо захищену ручку /users/me
    me_response = await client.get("/users/me")
    assert me_response.status_code == 200
    assert me_response.json()["email"] == "auth@example.com"