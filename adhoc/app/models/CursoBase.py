from models.BaseModel import BaseModel

class CursoBase(BaseModel):
    """
    Modelo para representar o catálogo de cursos disponíveis no sistema SISU.
    Esta tabela contém todos os cursos que podem ser selecionados ao criar edições.
    """
    __table__ = 'cursos_base'
    __timestamps__ = False
    __fillable__ = ['curso_id', 'nome', 'area', 'modalidade', 'duracao_semestres']

    def validate(self):
        """
        Validação básica para um curso base.
        """
        errors = []
        
        if not self.curso_id or not str(self.curso_id).isdigit():
            errors.append('ID do curso deve ser um número válido')
        
        if not self.nome or len(self.nome.strip()) < 2:
            errors.append('Nome do curso deve ter pelo menos 2 caracteres')
            
        if not self.area or len(self.area.strip()) < 2:
            errors.append('Área do curso deve ter pelo menos 2 caracteres')
        
        if errors:
            self.error = '; '.join(errors)
            return False
        
        return True

    def save(self, **kwargs):
        """
        Salva o curso base com validação.
        """
        if self.validate():
            return super().save(**kwargs)
        return False
    
    @classmethod
    def todos_cursos_disponiveis(cls):
        """
        Retorna todos os cursos disponíveis para seleção.
        """
        try:
            return cls.all()
        except:
            return []
    
    @classmethod
    def buscar_por_area(cls, area):
        """
        Busca cursos por área.
        """
        try:
            return cls.where('area', area).get()
        except:
            return []
    
    def to_dict(self):
        """
        Converte o modelo para dicionário.
        """
        return {
            'id': self.id,
            'curso_id': self.curso_id,
            'nome': self.nome,
            'area': self.area,
            'modalidade': self.modalidade,
            'duracao_semestres': self.duracao_semestres
        }
    
    @staticmethod
    def calcular_distribuicao_vagas(total_vagas):
        """
        Calcula a distribuição automática de vagas conforme os critérios do SISU.
        
        Lógica de Negócio:
        - 50% das vagas vão para Ampla Concorrência
        - 50% das vagas vão para sistemas de cotas, distribuídas assim:
          * 25%: PPI + Escola Pública + Baixa Renda
          * 25%: Escola Pública + Baixa Renda  
          * 20%: PPI + Escola Pública
          * 20%: Escola Pública
          * 10%: Pessoas com Deficiência
        
        Args:
            total_vagas (int): Total de vagas do curso
            
        Returns:
            dict: Distribuição das vagas por modalidade
        """
        if not isinstance(total_vagas, int) or total_vagas <= 0:
            raise ValueError("Total de vagas deve ser um número inteiro positivo")
        
        # Calcular 50% para ampla concorrência (arredondando para baixo)
        vagas_ac = total_vagas // 2
        
        # Os 50% restantes (ou mais, se total for ímpar) vão para cotas
        vagas_cotas = total_vagas - vagas_ac
        
        # Distribuição dentro das cotas (percentuais sobre as vagas de cota)
        # 25% = 0.25, 20% = 0.20, 10% = 0.10
        vagas_ppi_br = int(vagas_cotas * 0.25)          # 25%
        vagas_publica_br = int(vagas_cotas * 0.25)      # 25% 
        vagas_ppi_publica = int(vagas_cotas * 0.20)     # 20%
        vagas_publica = int(vagas_cotas * 0.20)         # 20%
        vagas_deficientes = int(vagas_cotas * 0.10)     # 10%
        
        # Calcular vagas já distribuídas nas cotas
        vagas_cotas_distribuidas = (vagas_ppi_br + vagas_publica_br + 
                                   vagas_ppi_publica + vagas_publica + vagas_deficientes)
        
        # Se houver diferença (devido a arredondamentos), ajustar a categoria de deficientes
        diferenca = vagas_cotas - vagas_cotas_distribuidas
        vagas_deficientes += diferenca
        
        # Garantir que nenhuma categoria tenha valor negativo
        vagas_deficientes = max(0, vagas_deficientes)
        
        distribuicao = {
            'vagas_ac': vagas_ac,
            'vagas_ppi_br': vagas_ppi_br,
            'vagas_publica_br': vagas_publica_br,
            'vagas_ppi_publica': vagas_ppi_publica,
            'vagas_publica': vagas_publica,
            'vagas_deficientes': vagas_deficientes
        }
        
        # Verificação final: a soma deve ser igual ao total
        soma_verificacao = sum(distribuicao.values())
        if soma_verificacao != total_vagas:
            # Se ainda há diferença, ajustar ampla concorrência
            diferenca_final = total_vagas - soma_verificacao
            distribuicao['vagas_ac'] += diferenca_final
        
        return distribuicao
