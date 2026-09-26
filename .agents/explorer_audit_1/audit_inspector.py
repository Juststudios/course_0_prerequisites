#!/usr/bin/env python3
"""
Deep inspection script for Course -1 audit.
Analyzes all 33 modules for exact header order, line counts, comment ratios,
print counts, exercise tiers, solution executability, and failure causes.
"""

import json
import os
import re
import subprocess
import sys
from pathlib import Path

COURSE_DIR = Path("/home/settings/Documents/pearl/course_-1_python_foundations")
REPO_ROOT = Path("/home/settings/Documents/pearl")
sys.path.insert(0, str(REPO_ROOT))

EXPECTED_HEADERS = [
    (1, "Topic", re.compile(r"^#\s+(?:Topic\b|[A-Za-z0-9])", re.IGNORECASE)),
    (2, "What You Will Learn", re.compile(r"^##\s+What You Will Learn", re.IGNORECASE)),
    (3, "Prerequisites", re.compile(r"^##\s+Prerequisites", re.IGNORECASE)),
    (4, "The Problem", re.compile(r"^##\s+The Problem", re.IGNORECASE)),
    (5, "Key Terminology", re.compile(r"^##\s+Key Terminology", re.IGNORECASE)),
    (6, "Intuition", re.compile(r"^##\s+Intuition", re.IGNORECASE)),
    (7, "Concept", re.compile(r"^##\s+Concept", re.IGNORECASE)),
    (8, "Syntax", re.compile(r"^##\s+Syntax", re.IGNORECASE)),
    (9, "Example", re.compile(r"^##\s+Example", re.IGNORECASE)),
    (10, "Line-by-Line Explanation", re.compile(r"^##\s+Line-by-Line Explanation", re.IGNORECASE)),
    (11, "What Python Is Doing", re.compile(r"^##\s+What Python Is Doing", re.IGNORECASE)),
    (12, "Common Mistakes", re.compile(r"^##\s+Common Mistakes", re.IGNORECASE)),
    (13, "Real-World Uses", re.compile(r"^##\s+Real-World Uses", re.IGNORECASE)),
    (14, "Connection to AI Agents", re.compile(r"^##\s+Connection to AI Agents", re.IGNORECASE)),
    (15, "Practice", re.compile(r"^##\s+Practice", re.IGNORECASE)),
    (16, "Challenge", re.compile(r"^##\s+Challenge", re.IGNORECASE)),
    (17, "Summary", re.compile(r"^##\s+Summary", re.IGNORECASE)),
    (18, "What You Should Know Before Moving On", re.compile(r"^##\s+What You Should Know Before Moving On", re.IGNORECASE)),
]

MILESTONES = {
    "01": "M1", "02": "M1", "03": "M1", "04": "M1", "05": "M1", "06": "M1",
    "07": "M2", "08": "M2", "09": "M2", "10": "M2", "11": "M2",
    "12": "M3", "13": "M3", "14": "M3", "15": "M3", "16": "M3",
    "17": "M4", "18": "M4", "19": "M4", "20": "M4", "21": "M4", "22": "M4",
    "23": "M5", "24": "M5", "25": "M5", "26": "M5", "27": "M5", "28": "M5", "29": "M5",
    "30": "M6", "31": "M6", "32": "M6", "33": "M6",
}

EXERCISE_LEVEL_PATTERNS = [
    ("Recall", re.compile(r"(?:level\s*1|tier\s*1|#.*recall|\brecall\b)", re.IGNORECASE)),
    ("Modify", re.compile(r"(?:level\s*2|tier\s*2|#.*modify|\bmodify\b)", re.IGNORECASE)),
    ("Build", re.compile(r"(?:level\s*3|tier\s*3|#.*build|\bbuild\b)", re.IGNORECASE)),
    ("Debug", re.compile(r"(?:level\s*4|tier\s*4|#.*debug|\bdebug\b)", re.IGNORECASE)),
]

