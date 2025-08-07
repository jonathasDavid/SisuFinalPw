#!/usr/bin/env python3
"""
Script para recriar as tabelas do banco de dados SISU via Docker
Executa o SQL dentro do container do banco.
"""

import os
import sys
import subprocess
import time

def main():
    print("🔄 Recriando tabelas do banco de dados SISU...")
    
    # Aguarda um pouco para o banco subir completamente
    print("⏳ Aguardando banco de dados subir...")
    time.sleep(3)
    
    # Arquivo SQL
    sql_file = './initdb/003.ticket2_tables.sql'
    
    # Verifica se o arquivo existe
    if not os.path.exists(sql_file):
        print(f"❌ Arquivo SQL não encontrado: {sql_file}")
        sys.exit(1)
    
    print(f"📋 Executando script SQL: {sql_file}")
    print(f"🐳 Usando Docker container: adhoc-db-1")
    
    # Comando docker exec para executar dentro do container
    cmd = [
        'docker', 'exec', '-i', 'adhoc-db-1',
        'psql', '-U', 'app', '-d', 'basefeedback'
    ]
    
    try:
        # Lê o conteúdo do arquivo SQL
        with open(sql_file, 'r', encoding='utf-8') as f:
            sql_content = f.read()
        
        # Executa o comando passando o SQL via stdin
        result = subprocess.run(cmd, input=sql_content, capture_output=True, text=True)
        
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
            print("🌐 Acesse: http://localhost:1080")
            
        else:
            print("❌ Erro ao executar o script SQL")
            print(f"Saída: {result.stdout}")
            print(f"Erro: {result.stderr}")
            sys.exit(1)
            
    except FileNotFoundError:
        print("❌ Comando 'docker' não encontrado")
        print("💡 Verifique se o Docker está instalado e rodando")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
