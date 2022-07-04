def bytes_to_megabytes(bytes: int) -> str:
    return f"{round(bytes / 1000 / 1000, 2):.2f}"
