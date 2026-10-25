from wsgiref.simple_server import make_server
from urllib.parse import parse_qs
from module import StaticFileHandler
import os


USER = {'username': 'Максим', 'password': '123456', 'balance': 15000}

static_finder = StaticFileHandler('static')

def read_file(path):
    """ Чтение файла и возврат его содержимого """
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def application(environ, start_response):
    """ WSGI-приложение для обработки HTTP-запросов,environ(словарь),start_response(функция для статусов и заголовков) """
    method = environ['REQUEST_METHOD']
    path = environ['PATH_INFO']
    body = b''
    status = '200 OK'
    content_type = 'text/html; charset=utf-8'
    content = None
    detected_type = 'text/html; charset=utf-8'

    if method == 'POST' and path == '/login':
        length = int(environ.get('CONTENT_LENGTH') or 0)
        data = parse_qs(environ['wsgi.input'].read(length).decode('utf-8'))
        username = data.get('username', [''])[0]
        password = data.get('password', [''])[0]

        if username == USER['username'] and password == USER['password']:
            body = read_file('templates/account')
            body = body.replace('{{USER.username}}', USER['username'])
            body = body.replace('{{USER.balance}}', str(USER['balance']))
            body = body.encode('utf-8')
            status = '200 OK'
        else:
            body = read_file('templates/loginerror').encode('utf-8')
            status = '401 Unauthorized'
    else:
        if path == '/':
            path = '/main'

        if not os.path.splitext(path)[1]:
            path += '.html'

        content, detected_type = static_finder.getfile(path)

        if content is not None:
            body = content
            content_type = detected_type

            if content_type.startswith('text/'):
                content_type += '; charset=utf-8'
        else:
            body = '<h1>404 Страница не найдена</h1>'.encode('utf-8')
            status = '404 Not Found'

    headers = [('Content-Type', content_type)]
    start_response(status, headers)
    return [body]


if __name__ == '__main__':
    with make_server('', 5500, application) as httpd:
        print('Сервер запущен на порту 5500...')
        httpd.serve_forever()
        