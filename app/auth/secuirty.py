from pydantic import SecretStr

from app.server.security import generate_jwt


def generate_session_id(username: str, email: str, secret_key: str | SecretStr):
    return generate_jwt(
        data={
            "username": username,
            "email": email,
        },
        secret=secret_key,
    )
