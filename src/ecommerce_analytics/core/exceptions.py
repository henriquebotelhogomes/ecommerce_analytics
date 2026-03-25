"""
Custom Exceptions for E-commerce Analytics API
Exceções específicas do domínio para tratamento de erros estruturado.
"""

from typing import Any, Optional


class EcommerceAnalyticsException(Exception):
    """
    Exceção base para todas as exceções do projeto.
    Fornece estrutura consistente para tratamento de erros.
    """

    def __init__(
        self,
        message: str,
        status_code: int = 500,
        error_code: Optional[str] = None,
        details: Optional[dict[str, Any]] = None,
    ):
        """
        Inicializa exceção com contexto estruturado.

        Args:
            message: Mensagem de erro legível
            status_code: Código HTTP associado
            error_code: Código interno de erro (ex: "AUTH_001")
            details: Detalhes adicionais do erro
        """
        self.message = message
        self.status_code = status_code
        self.error_code = error_code or self.__class__.__name__
        self.details = details or {}

        super().__init__(self.message)

    def to_dict(self) -> dict[str, Any]:
        """Converte exceção para dicionário para resposta JSON."""
        return {
            "error": self.error_code,
            "message": self.message,
            "status_code": self.status_code,
            "details": self.details,
        }


# ========== AUTENTICAÇÃO ==========
class AuthenticationError(EcommerceAnalyticsException):
    """Erro de autenticação (credenciais inválidas, token expirado, etc)."""

    def __init__(
        self,
        message: str = "Autenticação falhou",
        error_code: str = "AUTH_001",
        details: Optional[dict[str, Any]] = None,
    ):
        super().__init__(
            message=message,
            status_code=401,
            error_code=error_code,
            details=details,
        )


class InvalidTokenError(AuthenticationError):
    """Token JWT inválido ou expirado."""

    def __init__(self, message: str = "Token inválido ou expirado"):
        super().__init__(
            message=message,
            error_code="AUTH_002",
        )


class MissingTokenError(AuthenticationError):
    """Token não fornecido na requisição."""

    def __init__(self, message: str = "Token não fornecido"):
        super().__init__(
            message=message,
            error_code="AUTH_003",
        )


class InvalidCredentialsError(AuthenticationError):
    """Credenciais inválidas (username/password)."""

    def __init__(self, message: str = "Credenciais inválidas"):
        super().__init__(
            message=message,
            error_code="AUTH_004",
        )


# ========== AUTORIZAÇÃO ==========
class AuthorizationError(EcommerceAnalyticsException):
    """Erro de autorização (usuário não tem permissão)."""

    def __init__(
        self,
        message: str = "Acesso negado",
        error_code: str = "AUTHZ_001",
        details: Optional[dict[str, Any]] = None,
    ):
        super().__init__(
            message=message,
            status_code=403,
            error_code=error_code,
            details=details,
        )


class InsufficientPermissionsError(AuthorizationError):
    """Usuário não tem permissões suficientes."""

    def __init__(self, message: str = "Permissões insuficientes"):
        super().__init__(
            message=message,
            error_code="AUTHZ_002",
        )


# ========== VALIDAÇÃO ==========
class ValidationError(EcommerceAnalyticsException):
    """Erro de validação de dados."""

    def __init__(
        self,
        message: str = "Dados inválidos",
        error_code: str = "VAL_001",
        details: Optional[dict[str, Any]] = None,
    ):
        super().__init__(
            message=message,
            status_code=400,
            error_code=error_code,
            details=details,
        )


class InvalidLocationError(ValidationError):
    """Localização inválida no warehouse."""

    def __init__(
        self,
        location: str,
        valid_locations: Optional[list[str]] = None,
    ):
        super().__init__(
            message=f"Localização inválida: {location}",
            error_code="VAL_002",
            details={"location": location, "valid_locations": valid_locations},
        )


class InvalidParameterError(ValidationError):
    """Parâmetro inválido na requisição."""

    def __init__(
        self,
        parameter: str,
        message: str = "Parâmetro inválido",
    ):
        super().__init__(
            message=f"{message}: {parameter}",
            error_code="VAL_003",
            details={"parameter": parameter},
        )


