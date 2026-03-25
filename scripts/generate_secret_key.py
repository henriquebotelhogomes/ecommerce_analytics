# scripts/generate_secret_key.py
"""
Script para gerar SECRET_KEY segura para JWT
Uso: python scripts/generate_secret_key.py
"""

import secrets
import sys


def generate_secret_key(length: int = 32) -> str:
    """
    Gera uma chave secreta segura para JWT

    Args:
        length: Tamanho em bytes (padrão: 32 = 256 bits)

    Returns:
        Chave secreta em formato URL-safe base64
    """
    return secrets.token_urlsafe(length)


def main():
    """Gera e exibe a chave secreta"""
    secret_key = generate_secret_key()

    print("\n" + "=" * 70)
    print("🔐 CHAVE SECRETA JWT GERADA COM SUCESSO")
    print("=" * 70)
    print(f"\nSECRET_KEY={secret_key}\n")
    print("⚠️  INSTRUÇÕES IMPORTANTES:")
    print("1. Copie a chave acima")
    print("2. Cole no arquivo .env:")
    print("   SECRET_KEY=<chave_copiada>")
    print("3. NUNCA commit .env no Git")
    print("4. NUNCA compartilhe esta chave")
    print("5. Regenere em produção regularmente")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()