from models.BaseModel import BaseModel

class Edicao(BaseModel):
    """
    Modelo para representar uma Edição do SISU (entidade mestre).
    Agora com suporte a saveMany para persistência mestre-detalhe.
    """
    __table__ = 'edicoes'
    __timestamps__ = False
    __fillable__ = ['nome', 'ano', 'semestre', 'data_inicio', 'data_fim']
    
    # Configuração dos modelos de detalhe para saveMany
    _detail_models = {
        'cursos': None  # Será configurado dinamicamente para evitar import circular
    }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Configurar modelos de detalhe dinamicamente
        if self._detail_models['cursos'] is None:
            from models.Curso import Curso
            self._detail_models['cursos'] = Curso

    def validate(self):
        """
        Validação básica para uma edição do SISU.
        """
        errors = []
        
        if not self.nome or len(self.nome.strip()) < 3:
            errors.append('Nome deve ter pelo menos 3 caracteres')
        
        if not self.ano or not str(self.ano).isdigit():
            errors.append('Ano deve ser um número válido')
            
        if not self.semestre or self.semestre not in ['1', '2']:
            errors.append('Semestre deve ser 1 ou 2')
        
        if errors:
            self.error = '; '.join(errors)
            return False
        
        return True

    def save(self, **kwargs):
        """
        Salva a edição com validação.
        Mantém comportamento original para compatibilidade.
        """
        if self.validate():
            return super().save(**kwargs)
        return False
    
    def save_with_cursos(self, cursos_data):
        """
        Método auxiliar para salvar edição com cursos.
        
        Args:
            cursos_data (list): Lista de dicionários com dados dos cursos
            
        Returns:
            bool: True se salvou com sucesso
        """
        return self.save_many({'cursos': cursos_data})
    
    def update_with_cursos(self, cursos_data):
        """
        Método auxiliar para atualizar edição com cursos.
        
        Args:
            cursos_data (list): Lista de dicionários com dados dos cursos
            
        Returns:
            bool: True se atualizou com sucesso
        """
        return self.update_many({'cursos': cursos_data})
    
    def cursos(self):
        """
        Relacionamento com cursos (hasMany).
        """
        from models.Curso import Curso
        return self.has_many(Curso, 'edicao_id')
