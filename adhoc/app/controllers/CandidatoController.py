import sys
sys.path.append('./app')
from jinja2 import Environment, FileSystemLoader
from controllers.Controller import Controller
import os


class CandidatoController(Controller):
    """
    Controller para o painel do candidato.
    Gerencia funcionalidades do candidato como visualizar edições e fazer inscrições.
    """

    def index(self):
        """
        Página inicial do painel do candidato.
        Placeholder para futuras implementações dos tickets 4 e 5.
        """
        template = self.env.get_template("index.html")
        self.data = template.render(
            message="Painel do Candidato - Em desenvolvimento"
        )
