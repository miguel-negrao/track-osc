import subprocess

def main():
    subprocess.run([
        "pyinstaller",
        "--onefile",
        "mytool/cli.py"
    ])
