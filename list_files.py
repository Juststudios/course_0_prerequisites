import os

base_dir = '/home/settings/Documents/pearl'
ignore = ['.venv', '.git', '__pycache__', '.pytest_cache', '.idea', '.vscode', 'hshs']
include_dirs = ['python-data-tools', 'engineering-mathematics', 'machine-learning', 'ml-course', 'neat', 'game-ai']

def print_tree(directory, prefix=""):
    try:
        entries = sorted(os.listdir(directory))
    except:
        return
    for i, entry in enumerate(entries):
        if entry in ignore:
            continue
        path = os.path.join(directory, entry)
        is_last = i == len(entries) - 1
        connector = "└── " if is_last else "├── "
        print(f"{prefix}{connector}{entry}")
        if os.path.isdir(path):
            new_prefix = prefix + ("    " if is_last else "│   ")
            print_tree(path, new_prefix)

for d in include_dirs:
    print(d)
    print_tree(os.path.join(base_dir, d))
