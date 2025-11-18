import re
from pathlib import Path

def secure_filename(filename: str) -> str:
    name = Path(filename).name
    # Replace spaces and dangerous chars
    name = re.sub(r"[^A-Za-z0-9._-]", "_", name)
    return name
