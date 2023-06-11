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

"""Utility function to interact with the file system."""
import hashlib
import os

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


def hash_file(path: str, algorithm: str="md5") -> str:
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


def db_for_dir(dir_path):
    files = []
    for_each_file(dir_path, lambda x: files.append(
        (hash_file(x), x)), recursive=True)
    return files