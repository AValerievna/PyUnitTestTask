import time

import pytest

from file import File
from proj.file_already_exist_error import FileAlreadyExistError
from proj.file_storage import FileStorage


class TestFileStorage(object):

    @pytest.mark.parametrize("size", [
        3,
        0,
        100
    ])
    def test_init(self, size):
        FileStorage(size)
        assert isinstance(size, int), "Invalid init"

    @pytest.mark.parametrize("size", [
        3,
        0,
        100
    ])
    def test_get_available_size_before_any_write(self, size):
        file_storage = FileStorage(size)
        assert file_storage.get_available_size() == size, "Invalid get_available_size"

    @pytest.mark.parametrize("size,filename, content", [
        (10, "file1.txt", "some"),
        (20, "file1.txt", "file_content"),
        (20, "file1.txt", ""),
    ])
    def test_get_available_size_after_any_write(self, size, filename, content):
        file_storage = FileStorage(size)
        file = File(filename, content)
        file_storage.write(file)
        assert file_storage.get_available_size() == file_storage.get_max_size() - file.get_size(), \
            "Invalid get_available_size"

    @pytest.mark.parametrize("size", [
        3,
        0,
        100
    ])
    def test_get_files_before_any_write(self, size):
        file_storage = FileStorage(size)
        assert file_storage.get_files() == [], "Invalid get_files"

    @pytest.mark.parametrize("size,filename, content", [
        (10, "file1.txt", "some"),
        (20, "file1.txt", "file_content"),
        (20, "file1.txt", ""),
    ])
    def test_get_files_after_any_write(self, size, filename, content):
        file_storage = FileStorage(size)
        file = File(filename, content)
        file_storage.write(file)
        assert file in file_storage.get_files(), "Invalid get_files"

    @pytest.mark.parametrize("size", [
        3,
        0,
        100
    ])
    def test_get_max_size(self, size):
        file_storage = FileStorage(size)
        assert file_storage.get_max_size() == size, "Invalid get_max_size"

    @pytest.mark.parametrize("size,filename, content", [
        (10, "file1.txt", "some"),
        (20, "file1.txt", "file_content"),
        (20, "file1.txt", ""),
    ])
    def test_get_files_after_any_write(self, size, filename, content):
        file_storage = FileStorage(size)
        file = File(filename, content)
        file_storage.write(file)
        assert file_storage.get_max_size() == size, "Invalid get_max_size"

    @pytest.mark.parametrize("size,filename, content", [
        (10, "file1.txt", "some"),
        (20, "file1.txt", "file_content"),
        (20, "file1.txt", ""),
        pytest.param(9, "file2.file2.png", "cont",
                     marks=pytest.mark.xfail(reason="invalid timing", strict=True)),
        pytest.param(15, "file2.file2.png", "some_content",
                     marks=pytest.mark.xfail(reason="invalid timing", strict=True)),
        pytest.param(10, "file.zip", "some-zip-file-content",
                     marks=pytest.mark.xfail(reason="invalid size", strict=True)),
        pytest.param(5, "file.zip", "some-cont",
                     marks=pytest.mark.xfail(reason="invalid size", strict=True))
    ])
    def test_write(self, size, filename, content):
        file_storage = FileStorage(size)
        file = File(filename, content)
        prev_size = file_storage.get_available_size()
        t0 = time.time()
        res = file_storage.write(file)
        t1 = time.time()
        total_time = t1 - t0
        print(total_time)

        assert file in file_storage.get_files() \
               and file_storage.get_available_size() == prev_size - file.get_size() \
               and res \
               and total_time <= 2, "Invalid write "

    @pytest.mark.parametrize("size,filename, content", [
        (10, "file1.txt", "some"),
        (20, "file1.txt", "file_content"),
        (20, "file1.txt", ""),
    ])
    @pytest.mark.xfail(raises=FileAlreadyExistError, reason="already exists", strict=True)
    def test_write_with_existing_file(self, size, filename, content):
        file_storage = FileStorage(size)
        file = File(filename, content)
        file_storage.write(file)
        file_storage.write(file)

    @pytest.mark.parametrize("size,filename, content", [
        (10, "file1.txt", "some"),
        (20, "file1.txt", "file_content"),
        (20, "file1.txt", ""),
    ])
    def test_is_exists_return_true(self, size, filename, content):
        file_storage = FileStorage(size)
        file = File(filename, content)
        file_storage.write(file)
        assert file_storage.is_exists(file.get_filename())

    @pytest.mark.parametrize("size,filename", [
        (10, "file1.txt"),
        (20, "file1.txt"),
        (20, "file1.txt"),
    ])
    def test_is_exists_return_false(self, size, filename):
        file_storage = FileStorage(size)
        assert not file_storage.is_exists(filename)

    @pytest.mark.parametrize("size,filename, content", [
        (10, "file1.txt", "some"),
        (20, "file1.txt", "file_content"),
        (20, "file1.txt", ""),
    ])
    def test_get_file_return_file(self, size, filename, content):
        file_storage = FileStorage(size)
        file = File(filename, content)
        file_storage.write(file)
        assert file_storage.get_file(file.get_filename()) == file

    @pytest.mark.parametrize("size,filename", [
        (10, "file1.txt"),
        (20, "file1.txt"),
        (20, "file1.txt"),
    ])
    def test_get_file_return_none(self, size, filename):
        file_storage = FileStorage(size)
        assert file_storage.get_file(filename) is None

    @pytest.mark.parametrize("size,filename, content", [
        (10, "file1.txt", "some"),
        (20, "file1.txt", "file_content"),
        (20, "file1.txt", ""),
    ])
    def test_delete_return_true(self, size, filename, content):
        file_storage = FileStorage(size)
        file = File(filename, content)
        file_storage.write(file)
        assert file_storage.delete(file.get_filename()) and file not in file_storage.get_files()

    @pytest.mark.parametrize("size,filename", [
        (10, "file1.txt"),
        (20, "file1.txt"),
        (20, "file1.txt"),
    ])
    def test_delete_return_false(self, size, filename):
        file_storage = FileStorage(size)
        assert not file_storage.delete(filename)
