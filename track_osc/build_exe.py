import subprocess

def main():
    subprocess.run([
        "pyinstaller",
        "--onefile",
        "track_osc/cli.py",
        "-n",
        "track-osc"
    ])
