import sqlite3

FILE_TABLE_NAME = "file"
PUBLICATION_TABLE_NAME = "publication"
TOPIC_TABLE_NAME = "topic"
AUTHOR_TABLE_NAME = "author"

def has_table(db, table):
    result = db.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table}';")
    table_exists = result.fetchone() is not None
    return table_exists

def has_schema(cur):
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='file';")
    table_exists = cur.fetchone() is not None
    return table_exists

def create_schema(db, script=None):
    if has_schema(db.cursor()):
        return
    cur = db.cursor()
    if not script:
        script = open("./sql/schema.sql").read()
    cur.executescript(script)
    
def add_file(db, md5, path, publication=None):
    pass

def list_of_files(db):
    result = db.execute(f"SELECT md5 FROM file;")
    return [row[0] for row in result]

