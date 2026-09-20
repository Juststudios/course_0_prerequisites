# Content Audit Execution Plan: Levels 1–7 Deep-Reading Audit

## Objective
Execute a deep-reading manual content audit of the entire educational curriculum repository across Levels 1 through 7 to evaluate actual instructional depth and generate a Master TODO list, strictly adhering to the "Non-Negotiable Inspection Protocol."

## Protocols & Constraints
1. **Deep-Reading Inspection Protocol**: Automated scripts (file counters, linters, TODO scanners) as a substitute for manual reading are strictly forbidden. No `audit.py` or equivalent scripts. Agents must open and read READMEs, Python scripts, and MATLAB files using file-reading tools.
2. **Mandatory Reading Record**: Every batch must record the exact file paths opened and read.
3. **Instructional Depth Evaluation**: Verify mathematical derivations, worked numerical examples, and from-scratch implementations rather than black-box library calls.
4. **Evidence-Based Judgments**: Zero status judgments based solely on file existence, file names, or compilation success. Every status (COMPLETE, PARTIAL, MISSING) must cite specific textual evidence.
5. **Master TODO List**: Actionable, granular tasks with exact target paths, missing components, and clear implementation specifications.
6. **No Project Modifications**: Do not modify project files during the audit.

## Phases and Steps

### Phase 1: Survey & Repository Mapping
- Step 1.1: Dispatch 3 parallel Explorers to survey the repository layout across Levels 1-7, locating all curriculum directories, specifications, syllabus files, and module structures.
- Step 1.2: Aggregate Explorer findings into `PROJECT.md § Feature & Curriculum Inventory`.
- Step 1.3: Confirm the exact level-to-directory mapping and establish the deep-reading batch schedule.

### Phase 2: Batch Deep-Reading Audits
- Step 2.1: Dispatch Batch 1 Audit (Level 1: Foundations)
- Step 2.2: Dispatch Batch 2 Audit (Level 2: Engineering Mathematics & MATLAB)
- Step 2.3: Dispatch Batch 3 Audit (Level 3: Machine Learning)
- Step 2.4: Dispatch Batch 4 Audit (Level 4: Deep Learning & Advanced Modules)
- Step 2.5: Dispatch Batch 5 Audit (Level 5: Specialized Topics / MLOps / Systems)
- Step 2.6: Dispatch Batch 6 Audit (Levels 6 & 7: Capstones, Advanced Research & Projects)

### Phase 3: Synthesis & Gap Analysis
- Step 3.1: Aggregate Mandatory Reading Records from all batches.
- Step 3.2: Construct the Curriculum Completion Matrix (Topic, Status, Evidence, Missing Elements).
- Step 3.3: Synthesize Major Gaps & Mathematics Coverage Analysis (derivations, worked examples, scratch vs black-box).
- Step 3.4: Formulate the Granular Prioritized Master TODO List (P0, P1, P2).

### Phase 4: Final Report & Verification
- Step 4.1: Compile the comprehensive Audit Report document.
- Step 4.2: Verify compliance with all acceptance criteria (reading records present, no automated scanner scripts used, textual evidence for all judgments, actionable tasks).
- Step 4.3: Present results and report completion to caller.
