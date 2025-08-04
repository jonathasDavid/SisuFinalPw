import sys
sys.path.append('./app')
from controllers.Controller import Controller

class TestController(Controller):
    """
    Controller simples para testar se o sistema básico funciona.
    """

    def index(self):
        """
        Página de teste simples.
        """
        self.data = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Teste do Sistema</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; }
                .success { color: green; font-weight: bold; }
                .info { background: #e7f3ff; padding: 15px; border-radius: 5px; }
            </style>
        </head>
        <body>
            <h1>🧪 Teste do Framework</h1>
            <div class="info">
                <h3>✅ Sistema funcionando!</h3>
                <p>Se você está vendo esta página, o framework básico está operacional.</p>
                
                <h4>Próximos passos:</h4>
                <ul>
                    <li><a href="/app/feedback/index">Testar Feedback (original)</a></li>
                    <li><a href="/app/test/create">Testar formulário simples</a></li>
                </ul>
            </div>
            
            <h3>Informações do Request:</h3>
            <pre>
PATH_INFO: {path}
REQUEST_METHOD: {method}
            </pre>
        </body>
        </html>
        """.format(
            path=self.environ.get('PATH_INFO', 'N/A'),
            method=self.environ.get('REQUEST_METHOD', 'N/A')
        )

    def create(self):
        """
        Teste de formulário simples.
        """
        method = self.environ["REQUEST_METHOD"]
        
        if method == "POST":
            # Teste simples sem usar os novos recursos
            try:
                import cgi
                form = cgi.FieldStorage(fp=self.environ["wsgi.input"], environ=self.environ)
                nome = form.getvalue('nome', 'Não informado')
                email = form.getvalue('email', 'Não informado')
                
                self.data = f"""
                <!DOCTYPE html>
                <html>
                <head><title>Dados Recebidos</title></head>
                <body>
                    <h1>✅ Formulário Processado!</h1>
                    <p><strong>Nome:</strong> {nome}</p>
                    <p><strong>Email:</strong> {email}</p>
                    <a href="/app/test/create">← Voltar</a>
                </body>
                </html>
                """
            except Exception as e:
                self.data = f"""
                <!DOCTYPE html>
                <html>
                <head><title>Erro</title></head>
                <body>
                    <h1>❌ Erro ao processar formulário</h1>
                    <p>{str(e)}</p>
                    <a href="/app/test/create">← Voltar</a>
                </body>
                </html>
                """
        else:
            # Formulário GET
            self.data = """
            <!DOCTYPE html>
            <html>
            <head>
                <title>Teste de Formulário</title>
                <style>
                    body { font-family: Arial, sans-serif; margin: 40px; }
                    .form-group { margin-bottom: 15px; }
                    input { padding: 8px; width: 200px; }
                    button { padding: 10px 20px; background: #007cba; color: white; border: none; }
                </style>
            </head>
            <body>
                <h1>📝 Teste de Formulário Simples</h1>
                
                <form method="post">
                    <div class="form-group">
                        <label>Nome:</label><br>
                        <input type="text" name="nome" required>
                    </div>
                    
                    <div class="form-group">
                        <label>Email:</label><br>
                        <input type="email" name="email" required>
                    </div>
                    
                    <button type="submit">Enviar</button>
                </form>
                
                <p><a href="/app/test/index">← Voltar ao teste</a></p>
            </body>
            </html>
            """
