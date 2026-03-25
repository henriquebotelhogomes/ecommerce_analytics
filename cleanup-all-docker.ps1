# cleanup-all-docker.ps1
# Script para limpar todos os containers e fazer rebuild do ecommerce-api

Write-Host "╔════════════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║  🧹 LIMPEZA COMPLETA - REMOVER WAREHOUSE_ROUTING          ║" -ForegroundColor Green
Write-Host "╚════════════════════════════════════════════════════════════╝" -ForegroundColor Green

# ========== PARAR CONTAINERS ESPECÍFICOS ==========
Write-Host "`n🛑 Parando warehouse_routing containers..." -ForegroundColor Yellow
docker stop warehouse_dashboard warehouse_api 2>$null
Write-Host "✅ Containers parados" -ForegroundColor Green

# ========== REMOVER CONTAINERS ==========
Write-Host "`n🗑️  Removendo containers..." -ForegroundColor Yellow
docker rm warehouse_dashboard warehouse_api 2>$null
Write-Host "✅ Containers removidos" -ForegroundColor Green

# ========== REMOVER IMAGENS ==========
Write-Host "`n🗑️  Removendo imagens warehouse_routing..." -ForegroundColor Yellow
docker rmi warehouse_routing-dashboard warehouse_routing-api 2>$null
Write-Host "✅ Imagens removidas" -ForegroundColor Green

# ========== REMOVER IMAGEM ECOMMERCE ANTIGA ==========
Write-Host "`n🗑️  Removendo imagem ecommerce-api antiga..." -ForegroundColor Yellow
docker rmi ecommerce-api:latest 2>$null
Write-Host "✅ Imagem ecommerce-api removida" -ForegroundColor Green

# ========== VERIFICAR LIMPEZA ==========
Write-Host "`n📋 Verificando containers restantes..." -ForegroundColor Yellow
docker ps -a
Write-Host "`n📋 Verificando imagens restantes..." -ForegroundColor Yellow
docker images

# ========== BUILD NOVO ==========
Write-Host "`n🐳 Building Docker image ecommerce-api:latest..." -ForegroundColor Yellow
docker build -t ecommerce-api:latest .

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Build bem-sucedido" -ForegroundColor Green
} else {
    Write-Host "❌ Build falhou" -ForegroundColor Red
    exit 1
}

# ========== TESTAR LOCALMENTE ==========
Write-Host "`n🧪 Iniciando container ecommerce-api..." -ForegroundColor Yellow
Write-Host "Aguarde alguns segundos para a aplicação iniciar..." -ForegroundColor Cyan

docker run -p 8080:8080 `
  -e ENVIRONMENT=development `
  -e DEBUG=true `
  ecommerce-api:latest

Write-Host "`n✅ Container iniciado na porta 8080" -ForegroundColor Green
Write-Host "📚 Acessar documentação em: http://localhost:8080/docs" -ForegroundColor Cyan