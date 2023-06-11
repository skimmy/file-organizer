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

"""Tasks performed by the software."""
from collections.abc import Callable
import sqlite3

import pynder.db as dbu

def scan_and_add_directory(db: sqlite3.Connection, path: str, f_condition: Callable[[str], bool]) -> int:
    """Scans a directory adding files passing a given condition.
    
    Starts at the directory indicated by `path` and recursively considers
    each file it encounters. The file path is passed to the `f_condition`
    callable and it is added to the database only if the callable returns
    `True`. If such callable is not indicated, each file is processed and
    added to the database.

    Args:
        db (sqlite3.Connection): The target database
        path (str): The path of the scanned directory
        f_condition (Callable: A callable that indicates whether to consider or not a file.
        
    Returns:
        int: The total number of rows added to the 'file' table.
    """
    pass

def add_repo(db: sqlite3.Connection, path: str, desc: str, allow_duplicate: bool=False) -> int | None:
    """Adds a repository to the database.
    
    It first checks whether a repository exists with the same path.
    If so, the function inserts a new repository if `allow_duplicate`
    is `True` otherwise if doesn't change the database.
    
    The functions return the id of the repository that has been added or
    `None` if nothing has been added to the DB.

    Args:
        db (sqlite3.Connection): The target database.
        path (str): The path of the repository to add.
        desc (str): The description of the repository.
        allow_duplicate(bool): Whether or not inserts if path already exists. Defaults to `False`.

    Returns:
        int: The id of the newly added repository, `None` if nothing is added.
    """
    # Checks the existence of the path
    repo = dbu.repository_by_path(db, path)
    if (len(repo) != 0) and (not allow_duplicate):
        return None
    # add repo
    newId = dbu.add_repository(db=db, path=path, description=desc)
    return newId
    
