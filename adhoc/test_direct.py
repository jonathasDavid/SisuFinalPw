#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Teste direto com psycopg2
import psycopg2
import os

print("=== TESTE DIRETO DO BANCO ===")

try:
    # Conectar diretamente ao banco
    conn = psycopg2.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        database=os.getenv('DB_NAME', 'sisu_db'),
        user=os.getenv('DB_USER', 'sisu_user'),
        password=os.getenv('DB_PASS', 'sisu_pass'),
        port=int(os.getenv('DB_PORT', 5439))  # Porta que vimos no docker ps
    )
    
    cursor = conn.cursor()
    
    print("✅ Conexão estabelecida com sucesso!")
    
    # Verificar tabelas
    cursor.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public' 
        AND table_type = 'BASE TABLE'
        ORDER BY table_name
    """)
    
    tables = cursor.fetchall()
    table_names = [t[0] for t in tables]
    print(f"\nTabelas: {table_names}")
    
    # Verificar edições
    if 'edicoes' in table_names:
        cursor.execute("SELECT * FROM edicoes ORDER BY id")
        edicoes = cursor.fetchall()
        print(f"\nEdições ({len(edicoes)}):")
        for e in edicoes:
            print(f"  - ID {e[0]}: {e[1]} ({e[2]}.{e[3]})")
    
    # Verificar edicao_cursos
    if 'edicao_cursos' in table_names:
        cursor.execute("SELECT * FROM edicao_cursos ORDER BY id")
        edicao_cursos = cursor.fetchall()
        print(f"\nEdicao_Cursos ({len(edicao_cursos)}):")
        for ec in edicao_cursos:
            print(f"  - ID {ec[0]}: Edição {ec[1]}, Curso {ec[2]}, AC: {ec[3]}")
    else:
        print("\n❌ Tabela edicao_cursos não existe!")
    
    # Verificar cursos_base
    if 'cursos_base' in table_names:
        cursor.execute("SELECT * FROM cursos_base ORDER BY id LIMIT 5")
        cursos = cursor.fetchall()
        print(f"\nCursos_Base ({len(cursos)} primeiros):")
        for c in cursos:
            print(f"  - ID {c[0]}: {c[2]} (curso_id: {c[1]})")
    
    # Testar a consulta específica do view
    if 'edicao_cursos' in table_names and len(edicoes) > 0:
        edicao_id = edicoes[0][0]  # Primeiro ID
        print(f"\nTeste JOIN para edição {edicao_id}:")
        
        cursor.execute("""
            SELECT 
                ec.id as edicao_curso_id,
                ec.edicao_id,
                ec.curso_id,
                ec.vagas_ac,
                cb.nome as curso_nome
            FROM edicao_cursos ec
            LEFT JOIN cursos_base cb ON ec.curso_id = cb.curso_id
            WHERE ec.edicao_id = %s
        """, (edicao_id,))
        
        resultados = cursor.fetchall()
        print(f"Resultados ({len(resultados)}):")
        for r in resultados:
            print(f"  - EdicaoCurso {r[0]}: Curso {r[2]} ({r[4] or 'Nome não encontrado'}), AC: {r[3]}")
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"❌ Erro: {e}")
    import traceback
    traceback.print_exc()
