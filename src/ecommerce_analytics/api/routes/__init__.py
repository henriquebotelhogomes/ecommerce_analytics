"""
API Routes Package
Expõe todos os routers para importação centralizada.
"""

from . import analytics, auth, forecast, recommendations

__all__ = ["auth", "analytics", "forecast", "recommendations"]
