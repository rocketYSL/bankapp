import os
import mimetypes

class StaticFileHandler:
    """Находит файлы в папке static и определяет их MIME-тип."""
    def __init__(self, static_dir='static'):
        self.static_dir = os.path.abspath(static_dir)
    """ Принимаем название папки,превращаем в абсолютный путь и запоминаем его в объекте'static_dir'"""

    def getfile(self, url_path):
        file_path = os.path.abspath(os.path.join(self.static_dir, url_path.lstrip('/')))
        """ Получаем абсолютный путь к файлу, который нужно вернуть. Используем os.path.join для объединения пути к статической папке и запрошенного пути. lstrip('/') удаляет ведущий слэш из url_path, чтобы избежать проблем с путями. """

        if not os.path.isfile(file_path):
            return None, None

        content_type, _ = mimetypes.guess_type(file_path)

        if content_type is None:
            content_type = 'application/octet-stream'

        with open(file_path, 'rb') as file:
            content = file.read()

        return content, content_type