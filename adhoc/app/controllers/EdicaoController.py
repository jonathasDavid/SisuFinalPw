import sys
sys.path.append('./app')
from jinja2 import Environment, FileSystemLoader
from models.Edicao import Edicao
from models.Curso import Curso
from controllers.Controller import Controller
import os


class EdicaoController(Controller):
    """
    Controller para demonstrar o uso de nested models.
    Cenário: Criar uma Edição do SISU com múltiplos Cursos simultaneamente.
    """

    def create(self):
        """
        Criar nova edição com cursos aninhados.
        Agora usando saveMany() para persistência mestre-detalhe.
        """
        method = self.environ["REQUEST_METHOD"]
        template = self.env.get_template("create.html")
        edicao = Edicao()
        
        if method == "POST":
            # Usa o método para processar formulários aninhados
            form_data = self.loadNestedForm(edicao)
            
            # Extrai dados dos cursos
            cursos_data = form_data.get('cursos', [])
            
            if edicao.validate() and cursos_data:
                # Usa saveMany para salvar mestre + detalhes em transação
                if edicao.save_with_cursos(cursos_data):
                    self.session['flash'] = f'Edição "{edicao.nome}" criada com {len(cursos_data)} curso(s)!'
                    self.redirectPage('view', {'id': edicao.id})
                else:
                    # Em caso de erro, mostra a mensagem
                    pass  # edicao.error já está definido
            elif not cursos_data:
                edicao.error = "Deve haver pelo menos um curso cadastrado"
            
        self.data = template.render(edicao=edicao)

    def update(self, id):
        """
        Atualizar edição existente com cursos.
        Usa update_many para gerenciar add/modify/remove de detalhes.
        """
        method = self.environ["REQUEST_METHOD"]
        template = self.env.get_template("update.html")
        edicao = Edicao.find(id[0])
        
        if not edicao:
            self.notFound()
            return
        
        if method == "POST":
            # Processa formulário aninhado
            form_data = self.loadNestedForm(edicao)
            cursos_data = form_data.get('cursos', [])
            
            if edicao.validate():
                # Usa update_many para gerenciar mudanças nos detalhes
                if edicao.update_with_cursos(cursos_data):
                    self.session['flash'] = f'Edição "{edicao.nome}" atualizada!'
                    self.redirectPage('view', {'id': edicao.id})
        else:
            # Carregar cursos existentes para o formulário
            cursos_existentes = edicao.cursos().get()
            self.session['cursos_existentes'] = [curso.to_dict() for curso in cursos_existentes]
        
        self.data = template.render(edicao=edicao)

    def view(self, id):
        """
        Visualizar edição com seus cursos.
        """
        edicao = Edicao.find(id[0])
        if not edicao:
            self.notFound()
            return
        
        # Carregar cursos relacionados
        cursos = edicao.cursos().get()
        
        # Mensagem flash se houver
        message = ""
        if 'flash' in self.session:
            message = self.session['flash']
            self.session['flash'] = ""
        
        template = self.env.get_template("view.html")
        self.data = template.render(
            edicao=edicao, 
            cursos=cursos, 
            message=message
        )

    def debug(self):
        """
        Página para mostrar como os dados aninhados foram processados.
        """
        debug_data = self.session.get('debug_data', {})
        template = self.env.get_template("debug.html")
        self.data = template.render(debug_data=debug_data)

    def index(self):
        """
        Lista edições (placeholder).
        """
        template = self.env.get_template("index.html")
        self.data = template.render(edicoes=[])
