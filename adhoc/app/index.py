import importlib
from wsgiref import simple_server
from urllib.parse import parse_qs
from orator import DatabaseManager, Model
import os
from session import get_session

def app(environ, start_response):
    try:
        path = environ['PATH_INFO']
        param = parse_qs(environ['QUERY_STRING'])
        session_id,session = get_session(environ)
        environ['session']= session

        path_array = path.split('/')
        classname = path_array[2].capitalize() + 'Controller'

        module = importlib.import_module("controllers."+ classname)
        instance= getattr(module, classname)(environ)
        getattr(instance, path_array[3] or 'index')(*param.values())

        start_response(instance.status, [
            ("Content-Type", "text/html"),
            ("location", instance.redirect_url),
            ("Set-Cookie",f"session_id={session_id}; Path=/"),
            ("Content-Length", str(len(instance.data)))
        ])
        return [instance.data.encode()]
    except Exception as e:
        error_msg = f"""
        <!DOCTYPE html>
        <html>
        <head><title>Erro do Servidor</title></head>
        <body>
            <h1>❌ Erro do Servidor</h1>
            <p><strong>Erro:</strong> {str(e)}</p>
            <p><strong>Path:</strong> {environ.get('PATH_INFO', 'N/A')}</p>
            <p><strong>Método:</strong> {environ.get('REQUEST_METHOD', 'N/A')}</p>
            <hr>
            <h3>Links para teste:</h3>
            <ul>
                <li><a href="/app/feedback/index">Feedback (original)</a></li>
                <li><a href="/app/test/index">Teste simples</a></li>
            </ul>
        </body>
        </html>
        """
        start_response("500 Internal Server Error", [
            ("Content-Type", "text/html"),
            ("Content-Length", str(len(error_msg)))
        ])
        return [error_msg.encode()]

if __name__ == '__main__':
    config = {
        'pgsql': {
            'driver': 'pgsql',
            'host': 'db',
            'database': os.environ.get('DB_DATABASE', 'basefeedback'),
            'user': os.environ['DB_USER'],
            'password': os.environ['DB_PASSWORD'],
            'prefix': ''
        }
    }

    db = DatabaseManager(config)
    Model.set_connection_resolver(db)
    w_s = simple_server.make_server(
        host="",
        port=8000,
        app=app
    )
    w_s.serve_forever()