def analyze_module(mod_dir: Path):
    prefix = mod_dir.name[:2]
    result = {
        "prefix": prefix,
        "name": mod_dir.name,
        "milestone": MILESTONES.get(prefix, "UNKNOWN"),
        "readme": {},
        "lesson": {},
        "exercises": {},
        "solutions": {},
        "overall_status": "PASS"
    }

    # 1. Analyze README
    readme_path = mod_dir / "README.md"
    if not readme_path.exists():
        result["readme"] = {
            "exists": False,
            "lines": 0,
            "words": 0,
            "headers_present": 0,
            "missing_headers": [h[1] for h in EXPECTED_HEADERS],
            "in_order": False,
            "error": "README.md missing"
        }
        result["overall_status"] = "FAIL"
    else:
        content = readme_path.read_text(encoding="utf-8")
        lines = content.splitlines()
        words = len(content.split())
        
        # Check presence and order of headers
        found_indices = []
        found_names = []
        missing_names = []
        
        # Track line positions of headers
        header_positions = []
        for line_num, line in enumerate(lines):
            for hid, hname, pat in EXPECTED_HEADERS:
                if pat.search(line.strip()):
                    header_positions.append((line_num, hid, hname))
                    break

        # Deduplicate positions keeping first match for each hid
        seen_hids = set()
        dedup_positions = []
        for pos, hid, hname in header_positions:
            if hid not in seen_hids:
                seen_hids.add(hid)
                dedup_positions.append((pos, hid, hname))

        found_hids = [hid for _, hid, _ in dedup_positions]
        for hid, hname, _ in EXPECTED_HEADERS:
            if hid in seen_hids:
                found_names.append(hname)
            else:
                missing_names.append(hname)

        # Check if in exact order
        in_order = found_hids == sorted(found_hids) and len(found_hids) == 18

        result["readme"] = {
            "exists": True,
            "lines": len(lines),
            "words": words,
            "headers_present": len(found_names),
            "missing_headers": missing_names,
            "in_order": in_order,
            "passed": (len(missing_names) == 0 and in_order)
        }
        if not result["readme"]["passed"]:
            result["overall_status"] = "FAIL"

    # 2. Analyze Lesson
    from scripts.verify_course_minus_1 import find_main_lesson_file
    lesson_path = find_main_lesson_file(mod_dir)
    if not lesson_path or not lesson_path.exists():
        result["lesson"] = {
            "exists": False,
            "filename": None,
            "lines": 0,
            "comments": 0,
            "prints": 0,
            "exit_code": None,
            "passed": False,
            "error": "Main lesson script not found"
        }
        result["overall_status"] = "FAIL"
    else:
        try:
            l_content = lesson_path.read_text(encoding="utf-8")
            l_lines = l_content.splitlines()
            l_comments = sum(1 for line in l_lines if line.strip().startswith("#"))
            l_prints = sum(1 for line in l_lines if "print(" in line)
            
            # Execution
            env = os.environ.copy()
            env["PYTHONPATH"] = f"{REPO_ROOT}:{mod_dir}"
            proc = subprocess.run(
                [sys.executable, str(lesson_path)],
                cwd=str(mod_dir),
                capture_output=True,
                text=True,
                timeout=15,
                env=env
            )
            passed = len(l_lines) >= 150 and proc.returncode == 0
            result["lesson"] = {
                "exists": True,
                "filename": lesson_path.name,
                "lines": len(l_lines),
                "comments": l_comments,
                "prints": l_prints,
                "exit_code": proc.returncode,
                "stderr": proc.stderr[:300] if proc.stderr else "",
                "passed": passed
            }
            if not passed:
                result["overall_status"] = "FAIL"
        except Exception as e:
            result["lesson"] = {
                "exists": True,
                "filename": lesson_path.name,
                "lines": 0,
                "passed": False,
                "error": str(e)
            }
            result["overall_status"] = "FAIL"

    # 3. Analyze Exercises
    ex_path = mod_dir / "exercises.py"
    if not ex_path.exists():
        result["exercises"] = {
            "exists": False,
            "lines": 0,
            "found_levels": [],
            "missing_levels": ["Recall", "Modify", "Build", "Debug"],
            "todo_count": 0,
            "not_implemented_count": 0,
            "passed": False,
            "error": "exercises.py missing"
        }
        result["overall_status"] = "FAIL"
    else:
        try:
            ex_content = ex_path.read_text(encoding="utf-8")
            found_levels = []
            missing_levels = []
            for lname, pat in EXERCISE_LEVEL_PATTERNS:
                if pat.search(ex_content):
                    found_levels.append(lname)
                else:
                    missing_levels.append(lname)
            todos = len(re.findall(r"#\s*TODO\b", ex_content, re.IGNORECASE))
            not_impls = len(re.findall(r"\bNotImplementedError\b", ex_content))
            passed = (len(missing_levels) == 0) and (todos > 0) and (not_impls > 0)
            result["exercises"] = {
                "exists": True,
                "lines": len(ex_content.splitlines()),
                "found_levels": found_levels,
                "missing_levels": missing_levels,
                "todo_count": todos,
                "not_implemented_count": not_impls,
                "passed": passed
            }
            if not passed:
                result["overall_status"] = "FAIL"
        except Exception as e:
            result["exercises"] = {"exists": True, "passed": False, "error": str(e)}
            result["overall_status"] = "FAIL"

    # 4. Analyze Solutions
    sol_path = mod_dir / "solutions.py"
    if not sol_path.exists():
        result["solutions"] = {
            "exists": False,
            "lines": 0,
            "exit_code": None,
            "passed": False,
            "error": "solutions.py missing"
        }
        result["overall_status"] = "FAIL"
    else:
        try:
            s_content = sol_path.read_text(encoding="utf-8")
            s_lines = s_content.splitlines()
            
            # Check execution
            env = os.environ.copy()
            env["PYTHONPATH"] = f"{REPO_ROOT}:{mod_dir}"
            proc = subprocess.run(
                [sys.executable, str(sol_path)],
                cwd=str(mod_dir),
                capture_output=True,
                text=True,
                timeout=15,
                env=env
            )
            passed = len(s_lines) >= 10 and proc.returncode == 0
            result["solutions"] = {
                "exists": True,
                "lines": len(s_lines),
                "exit_code": proc.returncode,
                "stderr": proc.stderr[:300] if proc.stderr else "",
                "passed": passed
            }
            if not passed:
                result["overall_status"] = "FAIL"
        except Exception as e:
            result["solutions"] = {"exists": True, "passed": False, "error": str(e)}
            result["overall_status"] = "FAIL"

    return result

def main():
    modules = sorted([d for d in COURSE_DIR.iterdir() if d.is_dir() and re.match(r"^\d{2}_", d.name)])
    all_results = [analyze_module(m) for m in modules]
    
    out_file = Path("/home/settings/Documents/pearl/.agents/explorer_audit_1/detailed_audit.json")
    out_file.write_text(json.dumps(all_results, indent=2), encoding="utf-8")
    print(f"Detailed audit saved to {out_file}. Total modules: {len(all_results)}")
    
    # Summary stats
    pass_cnt = sum(1 for r in all_results if r["overall_status"] == "PASS")
    print(f"Passing: {pass_cnt}/{len(all_results)}")

if __name__ == "__main__":
    main()
