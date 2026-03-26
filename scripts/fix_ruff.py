"""
Script para corrigir automaticamente erros de ruff
Suporta UTF-8 em Windows, Linux e Mac
"""
import re
from pathlib import Path

def fix_analytics_py():
    """Fix B904 error in analytics.py"""
    file = Path("src/ecommerce_analytics/api/routes/analytics.py")
    content = file.read_text(encoding="utf-8")  # ✅ Especificar UTF-8

    # Fix B904 - adicionar 'from e' ao raise
    old_pattern = r"raise HTTPException\(status_code=500, detail=\"Error retrieving dashboard data from BigQuery\"\)"
    new_pattern = 'raise HTTPException(\n            status_code=500,\n            detail="Error retrieving dashboard data from BigQuery"\n        ) from e'

    content = re.sub(old_pattern, new_pattern, content)

    file.write_text(content, encoding="utf-8")  # ✅ Especificar UTF-8
    print("✅ Fixed analytics.py")


def fix_dashboard_py():
    """Fix C408 errors in dashboard.py"""
    file = Path("src/ecommerce_analytics/dashboard/app.py")
    content = file.read_text(encoding="utf-8")  # ✅ Especificar UTF-8

    # Replace dict() with {} literals
    # dict(color="#1f77b4", width=3) → {"color": "#1f77b4", "width": 3}
    content = re.sub(
        r'dict\(([^)]+)\)',
        lambda m: '{' + m.group(1).replace('=', ': ') + '}',
        content
    )

    file.write_text(content, encoding="utf-8")  # ✅ Especificar UTF-8
    print("✅ Fixed dashboard.py")


def fix_trailing_whitespace():
    """Fix W291 trailing whitespace"""
    files = [
        "src/ecommerce_analytics/services/analytics_service.py",
        "src/ecommerce_analytics/services/forecast_service.py",
        "src/ecommerce_analytics/services/ml_service.py",
    ]

    for file_path in files:
        file = Path(file_path)
        if file.exists():
            content = file.read_text(encoding="utf-8")  # ✅ Especificar UTF-8
            # Remove trailing whitespace
            lines = [line.rstrip() for line in content.split('\n')]
            file.write_text('\n'.join(lines), encoding="utf-8")  # ✅ Especificar UTF-8
            print(f"✅ Fixed {file_path}")
        else:
            print(f"⚠️  File not found: {file_path}")


if __name__ == "__main__":
    try:
        fix_analytics_py()
        fix_dashboard_py()
        fix_trailing_whitespace()
        print("\n✅ Todos os erros foram corrigidos!")
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()