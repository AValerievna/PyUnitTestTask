import time

import pytest

from file import File
from proj.file_already_exist_error import FileAlreadyExistError
from proj.file_storage import FileStorage


class TestFileStorage(object):

    @pytest.fixture(scope="function", params=[
        3,
        0,
        100
    ])
    def storage_size_data(self, request):
        return request.param

    @pytest.fixture(scope="function", params=[
        (10, "file1.txt", "some"),
        (20, "file1.txt", "file_content"),
        (20, "file1.txt", ""),
    ])
    def size_filename_content_data(self, request):
        return request.param

    @pytest.fixture(scope="function", params=[
        (10, "file1.txt"),
        (20, "file1.txt"),
        (20, "file1.txt"),
    ])
    def size_and_filename_data(self, request):
        return request.param

    @pytest.mark.parametrize("size", [
        3,
        0,
        100,
        pytest.param(-10,
                     marks=pytest.mark.xfail(reason="invalid arg", strict=True)),
        pytest.param("some",
                     marks=pytest.mark.xfail(reason="invalid arg", strict=True)),
    ])
    def test_init(self, size):
        FileStorage(size)
        assert size >= 0, "Invalid init"

    def test_get_available_size_before_any_write(self, storage_size_data):
        (size) = storage_size_data
        file_storage = FileStorage(size)
        assert file_storage.get_available_size() == size, "Invalid get_available_size"

    def test_get_available_size_after_any_write(self, size_filename_content_data):
        (size, filename, content) = size_filename_content_data
        file_storage = FileStorage(size)
        file = File(filename, content)
        file_storage.write(file)
        assert file_storage.get_available_size() == file_storage.get_max_size() - file.get_size(), \
            "Invalid get_available_size"

    def test_get_files_before_any_write(self, storage_size_data):
        (size) = storage_size_data
        file_storage = FileStorage(size)
        assert file_storage.get_files() == [], "Invalid get_files"

    def test_get_files_after_any_write(self, size_filename_content_data):
        (size, filename, content) = size_filename_content_data
        file_storage = FileStorage(size)
        file = File(filename, content)
        file_storage.write(file)
        assert file in file_storage.get_files(), "Invalid get_files"

    def test_get_max_size_before_any_write(self, storage_size_data):
        (size) = storage_size_data
        file_storage = FileStorage(size)
        assert file_storage.get_max_size() == size, "Invalid get_max_size"

    def test_get_max_size_after_any_write(self, size_filename_content_data):
        (size, filename, content) = size_filename_content_data
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
    def test_write_success(self, size, filename, content):
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

    @pytest.mark.xfail(raises=FileAlreadyExistError, reason="already exists", strict=True)
    def test_write_with_existing_file(self, size_filename_content_data):
        (size, filename, content) = size_filename_content_data
        file_storage = FileStorage(size)
        file = File(filename, content)
        file_storage.write(file)
        file_storage.write(file)

    def test_is_exists_return_true(self, size_filename_content_data):
        (size, filename, content) = size_filename_content_data
        file_storage = FileStorage(size)
        file = File(filename, content)
        file_storage.write(file)
        assert file_storage.is_exists(file.get_filename())

    def test_is_exists_return_false(self, size_and_filename_data):
        (size, filename) = size_and_filename_data
        file_storage = FileStorage(size)
        assert not file_storage.is_exists(filename)

    def test_get_file_return_file(self, size_filename_content_data):
        (size, filename, content) = size_filename_content_data
        file_storage = FileStorage(size)
        file = File(filename, content)
        file_storage.write(file)
        assert file_storage.get_file(file.get_filename()) == file

    def test_get_file_return_none(self, size_and_filename_data):
        (size, filename) = size_and_filename_data
        file_storage = FileStorage(size)
        assert file_storage.get_file(filename) is None

    def test_delete_success(self, size_filename_content_data):
        (size, filename, content) = size_filename_content_data
        file_storage = FileStorage(size)
        file = File(filename, content)
        file_storage.write(file)
        assert file_storage.delete(file.get_filename()) and file not in file_storage.get_files()

    def test_delete_failed(self, size_filename_content_data):
        (size, filename, content) = size_filename_content_data
        file_storage = FileStorage(size)
        assert not file_storage.delete(filename)
