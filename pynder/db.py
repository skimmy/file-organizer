import sqlite3

FILE_TABLE_NAME = "file"
PUBLICATION_TABLE_NAME = "publication"
TOPIC_TABLE_NAME = "topic"
AUTHOR_TABLE_NAME = "author"

def has_schema(cur):
    cur.execute(f"SELECT name FROM sqlite_master WHERE type='{FILE_TABLE_NAME}' AND name='file';")
    table_exists = cur.fetchone() is not None
    return table_exists
    

def create_schema(db_path, script=None):
    db = sqlite3.connect(db_path)
    if has_schema(db.cursor()):
        return
    cur = db.cursor()
    if not script:
        script = open("./sql/schema.sql").read()
    print(script)
    cur.executescript(script)

def list_of_files(db_path):
    db = sqlite3.connect(db_path)
    result = db.execute(f"SELECT md5 FROM {FILE_TABLE_NAME};")
    return [row[0] for row in result]

