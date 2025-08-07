from orator import Model

class EdicaoCurso(Model):
    """
    Modelo para representar a tabela associativa EdicaoCurso.
    Armazena o número de vagas por modalidade para um curso em uma edição específica.
    
    Campos:
    - id: Chave Primária
    - edicao_id: Chave Estrangeira para Edicao
    - curso_id: Chave Estrangeira para Curso
    - vagas_ac: Integer (Ampla Concorrência)
    - vagas_ppi_br: Integer (PPI - Pública - Baixa Renda)
    - vagas_publica_br: Integer (Pública - Baixa Renda)
    - vagas_ppi_publica: Integer (PPI - Pública)
    - vagas_publica: Integer (Pública)
    - vagas_deficientes: Integer (Deficientes)
    """
    __table__ = 'edicao_cursos'
    __timestamps__ = False
    __fillable__ = [
        'edicao_id', 'curso_id', 'vagas_ac', 'vagas_ppi_br', 
        'vagas_publica_br', 'vagas_ppi_publica', 'vagas_publica', 'vagas_deficientes'
    ]

    def total_vagas(self):
        """
        Calcula o total de vagas para esta configuração.
        """
        def safe_int(value):
            try:
                return int(value) if value and str(value).strip() else 0
            except (ValueError, TypeError):
                return 0
        
        return sum([
            safe_int(self.vagas_ac),
            safe_int(self.vagas_ppi_br),
            safe_int(self.vagas_publica_br),
            safe_int(self.vagas_ppi_publica),
            safe_int(self.vagas_publica),
            safe_int(self.vagas_deficientes),
        ])
    
    def modalidades_disponiveis(self):
        """
        Retorna lista de modalidades que têm vagas configuradas.
        """
        def safe_int(value):
            try:
                return int(value) if value and str(value).strip() else 0
            except (ValueError, TypeError):
                return 0
        
        modalidades = []
        
        if safe_int(self.vagas_ac) > 0:
            modalidades.append({'nome': 'Ampla Concorrência', 'vagas': self.vagas_ac})
        if safe_int(self.vagas_ppi_br) > 0:
            modalidades.append({'nome': 'PPI - Pública - Baixa Renda', 'vagas': self.vagas_ppi_br})
        if safe_int(self.vagas_publica_br) > 0:
            modalidades.append({'nome': 'Pública - Baixa Renda', 'vagas': self.vagas_publica_br})
        if safe_int(self.vagas_ppi_publica) > 0:
            modalidades.append({'nome': 'PPI - Pública', 'vagas': self.vagas_ppi_publica})
        if safe_int(self.vagas_publica) > 0:
            modalidades.append({'nome': 'Pública', 'vagas': self.vagas_publica})
        if safe_int(self.vagas_deficientes) > 0:
            modalidades.append({'nome': 'Deficientes', 'vagas': self.vagas_deficientes})
        
        return modalidades
    
    def edicao(self):
        """
        Relacionamento com Edicao (belongsTo).
        """
        from models.Edicao import Edicao
        return self.belongs_to(Edicao, 'edicao_id')
    
    def curso(self):
        """
        Relacionamento com Curso (belongsTo).
        """
        from models.Curso import Curso
        return self.belongs_to(Curso, 'curso_id')
