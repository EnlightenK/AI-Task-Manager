from abc import ABC, abstractmethod
from pathlib import Path
import email
from email import policy
import extract_msg

class FileParser(ABC):
    @abstractmethod
    def parse(self, file_path: Path) -> str:
        """Extract text content from the given file."""
        pass

class TextFileParser(FileParser):
    def parse(self, file_path: Path) -> str:
        return file_path.read_text(encoding="utf-8")

class EmailFileParser(FileParser):
    def parse(self, file_path: Path) -> str:
        suffix = file_path.suffix.lower()
        if suffix == ".msg":
            msg = extract_msg.Message(str(file_path))
            return msg.body
        elif suffix == ".eml":
            with open(file_path, "rb") as f:
                msg = email.message_from_binary_file(f, policy=policy.default)
            
            body = ""
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == "text/plain":
                        body += part.get_payload(decode=True).decode(part.get_content_charset() or "utf-8")
            else:
                body = msg.get_payload(decode=True).decode(msg.get_content_charset() or "utf-8")
            return body
        else:
            raise ValueError(f"Unsupported email format: {suffix}")
