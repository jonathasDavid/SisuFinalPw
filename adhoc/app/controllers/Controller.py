from jinja2 import Environment, FileSystemLoader
import os
import cgi
import re
from html import escape
from urllib.parse import urlencode

class Controller:
    def __init__(self,env):
        self.environ=env
        self.data = ""
        self.status = "200 OK"
        self.redirect_url = ""
        self.session = env['session']
        self.nome=(self.__class__.__name__).lower()[:-len("controller")]
        self.env = Environment(loader=FileSystemLoader(os.getcwd()+f'/views/{self.nome}'))

    def form2dict(self,form):
        dict ={}
        for  key in form:
            dict[key]= escape(form.getvalue(key))
        return dict
    
    def parseNestedFields(self, form_data):
        """
        Converte dados de formulário com campos indexados em estrutura aninhada.
        
        Exemplo:
        Input: {
            'nome': 'João',
            'cursos[0][curso_id]': '1',
            'cursos[0][nome]': 'Matemática',
            'cursos[1][curso_id]': '2',
            'cursos[1][nome]': 'Física'
        }
        
        Output: {
            'nome': 'João',
            'cursos': [
                {'curso_id': '1', 'nome': 'Matemática'},
                {'curso_id': '2', 'nome': 'Física'}
            ]
        }
        """
        nested_data = {}
        
        # Padrão para campos indexados: campo[index][subcampo] ou campo[index]
        pattern = r'^([a-zA-Z_][a-zA-Z0-9_]*)\[(\d+)\](?:\[([a-zA-Z_][a-zA-Z0-9_]*)\])?$'
        
        for key, value in form_data.items():
            match = re.match(pattern, key)
            
            if match:
                field_name = match.group(1)  # ex: 'cursos'
                index = int(match.group(2))  # ex: 0, 1, 2...
                subfield = match.group(3)    # ex: 'curso_id', 'nome' (pode ser None)
                
                # Inicializa a lista se não existir
                if field_name not in nested_data:
                    nested_data[field_name] = []
                
                # Garante que a lista tem o tamanho necessário
                while len(nested_data[field_name]) <= index:
                    nested_data[field_name].append({})
                
                if subfield:
                    # Caso: cursos[0][curso_id]
                    nested_data[field_name][index][subfield] = value
                else:
                    # Caso: cursos[0] (valor direto)
                    nested_data[field_name][index] = value
            else:
                # Campo simples, mantém como está
                nested_data[key] = value
        
        return nested_data
    def loadForm(self, model, nested=False):
        """
        Carrega dados do formulário no modelo.
        
        Args:
            model: Instância do modelo a ser preenchida
            nested (bool): Se True, processa campos aninhados
        
        Returns:
            dict: Dados processados do formulário
        """
        form = cgi.FieldStorage(fp=self.environ["wsgi.input"], environ=self.environ)
        form_data = self.form2dict(form)
        
        if nested:
            # Processa campos aninhados e retorna a estrutura completa
            parsed_data = self.parseNestedFields(form_data)
            
            # Preenche apenas os campos "planos" no modelo principal
            model_data = {k: v for k, v in parsed_data.items() 
                         if not isinstance(v, (list, dict))}
            model.fill(model_data)
            
            return parsed_data
        else:
            # Comportamento original para compatibilidade
            model.fill(form_data)
            return form_data
    
    def loadNestedForm(self, model):
        """
        Método auxiliar para facilitar o uso de formulários aninhados.
        
        Args:
            model: Instância do modelo principal
            
        Returns:
            dict: Dados completos do formulário com estruturas aninhadas
        """
        return self.loadForm(model, nested=True)

    def redirectPage(self,path:str,params=None):
        self.status = "302 OK"
        self.redirect_url = f'/app/{self.nome}/{path}'
        if params:
            self.redirect_url += f'?{urlencode(params)}'

    def notFound(self):
        self.status = "404 Not Found"
        template = Environment(loader=FileSystemLoader(os.getcwd()+f'/views/public')).get_template("404.html")
        self.data=template.render()