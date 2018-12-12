import pytest

from proj.file import File


class TestFile(object):

    @pytest.mark.parametrize("filename,content", [
        ("file1.txt", "some-content"),
        ("file2.file2.png", "file_content"),
        ("file.zip", "some-zip-content"),
        pytest.param("file.", "content", marks=pytest.mark.xfail(reason="invalid args", strict=True)),
        pytest.param("file3", "content", marks=pytest.mark.xfail(reason="invalid args", strict=True)),
        pytest.param("file ", "content", marks=pytest.mark.xfail(reason="invalid args", strict=True)),
        pytest.param("file*some.txt", "content", marks=pytest.mark.xfail(reason="invalid args", strict=True))
    ])
    def test_init_valid_params(self, filename, content):
        """Validation for Windows"""
        File(filename, content)
        restricted_chars = ["<", ">", ":", "\"", "/", "\\", "|", "?", "*"]
        assert "." in filename \
               and filename.index(".") != (len(filename) - 1) \
               and filename.find(" ") != (len(filename) - 1) \
               and not any(elem in filename for elem in restricted_chars) \
               and isinstance(content, str), "Invalid init"

    @pytest.mark.parametrize("filename,content,exp_ext", [
        ("file1.txt", "some-content", "txt"),
        ("file2.file2.png", "file_content", "png"),
        ("file.zip", "some-zip-content", "zip")
    ])
    def test_get_extension(self, filename, content, exp_ext):
        file = File(filename, content)
        assert file.get_extension() == exp_ext, "Invalid get_extension"

    @pytest.mark.parametrize("filename,content,exp_size", (
            ("file1.txt", "some-content", 12),
            pytest.param("file2.file2.png", "content", 7,
                         marks=pytest.mark.xfail(reason="wrong get_size realisation", strict=True)),
            ("file.zip", "", 0)
    ))
    def test_get_size(self, filename, content, exp_size):
        file = File(filename, content)
        assert file.get_size() == exp_size, "Invalid get_size"

    @pytest.mark.parametrize("filename,content", [
        ("file1.txt", "some-content"),
        ("file2.file2.png", "file_content"),
        ("file.zip", "some-zip-content")
    ])
    def test_get_content(self, filename, content):
        file = File(filename, content)
        assert file.get_content() == content, "Invalid get_content"

    @pytest.mark.parametrize("filename,content", [
        ("file1.txt", "some-content"),
        ("file2.file2.png", "file_content"),
        ("file.zip", "some-zip-content")
    ])
    def test_get_filename(self, filename, content):
        file = File(filename, content)
        assert file.get_filename() == filename, "Invalid get_extension"

    @pytest.mark.parametrize("filename,content", [
        ("file1.txt", "some-content"),
        ("file2.file2.png", "file_content"),
        ("file.zip", "some-zip-content")
    ])
    def test_print_text(self, filename, content, capsys):
        file = File(filename, content)
        file.print_text()
        captured = capsys.readouterr()
        assert captured.out == content + "\n", "Not expected print result"
