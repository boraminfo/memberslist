import os
import subprocess
from pathlib import Path

# ✅ 사용자 이름 감지
user_name = os.getlogin()
env_path = Path(f"./pish_pc_{user_name}.env")

# ✅ 환경 파일 존재 여부 확인
if not env_path.exists():
    print(f"❌ 환경 파일이 없습니다: {env_path}")
    print("pish_pc_사용자명.env 파일을 준비해 주세요.")
    exit(1)

# ✅ .env 파일 로드
env_vars = {}
with open(env_path, encoding="utf-8") as f:
    for line in f:
        if "=" in line and not line.strip().startswith("#"):
            key, val = line.strip().split("=", 1)
            env_vars[key.strip()] = val.strip()

# ✅ Git 사용자 선택
print("\n🔐 Git 사용자 계정을 선택하세요:")
print(f"[1] {env_vars['USER1_NAME']}")
print(f"[2] {env_vars['USER2_NAME']}")
print(f"[3] {env_vars['USER3_NAME']}")
choice = input("번호를 입력하세요 (1~3): ").strip()

if choice not in {"1", "2", "3"}:
    print("❌ 잘못된 선택입니다.")
    exit(1)

ssh_key = env_vars[f"USER{choice}_SSH"]
remote_url = env_vars[f"USER{choice}_REMOTE"]

# ✅ SSH 등록
print(f"🔐 SSH 키 등록 중: {ssh_key}")
subprocess.run("ssh-agent", shell=True)
subprocess.run(f'ssh-add "{ssh_key}"', shell=True)

# ✅ Git push 실행
print("📦 Git 작업 시작...")
subprocess.run("git add .", shell=True)
subprocess.run('git commit -m "자동 커밋"', shell=True)
subprocess.run(f"git push {remote_url}", shell=True)
