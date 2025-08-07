-- Correção da tabela edicoes para adicionar colunas que faltam
-- Este arquivo será executado quando o banco for recriado

-- Adicionar colunas que faltam
ALTER TABLE edicoes ADD COLUMN IF NOT EXISTS ano INTEGER;
ALTER TABLE edicoes ADD COLUMN IF NOT EXISTS semestre INTEGER CHECK (semestre IN (1, 2));
ALTER TABLE edicoes ADD COLUMN IF NOT EXISTS data_inicio DATE;
ALTER TABLE edicoes ADD COLUMN IF NOT EXISTS data_fim DATE;

-- Adicionar valores padrão para registros existentes se houver
UPDATE edicoes SET 
    ano = 2025,
    semestre = 1,
    data_inicio = CURRENT_DATE,
    data_fim = CURRENT_DATE + INTERVAL '6 months'
WHERE ano IS NULL;
