import re

class TextNormalizer:
    @staticmethod
    def normalize(text: str) -> str:
        if not text:
            return ""
        # Remove weird bullets and symbols
        text = re.sub(r"[¢•·▪■○●]", "", text)
        # Remove 'e' used as bullet point at start of lines
        text = re.sub(r"\ne\s+", "\n", text)
        text = re.sub(r"^e\s+", "", text)
        # Normalize multiple spaces
        text = re.sub(r"[ \t]+", " ", text)
        # Normalize multiple line breaks
        text = re.sub(r"\n{3,}", "\n\n", text)
        # Trim spaces per line
        lines = [line.strip() for line in text.split("\n")]
        return "\n".join(lines)
