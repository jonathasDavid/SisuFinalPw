# Script PowerShell para recriar as tabelas do banco de dados SISU

Write-Host "🔄 Recriando tabelas do banco de dados SISU..." -ForegroundColor Cyan

# Configurações do banco (ajuste conforme necessário)
$DB_HOST = if ($env:DB_HOST) { $env:DB_HOST } else { "localhost" }
$DB_PORT = if ($env:DB_PORT) { $env:DB_PORT } else { "5432" }
$DB_NAME = if ($env:DB_DATABASE) { $env:DB_DATABASE } else { "basefeedback" }
$DB_USER = if ($env:DB_USER) { $env:DB_USER } else { "postgres" }

# Arquivo SQL a ser executado
$SQL_FILE = "./initdb/003.ticket2_tables.sql"

# Verifica se o arquivo SQL existe
if (-not (Test-Path $SQL_FILE)) {
    Write-Host "❌ Arquivo SQL não encontrado: $SQL_FILE" -ForegroundColor Red
    exit 1
}

Write-Host "📋 Executando script SQL: $SQL_FILE" -ForegroundColor Yellow
Write-Host "🔗 Conectando em: $DB_HOST:$DB_PORT/$DB_NAME como $DB_USER" -ForegroundColor Yellow

try {
    # Executa o SQL usando psql (certifique-se de que está no PATH)
    $command = "psql -h `"$DB_HOST`" -p `"$DB_PORT`" -d `"$DB_NAME`" -U `"$DB_USER`" -f `"$SQL_FILE`""
    Invoke-Expression $command
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Tabelas criadas com sucesso!" -ForegroundColor Green
        Write-Host ""
        Write-Host "📊 Tabelas criadas:" -ForegroundColor Green
        Write-Host "   - edicoes (edições do SISU)"
        Write-Host "   - cursos (cursos de cada edição)"
        Write-Host "   - cursos_base (catálogo de 10 cursos disponíveis)"
        Write-Host ""
        Write-Host "🎓 Cursos base inseridos:" -ForegroundColor Green
        Write-Host "   10001 - Engenharia da Computação"
        Write-Host "   10002 - Medicina"
        Write-Host "   10003 - Direito"
        Write-Host "   10004 - Administração"
        Write-Host "   10005 - Psicologia"
        Write-Host "   10006 - Engenharia Civil"
        Write-Host "   10007 - Arquitetura e Urbanismo"
        Write-Host "   10008 - Ciências Contábeis"
        Write-Host "   10009 - Enfermagem"
        Write-Host "   10010 - Sistemas de Informação"
        Write-Host ""
        Write-Host "🚀 Sistema pronto para uso!" -ForegroundColor Green
    } else {
        Write-Host "❌ Erro ao executar o script SQL (Exit Code: $LASTEXITCODE)" -ForegroundColor Red
        exit 1
    }
}
catch {
    Write-Host "❌ Erro ao executar psql: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "💡 Verifique se o PostgreSQL está instalado e psql está no PATH" -ForegroundColor Yellow
    Write-Host "💡 Ou execute manualmente: psql -h $DB_HOST -p $DB_PORT -d $DB_NAME -U $DB_USER -f $SQL_FILE" -ForegroundColor Yellow
    exit 1
}
