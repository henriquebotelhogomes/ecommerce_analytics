"""
Schemas Pydantic para validação de entrada/saída da API
"""

from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    """Schema para requisição de login"""

    username: str = Field(..., min_length=1, max_length=50)
    password: str = Field(..., min_length=1, max_length=100)


class LoginResponse(BaseModel):
    """Schema para resposta de login"""

    access_token: str
    token_type: str = "bearer"
