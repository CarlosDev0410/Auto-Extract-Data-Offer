# Build Script - Gera executável do Oferta Relâmpago
# Execute este script para criar o executável standalone

Write-Host "🚀 Iniciando build do executável..." -ForegroundColor Cyan
Write-Host ""

# Verifica se PyInstaller está instalado
Write-Host "📦 Verificando PyInstaller..." -ForegroundColor Yellow
pip show pyinstaller > $null 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "⚠️  PyInstaller não encontrado. Instalando..." -ForegroundColor Yellow
    pip install pyinstaller
}

Write-Host "✅ PyInstaller pronto!" -ForegroundColor Green
Write-Host ""

# Remove builds anteriores
Write-Host "🧹 Limpando builds anteriores..." -ForegroundColor Yellow
if (Test-Path "dist") { Remove-Item -Recurse -Force "dist" }
if (Test-Path "build") { Remove-Item -Recurse -Force "build" }
if (Test-Path "*.spec") { Remove-Item -Force "*.spec" }

Write-Host "✅ Limpeza concluída!" -ForegroundColor Green
Write-Host ""

# Cria o executável
Write-Host "🔨 Criando executável..." -ForegroundColor Cyan
Write-Host "   Este processo pode levar alguns minutos..." -ForegroundColor Gray
Write-Host ""

pyinstaller --clean `
    --onefile `
    --windowed `
    --name "OfertaRelampago" `
    --icon NONE `
    --add-data ".env.example;." `
    --add-data "query.sql;." `
    --hidden-import "openpyxl" `
    --hidden-import "psycopg2" `
    gui.py

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "✅ EXECUTÁVEL CRIADO COM SUCESSO!" -ForegroundColor Green
    Write-Host ""
    Write-Host "📁 Localização: dist\OfertaRelampago.exe" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "📝 Próximos passos:" -ForegroundColor Yellow
    Write-Host "   1. Crie uma pasta 'OfertaRelampago' para distribuir" -ForegroundColor White
    Write-Host "   2. Copie o executável: dist\OfertaRelampago.exe" -ForegroundColor White
    Write-Host "   3. Copie o arquivo .env com credenciais do banco" -ForegroundColor White
    Write-Host "   4. Distribua a pasta completa" -ForegroundColor White
    Write-Host ""
    
    # Abre a pasta dist
    Invoke-Item "dist"
} else {
    Write-Host ""
    Write-Host "❌ Erro ao criar executável!" -ForegroundColor Red
    Write-Host "   Verifique os logs acima para detalhes" -ForegroundColor Yellow
}
