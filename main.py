import subprocess

def run_script(script_name):
    result = subprocess.run(['python', script_name], capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print(f"Errors in {script_name}:\n", result.stderr)

if __name__ == "__main__":
    scripts = ['sync.py', 'async.py', 'parallel.py']
    
    for script in scripts:
        print(f"\n-------- Running {script}... -----------\n")
        run_script(script)
    print(f"Finished running {scripts}")
