-- Criar tabela edicao_cursos se não existir
CREATE TABLE IF NOT EXISTS edicao_cursos (
    id SERIAL PRIMARY KEY,
    edicao_id INTEGER NOT NULL,
    curso_id INTEGER NOT NULL,
    vagas_ac INTEGER DEFAULT 0,
    vagas_l1 INTEGER DEFAULT 0,
    vagas_l2 INTEGER DEFAULT 0,
    vagas_l5 INTEGER DEFAULT 0,
    vagas_l6 INTEGER DEFAULT 0,
    vagas_l9 INTEGER DEFAULT 0,
    vagas_l10 INTEGER DEFAULT 0,
    vagas_l13 INTEGER DEFAULT 0,
    vagas_l14 INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (edicao_id) REFERENCES edicoes(id) ON DELETE CASCADE,
    FOREIGN KEY (curso_id) REFERENCES cursos_base(id) ON DELETE CASCADE,
    UNIQUE(edicao_id, curso_id)
);

-- Criar índices para performance
CREATE INDEX IF NOT EXISTS idx_edicao_cursos_edicao_id ON edicao_cursos(edicao_id);
CREATE INDEX IF NOT EXISTS idx_edicao_cursos_curso_id ON edicao_cursos(curso_id);

-- Verificar se a tabela foi criada
SELECT 'Tabela edicao_cursos criada com sucesso!' as resultado;
