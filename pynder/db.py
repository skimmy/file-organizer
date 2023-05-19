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

def create_schema(db: sqlite3.Connection, script: str=None):
    """_summary_

    Args:
        db (sqlite3.Connection): _description_
        script (str, optional): _description_. Defaults to None.
    """
    if has_schema(db.cursor()):
        return
    cur = db.cursor()
    if not script:
        script = open("./sql/schema.sql").read()
    cur.executescript(script)
    
def add_file(db: sqlite3.Connection, md5: str, path: str, publication: int=None):
    pass

def list_of_files(db: sqlite3.Connection) -> list:
    result = db.execute(f"SELECT md5 FROM file;")
    return [row[0] for row in result]

