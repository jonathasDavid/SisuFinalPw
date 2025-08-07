from models.BaseModel import BaseModel
import re
from datetime import datetime, date

class Candidato(BaseModel):
    """
    Modelo para representar um Candidato do SISU.
    
    Campos:
    - id: Chave Primária
    - nome: String
    - cpf: String (único)
    - data_nascimento: Date
    - categoria: String (deve corresponder a uma das modalidades de vaga)
    - curso_id: Chave Estrangeira para Curso
    - nota: Float
    """
    __table__ = 'candidatos'
    __timestamps__ = False
    __fillable__ = ['nome', 'cpf', 'data_nascimento', 'categoria', 'curso_id', 'nota']

    def validate(self):
        """
        Validação completa para um candidato.
        """
        errors = []
        
        # Validar nome
        if not self.nome or len(self.nome.strip()) < 2:
            errors.append('Nome deve ter pelo menos 2 caracteres')
        
        # Validar CPF
        if not self._validate_cpf():
            errors.append('CPF inválido')
        
        # Validar data de nascimento
        if not self._validate_data_nascimento():
            errors.append('Data de nascimento inválida')
        
        # Validar categoria
        if not self._validate_categoria():
            errors.append('Categoria inválida')
        
        # Validar curso_id
        if not self.curso_id or not str(self.curso_id).isdigit():
            errors.append('ID do curso deve ser um número válido')
        
        # Validar nota
        if not self._validate_nota():
            errors.append('Nota deve ser um número entre 0 e 1000')
        
        if errors:
            self.error = '; '.join(errors)
            return False
        
        return True

    def _validate_cpf(self):
        """
        Valida formato e dígitos verificadores do CPF.
        """
        if not self.cpf:
            return False
        
        # Remove caracteres não numéricos
        cpf = re.sub(r'[^0-9]', '', str(self.cpf))
        
        # Verifica se tem 11 dígitos
        if len(cpf) != 11:
            return False
        
        # Verifica se não é uma sequência de números iguais
        if cpf == cpf[0] * 11:
            return False
        
        # Calcula primeiro dígito verificador
        soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
        primeiro_digito = (soma * 10) % 11
        if primeiro_digito == 10:
            primeiro_digito = 0
        
        # Calcula segundo dígito verificador
        soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
        segundo_digito = (soma * 10) % 11
        if segundo_digito == 10:
            segundo_digito = 0
        
        # Verifica se os dígitos calculados conferem
        return cpf[-2:] == f"{primeiro_digito}{segundo_digito}"
    
    def _validate_data_nascimento(self):
        """
        Valida se a data de nascimento é válida e se o candidato tem idade mínima.
        """
        if not self.data_nascimento:
            return False
        
        try:
            # Converte string para date se necessário
            if isinstance(self.data_nascimento, str):
                data_nasc = datetime.strptime(self.data_nascimento, '%Y-%m-%d').date()
            else:
                data_nasc = self.data_nascimento
            
            # Verifica se a data não é futura
            if data_nasc > date.today():
                return False
            
            # Verifica idade mínima (por exemplo, 16 anos)
            idade = date.today().year - data_nasc.year
            if date.today() < date(date.today().year, data_nasc.month, data_nasc.day):
                idade -= 1
            
            return idade >= 16
            
        except (ValueError, TypeError):
            return False
    
    def _validate_categoria(self):
        """
        Valida se a categoria corresponde a uma modalidade válida.
        """
        categorias_validas = [
            'Ampla Concorrência',
            'PPI - Pública - Baixa Renda',
            'Pública - Baixa Renda',
            'PPI - Pública',
            'Pública',
            'Deficientes'
        ]
        
        return self.categoria in categorias_validas
    
    def _validate_nota(self):
        """
        Valida se a nota está em um formato válido.
        """
        if not self.nota:
            return False
        
        try:
            nota_float = float(self.nota)
            return 0 <= nota_float <= 1000
        except (ValueError, TypeError):
            return False

    def save(self, **kwargs):
        """
        Salva o candidato com validação.
        """
        if self.validate():
            return super().save(**kwargs)
        return False
    
    def get_idade(self):
        """
        Calcula e retorna a idade do candidato.
        """
        if not self.data_nascimento:
            return None
        
        try:
            if isinstance(self.data_nascimento, str):
                data_nasc = datetime.strptime(self.data_nascimento, '%Y-%m-%d').date()
            else:
                data_nasc = self.data_nascimento
            
            idade = date.today().year - data_nasc.year
            if date.today() < date(date.today().year, data_nasc.month, data_nasc.day):
                idade -= 1
            
            return idade
            
        except (ValueError, TypeError):
            return None
    
    def curso(self):
        """
        Relacionamento com Curso (belongsTo).
        """
        from models.Curso import Curso
        return self.belongs_to(Curso, 'curso_id')
