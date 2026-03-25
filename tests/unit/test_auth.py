"""
Unit Tests - Authentication Module
Testa funções de autenticação, hashing e token generation.
"""

from datetime import timedelta

import pytest

from ecommerce_analytics.api.auth import (
    create_access_token,
    get_password_hash,
    verify_password,
    verify_token,
)
from ecommerce_analytics.core.exceptions import InvalidTokenError


class TestPasswordHashing:
    """Testes para hashing de senhas."""

    def test_password_hash_creates_different_hash(self):
        """Testa se senhas diferentes geram hashes diferentes."""
        password1 = "password123"
        password2 = "password456"

        hash1 = get_password_hash(password1)
        hash2 = get_password_hash(password2)

        assert hash1 != hash2
        assert hash1 != password1
        assert hash2 != password2

    def test_password_hash_same_password_different_hash(self):
        """Testa se a mesma senha gera hashes diferentes (Argon2 com salt)."""
        password = "password123"

        hash1 = get_password_hash(password)
        hash2 = get_password_hash(password)

        # Argon2 com salt gera hashes diferentes para a mesma senha
        assert hash1 != hash2

    def test_verify_password_correct(self):
        """Testa verificação de senha correta."""
        password = "password123"
        hashed = get_password_hash(password)

        assert verify_password(password, hashed) is True

    def test_verify_password_incorrect(self):
        """Testa verificação de senha incorreta."""
        password = "password123"
        wrong_password = "wrong_password"
        hashed = get_password_hash(password)

        assert verify_password(wrong_password, hashed) is False


class TestTokenGeneration:
    """Testes para geração e verificação de tokens."""

    def test_create_access_token(self):
        """Testa criação de token de acesso."""
        data = {"sub": "testuser"}
        token = create_access_token(data)

        assert isinstance(token, str)
        assert len(token) > 0
        assert token.count(".") == 2  # JWT tem 3 partes separadas por ponto

    def test_create_access_token_with_expiration(self):
        """Testa criação de token com expiração customizada."""
        data = {"sub": "testuser"}
        expires_delta = timedelta(hours=1)
        token = create_access_token(data, expires_delta)

        assert isinstance(token, str)
        assert len(token) > 0

    def test_verify_token_valid(self):
        """Testa verificação de token válido."""
        data = {"sub": "testuser"}
        token = create_access_token(data)

        payload = verify_token(token)

        assert payload["sub"] == "testuser"
        assert "exp" in payload

    def test_verify_token_invalid(self):
        """Testa verificação de token inválido."""
        invalid_token = "invalid.token.here"

        with pytest.raises(InvalidTokenError):
            verify_token(invalid_token)

    def test_verify_token_missing_sub(self):
        """Testa verificação de token sem 'sub' claim."""
        from jose import jwt

        from ecommerce_analytics.core.config import settings

        # Criar token sem 'sub'
        data = {"exp": 9999999999}
        token = jwt.encode(data, settings.secret_key, algorithm="HS256")

        with pytest.raises(InvalidTokenError):
            verify_token(token)
