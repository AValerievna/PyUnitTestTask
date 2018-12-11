import pytest

from proj.file import File


class TestFile(object):

    @pytest.mark.parametrize("filename,content", [
        ("file1.txt", "some-content"),
        ("file2.file2.png", "file_content"),
        ("file.zip", "some-zip-content")
    ])
    def test_init(self, filename, content):
        File(filename, content)
        assert filename.split(".")[len(filename.split(".")) - 1] != '' and isinstance(content, str), "Invalid init"

    @pytest.mark.parametrize("filename,content,exp_ext", [
        ("file1.txt", "some-content", "txt"),
        ("file2.file2.png", "file_content", "png"),
        ("file.zip", "some-zip-content", "zip")
    ])
    def test_get_extension(self, filename, content, exp_ext):
        f = File(filename, content)
        assert f.get_extension() == exp_ext, "Invalid get_extension"

    @pytest.mark.parametrize("filename,content,exp_size", [
        ("file1.txt", "some-content", 12),
        ("file2.file2.png", "content", 7),
        ("file.zip", "", 0)
    ])
    def test_get_size(self, filename, content, exp_size):
        f = File(filename, content)
        assert f.get_size() == exp_size, "Invalid get_size"
