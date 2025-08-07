#!/usr/bin/env python3
"""
Script para corrigir a tabela edicao_cursos via Docker
Usa o container do PostgreSQL para executar o SQL
"""

import subprocess
import os

def main():
    print("🐳 CORREÇÃO VIA DOCKER: Criando tabela edicao_cursos")
    print("=" * 60)
    
    sql_correcao = """
DO \\$\\$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM information_schema.tables 
                   WHERE table_name = 'edicao_cursos' AND table_schema = 'public') THEN
        
        CREATE TABLE public.edicao_cursos
        (
            id SERIAL PRIMARY KEY,
            edicao_id INTEGER NOT NULL REFERENCES public.edicoes(id) ON DELETE CASCADE,
            curso_id INTEGER NOT NULL,
            vagas_ac INTEGER DEFAULT 0 CHECK (vagas_ac >= 0),
            vagas_ppi_br INTEGER DEFAULT 0 CHECK (vagas_ppi_br >= 0),
            vagas_publica_br INTEGER DEFAULT 0 CHECK (vagas_publica_br >= 0),
            vagas_ppi_publica INTEGER DEFAULT 0 CHECK (vagas_ppi_publica >= 0),
            vagas_publica INTEGER DEFAULT 0 CHECK (vagas_publica >= 0),
            vagas_deficientes INTEGER DEFAULT 0 CHECK (vagas_deficientes >= 0),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE INDEX idx_edicao_cursos_edicao_id ON public.edicao_cursos(edicao_id);
        CREATE INDEX idx_edicao_cursos_curso_id ON public.edicao_cursos(curso_id);
        
        RAISE NOTICE 'Tabela edicao_cursos criada com sucesso!';
    ELSE
        RAISE NOTICE 'Tabela edicao_cursos já existe.';
    END IF;
END \\$\\$;
"""
    
    try:
        # Comando para executar via Docker
        cmd = [
            'docker', 'exec', '-i',
            'adhoc-db-1',  # Nome padrão do container
            'psql', '-U', 'app', '-d', 'basefeedback',
            '-c', sql_correcao
        ]
        
        print("🔄 Executando correção via Docker...")
        print(f"📋 Container: adhoc-db-1")
        print(f"👤 Usuário: app")
        print(f"🗄️  Database: basefeedback")
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Correção executada com sucesso!")
            print("")
            if result.stdout:
                print("📄 Saída:")
                print(result.stdout)
            
            # Verificar se a tabela foi criada
            cmd_verify = [
                'docker', 'exec', '-i',
                'adhoc-db-1',
                'psql', '-U', 'app', '-d', 'basefeedback',
                '-c', "\\d edicao_cursos"
            ]
            
            verify_result = subprocess.run(cmd_verify, capture_output=True, text=True)
            if verify_result.returncode == 0:
                print("📋 Estrutura da tabela criada:")
                print(verify_result.stdout)
            
            print("")
            print("🎉 Problema corrigido! A aplicação agora deve funcionar.")
            
        else:
            print("❌ Erro ao executar a correção")
            print(f"Código de saída: {result.returncode}")
            if result.stderr:
                print(f"Erro: {result.stderr}")
            if result.stdout:
                print(f"Saída: {result.stdout}")
                
            print("")
            print("💡 Possíveis soluções:")
            print("1. Verificar se o Docker está rodando")
            print("2. Verificar se o container está ativo: docker ps")
            print("3. O nome do container pode ser diferente. Use: docker ps | grep postgres")
            
    except FileNotFoundError:
        print("❌ Docker não encontrado")
        print("💡 Instale o Docker ou use o script corrigir_tabela_edicao_cursos.py")
        
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")

if __name__ == '__main__':
    main()
