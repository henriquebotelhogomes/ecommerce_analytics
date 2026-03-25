"""
Exceções customizadas para a aplicação E-commerce Analytics
"""


class EcommerceAnalyticsError(Exception):
    """Exceção base para a aplicação"""

    pass


class AuthenticationError(EcommerceAnalyticsError):
    """Exceção para erros de autenticação"""

    pass


class BigQueryError(EcommerceAnalyticsError):
    """Exceção para erros do BigQuery"""

    pass
