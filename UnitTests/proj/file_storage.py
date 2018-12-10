# encoding=utf8
import time

from proj.file_already_exist_error import FileAlreadyExistError


class FileStorage(object):

    def __init__(self, size):
        """
        Конструктор хранилища

        :param size: размер хранилища
        """
        self._max_size = self._available_size = size
        self._files = []

    def write(self, file):
        """
        Добавление файла в хранилище(если достаточно свободного места)

        Если файл существует, то будет выброшена FileAlreadyExistError

        :param file: объект класса File, который нужно записать
        :return: True - файл записан, False - файл не записан
        """
        if file in self._files:
            raise FileAlreadyExistError()

        if file.get_size() >= self._available_size:
            return False

        self._files.append(file)
        self._available_size -= file.get_size()

        if self._available_size % 2 == 0:
            time.sleep(1.8)
        else:
            time.sleep(3)
        return True

    def is_exists(self, filename):
        """
        Проверка наличия файла

        :param filename: название файла с расширением
        :return: True - файл имеется, False - файл отсутствует
        """
        for file_in_list in self._files:
            if file_in_list.get_filename() == filename:
                return True
        return False

    def delete(self, filename):
        """
        Удаление файла

        :param filename: название файла с расширением
        :return: True - файл удалён, False - файл не удалён
        """
        for file_in_list in self._files:
            if file_in_list.get_filename() == filename:
                self._files.remove(file_in_list)
                return True
        return False

    def get_files(self):
        """
        Получение всех файлов

        :return: list с объектами класса File
        """
        return self._files

    def get_file(self, filename):
        """
        Получение файла по имени

        :param filename: имя файла с расширением
        :return: объект класса File, если файл найден, иначе - None
        """
        for file_in_list in self._files:
            if file_in_list.get_filename() == filename:
                return file_in_list
        return None

    def get_available_size(self):
        """
        Получение оставшегося места

        :return: размер оставшегося места
        """
        return self._available_size

    def get_max_size(self):
        """
        Получение ёмкости хранилища

        :return: ёмкость хранилища
        """
        return self._max_size
