# python dedupe_research.py#!/usr/bin/env python3
"""
dedupe_research.py
Smart de-duplicator for your research Python files.
Only keeps ONE copy of every identical function/class.
"""

import ast
import hashlib
import os
from pathlib import Path
import difflib

SRC_DIR = Path(__file__).parent     # folder where script is located
BACKUP_DIR = SRC_DIR / "backup_before_dedupe"
BACKUP_DIR.mkdir(exist_ok=True)

def file_hash(path):
    """SHA256 of file bytes."""
    return hashlib.sha256(path.read_bytes()).hexdigest()

def get_definitions(code):
    """Return list of (type, name, start, end, source) for top-level defs."""
    tree = ast.parse(code)
    lines = code.splitlines(True)
    defs = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.AsyncFunctionDef)):
            start, end = node.lineno - 1, node.end_lineno
            src = ''.join(lines[start:end])
            defs.append((type(node).__name__, node.name, start, end, src))
    return defs

def unify():
    seen = {}   # (type, name) -> (file, src)
    removed_log = []
    for pyfile in SRC_DIR.glob("*.py"):
        if pyfile.name == __file__:   # skip self
            continue
        code = pyfile.read_text(encoding='utf-8', errors='ignore')
        defs = get_definitions(code)
        new_lines = code.splitlines(True)
        offset = 0
        for typ, name, start, end, src in defs:
            key = (typ, name)
            if key in seen:
                # exact duplicate? drop it
                if seen[key][1] == src:
                    del new_lines[start - offset : end - offset]
                    offset += (end - start)
                    removed_log.append(f"{pyfile.name}:{name} -> duplicate removed")
                # same name but different body – keep with file suffix
                else:
                    new_name = f"{name}_{pyfile.stem}"
                    new_lines[start - offset] = new_lines[start - offset].replace(name, new_name)
                    removed_log.append(f"{pyfile.name}:{name} -> renamed to {new_name}")
                    seen[(typ, new_name)] = (pyfile, src)
            else:
                seen[key] = (pyfile, src)
        # write back stripped file
        pyfile.rename(BACKUP_DIR / pyfile.name)     # backup
        (SRC_DIR / pyfile.name).write_text(''.join(new_lines), encoding='utf-8')
    # summary
    summary = "\n".join(removed_log) if removed_log else "No duplicates found."
    (SRC_DIR / "dedupe_log.txt").write_text(summary)
    print(summary)

if __name__ == "__main__":
    unify()
