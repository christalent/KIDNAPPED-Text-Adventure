#!/usr/bin/env python3
"""Run every test file in this directory and report honestly.

The repo's test files are script-style (each has its own __main__ runner),
so `python3 -m unittest discover` collects ZERO tests and reports "OK".
This runner executes each file as a subprocess and fails loudly.

Usage: python3 tests/run_all.py
"""
import glob
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

failed = []
files = sorted(glob.glob(os.path.join(HERE, "test_*.py")))
for path in files:
    name = os.path.basename(path)
    p = subprocess.run([sys.executable, path], cwd=ROOT,
                       capture_output=True, text=True, timeout=600)
    ok = p.returncode == 0
    print(("PASS " if ok else "FAIL ") + name)
    if not ok:
        failed.append(name)
        tail = (p.stdout or "")[-2500:] + "\n" + (p.stderr or "")[-2500:]
        print(tail)

print()
print(f"{len(files) - len(failed)}/{len(files)} test files passed")
if failed:
    print("FAILED: " + ", ".join(failed))
sys.exit(1 if failed else 0)
