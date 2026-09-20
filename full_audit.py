import os
import subprocess
import glob

def find_files(directories, extensions):
    matched_files = []
    for d in directories:
        for root, dirs, files in os.walk(d):
            if '.venv' in root or '.git' in root or '__pycache__' in root or '.pytest_cache' in root or '.idea' in root:
                continue
            for f in files:
                if any(f.endswith(ext) for ext in extensions):
                    matched_files.append(os.path.join(root, f))
    return matched_files

def check_placeholders(filepath):
    # If the file is specifically meant to have TODOs (like an exercise starter), we can skip strict checks
    is_starter = 'starter' in filepath or 'practice' in filepath or 'exercise' in filepath
    
    with open(filepath, 'r', encoding='utf-8') as f:
        try:
            lines = f.readlines()
        except UnicodeDecodeError:
            return [] # skip binary
            
    issues = []
    if not is_starter:
        for i, line in enumerate(lines):
            line_lower = line.lower()
            if 'todo' in line_lower:
                issues.append(f"Line {i+1}: Contains 'TODO'")
            if 'tbd' in line_lower:
                issues.append(f"Line {i+1}: Contains 'TBD'")
    
    # Check if file is suspiciously short (e.g. less than 5 lines for a Markdown file, unless it's a specific short file)
    if filepath.endswith('.md') and len(lines) < 5 and filepath.endswith('README.md'):
        issues.append("Markdown file is suspiciously short (less than 5 lines).")
        
    return issues

def run_flake8(directories):
    # F821: undefined name
    # E999: syntax error
    # F401: unused import
    cmd = ['flake8', '--select=E999,F821', '--exclude=.venv,.git,__pycache__'] + directories
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result.stdout.strip().split('\n') if result.stdout else []
    except Exception as e:
        return [str(e)]

def main():
    dirs = ['python-data-tools', 'engineering-mathematics', 'machine-learning', 'ml-course', 'neat', 'game-ai']
    
    print("=== STARTING FULL AUDIT ===")
    
    # 1. Static Analysis (Flake8)
    print("\n--- Running Flake8 Static Analysis (Syntax & Undefined Variables) ---")
    flake_errors = run_flake8(dirs)
    actual_errors = [e for e in flake_errors if e and 'flake8' not in e.lower()]
    if actual_errors:
        for err in actual_errors:
            print(err)
    else:
        print("No critical syntax or undefined variable errors found.")
        
    # 2. Text/Content Audit
    print("\n--- Content Audit (Placeholders & Stubs) ---")
    files = find_files(dirs, ['.py', '.md', '.m'])
    total_issues = 0
    for f in files:
        issues = check_placeholders(f)
        if issues:
            total_issues += len(issues)
            print(f"Issues in {f}:")
            for issue in issues:
                print(f"  - {issue}")
                
    if total_issues == 0:
        print("No unexpected TODOs, TBDs, or stubs found in non-starter files.")

    print("\n=== AUDIT COMPLETE ===")

if __name__ == '__main__':
    main()
