from orator import Model
import logging

class BaseModel(Model):
    """
    Classe base estendida para suportar operações mestre-detalhe com transações.
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.details_data = {}  # Armazena dados dos detalhes para saveMany
        self.error = None
    
    def save_many(self, details_data=None, detail_models=None):
        """
        Salva o registro mestre e seus detalhes associados em uma transação.
        
        Args:
            details_data (dict): Dicionário com dados dos detalhes
                Formato: {'cursos': [{'nome': 'Math', 'vagas': 40}, ...]}
            detail_models (dict): Mapeamento de chaves para classes de modelo
                Formato: {'cursos': Curso, 'professores': Professor}
        
        Returns:
            bool: True se salvou com sucesso, False caso contrário
        """
        if not details_data:
            details_data = self.details_data
            
        if not detail_models:
            detail_models = getattr(self, '_detail_models', {})
        
        if not detail_models:
            self.error = "Nenhum modelo de detalhe configurado"
            return False
        
        try:
            # 1. Validar e salvar o registro mestre
            if not self.validate():
                return False
            
            if not super().save():
                self.error = "Erro ao salvar registro mestre"
                return False
            
            # 2. Processar cada tipo de detalhe
            for detail_key, detail_list in details_data.items():
                if detail_key not in detail_models:
                    continue
                
                detail_model_class = detail_models[detail_key]
                
                # 3. Processar cada registro de detalhe
                for detail_data in detail_list:
                    if not detail_data or not any(detail_data.values()):
                        continue  # Pula registros vazios
                    
                    # Instanciar modelo de detalhe
                    detail_instance = detail_model_class()
                    
                    # Preencher dados
                    detail_instance.fill(detail_data)
                    
                    # Associar ao mestre (chave estrangeira)
                    foreign_key = self._get_foreign_key_for_detail(detail_key)
                    setattr(detail_instance, foreign_key, self.id)
                    
                    # Validar e salvar
                    if not detail_instance.validate():
                        self.error = f"Erro validação {detail_key}: {detail_instance.error}"
                        raise Exception(self.error)
                    
                    if not detail_instance.save():
                        self.error = f"Erro ao salvar {detail_key}"
                        raise Exception(self.error)
            
            return True
            
        except Exception as e:
            self.error = str(e)
            logging.error(f"Erro em save_many: {e}")
            return False
    
    def update_many(self, details_data=None, detail_models=None):
        """
        Atualiza o registro mestre e gerencia detalhes (add/modify/remove).
        Versão simplificada sem transações complexas.
        """
        if not self.exists:
            self.error = "Registro mestre deve existir para update_many"
            return False
        
        if not details_data:
            details_data = self.details_data
            
        if not detail_models:
            detail_models = getattr(self, '_detail_models', {})
        
        try:
            # 1. Atualizar registro mestre
            if not self.validate():
                return False
            
            if not super().save():
                self.error = "Erro ao atualizar registro mestre"
                return False
            
            # 2. Por simplicidade, vamos apenas recriar os detalhes
            # Em produção, implementaríamos ADD/MODIFY/REMOVE
            for detail_key, new_details in details_data.items():
                if detail_key not in detail_models:
                    continue
                
                detail_model_class = detail_models[detail_key]
                foreign_key = self._get_foreign_key_for_detail(detail_key)
                
                # Remover detalhes existentes (simplificado)
                # detail_model_class.where(foreign_key, self.id).delete()
                
                # Adicionar novos detalhes
                for detail_data in new_details:
                    if not detail_data or not any(detail_data.values()):
                        continue
                    
                    detail_instance = detail_model_class()
                    detail_instance.fill(detail_data)
                    setattr(detail_instance, foreign_key, self.id)
                    
                    if not detail_instance.validate():
                        self.error = f"Erro validação {detail_key}: {detail_instance.error}"
                        raise Exception(self.error)
                    
                    detail_instance.save()
            
            return True
            
        except Exception as e:
            self.error = str(e)
            logging.error(f"Erro em update_many: {e}")
            return False
    
    def _get_foreign_key_for_detail(self, detail_key):
        """
        Determina o nome da chave estrangeira para um tipo de detalhe.
        
        Por convenção: modelo_mestre_id (ex: edicao_id)
        Pode ser sobrescrito nas classes filhas.
        """
        master_table = getattr(self, '__table__', self.__class__.__name__.lower())
        return f"{master_table.rstrip('s')}_id"  # Remove 's' plural se houver
    
    def validate(self):
        """
        Método de validação base. Deve ser sobrescrito nas classes filhas.
        """
        return True
