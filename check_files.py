import ast
import os

def check_file(filepath):
    if not filepath.endswith('.py'):
        return
    try:
        with open(filepath, 'r') as f:
            content = f.read()
    except:
        return
        
    try:
        tree = ast.parse(content)
    except SyntaxError:
        print(f"SyntaxError in {filepath}")
        return

    meaningful_nodes = 0
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.Import, ast.ImportFrom, ast.Pass, ast.Load, ast.Store, ast.Expr, ast.Constant)):
            continue
                
        meaningful_nodes += 1

    if meaningful_nodes < 5:
        print(f"Low functionality ({meaningful_nodes} nodes): {filepath}")


dirs_to_check = ['python-data-tools', 'engineering-mathematics', 'machine-learning', 'ml-course', 'neat', 'game-ai']

for d in dirs_to_check:
    for root, dirs, files in os.walk(d):
        if '.venv' in root or '.git' in root or '.idea' in root:
            continue
        for f in files:
            check_file(os.path.join(root, f))
