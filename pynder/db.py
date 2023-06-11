# Copyright 2023 Michele Schimd

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==========================================================================

"""Database management helper functions."""
import sqlite3

def has_table(db: sqlite3.Connection, table: str) -> bool:
    result = db.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table}';")
    table_exists = result.fetchone() is not None
    return table_exists

def has_schema(cur) -> bool:
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='file';")
    table_exists = cur.fetchone() is not None
    return table_exists

def file_exists(db: sqlite3.Connection, md5: str) -> bool:
    return False

def repository_by_path(db: sqlite3.Connection, path: str) -> list[tuple]:
    """Returns all repositories matching the given path.

    Args:
        db (sqlite3.Connection): The DB to run the query on.
        path (str): The path to match.

    Returns:
        list[tuple]: The list of tuples matching the given path on the given DB.
    """
    return []

def create_schema(db: sqlite3.Connection, script: str=None):
    """Creates a schema, if not already existing.
    
    The function checks if the schema exists using `has_schema()` function.
    If the schema is not detected this way, it is created with the `script`
    passed (resorting to the default one this is none).

    Args:
        db (sqlite3.Connection): A connection to the database.
        script (str, optional): Path to the creation script. Defaults to None (default script).
    """
    if has_schema(db.cursor()):
        return
    cur = db.cursor()
    if not script:
        script = open("./sql/schema.sql").read()
    cur.executescript(script)
    
def add_file(db: sqlite3.Connection, md5: str, publication: int=None, repository: int=None, path: str=None):
    if (file_exists(md5)):
        return 0
    cur = db.cursor()
    cur.execute(
        "INSERT INTO file VALUES (?, ?);",
        (md5, publication)
    )
    if repository:
        cur.execute(
            "INSERT INTO repository_file VALUES(?, ?, ?);",
            (repository, md5, path)
        )
    db.commit()
    return cur.rowcount

def add_repository(db: sqlite3.Connection, path: str, description: str) -> int:
    """Adds a new repository to the give database.
    
    The functions adds the repository creating a new tuple with primary
    key given by the row number in the database. This id is returned by
    the function. Notice that this function always inserts a new tuple
    even if an identical path already exists in the DB. This can be useful
    since the same path could exists in different volumes (e.g. local disk
    and external drive or USB pen), in which case one really wants to have
    distinct repository. The description column can be used to discriminate
    between two or more repository with the same path. 
    
    If one wants to prevent insertion when the path already exists, then
    they must call `repository_by_path` first to check the existence of a
    tuple with the given path and possibly not calling this function if the
    path is found in the DB.

    Args:
        db (sqlite3.Connection): A connection to the database
        path (str): The path of the repository to add.
        description (str): The description of the repository to add.

    Returns:
        int: The id used as key of the newly inserted repository.
    """
    cur = db.cursor()
    cur.execute(
        "INSERT INTO repository (description, path) VALUES (?, ?);",
        (description, path)
    )
    db.commit()
    return cur.lastrowid

def list_of_files(db: sqlite3.Connection) -> list:
    result = db.execute(f"SELECT md5 FROM file;")
    return [row[0] for row in result]

def list_of_repository(db: sqlite3.Connection) -> list:
    result = db.execute(f"SELECT * FROM repository")
    return result.fetchall()