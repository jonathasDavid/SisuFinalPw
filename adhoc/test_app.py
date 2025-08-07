#!/usr/bin/env python3
"""
Script de teste para verificar se a aplicação está funcionando
"""

import sys
import os
sys.path.append('./app')

try:
    print("=== TESTE DE CONECTIVIDADE ===")
    
    # Teste 1: Import básico
    print("1. Testando imports...")
    from orator import DatabaseManager, Model
    print("✅ Orator importado")
    
    # Teste 2: Configuração do banco
    print("2. Testando configuração do banco...")
    config = {
        'default': 'postgresql',
        'databases': {
            'postgresql': {
                'driver': 'postgresql',
                'host': os.environ.get('DB_HOST', 'db'),
                'database': os.environ.get('DB_DATABASE', 'basefeedback'),
                'user': os.environ.get('DB_USER', 'app'),
                'password': os.environ.get('DB_PASSWORD', 'app2025'),
                'prefix': ''
            }
        }
    }
    
    db = DatabaseManager(config)
    Model.set_connection_resolver(db)
    print("✅ Banco configurado")
    
    # Teste 3: Conectividade
    print("3. Testando conectividade...")
    from models.Curso import Curso
    cursos = Curso.todos_cursos()
    print(f"✅ {len(cursos)} cursos encontrados")
    
    # Teste 4: Teste de aplicação web simples
    print("4. Testando servidor web...")
    from wsgiref import simple_server
    
    def test_app(environ, start_response):
        status = '200 OK'
        headers = [('Content-type', 'text/plain')]
        start_response(status, headers)
        return [b'Hello World - App funcionando!']
    
    print("Iniciando servidor na porta 8000...")
    w_s = simple_server.make_server(
        host="",
        port=8000,
        app=test_app
    )
    
    print("✅ Servidor iniciado com sucesso!")
    print("Servidor rodando... (Ctrl+C para parar)")
    w_s.serve_forever()
    
except Exception as e:
    print(f"❌ ERRO: {e}")
    import traceback
    traceback.print_exc()
