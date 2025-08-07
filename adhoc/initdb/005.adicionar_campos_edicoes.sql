-- Script para adicionar novos campos na tabela edicoes
-- Execute apenas se os campos não existirem

DO $$
BEGIN
    -- Adicionar campo ano se não existir
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                   WHERE table_name = 'edicoes' AND column_name = 'ano') THEN
        ALTER TABLE edicoes ADD COLUMN ano INTEGER;
    END IF;
    
    -- Adicionar campo semestre se não existir
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                   WHERE table_name = 'edicoes' AND column_name = 'semestre') THEN
        ALTER TABLE edicoes ADD COLUMN semestre VARCHAR(1);
    END IF;
    
    -- Adicionar campo data_inicio se não existir
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                   WHERE table_name = 'edicoes' AND column_name = 'data_inicio') THEN
        ALTER TABLE edicoes ADD COLUMN data_inicio DATE;
    END IF;
    
    -- Adicionar campo data_fim se não existir
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                   WHERE table_name = 'edicoes' AND column_name = 'data_fim') THEN
        ALTER TABLE edicoes ADD COLUMN data_fim DATE;
    END IF;
END $$;
