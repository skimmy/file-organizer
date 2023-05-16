import hashlib
import os

def hash_file(path, algorithm="md5"):
    if not os.path.isfile(path):
        raise IOError(f'File not found: ${path}')
    content = None
    with open(path, 'rb') as f:
        content = f.read()
    if not content:
        raise Exception('Unable to read file content')
    h = hashlib.new(algorithm)
    h.update(content)
    return h.hexdigest()