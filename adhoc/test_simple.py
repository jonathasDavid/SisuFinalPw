#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Teste simplificado para verificar dados no banco
import os
import sys

# Adicionar o diretório app ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

# Configurar o banco de dados como a aplicação faz
from orator import DatabaseManager, Model

# Configuração do banco
DATABASES = {
    'default': 'postgres',
    'postgres': {
        'driver': 'postgres',
        'host': os.getenv('DB_HOST', 'localhost'),
        'database': os.getenv('DB_NAME', 'sisu_db'),
        'user': os.getenv('DB_USER', 'sisu_user'),
        'password': os.getenv('DB_PASS', 'sisu_pass'),
        'port': int(os.getenv('DB_PORT', 5432)),
        'prefix': '',
        'options': {
            'charset': 'utf8',
            'use_unicode': True,
        }
    }
}

# Inicializar ORM
db = DatabaseManager(DATABASES)
Model.set_connection_resolver(db)

print("=== TESTE SIMPLES DE DADOS ===")

try:
    # Teste 1: Verificar tabelas
    print("\n1. TESTE DE CONEXÃO:")
    tables = db.table('information_schema.tables').where('table_schema', 'public').where('table_type', 'BASE TABLE').get()
    table_names = [t.table_name for t in tables]
    print(f"Tabelas encontradas: {table_names}")
    
    # Teste 2: Dados da tabela edicoes
    print("\n2. EDIÇÕES:")
    edicoes = db.table('edicoes').get()
    print(f"Total de edições: {len(edicoes)}")
    for e in edicoes:
        print(f"  - ID {e.id}: {e.nome}")
    
    # Teste 3: Dados da tabela edicao_cursos
    print("\n3. EDICAO_CURSOS:")
    if 'edicao_cursos' in table_names:
        edicao_cursos = db.table('edicao_cursos').get()
        print(f"Total de edicao_cursos: {len(edicao_cursos)}")
        for ec in edicao_cursos:
            print(f"  - ID {ec.id}: Edição {ec.edicao_id}, Curso {ec.curso_id}, AC: {ec.vagas_ac}")
    else:
        print("❌ Tabela edicao_cursos não encontrada!")
    
    # Teste 4: Dados da tabela cursos_base
    print("\n4. CURSOS_BASE:")
    if 'cursos_base' in table_names:
        cursos = db.table('cursos_base').get()
        print(f"Total de cursos_base: {len(cursos)}")
        for c in cursos[:3]:
            print(f"  - ID {c.id}: {c.nome} (curso_id: {c.curso_id})")
    else:
        print("❌ Tabela cursos_base não encontrada!")
    
    # Teste 5: Simular a consulta do view controller
    print("\n5. TESTE DA LÓGICA DO VIEW (Edição ID 1):")
    if 'edicao_cursos' in table_names and len(edicoes) > 0:
        edicao_id = edicoes[0].id
        
        # Buscar EdicaoCursos da edição
        edicao_cursos_query = db.table('edicao_cursos').where('edicao_id', edicao_id).get()
        print(f"EdicaoCursos encontrados para edição {edicao_id}: {len(edicao_cursos_query)}")
        
        for ec in edicao_cursos_query:
            print(f"  - EdicaoCurso ID: {ec.id}, Curso ID: {ec.curso_id}")
            
            # Buscar curso na tabela cursos_base
            if 'cursos_base' in table_names:
                curso = db.table('cursos_base').where('curso_id', ec.curso_id).first()
                if curso:
                    print(f"    ✅ Curso encontrado: {curso.nome}")
                else:
                    print(f"    ❌ Curso ID {ec.curso_id} não encontrado em cursos_base")
    else:
        print("❌ Não é possível testar - dados insuficientes")
        
except Exception as e:
    print(f"❌ Erro: {e}")
    import traceback
    traceback.print_exc()
