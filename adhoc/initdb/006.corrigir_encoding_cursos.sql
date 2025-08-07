-- Script para corrigir nomes de cursos com problemas de encoding
-- Atualiza nomes com caracteres especiais

UPDATE cursos SET nome = 'Engenharia da Computação' WHERE nome LIKE '%Computa%';
UPDATE cursos SET nome = 'Administração' WHERE nome LIKE '%Administra%';
UPDATE cursos SET nome = 'Educação Física' WHERE nome LIKE '%Educa%';
UPDATE cursos SET nome = 'Ciência da Computação' WHERE nome LIKE '%Ci%ncia%';
UPDATE cursos SET nome = 'Educação' WHERE nome LIKE '%ducação%';
UPDATE cursos SET nome = 'Psicologia' WHERE nome LIKE '%Psicologia%';
UPDATE cursos SET nome = 'História' WHERE nome LIKE '%Hist%ria%';
UPDATE cursos SET nome = 'Geografia' WHERE nome LIKE '%Geografia%';
UPDATE cursos SET nome = 'Matemática' WHERE nome LIKE '%Matem%tica%';
UPDATE cursos SET nome = 'Português' WHERE nome LIKE '%Portugu%s%';

-- Verificar resultados
SELECT id, nome FROM cursos ORDER BY id;
