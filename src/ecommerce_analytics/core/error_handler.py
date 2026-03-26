"""
Error Handler - Centralized error handling and retry logic
"""

import time
from collections.abc import Callable
from functools import wraps
from typing import Any

from loguru import logger

from ecommerce_analytics.core.exceptions import (
    BigQueryConnectionException,
    BigQueryQueryException,
    BigQueryTimeoutException,
)

# ========== ERROR MASKING ==========


def mask_sensitive_data(data: str, mask_char: str = "*") -> str:
    """
    Mask sensitive data in strings (passwords, tokens, etc).

    Args:
        data: String to mask
        mask_char: Character to use for masking

    Returns:
        Masked string
    """
    if not data or len(data) < 4:
        return mask_char * len(data)

    return data[:2] + mask_char * (len(data) - 4) + data[-2:]


# ========== SAFE LOGGING ==========


def safe_log_error(
    error: Exception,
    context: str = "Error",
    include_traceback: bool = False,
) -> None:
    """
    Log error safely without exposing sensitive data.

    Args:
        error: Exception to log
        context: Context description
        include_traceback: Whether to include full traceback
    """
    error_type = type(error).__name__
    error_message = str(error)

    log_data = {
        "context": context,
        "error_type": error_type,
        "error_message": error_message,
    }

    if include_traceback:
        logger.exception(f"❌ {context}: {error_type}", extra=log_data)
    else:
        logger.error(f"❌ {context}: {error_type}", extra=log_data)


# ========== RETRY WITH BACKOFF ==========


def retry_with_backoff(
    max_retries: int = 3,
    initial_delay: float = 1.0,
    max_delay: float = 60.0,
    exponential_base: float = 2.0,
    exceptions: tuple[type[BaseException], ...] = (Exception,),
) -> Callable:
    """
    Decorator para retry com backoff exponencial.

    Args:
        max_retries: Número máximo de tentativas
        initial_delay: Delay inicial em segundos
        max_delay: Delay máximo em segundos
        exponential_base: Base para cálculo exponencial
        exceptions: Tupla de exceções a capturar

    Returns:
        Decorator function

    Example:
        @retry_with_backoff(max_retries=3, initial_delay=1.0)
        def fetch_data():
            return requests.get("https://api.example.com/data")
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # ✅ Inicializar como BaseException | None
            last_exception: BaseException | None = None

            for attempt in range(1, max_retries + 1):
                try:
                    logger.debug(
                        f"🔄 Tentativa {attempt}/{max_retries} para {func.__name__}",
                    )
                    return func(*args, **kwargs)

                except exceptions as e:
                    # ✅ 'e' é do tipo da tupla 'exceptions'
                    last_exception = e

                    if attempt == max_retries:
                        logger.error(
                            f"❌ Todas as {max_retries} tentativas falharam",
                            extra={"function": func.__name__, "error": str(e)},
                        )
                        raise

                    # ✅ Calcular delay com backoff exponencial
                    delay = min(
                        initial_delay * (exponential_base ** (attempt - 1)),
                        max_delay,
                    )

                    logger.warning(
                        f"⚠️  Tentativa {attempt} falhou, aguardando {delay}s",
                        extra={
                            "function": func.__name__,
                            "error": str(e),
                            "next_retry_in": delay,
                        },
                    )

                    time.sleep(delay)

            # ✅ Se chegou aqui, todas as tentativas falharam
            if last_exception:
                raise last_exception

        return wrapper

    return decorator


# ========== BIGQUERY ERROR HANDLING ==========


def handle_bigquery_error(func: Callable) -> Callable:
    """
    Decorator para tratamento de erros BigQuery.

    Converte exceções genéricas em exceções específicas do BigQuery.

    Args:
        func: Função a decorar

    Returns:
        Função decorada

    Example:
        @handle_bigquery_error
        def execute_query(query: str):
            return client.query(query).result()
    """

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            return func(*args, **kwargs)

        except TimeoutError as e:
            safe_log_error(
                e,
                context=f"BigQuery timeout in {func.__name__}",
                include_traceback=True,
            )
            # ✅ CORRIGIDO: Passar message e details como argumentos posicionais
            raise BigQueryTimeoutException(
                f"BigQuery query timeout: {e!s}",
                {"function": func.__name__},
            ) from e

        except ConnectionError as e:
            safe_log_error(
                e,
                context=f"BigQuery connection error in {func.__name__}",
                include_traceback=True,
            )
            # ✅ CORRIGIDO: Passar message e details como argumentos posicionais
            raise BigQueryConnectionException(
                f"BigQuery connection failed: {e!s}",
                {"function": func.__name__},
            ) from e

        except Exception as e:
            error_type = type(e).__name__

            if "not found" in str(e).lower():
                safe_log_error(
                    e,
                    context=f"BigQuery resource not found in {func.__name__}",
                    include_traceback=True,
                )
                raise BigQueryQueryException(
                    f"BigQuery resource not found: {e!s}",
                    {"function": func.__name__, "error_type": error_type},
                ) from e

            elif "permission" in str(e).lower():
                safe_log_error(
                    e,
                    context=f"BigQuery permission denied in {func.__name__}",
                    include_traceback=True,
                )
                # ✅ CORRIGIDO: Passar message e details como argumentos posicionais
                raise BigQueryConnectionException(
                    f"BigQuery permission denied: {e!s}",
                    {"function": func.__name__, "error_type": error_type},
                ) from e

            else:
                safe_log_error(
                    e,
                    context=f"BigQuery error in {func.__name__}",
                    include_traceback=True,
                )
                raise BigQueryQueryException(
                    f"BigQuery query failed: {e!s}",
                    {"function": func.__name__, "error_type": error_type},
                ) from e

    return wrapper
