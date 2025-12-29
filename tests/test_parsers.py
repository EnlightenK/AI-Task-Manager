import pytest
from pathlib import Path
from backend.utils.parsers import FileParser, TextFileParser, EmailFileParser
from unittest.mock import MagicMock, patch
from email.message import EmailMessage

def test_file_parser_abstract():
    with pytest.raises(TypeError):
        FileParser()

def test_subclass_must_implement_parse():
    class IncompleteParser(FileParser):
        pass
    
    with pytest.raises(TypeError):
        IncompleteParser()

def test_text_file_parser(tmp_path):
    f = tmp_path / "test.txt"
    content = "Hello, this is a test task."
    f.write_text(content)
    
    parser = TextFileParser()
    assert parser.parse(f) == content

def test_email_file_parser_eml(tmp_path):
    f = tmp_path / "test.eml"
    content = "Subject: Test\n\nThis is the body."
    f.write_text(content)
    
    parser = EmailFileParser()
    result = parser.parse(f)
    assert "This is the body." in result

def test_email_file_parser_eml_multipart(tmp_path):
    f = tmp_path / "test_multi.eml"
    msg = EmailMessage()
    msg["Subject"] = "Test Multipart"
    msg.set_content("This is the plain text body.")
    msg.add_alternative("<html><body>This is HTML</body></html>", subtype="html")
    
    with open(f, "wb") as wb:
        wb.write(msg.as_bytes())
    
    parser = EmailFileParser()
    result = parser.parse(f)
    assert "This is the plain text body." in result
    assert "<html>" not in result

@patch("extract_msg.Message")
def test_email_file_parser_msg(mock_msg, tmp_path):
    f = tmp_path / "test.msg"
    f.write_text("dummy")
    
    mock_instance = mock_msg.return_value
    mock_instance.body = "This is a msg body."
    
    parser = EmailFileParser()
    result = parser.parse(f)
    assert "This is a msg body." in result

def test_email_file_parser_unsupported(tmp_path):
    f = tmp_path / "test.unknown"
    f.write_text("dummy")
    
    parser = EmailFileParser()
    with pytest.raises(ValueError, match="Unsupported email format"):
        parser.parse(f)