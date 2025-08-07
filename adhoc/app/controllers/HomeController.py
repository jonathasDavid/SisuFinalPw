import sys
sys.path.append('./app')
from jinja2 import Environment, FileSystemLoader
from controllers.Controller import Controller
import os


class HomeController(Controller):
    """
    Controller para a página inicial do sistema SISU.
    Gerencia a escolha entre acesso de Administrador ou Candidato.
    """

    def index(self):
        """
        Página inicial com escolha de tipo de acesso.
        Rota: / ou /app/home/index
        """
        template = self.env.get_template("index.html")
        self.data = template.render()

    def admin(self):
        """
        Redireciona para o painel do administrador.
        Rota: /admin → redireciona para /app/edicao/index
        """
        self.status = "302 Found"
        self.redirect_url = '/app/edicao/index'

    def candidato(self):
        """
        Redireciona para o painel do candidato.
        Rota: /candidato → redireciona para /app/candidato/index
        """
        self.status = "302 Found"
        self.redirect_url = '/app/candidato/index'
