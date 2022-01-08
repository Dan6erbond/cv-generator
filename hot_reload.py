import os
import subprocess
import sys
import time

import pathspec

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: hot_reload.py <file> <args>")
        sys.exit(1)

    file_path = sys.argv[1]
    if not os.path.isfile(file_path):
        print("File not found:", file_path)
        sys.exit(1)

    dir_path = os.path.abspath(os.path.dirname(file_path))

    spec: pathspec.PathSpec = None
    if os.path.exists(os.path.join(dir_path, ".gitignore")):
        spec = pathspec.PathSpec.from_lines(
            pathspec.patterns.GitWildMatchPattern,
            open(os.path.join(dir_path, ".gitignore")),
        )

    last_mtime: float = None
    while True:
        should_reload = False
        for root, dirs, files in os.walk(dir_path):
            for f in files:
                if os.path.join(root, f) == os.path.abspath(__file__):
                    continue
                if os.path.join(root, f) == os.path.abspath(os.path.join(dir_path, ".gitignore")):
                    continue
                if ".git" in root:
                    continue
                if spec and spec.match_file(os.path.relpath(os.path.join(root, f), dir_path)):
                    continue
                mtime = os.stat(os.path.join(root, f)).st_mtime
                if last_mtime is None:
                    last_mtime = mtime
                    should_reload = True
                elif mtime > last_mtime:
                    print("Reloading:", f)
                    last_mtime = mtime
                    should_reload = True
        if should_reload:
            subprocess.call([sys.executable, file_path, *sys.argv[2:]])
        time.sleep(1)
