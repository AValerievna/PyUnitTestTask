import time

import pytest

from file import File
from proj.file_storage import FileStorage


class TestFileStorage(object):
    """def test_is_exist(self):
      #  assert FileStorage.is_exists()"""

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
    def test_get_available_size(self, size):
        fs = FileStorage(size)
        assert fs.get_available_size() == size, "Invalid get_available_size"

    @pytest.mark.parametrize("size", [
        3,
        0,
        100
    ])
    def test_get_max_size(self, size):
        fs = FileStorage(size)
        assert fs.get_max_size() == size, "Invalid get_max_size"

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
        fs = FileStorage(size)
        f = File(filename, content)
        prev_size = fs.get_available_size()
        t0 = time.time()
        res = fs.write(f)
        t1 = time.time()
        total_time = t1 - t0
        print(total_time)

        assert f in fs.get_files() \
               and fs.get_available_size() == prev_size - f.get_size() \
               and res \
               and total_time <= 2, "Invalid write"
