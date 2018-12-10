import pytest

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
        fs = FileStorage.__init__(size)
        assert fs._max_size == size and fs._available_size == size and len(fs._files) == 0, "Invalid init"

    @pytest.mark.parametrize("size", [
        3,
        0,
        100
    ])
    def test_get_available_size(self, size):
        fs = FileStorage.__init__(size)
        assert fs.get_available_size() == size, "Invalid get_available_size"

    @pytest.mark.parametrize("size", [
        3,
        0,
        100
    ])
    def test_get_max_size(self, size):
        fs = FileStorage.__init__(size)
        assert fs.get_max_size() == size, "Invalid get_max_size"
