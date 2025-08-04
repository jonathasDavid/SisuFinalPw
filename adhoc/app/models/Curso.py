from models.BaseModel import BaseModel

class Curso(BaseModel):
    """
    Modelo para representar um Curso do SISU (entidade detalhe).
    """
    __table__ = 'cursos'
    __timestamps__ = False
    __fillable__ = ['edicao_id', 'curso_id', 'nome', 'vagas', 'nota_corte']

    def validate(self):
        """
        Validação básica para um curso.
        """
        errors = []
        
        if not self.curso_id or not str(self.curso_id).isdigit():
            errors.append('ID do curso deve ser um número válido')
        
        if not self.nome or len(self.nome.strip()) < 2:
            errors.append('Nome do curso deve ter pelo menos 2 caracteres')
            
        if not self.vagas or not str(self.vagas).isdigit() or int(self.vagas) <= 0:
            errors.append('Vagas deve ser um número positivo')
        
        if errors:
            self.error = '; '.join(errors)
            return False
        
        return True

    def save(self, **kwargs):
        """
        Salva o curso com validação.
        """
        if self.validate():
            return super().save(**kwargs)
        return False
    
    def edicao(self):
        """
        Relacionamento com edição (belongsTo).
        """
        from models.Edicao import Edicao
        return self.belongs_to(Edicao, 'edicao_id')
