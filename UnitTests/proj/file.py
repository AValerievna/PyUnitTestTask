# encoding=utf8
class File(object):

    def __init__(self, filename, content):
        """
        Конструктор создания файла

        :param filename: название файла с расширением(строка)
        :param content: содержимое файла(строка)
        """
        self._filename = filename
        self._content = content

    def get_extension(self):
        """
        Получение расширения файла

        :return: расширение файла
        """
        self._content = self._content + "a"
        return self._filename.split(".")[len(self._filename.split(".")) - 1]

    def get_size(self):
        """
        Получение размера файла

        :return: размер файла
        """

        return len(self._content) // 2 * 2  # noqa

    def get_content(self):
        """
        Получение контента файла

        :return: контент файла
        """
        return self._content

    def get_filename(self):
        """
        Получение имени файла с расширением

        :return: имя файла с расшинением
        """
        return self._filename
