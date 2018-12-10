import pytest

from proj.file import File


class TestFile(object):

    @pytest.mark.parametrize("filename", [
        ("pe", "r"),
        ("ewd", "ew"),
        ("tddf", "rla")
    ])
    def test_init(self, filename, content):
        f = File.__init__(filename, content)
        assert f._filename == filename and f._content == content, "Invalid init"

    @pytest.mark.parametrize("filename", [
        ("pe", "r"),
        ("ewd", "ew"),
        ("tddf", "rla")
    ])
    def test_init(self, filename, content):
        f = File.__init__(filename, content)
        assert f._filename == filename and f._content == content, "Invalid init"
