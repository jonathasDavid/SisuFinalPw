-- Criação das tabelas para demonstração do Ticket 2
-- Edições SISU (mestre) e Cursos (detalhe)

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
    edicao_id INTEGER NOT NULL REFERENCES public.edicoes(id) ON DELETE CASCADE,
    curso_id INTEGER NOT NULL,
    nome TEXT NOT NULL,
    vagas INTEGER NOT NULL CHECK (vagas > 0),
    nota_corte DECIMAL(6,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Índices para performance
CREATE INDEX IF NOT EXISTS idx_cursos_edicao_id ON public.cursos(edicao_id);
CREATE INDEX IF NOT EXISTS idx_cursos_curso_id ON public.cursos(curso_id);

-- Dados de exemplo para testes
INSERT INTO public.edicoes (nome, ano, semestre, data_inicio, data_fim) VALUES
('SISU 2025.1 - Primeiro Semestre', 2025, 1, '2025-01-15', '2025-06-30'),
('SISU 2025.2 - Segundo Semestre', 2025, 2, '2025-07-15', '2025-12-15')
ON CONFLICT DO NOTHING;

-- Cursos de exemplo para a primeira edição
INSERT INTO public.cursos (edicao_id, curso_id, nome, vagas, nota_corte) VALUES
(1, 12345, 'Engenharia da Computação', 40, 750.50),
(1, 12346, 'Medicina', 50, 890.25),
(1, 12347, 'Direito', 60, 680.75),
(2, 22345, 'Administração', 45, 620.30),
(2, 22346, 'Psicologia', 35, 700.80)
ON CONFLICT DO NOTHING;

-- Comentários para documentação
COMMENT ON TABLE public.edicoes IS 'Tabela mestre: Edições do SISU';
COMMENT ON TABLE public.cursos IS 'Tabela detalhe: Cursos de cada edição';
COMMENT ON COLUMN public.cursos.edicao_id IS 'Chave estrangeira para edicoes';
COMMENT ON COLUMN public.cursos.curso_id IS 'ID único do curso no sistema SISU';
