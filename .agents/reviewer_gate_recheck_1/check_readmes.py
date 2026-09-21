import re
from pathlib import Path

modules = [
    "01_callables_and_functional_python",
    "02_classes_dunder_and_oop",
    "03_type_hints_and_pydantic",
    "04_async_and_event_loops",
    "05_contextvars_and_state",
    "06_http_and_rest_apis",
    "07_json_and_schema_validation",
    "08_config_management",
    "09_subprocesses_and_sandboxing",
    "10_sqlite_and_memory",
    "11_architecture_patterns",
    "12_prompt_templating",
    "13_logging_and_observability",
    "14_streaming_and_sse",
    "15_math_bridges",
]

base_dir = Path("/home/settings/Documents/pearl/course_0_prerequisites")

all_concepts_valid = True
total_concepts = 0

for mod in modules:
    readme = base_dir / mod / "README.md"
    content = readme.read_text(encoding="utf-8")
    
    concept_headers = list(re.finditer(r"###\s+Concept\s+\d+:\s*(.*)", content))
    if not concept_headers:
        print(f"ERROR: {mod} has no concept headers!")
        all_concepts_valid = False
        continue
        
    print(f"\n--- {mod} ({len(concept_headers)} concepts) ---")
    for i, ch in enumerate(concept_headers):
        total_concepts += 1
        start = ch.start()
        end = concept_headers[i+1].start() if i+1 < len(concept_headers) else len(content)
        next_sec = re.search(r"\n##\s+", content[start+len(ch.group()):end])
        if next_sec:
            end = start + len(ch.group()) + next_sec.start()
        
        block = content[start:end]
        cname = ch.group(1).strip()
        
        tags = ["**TERM**", "**DEFINITION**", "**INTUITION**", "**WHY IT EXISTS**", "**HOW IT WORKS**", "**CODE**"]
        tag_positions = []
        missing = []
        for tag in tags:
            idx = block.find(tag)
            if idx == -1:
                missing.append(tag)
            else:
                tag_positions.append((tag, idx))
                
        if missing:
            print(f"  FAIL: Concept '{cname}' missing {missing}")
            all_concepts_valid = False
        else:
            sorted_tags = [t[0] for t in sorted(tag_positions, key=lambda x: x[1])]
            if sorted_tags != tags:
                print(f"  FAIL: Concept '{cname}' wrong order: {sorted_tags}")
                all_concepts_valid = False
            else:
                code_idx = block.find("**CODE**")
                has_python = "```python" in block[code_idx:]
                if not has_python:
                    print(f"  FAIL: Concept '{cname}' missing ```python after **CODE**")
                    all_concepts_valid = False
                else:
                    print(f"  OK: Concept {i+1} '{cname}'")

print(f"\nTotal concepts examined: {total_concepts}")
print(f"All concepts follow TERM -> DEFINITION -> INTUITION -> WHY IT EXISTS -> HOW IT WORKS -> CODE: {all_concepts_valid}")
