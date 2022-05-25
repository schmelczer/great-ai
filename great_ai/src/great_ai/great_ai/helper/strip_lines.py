def strip_lines(text: str) -> str:
    return "\n".join(line.strip() for line in text.split("\n"))
