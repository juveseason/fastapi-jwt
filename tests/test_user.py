from configuration import settings


def test_post_default_superuser_first_time(test_app):
    test_data = {
        "email": settings.DEFAULT_SUPERUSER_EMAIL,
        "full_name": settings.DEFAULT_SUPERUSER_FULL_NAME,
        "is_active": True,
        "is_superuser": True,
    }
    response = test_app.post("/auth/users/init")
    assert response.status_code == 200
    assert response.json() == test_data


def test_post_default_superuser_again(test_app):
    test_data = {"detail": "Email already registered"}
    response = test_app.post("/auth/users/init")
    assert response.status_code == 400
    assert response.json() == test_data


def test_post_access_token(test_app):
    test_data = {
        "username": settings.DEFAULT_SUPERUSER_EMAIL,
        "password": settings.DEFAULT_SUPERUSER_PASSWORD,
    }
    response = test_app.post("/auth/token", data=test_data)
    assert response.status_code == 200
    r = response.json()
    assert "access_token" in r
    assert r["token_type"] == "bearer"


def login(test_app):
    login_data = {
        "username": settings.DEFAULT_SUPERUSER_EMAIL,
        "password": settings.DEFAULT_SUPERUSER_PASSWORD,
    }
    response = test_app.post("/auth/token", data=login_data)
    return response.json()["access_token"]


def test_get_user_me(test_app):
    access_token = login(test_app)
    response = test_app.get(
        "/auth/users/me", headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 200
    test_data = {
        "email": settings.DEFAULT_SUPERUSER_EMAIL,
        "full_name": settings.DEFAULT_SUPERUSER_FULL_NAME,
        "is_active": True,
        "is_superuser": True,
    }
    assert response.json() == test_data


def test_post_user(test_app):
    access_token = login(test_app)
    test_data = {
        "email": "test.user1@example.com",
        "full_name": "Test User1",
        "password": "dummypass",
        "is_active": True,
        "is_superuser": False,
    }
    response = test_app.post(
        "/auth/users",
        headers={"Authorization": f"Bearer {access_token}"},
        json=test_data,
    )
    assert response.status_code == 200
    test_data.pop("password")
    assert response.json() == test_data


def test_get_user_by_email(test_app):
    access_token = login(test_app)
    response = test_app.get(
        "/auth/users",
        headers={"Authorization": f"Bearer {access_token}"},
        params={"email": "test.user1@example.com"},
    )
    assert response.status_code == 200
    test_data = {
        "email": "test.user1@example.com",
        "full_name": "Test User1",
        "is_active": True,
        "is_superuser": False,
    }
    assert response.json() == test_data


def test_update_user_by_email(test_app):
    access_token = login(test_app)
    test_data = {
        "email": "test.user1@example.com",
        "full_name": "TEST USER1",
        "is_active": False,
        "is_superuser": True,
    }
    response = test_app.put(
        "/auth/users",
        headers={"Authorization": f"Bearer {access_token}"},
        json=test_data,
    )
    assert response.status_code == 200

    assert response.json() == test_data


def test_get_user_all(test_app):
    access_token = login(test_app)
    response = test_app.get(
        "/auth/users/all", headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 200
    test_data = [
        {
            "email": settings.DEFAULT_SUPERUSER_EMAIL,
            "full_name": settings.DEFAULT_SUPERUSER_FULL_NAME,
            "is_active": True,
            "is_superuser": True,
        },
        {
            "email": "test.user1@example.com",
            "full_name": "TEST USER1",
            "is_active": False,
            "is_superuser": True,
        },
    ]
    assert response.json() == test_data


def test_delete_user_by_email(test_app):
    access_token = login(test_app)
    test_data = {"email": "test.user1@example.com"}
    response = test_app.delete(
        "/auth/users",
        headers={"Authorization": f"Bearer {access_token}"},
        params=test_data,
    )
    assert response.status_code == 200

    correct_response = {
        "email": "test.user1@example.com",
        "full_name": "TEST USER1",
        "status": "deleted",
    }
    assert response.json() == correct_response


def test_get_user_all_again(test_app):
    access_token = login(test_app)
    response = test_app.get(
        "/auth/users/all", headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 200
    test_data = [
        {
            "email": settings.DEFAULT_SUPERUSER_EMAIL,
            "full_name": settings.DEFAULT_SUPERUSER_FULL_NAME,
            "is_active": True,
            "is_superuser": True,
        }
    ]
    assert response.json() == test_data
