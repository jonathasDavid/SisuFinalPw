#!/bin/bash
# Script para recriar as tabelas do banco de dados SISU

echo "🔄 Recriando tabelas do banco de dados SISU..."

# Configurações do banco (ajuste conforme necessário)
DB_HOST=${DB_HOST:-localhost}
DB_PORT=${DB_PORT:-5432}
DB_NAME=${DB_DATABASE:-basefeedback}
DB_USER=${DB_USER:-postgres}

# Arquivo SQL a ser executado
SQL_FILE="./initdb/003.ticket2_tables.sql"

# Verifica se o arquivo SQL existe
if [ ! -f "$SQL_FILE" ]; then
    echo "❌ Arquivo SQL não encontrado: $SQL_FILE"
    exit 1
fi

echo "📋 Executando script SQL: $SQL_FILE"
echo "🔗 Conectando em: $DB_HOST:$DB_PORT/$DB_NAME como $DB_USER"

# Executa o SQL
psql -h "$DB_HOST" -p "$DB_PORT" -d "$DB_NAME" -U "$DB_USER" -f "$SQL_FILE"

if [ $? -eq 0 ]; then
    echo "✅ Tabelas criadas com sucesso!"
    echo ""
    echo "📊 Tabelas criadas:"
    echo "   - edicoes (edições do SISU)"
    echo "   - cursos (cursos de cada edição)"
    echo "   - cursos_base (catálogo de 10 cursos disponíveis)"
    echo ""
    echo "🎓 Cursos base inseridos:"
    echo "   10001 - Engenharia da Computação"
    echo "   10002 - Medicina"
    echo "   10003 - Direito"
    echo "   10004 - Administração"
    echo "   10005 - Psicologia"
    echo "   10006 - Engenharia Civil"
    echo "   10007 - Arquitetura e Urbanismo"
    echo "   10008 - Ciências Contábeis"
    echo "   10009 - Enfermagem"
    echo "   10010 - Sistemas de Informação"
    echo ""
    echo "🚀 Sistema pronto para uso!"
else
    echo "❌ Erro ao executar o script SQL"
    exit 1
fi
