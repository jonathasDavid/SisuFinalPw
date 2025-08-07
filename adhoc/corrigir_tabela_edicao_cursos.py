#!/usr/bin/env python3
"""
Script para corrigir o problema da tabela edicao_cursos faltante
Este script cria a tabela necessária para o funcionamento da nova funcionalidade
"""

import os
import sys
import subprocess
import tempfile

def criar_sql_correcao():
    """
    Cria o SQL de correção para adicionar a tabela edicao_cursos
    """
    sql_content = """
-- Correção: Criar tabela edicao_cursos que estava faltando
-- Esta tabela é necessária para a nova funcionalidade de distribuição automática de vagas

-- Verificar se a tabela já existe
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM information_schema.tables 
                   WHERE table_name = 'edicao_cursos' AND table_schema = 'public') THEN
        
        -- Criar a tabela edicao_cursos
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

        -- Criar índices para performance
        CREATE INDEX idx_edicao_cursos_edicao_id ON public.edicao_cursos(edicao_id);
        CREATE INDEX idx_edicao_cursos_curso_id ON public.edicao_cursos(curso_id);
        
        -- Adicionar comentários
        COMMENT ON TABLE public.edicao_cursos IS 'Tabela associativa: relaciona edições com cursos e suas vagas por modalidade';
        COMMENT ON COLUMN public.edicao_cursos.edicao_id IS 'Chave estrangeira para edicoes';
        COMMENT ON COLUMN public.edicao_cursos.curso_id IS 'ID do curso (referência aos cursos_base)';
        COMMENT ON COLUMN public.edicao_cursos.vagas_ac IS 'Vagas para Ampla Concorrência';
        COMMENT ON COLUMN public.edicao_cursos.vagas_ppi_br IS 'Vagas para PPI + Escola Pública + Baixa Renda';
        COMMENT ON COLUMN public.edicao_cursos.vagas_publica_br IS 'Vagas para Escola Pública + Baixa Renda';
        COMMENT ON COLUMN public.edicao_cursos.vagas_ppi_publica IS 'Vagas para PPI + Escola Pública';
        COMMENT ON COLUMN public.edicao_cursos.vagas_publica IS 'Vagas para Escola Pública';
        COMMENT ON COLUMN public.edicao_cursos.vagas_deficientes IS 'Vagas para Pessoas com Deficiência';
        
        RAISE NOTICE 'Tabela edicao_cursos criada com sucesso!';
    ELSE
        RAISE NOTICE 'Tabela edicao_cursos já existe.';
    END IF;
    
    -- Verificar se a tabela foi criada corretamente
    SELECT 
        table_name,
        column_name,
        data_type
    FROM information_schema.columns 
    WHERE table_name = 'edicao_cursos' 
    ORDER BY ordinal_position;
    
END $$;

-- Mostrar estrutura da tabela criada
\\d edicao_cursos;
"""
    return sql_content

def main():
    print("🔧 CORREÇÃO: Criando tabela edicao_cursos faltante")
    print("=" * 60)
    
    # Configurações do banco (usar as mesmas do docker-compose)
    db_config = {
        'host': os.environ.get('DB_HOST', 'localhost'),
        'port': os.environ.get('DB_PORT', '5439'),  # Porta do docker-compose
        'database': os.environ.get('APP_DB', 'basefeedback'),
        'user': os.environ.get('APP_USER', 'app')
    }
    
    print(f"🔗 Conectando em: {db_config['host']}:{db_config['port']}/{db_config['database']} como {db_config['user']}")
    
    # Criar arquivo SQL temporário
    sql_content = criar_sql_correcao()
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.sql', delete=False) as temp_file:
        temp_file.write(sql_content)
        temp_sql_file = temp_file.name
    
    try:
        # Comando psql
        cmd = [
            'psql',
            '-h', db_config['host'],
            '-p', db_config['port'],
            '-d', db_config['database'],
            '-U', db_config['user'],
            '-f', temp_sql_file
        ]
        
        print("⚙️  Executando correção no banco de dados...")
        
        # Executa o comando
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Tabela edicao_cursos criada com sucesso!")
            print("")
            print("📋 Estrutura da tabela:")
            print("   - id (SERIAL PRIMARY KEY)")
            print("   - edicao_id (INTEGER, FK para edicoes)")
            print("   - curso_id (INTEGER, ref. cursos_base)")
            print("   - vagas_ac (INTEGER, Ampla Concorrência)")
            print("   - vagas_ppi_br (INTEGER, PPI + EP + BR)")
            print("   - vagas_publica_br (INTEGER, EP + BR)")
            print("   - vagas_ppi_publica (INTEGER, PPI + EP)")
            print("   - vagas_publica (INTEGER, EP)")
            print("   - vagas_deficientes (INTEGER, PcD)")
            print("")
            print("🎉 Problema corrigido! Agora você pode:")
            print("   1. Criar edições com cursos")
            print("   2. Visualizar cursos nas edições")
            print("   3. Usar a distribuição automática de vagas")
            
            # Mostrar a saída do comando
            if result.stdout:
                print("\\n📄 Saída do comando:")
                print(result.stdout)
                
        else:
            print("❌ Erro ao executar a correção")
            print(f"Código de saída: {result.returncode}")
            if result.stderr:
                print(f"Erro: {result.stderr}")
            if result.stdout:
                print(f"Saída: {result.stdout}")
            
    except FileNotFoundError:
        print("❌ Comando 'psql' não encontrado")
        print("")
        print("💡 Soluções alternativas:")
        print("1. Instalar PostgreSQL client: apt-get install postgresql-client")
        print("2. Conectar via Docker:")
        print(f"   docker exec -it $(docker ps -qf name=db) psql -U {db_config['user']} -d {db_config['database']}")
        print("3. Usar ferramenta gráfica (pgAdmin, DBeaver)")
        print("")
        print("📄 SQL para executar manualmente:")
        print("-" * 40)
        print(sql_content)
        
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        
    finally:
        # Limpar arquivo temporário
        try:
            os.unlink(temp_sql_file)
        except:
            pass

if __name__ == '__main__':
    main()
