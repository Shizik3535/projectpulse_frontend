from app.schemas.auth import TokenResponse
from app.schemas.users import UserResponse
from app.schemas.base import MessageResponse


class AuthAPI:
    def __init__(self, client):
        self.client = client

    def login(self, username: str, password: str) -> TokenResponse:
        """Авторизация пользователя и сохранение токена."""
        response = self.client.request(
            "POST",
            "/auth/login",
            data={"username": username, "password": password},
            headers={'Content-Type': 'application/x-www-form-urlencoded'}
        )

        if "error" in response:
            raise Exception("Неправильное имя пользователя или пароль")

        token_response = TokenResponse(**response['data'])
        self.client.set_token(token_response.access_token)
        return token_response

    def logout(self) -> MessageResponse:
        """Выход пользователя и удаление токена."""
        response = self.client.request("POST", "/auth/logout")

        self.client.clear_token()
        if "error" in response:
            raise Exception("Попробуйте выйти снова")

        return MessageResponse(**response['data'])

    def get_user_info(self) -> UserResponse:
        """Получение данных о пользователе"""
        response = self.client.request("GET", "/auth/me")

        if "error" in response:
            raise Exception("Попробуйте перезайти в приложение заново или обратитесь к разработчику")

        return UserResponse(**response['data'])
