#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script de debug para verificar problema na visualização de cursos
"""

import sqlite3
import os

def verificar_banco_dados():
    """
    Verifica se há dados nas tabelas e qual é a estrutura
    """
    print("🔍 VERIFICANDO BANCO DE DADOS")
    print("=" * 60)
    
    # Procurar arquivo de banco de dados
    possíveis_caminhos = [
        'database.db',
        'db.sqlite3',
        'sisu.db',
        '../database.db',
        'app/database.db'
    ]
    
    db_path = None
    for caminho in possíveis_caminhos:
        if os.path.exists(caminho):
            db_path = caminho
            break
    
    if not db_path:
        print("❌ Arquivo de banco de dados não encontrado")
        print(f"Caminhos verificados: {possíveis_caminhos}")
        return
    
    print(f"✅ Banco encontrado: {db_path}")
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Verificar estrutura das tabelas
        print("\n📋 ESTRUTURA DAS TABELAS:")
        
        # Listar todas as tabelas
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tabelas = cursor.fetchall()
        print(f"Tabelas encontradas: {[t[0] for t in tabelas]}")
        
        # Verificar estrutura da tabela edicoes
        if ('edicoes',) in tabelas:
            print("\n🏢 TABELA: edicoes")
            cursor.execute("PRAGMA table_info(edicoes);")
            colunas = cursor.fetchall()
            for coluna in colunas:
                print(f"  - {coluna[1]} ({coluna[2]})")
            
            # Contar registros
            cursor.execute("SELECT COUNT(*) FROM edicoes;")
            count = cursor.fetchone()[0]
            print(f"  📊 Total de registros: {count}")
            
            if count > 0:
                cursor.execute("SELECT id, nome, ano, semestre FROM edicoes;")
                edicoes = cursor.fetchall()
                print("  📝 Edições existentes:")
                for edicao in edicoes:
                    print(f"    - ID: {edicao[0]}, Nome: {edicao[1]}, Período: {edicao[2]}.{edicao[3]}")
        
        # Verificar estrutura da tabela cursos
        if ('cursos',) in tabelas:
            print("\n🎓 TABELA: cursos")
            cursor.execute("PRAGMA table_info(cursos);")
            colunas = cursor.fetchall()
            for coluna in colunas:
                print(f"  - {coluna[1]} ({coluna[2]})")
            
            cursor.execute("SELECT COUNT(*) FROM cursos;")
            count = cursor.fetchone()[0]
            print(f"  📊 Total de registros: {count}")
            
            if count > 0:
                cursor.execute("SELECT id, nome FROM cursos LIMIT 10;")
                cursos = cursor.fetchall()
                print("  📝 Cursos existentes (primeiros 10):")
                for curso in cursos:
                    print(f"    - ID: {curso[0]}, Nome: {curso[1]}")
        
        # Verificar estrutura da tabela edicao_cursos (crítica!)
        if ('edicao_cursos',) in tabelas:
            print("\n🔗 TABELA: edicao_cursos (CRÍTICA)")
            cursor.execute("PRAGMA table_info(edicao_cursos);")
            colunas = cursor.fetchall()
            for coluna in colunas:
                print(f"  - {coluna[1]} ({coluna[2]})")
            
            cursor.execute("SELECT COUNT(*) FROM edicao_cursos;")
            count = cursor.fetchone()[0]
            print(f"  📊 Total de registros: {count}")
            
            if count > 0:
                cursor.execute("SELECT * FROM edicao_cursos;")
                edicao_cursos = cursor.fetchall()
                print("  📝 Associações existentes:")
                for ec in edicao_cursos:
                    print(f"    - {ec}")
            else:
                print("  ⚠️  PROBLEMA: Nenhuma associação encontrada!")
        else:
            print("\n❌ PROBLEMA CRÍTICO: Tabela 'edicao_cursos' não existe!")
        
        # Verificar outras variações do nome da tabela
        tabelas_variantes = ['edicaocurso', 'edicao_curso', 'edicoes_cursos']
        for variante in tabelas_variantes:
            if (variante,) in tabelas:
                print(f"\n🔍 TABELA ALTERNATIVA ENCONTRADA: {variante}")
                cursor.execute(f"PRAGMA table_info({variante});")
                colunas = cursor.fetchall()
                for coluna in colunas:
                    print(f"  - {coluna[1]} ({coluna[2]})")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Erro ao acessar banco: {e}")
        import traceback
        traceback.print_exc()

def verificar_logs_aplicacao():
    """
    Verifica se há logs recentes da aplicação
    """
    print("\n\n📄 VERIFICANDO LOGS DA APLICAÇÃO")
    print("=" * 60)
    
    # Se a aplicação estiver rodando, deveria haver logs
    print("💡 Para ver logs em tempo real:")
    print("1. Execute a aplicação: python app/index.py")
    print("2. Acesse: http://localhost:5000/app/edicao/create")
    print("3. Crie uma edição com cursos")
    print("4. Observe as mensagens de debug no terminal")
    print("5. Acesse: http://localhost:5000/app/edicao/view/[ID]")

def sugerir_solucoes():
    """
    Sugere soluções baseadas nos problemas comuns
    """
    print("\n\n🔧 POSSÍVEIS SOLUÇÕES")
    print("=" * 60)
    
    solucoes = [
        {
            'problema': 'Tabela edicao_cursos não existe',
            'solucao': 'Execute o script de criação de tabelas: recreate_tables.py'
        },
        {
            'problema': 'Tabela existe mas está vazia',
            'solucao': 'Os dados não estão sendo salvos. Verifique logs do save_with_cursos_selecionados()'
        },
        {
            'problema': 'Dados existem mas não aparecem',
            'solucao': 'Problema na query do controller. Verifique o método view()'
        },
        {
            'problema': 'Erro de importação orator',
            'solucao': 'Execute: pip install -r requirements.txt'
        }
    ]
    
    for i, sol in enumerate(solucoes, 1):
        print(f"{i}. {sol['problema']}")
        print(f"   Solução: {sol['solucao']}")
        print()

if __name__ == "__main__":
    print("🔍 DEBUG: PROBLEMA NA VISUALIZAÇÃO DE CURSOS")
    print("🎯 Investigando por que cursos não aparecem na view")
    print("=" * 80)
    
    verificar_banco_dados()
    verificar_logs_aplicacao()
    sugerir_solucoes()
    
    print("=" * 80)
    print("✅ DEBUG CONCLUÍDO!")
    print("🔧 Use as informações acima para identificar o problema.")
    print("=" * 80)
