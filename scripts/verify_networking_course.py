import os
import re
from pathlib import Path

BASE = Path("/home/settings/Documents/pearl/networking")

REQUIRED_HEADERS = [
    r"^# .*$",
    r"^## What You Will Learn\s*$",
    r"^## Prerequisites\s*$",
    r"^## Key Terminology\s*$",
    r"^## The Problem\s*$",
    r"^## How It Works\s*$",
    r"^## Intuition\s*$",
    r"^## Technical Explanation\s*$",
    r"^## Example\s*$",
    r"^## Python Implementation\s*$",
    r"^## What Happens Underneath\s*$",
    r"^## Common Mistakes\s*$",
    r"^## Security Considerations\s*$",
    r"^## Real-World Applications\s*$",
    r"^## AI-Agent Connection\s*$",
    r"^## Exercises\s*$",
    r"^## Challenge\s*$",
    r"^## Summary\s*$",
    r"^## What You Should Know Before Moving On\s*$"
]

def verify_module(mod_path):
    issues = []
    
    # Check README
    readme_path = mod_path / "README.md"
    if not readme_path.exists():
        return ["Missing README.md"]
    
    content = readme_path.read_text(encoding="utf-8")
    for pattern in REQUIRED_HEADERS:
        if not re.search(pattern, content, re.MULTILINE):
            issues.append(f"Missing header matching: {pattern}")
            
    # Check exercises
    exercises_path = mod_path / "exercises.py"
    if not exercises_path.exists():
        issues.append("Missing exercises.py")
    else:
        ex_content = exercises_path.read_text(encoding="utf-8")
        if "NotImplementedError" not in ex_content and "TODO" not in ex_content:
            issues.append("exercises.py missing scaffolding (NotImplementedError or TODO)")
            
    # Check solutions
    solutions_path = mod_path / "solutions.py"
    if not solutions_path.exists():
        issues.append("Missing solutions.py")

    return issues

def main():
    if not BASE.exists():
        print(f"Error: {BASE} does not exist.")
        return

    modules = sorted([d for d in BASE.iterdir() if d.is_dir() and d.name[0].isdigit()])
    print(f"Found {len(modules)} modules.")
    
    all_passed = True
    for mod in modules:
        issues = verify_module(mod)
        if issues:
            all_passed = False
            print(f"❌ {mod.name}")
            for issue in issues:
                print(f"   - {issue}")
        else:
            print(f"✅ {mod.name}")

    if all_passed and len(modules) == 35:
        print("\nAll 35 modules passed verification!")
    else:
        print(f"\nVerification failed. {len(modules)}/35 modules found.")

if __name__ == "__main__":
    main()
