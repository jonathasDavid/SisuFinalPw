#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Teste manual de inserção de dados
import subprocess
import sys

print("=== VERIFICAÇÃO MANUAL DO BANCO ===")

# Comando para conectar ao PostgreSQL via docker
docker_cmd = [
    "docker", "exec", "-it", "adhoc-db-1", 
    "psql", "-U", "sisu_user", "-d", "sisu_db", "-c"
]

def run_sql(query):
    try:
        result = subprocess.run(
            docker_cmd + [query], 
            capture_output=True, 
            text=True, 
            timeout=10
        )
        print(f"Query: {query}")
        print(f"Output: {result.stdout}")
        if result.stderr:
            print(f"Error: {result.stderr}")
        print("-" * 50)
        return result.stdout
    except Exception as e:
        print(f"Erro executando query: {e}")
        return None

# Teste 1: Verificar tabelas
print("1. VERIFICAR TABELAS:")
run_sql("\\dt")

# Teste 2: Contar dados
print("2. CONTAR DADOS:")
run_sql("SELECT 'edicoes' as tabela, count(*) FROM edicoes UNION ALL SELECT 'edicao_cursos', count(*) FROM edicao_cursos UNION ALL SELECT 'cursos_base', count(*) FROM cursos_base;")

# Teste 3: Dados específicos
print("3. DADOS EDICOES:")
run_sql("SELECT id, nome FROM edicoes LIMIT 5;")

print("4. DADOS EDICAO_CURSOS:")
run_sql("SELECT id, edicao_id, curso_id, vagas_ac FROM edicao_cursos LIMIT 5;")

print("5. DADOS CURSOS_BASE:")
run_sql("SELECT id, curso_id, nome FROM cursos_base LIMIT 5;")

# Teste 4: JOIN específico para verificar associação
print("6. TESTE JOIN:")
run_sql("""
SELECT 
    e.id as edicao_id,
    e.nome as edicao_nome,
    ec.id as edicao_curso_id,
    ec.curso_id,
    cb.nome as curso_nome,
    ec.vagas_ac
FROM edicoes e
LEFT JOIN edicao_cursos ec ON e.id = ec.edicao_id
LEFT JOIN cursos_base cb ON ec.curso_id = cb.curso_id
WHERE e.id = 1
LIMIT 10;
""")
