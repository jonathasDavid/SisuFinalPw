-- Adicionar colunas que faltam na tabela edicoes
ALTER TABLE edicoes ADD COLUMN IF NOT EXISTS ano INTEGER;
ALTER TABLE edicoes ADD COLUMN IF NOT EXISTS semestre INTEGER;
ALTER TABLE edicoes ADD COLUMN IF NOT EXISTS data_inicio DATE;
ALTER TABLE edicoes ADD COLUMN IF NOT EXISTS data_fim DATE;

-- Verificar estrutura atualizada
\d edicoes;
