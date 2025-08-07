-- Criação das tabelas para demonstração do Ticket 2
-- Edições SISU (mestre) e Cursos (detalhe)

-- Drop das tabelas se existirem para recriar
DROP TABLE IF EXISTS public.cursos CASCADE;
DROP TABLE IF EXISTS public.edicoes CASCADE;

-- Tabela de edições (mestre)
CREATE TABLE IF NOT EXISTS public.edicoes
(
    id SERIAL PRIMARY KEY,
    nome TEXT NOT NULL,
    ano INTEGER NOT NULL,
    semestre INTEGER NOT NULL CHECK (semestre IN (1, 2)),
    data_inicio DATE,
    data_fim DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de cursos (detalhe)
CREATE TABLE IF NOT EXISTS public.cursos
(
    id SERIAL PRIMARY KEY,
    edicao_id INTEGER REFERENCES public.edicoes(id) ON DELETE CASCADE,
    curso_id INTEGER NOT NULL,
    nome TEXT NOT NULL,
    vagas INTEGER NOT NULL CHECK (vagas > 0),
    nota_corte DECIMAL(6,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de cursos base (catálogo de cursos disponíveis)
CREATE TABLE IF NOT EXISTS public.cursos_base
(
    id SERIAL PRIMARY KEY,
    curso_id INTEGER UNIQUE NOT NULL,
    nome TEXT NOT NULL,
    area TEXT,
    modalidade TEXT DEFAULT 'Presencial',
    duracao_semestres INTEGER DEFAULT 8,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Índices para performance
CREATE INDEX IF NOT EXISTS idx_cursos_edicao_id ON public.cursos(edicao_id);
CREATE INDEX IF NOT EXISTS idx_cursos_curso_id ON public.cursos(curso_id);
CREATE INDEX IF NOT EXISTS idx_cursos_base_curso_id ON public.cursos_base(curso_id);

-- Inserir cursos base (catálogo de 10 cursos para seleção)
INSERT INTO public.cursos_base (curso_id, nome, area, modalidade, duracao_semestres) VALUES
(10001, 'Engenharia da Computação', 'Exatas', 'Presencial', 10),
(10002, 'Medicina', 'Saúde', 'Presencial', 12),
(10003, 'Direito', 'Humanas', 'Presencial', 10),
(10004, 'Administração', 'Negócios', 'Presencial', 8),
(10005, 'Psicologia', 'Humanas', 'Presencial', 10),
(10006, 'Engenharia Civil', 'Exatas', 'Presencial', 10),
(10007, 'Arquitetura e Urbanismo', 'Exatas', 'Presencial', 10),
(10008, 'Ciências Contábeis', 'Negócios', 'Presencial', 8),
(10009, 'Enfermagem', 'Saúde', 'Presencial', 8),
(10010, 'Sistemas de Informação', 'Exatas', 'Presencial', 8);

-- Dados de exemplo para testes (edições já criadas)
INSERT INTO public.edicoes (nome, ano, semestre, data_inicio, data_fim) VALUES
('SISU 2025.1 - Primeiro Semestre', 2025, 1, '2025-01-15', '2025-06-30'),
('SISU 2025.2 - Segundo Semestre', 2025, 2, '2025-07-15', '2025-12-15')
ON CONFLICT DO NOTHING;

-- Exemplos de cursos associados a edições (para demonstração)
INSERT INTO public.cursos (edicao_id, curso_id, nome, vagas, nota_corte) VALUES
(1, 10001, 'Engenharia da Computação', 40, 750.50),
(1, 10002, 'Medicina', 50, 890.25),
(1, 10003, 'Direito', 60, 680.75),
(2, 10004, 'Administração', 45, 620.30),
(2, 10005, 'Psicologia', 35, 700.80)
ON CONFLICT DO NOTHING;

-- Comentários para documentação
COMMENT ON TABLE public.edicoes IS 'Tabela mestre: Edições do SISU';
COMMENT ON TABLE public.cursos IS 'Tabela detalhe: Cursos de cada edição específica';
COMMENT ON TABLE public.cursos_base IS 'Catálogo de cursos disponíveis para seleção';
COMMENT ON COLUMN public.cursos.edicao_id IS 'Chave estrangeira para edicoes';
COMMENT ON COLUMN public.cursos.curso_id IS 'ID único do curso no sistema SISU';
COMMENT ON COLUMN public.cursos_base.curso_id IS 'ID único do curso no catálogo';

-- View para facilitar consultas de cursos disponíveis
CREATE OR REPLACE VIEW public.view_cursos_disponiveis AS
SELECT 
    cb.curso_id,
    cb.nome,
    cb.area,
    cb.modalidade,
    cb.duracao_semestres,
    COUNT(c.id) as total_edicoes
FROM public.cursos_base cb
LEFT JOIN public.cursos c ON cb.curso_id = c.curso_id
GROUP BY cb.curso_id, cb.nome, cb.area, cb.modalidade, cb.duracao_semestres
ORDER BY cb.nome;
