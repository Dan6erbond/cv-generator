import os
import subprocess
import sys
import time
from typing import Optional

import pathspec

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: hot_reload.py <file> <args>")
        sys.exit(1)

    args = sys.argv[1:]

    file_path = args.pop(0)
    if not os.path.isfile(file_path):
        print("File not found:", file_path)
        sys.exit(1)

    dir_path = os.path.abspath(os.path.dirname(file_path))

    spec: pathspec.PathSpec = None

    ignore_file = ".cvignore" if os.path.exists(os.path.join(dir_path, ".cvignore")) else ".gitignore"
    for idx, arg in enumerate(args):
        if arg.startswith("--ignore-file="):
            ignore_file = "=".join(arg.split("=")[1:])
            args.pop(idx)
            break

    spec: Optional[pathspec.PathSpec] = None
    if os.path.exists(os.path.join(dir_path, ignore_file)):
        spec = pathspec.PathSpec.from_lines(
            pathspec.patterns.GitWildMatchPattern,
            open(os.path.join(dir_path, ignore_file)),
        )

    last_mtime: float = None
    while True:
        should_reload = False
        for root, dirs, files in os.walk(dir_path):
            for f in files:
                if os.path.join(root, f) == os.path.abspath(__file__):
                    continue
                if spec and spec.match_file(
                    os.path.relpath(os.path.join(root, f), dir_path)
                ):
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
                    break
            if should_reload:
                break
        if should_reload:
            subprocess.call([sys.executable, file_path, *args])
        time.sleep(0.5)
