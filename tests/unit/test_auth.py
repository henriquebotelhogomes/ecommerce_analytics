"""
Testes unitários para autenticação
"""

import pytest
from ecommerce_analytics.api.auth import (
    create_access_token,
    get_password_hash,
    verify_password,
)


@pytest.mark.unit
class TestAuth:
    """Testes de autenticação"""

    def test_password_hash(self):
        """Testa hashing de senha"""
        password = "test123"
        hashed = get_password_hash(password)

        assert hashed != password
        assert verify_password(password, hashed) is True

    def test_token_creation(self):
        """Testa criação de token"""
        data = {"sub": "test_user"}
        token = create_access_token(data)

        assert isinstance(token, str)
        assert len(token) > 0
