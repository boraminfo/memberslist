import os
import subprocess
from pathlib import Path
from datetime import datetime

# 📁 현재 디렉토리
base_dir = Path(__file__).parent

# 🔢 사용자 PC 선택
print("\n===============================")
print("🖥️  사용할 PC 환경을 선택하세요:")
print("[1] pc_home")
print("[2] pc_office")
print("[3] pc_pohang")
print("[4] pc_daejeon")
print("===============================")
pc_choice = input("번호를 입력하세요 (1~4): ").strip()

env_map = {
    "1": "pish_pc_home.env",
    "2": "pish_pc_office.env",
    "3": "pish_pc_pohang.env",
    "4": "pish_pc_daejeon.env"
}

if pc_choice not in env_map:
    print("❌ 잘못된 선택입니다. 종료합니다.")
    exit(1)

env_file = base_dir / env_map[pc_choice]

# 🌱 환경 변수 로드
env_vars = {}
with open(env_file, encoding="utf-8") as f:
    for line in f:
        if "=" in line and not line.strip().startswith("#"):
            key, val = line.strip().split("=", 1)
            env_vars[key.strip()] = val.strip()

# 🔐 사용자 계정 선택
print("\n===============================")
print("🔐 Git 사용자 계정을 선택하세요:")
print(f"[1] {env_vars.get('USER1_NAME')}")
print(f"[2] {env_vars.get('USER2_NAME')}")
print(f"[3] {env_vars.get('USER3_NAME')}")
print("===============================")
choice = input("번호를 입력하세요 (1~3): ").strip()

if choice not in {"1", "2", "3"}:
    print("❌ 잘못된 선택입니다.")
    exit(1)

ssh_key = env_vars.get(f"USER{choice}_SSH")
remote_url = env_vars.get(f"USER{choice}_REMOTE")

# 🔐 SSH 키 확인
if not Path(ssh_key).exists():
    print(f"❌ SSH 키 파일이 존재하지 않습니다: {ssh_key}")
    exit(1)

# 🔐 SSH 키 등록
print(f"🔐 SSH 키 등록 중: {ssh_key}")
subprocess.run("ssh-agent", shell=True)
subprocess.run(f'ssh-add "{ssh_key}"', shell=True)

# 🔁 Git pull
print("\n🔄 git pull 실행 중...")
subprocess.run("git pull", shell=True)

# 💬 커밋 메시지 입력
commit_msg = input("💬 커밋 메시지를 입력하세요 (기본값: 자동 커밋): ").strip()
if not commit_msg:
    commit_msg = "자동 커밋"

# 🚀 Git push
print("\n📦 Git 작업 시작...")
subprocess.run("git add .", shell=True)
subprocess.run(f'git commit -m "{commit_msg}"', shell=True)
subprocess.run(f"git push {remote_url}", shell=True)
