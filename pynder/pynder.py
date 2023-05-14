import hashlib
import os
import sys
import sqlite3

def list_to_db(files, db_name):
    con = sqlite3.connect(db_name)
    cur = con.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='file';")
    table_exists = cur.fetchone() is not None
    if not table_exists:
        cur.execute("CREATE TABLE file (md5, path);")
    cur.executemany("INSERT INTO file VALUES(?, ?)", files)
    con.commit()
    con.close()

def md5_for_file(path):
    if not os.path.isfile(path):
        raise IOError(f'File not found: ${path}')
    content = None
    with open(path, 'rb') as f:
        content = f.read()
    if not content:
        raise Exception('Unable to read file content')
    h = hashlib.new('md5')
    h.update(content)
    return h.hexdigest()

def for_each_file(path, operation, recursive=True):
    dirs = []
    for item in os.scandir(path):
        if item.is_dir():
            dirs.append(item.path)
        if item.is_file(follow_symlinks=False):
            operation(item.path)
    if recursive:
        for d in dirs:
            for_each_file(d, operation, recursive)
            
def db_for_dir(dir_path, db_path):
    files = []
    for_each_file(dir_path, lambda x: files.append((md5_for_file(x), x)), recursive=True)
    list_to_db(files, db_path)

def main():
    db_for_dir(sys.argv[1], sys.argv[2])
 

if __name__ == '__main__':
    main()