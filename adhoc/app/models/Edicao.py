from orator import Model

class Edicao(Model):
    """
    Modelo para representar uma Edição do SISU.
    Campos: id, nome, ano, semestre, data_inicio, data_fim
    """
    __table__ = 'edicoes'
    __timestamps__ = False
    __fillable__ = ['nome', 'ano', 'semestre', 'data_inicio', 'data_fim']
    
    def validate(self):
        """
        Validação básica para uma edição do SISU.
        """
        errors = []
        
        if not self.nome or len(self.nome.strip()) < 3:
            errors.append('Nome deve ter pelo menos 3 caracteres')
        
        if self.ano and not str(self.ano).isdigit():
            errors.append('Ano deve ser um número válido')
            
        if self.semestre and self.semestre not in ['1', '2']:
            errors.append('Semestre deve ser 1 ou 2')
        
        if errors:
            self.error = '; '.join(errors)
            return False
        
        return True

    def save(self, **kwargs):
        """
        Salva a edição com validação.
        """
        if self.validate():
            return super().save(**kwargs)
        return False
    
    def save_with_cursos_selecionados(self, cursos_selecionados):
        """
        Salva edição e associa cursos selecionados com suas configurações de vagas.
        
        Args:
            cursos_selecionados (list): Lista de cursos selecionados com configurações
            
        Returns:
            bool: True se salvou com sucesso
        """
        try:
            print(f"=== SAVE_WITH_CURSOS_SELECIONADOS ===")
            print(f"Cursos recebidos: {len(cursos_selecionados)}")
            
            # Primeiro salva a edição
            if not self.save():
                print(f"❌ Erro ao salvar edição principal: {getattr(self, 'error', 'Erro desconhecido')}")
                return False
            
            print(f"✅ Edição salva com ID: {self.id}")
            print(f"Processando {len(cursos_selecionados)} cursos...")
            
            # Agora salva os EdicaoCurso associados
            from models.EdicaoCurso import EdicaoCurso
            for i, curso_config in enumerate(cursos_selecionados):
                print(f"\n--- Curso {i+1}/{len(cursos_selecionados)} ---")
                print(f"Dados: {curso_config}")
                
                edicao_curso = EdicaoCurso()
                edicao_curso.edicao_id = self.id
                edicao_curso.curso_id = curso_config['curso_id']
                edicao_curso.vagas_ac = curso_config.get('vagas_ac', 0)
                edicao_curso.vagas_ppi_br = curso_config.get('vagas_ppi_br', 0)
                edicao_curso.vagas_publica_br = curso_config.get('vagas_publica_br', 0)
                edicao_curso.vagas_ppi_publica = curso_config.get('vagas_ppi_publica', 0)
                edicao_curso.vagas_publica = curso_config.get('vagas_publica', 0)
                edicao_curso.vagas_deficientes = curso_config.get('vagas_deficientes', 0)
                
                print(f"EdicaoCurso criado:")
                print(f"  - edicao_id: {edicao_curso.edicao_id}")
                print(f"  - curso_id: {edicao_curso.curso_id}")
                print(f"  - vagas_ac: {edicao_curso.vagas_ac}")
                print(f"  - vagas_ppi_br: {edicao_curso.vagas_ppi_br}")
                print(f"  - vagas_publica_br: {edicao_curso.vagas_publica_br}")
                print(f"  - vagas_ppi_publica: {edicao_curso.vagas_ppi_publica}")
                print(f"  - vagas_publica: {edicao_curso.vagas_publica}")
                print(f"  - vagas_deficientes: {edicao_curso.vagas_deficientes}")
                print(f"  - total_vagas: {edicao_curso.total_vagas()}")
                
                if not edicao_curso.save():
                    print(f"❌ ERRO ao salvar EdicaoCurso para curso {curso_config['curso_id']}")
                    print(f"   Erro: {getattr(edicao_curso, 'error', 'Erro desconhecido')}")
                    return False
                else:
                    print(f"✅ EdicaoCurso salvo com ID: {edicao_curso.id}")
                    
            print(f"\n🎉 Todos os {len(cursos_selecionados)} cursos foram salvos com sucesso!")
            return True
            
        except Exception as e:
            print(f"❌ EXCEÇÃO em save_with_cursos_selecionados: {str(e)}")
            import traceback
            traceback.print_exc()
            self.error = f"Erro ao salvar edição: {str(e)}"
            return False
    
    def edicao_cursos(self):
        """
        Relacionamento com EdicaoCurso (hasMany).
        """
        from models.EdicaoCurso import EdicaoCurso
        return self.has_many(EdicaoCurso, 'edicao_id')
