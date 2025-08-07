#!/usr/bin/env python3
"""
Script para recriar as tabelas do banco de dados SISU
Executa o arquivo SQL para criar tabelas e inserir cursos base.
"""

import os
import sys
import subprocess

def main():
    print("🔄 Recriando tabelas do banco de dados SISU...")
    
    # Configurações do banco
    db_config = {
        'host': os.environ.get('DB_HOST', 'localhost'),
        'port': os.environ.get('DB_PORT', '5432'),
        'database': os.environ.get('DB_DATABASE', 'basefeedback'),
        'user': os.environ.get('DB_USER', 'postgres')
    }
    
    # Arquivo SQL
    sql_file = './initdb/003.ticket2_tables.sql'
    
    # Verifica se o arquivo existe
    if not os.path.exists(sql_file):
        print(f"❌ Arquivo SQL não encontrado: {sql_file}")
        sys.exit(1)
    
    print(f"📋 Executando script SQL: {sql_file}")
    print(f"🔗 Conectando em: {db_config['host']}:{db_config['port']}/{db_config['database']} como {db_config['user']}")
    
    # Comando psql
    cmd = [
        'psql',
        '-h', db_config['host'],
        '-p', db_config['port'],
        '-d', db_config['database'],
        '-U', db_config['user'],
        '-f', sql_file
    ]
    
    try:
        # Executa o comando
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Tabelas criadas com sucesso!")
            print("")
            print("📊 Tabelas criadas:")
            print("   - edicoes (edições do SISU)")
            print("   - cursos (cursos de cada edição)")
            print("   - cursos_base (catálogo de 10 cursos disponíveis)")
            print("")
            print("🎓 Cursos base inseridos:")
            cursos = [
                "10001 - Engenharia da Computação",
                "10002 - Medicina",
                "10003 - Direito",
                "10004 - Administração",
                "10005 - Psicologia",
                "10006 - Engenharia Civil",
                "10007 - Arquitetura e Urbanismo",
                "10008 - Ciências Contábeis",
                "10009 - Enfermagem",
                "10010 - Sistemas de Informação"
            ]
            for curso in cursos:
                print(f"   {curso}")
            print("")
            print("🚀 Sistema pronto para uso!")
            
        else:
            print("❌ Erro ao executar o script SQL")
            print(f"Saída do erro: {result.stderr}")
            sys.exit(1)
            
    except FileNotFoundError:
        print("❌ Comando 'psql' não encontrado")
        print("💡 Verifique se o PostgreSQL está instalado e psql está no PATH")
        print(f"💡 Ou execute manualmente: psql -h {db_config['host']} -p {db_config['port']} -d {db_config['database']} -U {db_config['user']} -f {sql_file}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
