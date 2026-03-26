"""
Script para validar todos os imports do projeto
Valida que todas as dependências estão instaladas e importáveis
"""

import sys
from pathlib import Path

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent / "src"))

print("🔍 Validando imports do projeto...\n")

try:
    print("✅ Importando core.exceptions...")
    from ecommerce_analytics.core.exceptions import (
        AppException,
        AuthenticationException,
        InvalidTokenError,
        InvalidCredentialsError,
        UnauthorizedException,
        BigQueryException,
        BigQueryConnectionException,
        BigQueryQueryException,
        BigQueryTimeoutException,
        ValidationException,
        NotFoundException,
        RateLimitException,
    )
    print("   ✅ Todas as exceções importadas com sucesso\n")

    print("✅ Importando core.error_handler...")
    from ecommerce_analytics.core.error_handler import (
        mask_sensitive_data,
        safe_log_error,
        retry_with_backoff,
        handle_bigquery_error,
    )
    print("   ✅ Error handler importado com sucesso\n")

    print("✅ Importando core.bigquery_client...")
    from ecommerce_analytics.core.bigquery_client import (
        BigQueryClient,
        get_bigquery_client,
    )
    print("   ✅ BigQuery client importado com sucesso\n")

    print("✅ Importando api.auth...")
    from ecommerce_analytics.api.auth import (
        create_access_token,
        verify_token,
        authenticate_user,
        get_current_user,
    )
    print("   ✅ Auth importado com sucesso\n")

    print("✅ Importando api.routes.analytics...")
    from ecommerce_analytics.api.routes.analytics import router as analytics_router
    print("   ✅ Analytics router importado com sucesso\n")

    print("✅ Importando api.routes.forecast...")
    from ecommerce_analytics.api.routes.forecast import router as forecast_router
    print("   ✅ Forecast router importado com sucesso\n")

    print("✅ Importando api.main...")
    from ecommerce_analytics.api.main import app
    print("   ✅ API main importado com sucesso\n")

    print("╔════════════════════════════════════════════════════════════╗")
    print("║  ✅ TODOS OS IMPORTS VALIDADOS COM SUCESSO!               ║")
    print("║                                                            ║")
    print("║  Projeto pronto para produção! 🚀                         ║")
    print("╚════════════════════════════════════════════════════════════╝")

except ImportError as e:
    print(f"\n❌ ERRO DE IMPORT: {e}\n")
    sys.exit(1)
except Exception as e:
    print(f"\n❌ ERRO INESPERADO: {e}\n")
    sys.exit(1)