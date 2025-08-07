-- Script para criar a tabela edicao_cursos (associação entre edições e cursos com vagas)
-- Este script deve ser executado após o 003.ticket2_tables.sql

DO $$
BEGIN
    -- Verificar se a tabela edicao_cursos já existe
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
        COMMENT ON TABLE public.edicao_cursos IS 'Tabela associativa: relaciona edições com cursos e suas vagas por modalidade (nova estrutura)';
        COMMENT ON COLUMN public.edicao_cursos.edicao_id IS 'Chave estrangeira para edicoes';
        COMMENT ON COLUMN public.edicao_cursos.curso_id IS 'ID do curso (referência aos cursos base)';
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
END $$;
