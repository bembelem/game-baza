"""Тесты POST /auth/logout.

Логаут не ходит в БД — просто удаляет cookie и возвращает сообщение.
Поэтому большая часть тестов не требует поднятого postgres.
"""
import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


class TestLogout:
    """Базовая проверка контракта POST /auth/logout."""

    def test_returns_200(self, client: TestClient) -> None:
        response = client.post("/auth/logout")
        assert response.status_code == 200

    def test_clears_access_token_cookie(self, client: TestClient) -> None:
        """В Set-Cookie должен быть access_token="" с истёкшим/нулевым сроком."""
        response = client.post("/auth/logout")
        set_cookie = response.headers.get("set-cookie", "")
        assert "access_token=" in set_cookie
        # FastAPI/Starlette в delete_cookie выставляют Max-Age=0 или прошедший Expires
        assert "Max-Age=0" in set_cookie or "expires=" in set_cookie.lower()

    def test_logout_removes_cookie_with_proper_scope(self, client: TestClient) -> None:
        """Кука установленная с тем же path, что и сервер шлёт в delete_cookie, должна очиститься."""
        # Важно: тот же path='/', что у server-side delete_cookie — иначе httpx считает их разными.
        client.cookies.set("access_token", "fake-token-value", domain="testserver", path="/")
        assert client.cookies.get("access_token") == "fake-token-value"

        response = client.post("/auth/logout")
        assert response.status_code == 200
        assert client.cookies.get("access_token") in (None, "")

    def test_method_not_allowed_on_get(self, client: TestClient) -> None:
        """Logout — только POST. GET должен вернуть 405."""
        response = client.get("/auth/logout")
        assert response.status_code == 405


# ---------------------------------------------------------------------------
# Интеграционные тесты (требуют поднятый postgres + пользователь в БД).
# Запускаются только если есть переменная RUN_INTEGRATION_TESTS=1.
# ---------------------------------------------------------------------------

@pytest.mark.integration
class TestLogoutIntegration:
    """Полный цикл register → logout → /users/me должен дать 401."""

    def test_logout_invalidates_session_for_me(self, client: TestClient) -> None:
        # 1. Регистрируемся (получаем cookie)
        register = client.post(
            "/auth/register",
            json={
                "username": "test_logout_user",
                "email": "logout_test@example.com",
                "password": "SecurePass123!",
                "birthdate": "2000-01-01",
            },
        )
        assert register.status_code == 201

        # 2. /users/me должен быть доступен
        me_before = client.get("/users/me")
        assert me_before.status_code == 200

        # 3. Logout
        logout = client.post("/auth/logout")
        assert logout.status_code == 200

        # 4. /users/me теперь 401 — токена нет
        me_after = client.get("/users/me")
        assert me_after.status_code == 401
