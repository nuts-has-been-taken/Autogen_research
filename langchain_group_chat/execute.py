import os
import sys
import subprocess
from concurrent.futures import ThreadPoolExecutor

def execute_code(code: str):
    code = code.strip('python')
    filepath = os.path.join('./', 'test.py')
    with open(filepath, "w", encoding="utf-8") as fout:
            fout.write(code)
    cmd = [
            sys.executable,
            'test.py',
        ]
    with ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(
            subprocess.run,
            cmd,
            cwd='./',
            capture_output=True,
            text=True,
        )
        result = future.result(timeout=10)
    logs = result.stdout
    return logs