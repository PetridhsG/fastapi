import os

EXCLUDE_DIRS = {"__pycache__", ".venv", ".git", "htmlcov", ".VSCodeCounter"}
EXCLUDE_EXTS = {".pyc", ".pyo"}


def tree(dir_path, prefix=""):
    entries = []
    for e in sorted(os.listdir(dir_path)):
        path = os.path.join(dir_path, e)
        if os.path.isdir(path) and e in EXCLUDE_DIRS:
            continue
        if os.path.isfile(path) and os.path.splitext(e)[1] in EXCLUDE_EXTS:
            continue
        entries.append(e)

    pointers = ["├── "] * (len(entries) - 1) + ["└── "]

    for pointer, name in zip(pointers, entries):
        path = os.path.join(dir_path, name)
        print(prefix + pointer + name)
        if os.path.isdir(path):
            extension = "│   " if pointer == "├── " else "    "
            tree(path, prefix + extension)


with open("structure.txt", "w", encoding="utf-8") as f:
    import sys

    sys.stdout = f
    tree(".")
