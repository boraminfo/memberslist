import subprocess
import sys
from pathlib import Path

def run_generate_ssh_config():
    print("🛠 SSH config 생성 중...")
    subprocess.run([sys.executable, str(Path("generate_ssh_config.py"))], check=True)

def run_set_git_user():
    print("\n🔧 Git 사용자 설정 중...")
    subprocess.run([sys.executable, str(Path("set_git_user/set_git_user.py"))], check=True)

def main():
    run_generate_ssh_config()
    run_set_git_user()

if __name__ == "__main__":
    main()
