-- Criação da tabela edicao_cursos que faltava
-- Esta tabela é necessária para relacionar edições com cursos e suas vagas

CREATE TABLE IF NOT EXISTS public.edicao_cursos
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

-- Índices para performance
CREATE INDEX IF NOT EXISTS idx_edicao_cursos_edicao_id ON public.edicao_cursos(edicao_id);
CREATE INDEX IF NOT EXISTS idx_edicao_cursos_curso_id ON public.edicao_cursos(curso_id);

-- Comentários para documentação
COMMENT ON TABLE public.edicao_cursos IS 'Tabela associativa: relaciona edições com cursos e suas vagas por modalidade';
COMMENT ON COLUMN public.edicao_cursos.edicao_id IS 'Chave estrangeira para edicoes';
COMMENT ON COLUMN public.edicao_cursos.curso_id IS 'ID do curso (referência aos cursos base)';
COMMENT ON COLUMN public.edicao_cursos.vagas_ac IS 'Vagas para Ampla Concorrência';
COMMENT ON COLUMN public.edicao_cursos.vagas_ppi_br IS 'Vagas para PPI + Escola Pública + Baixa Renda';
COMMENT ON COLUMN public.edicao_cursos.vagas_publica_br IS 'Vagas para Escola Pública + Baixa Renda';
COMMENT ON COLUMN public.edicao_cursos.vagas_ppi_publica IS 'Vagas para PPI + Escola Pública';
COMMENT ON COLUMN public.edicao_cursos.vagas_publica IS 'Vagas para Escola Pública';
COMMENT ON COLUMN public.edicao_cursos.vagas_deficientes IS 'Vagas para Pessoas com Deficiência';

-- Verificar estrutura criada
\d edicao_cursos;
