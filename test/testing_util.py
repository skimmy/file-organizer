import random

def random_file_name(prefix: str=".test", ext: str=None, separator: str= "_") -> str:
    rand = random.randint(100000000, 999999999)
    extension = ""
    if ext:
        extension=f".{ext}"
    return f"{prefix}{separator}{rand}{extension}"