# ========== RECURSO NÃO ENCONTRADO ==========
class NotFoundError(EcommerceAnalyticsException):
    """Recurso não encontrado."""

    def __init__(
        self,
        message: str = "Recurso não encontrado",
        error_code: str = "NOT_FOUND_001",
        details: Optional[dict[str, Any]] = None,
    ):
        super().__init__(
            message=message,
            status_code=404,
            error_code=error_code,
            details=details,
        )


class UserNotFoundError(NotFoundError):
    """Usuário não encontrado."""

    def __init__(self, username: str):
        super().__init__(
            message=f"Usuário não encontrado: {username}",
            error_code="NOT_FOUND_002",
            details={"username": username},
        )


# ========== BIGQUERY ==========
class BigQueryError(EcommerceAnalyticsException):
    """Erro ao acessar BigQuery."""

    def __init__(
        self,
        message: str = "Erro ao acessar BigQuery",
        error_code: str = "BQ_001",
        details: Optional[dict[str, Any]] = None,
    ):
        super().__init__(
            message=message,
            status_code=503,
            error_code=error_code,
            details=details,
        )


class BigQueryConnectionError(BigQueryError):
    """Erro de conexão com BigQuery."""

    def __init__(self, message: str = "Falha ao conectar ao BigQuery"):
        super().__init__(
            message=message,
            error_code="BQ_002",
        )


class BigQueryQueryError(BigQueryError):
    """Erro ao executar query no BigQuery."""

    def __init__(
        self,
        query: str,
        original_error: Optional[str] = None,
    ):
        super().__init__(
            message="Erro ao executar query no BigQuery",
            error_code="BQ_003",
            details={"query": query, "original_error": original_error},
        )


# ========== ANALYTICS ==========
class AnalyticsError(EcommerceAnalyticsException):
    """Erro ao processar analytics."""

    def __init__(
        self,
        message: str = "Erro ao processar analytics",
        error_code: str = "ANALYTICS_001",
        details: Optional[dict[str, Any]] = None,
    ):
        super().__init__(
            message=message,
            status_code=500,
            error_code=error_code,
            details=details,
        )


class DashboardError(AnalyticsError):
    """Erro ao gerar dashboard."""

    def __init__(self, message: str = "Erro ao gerar dashboard"):
        super().__init__(
            message=message,
            error_code="ANALYTICS_002",
        )


class ForecastError(AnalyticsError):
    """Erro ao gerar previsão."""

    def __init__(self, message: str = "Erro ao gerar previsão"):
        super().__init__(
            message=message,
            error_code="ANALYTICS_003",
        )


class RecommendationError(AnalyticsError):
    """Erro ao gerar recomendação."""

    def __init__(self, message: str = "Erro ao gerar recomendação"):
        super().__init__(
            message=message,
            error_code="ANALYTICS_004",
        )


# ========== CONFIGURAÇÃO ==========
class ConfigurationError(EcommerceAnalyticsException):
    """Erro de configuração."""

    def __init__(
        self,
        message: str = "Erro de configuração",
        error_code: str = "CONFIG_001",
        details: Optional[dict[str, Any]] = None,
    ):
        super().__init__(
            message=message,
            status_code=500,
            error_code=error_code,
            details=details,
        )


class MissingEnvironmentVariableError(ConfigurationError):
    """Variável de ambiente obrigatória não definida."""

    def __init__(self, variable_name: str):
        super().__init__(
            message=f"Variável de ambiente obrigatória não definida: {variable_name}",
            error_code="CONFIG_002",
            details={"variable_name": variable_name},
        )


# ========== RATE LIMITING ==========
class RateLimitError(EcommerceAnalyticsException):
    """Limite de requisições excedido."""

    def __init__(
        self,
        message: str = "Limite de requisições excedido",
        retry_after: Optional[int] = None,
    ):
        super().__init__(
            message=message,
            status_code=429,
            error_code="RATE_LIMIT_001",
            details={"retry_after": retry_after},
        )
