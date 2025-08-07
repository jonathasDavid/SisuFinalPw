-- Inserir apenas os cursos base
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
(10010, 'Sistemas de Informação', 'Exatas', 'Presencial', 8)
ON CONFLICT (curso_id) DO NOTHING;
