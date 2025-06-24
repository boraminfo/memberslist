import os
import subprocess
import shutil
from pathlib import Path

# ✅ .git 디렉토리 강제 삭제 함수
def safe_rmtree(path):
    try:
        shutil.rmtree(path)
    except PermissionError:
        print("❌ 삭제 실패: 관리자 권한으로 실행하거나 VSCode를 완전히 종료하고 다시 시도하세요.")
    except Exception as e:
        print(f"⚠️ 기타 오류 발생: {e}")



# ✅ 환경 변수 로드 함수
def load_env(path):
    env_vars = {}
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if "=" in line and not line.strip().startswith("#"):
                key, val = line.strip().split("=", 1)
                env_vars[key.strip()] = val.strip()
    return env_vars

# ✅ PC 환경 선택
def select_pc_env():
    print("\n==============================")
    print("💻 사용할 PC 환경을 선택하세요:")
    print("[1] pc_home")
    print("[2] pc_office")
    print("[3] pc_pohang")
    print("[4] pc_daejeon")
    print("==============================")
    choice = input("번호를 입력하세요 (1~4): ").strip()
    pc_map = {"1": "home", "2": "office", "3": "pohang", "4": "daejeon"}
    return f"pish_pc_{pc_map.get(choice, 'home')}.env"

# ✅ 사용자 선택
def select_user(env_vars):
    print("\n==============================")
    print("🔐 Git 사용자 계정을 선택하세요:")
    print(f"[1] {env_vars.get('USER1_NAME')}")
    print(f"[2] {env_vars.get('USER2_NAME')}")
    print(f"[3] {env_vars.get('USER3_NAME')}")
    print("==============================")
    choice = input("번호를 입력하세요 (1~3): ").strip()
    return {
        "name": env_vars.get(f"USER{choice}_NAME"),
        "email": env_vars.get(f"USER{choice}_EMAIL"),
        "ssh": env_vars.get(f"USER{choice}_SSH"),
        "remote": env_vars.get(f"USER{choice}_REMOTE")
    }

def main():
    env_file = select_pc_env()
    env_vars = load_env(env_file)
    user = select_user(env_vars)

    # ✅ SSH 키 등록
    print(f"\n🔑 SSH 키 등록 중: {user['ssh']}")
    subprocess.run(["ssh-add", user["ssh"]], shell=True)

    # ✅ 기존 .git 폴더 삭제
    git_dir = ".git"
    if os.path.exists(git_dir):
        print("🧹 기존 Git 설정 초기화")
        safe_rmtree(git_dir)
    else:
        print("✅ .git 폴더가 존재하지 않습니다. 초기화 생략.")

    # ✅ Git 초기화
    subprocess.run(["git", "init"], shell=True)
    subprocess.run(["git", "config", "user.name", user["name"]], shell=True)
    subprocess.run(["git", "config", "user.email", user["email"]], shell=True)
    subprocess.run(["git", "remote", "add", "origin", user["remote"]], shell=True)

    # ✅ git pull
    print("\n📥 git pull 실행 중...")
    subprocess.run(["git", "pull", "origin", "main"], shell=True)

    # ✅ 커밋 메시지 입력
    commit_msg = input("\n💬 커밋 메시지를 입력하세요 (기본값: 자동 커밋): ").strip()
    if not commit_msg:
        commit_msg = "자동 커밋"

    # ✅ Git add, commit, push
    print("🚀 Git 작업 시작...")
    subprocess.run(["git", "add", "."], shell=True)
    subprocess.run(["git", "commit", "-m", commit_msg], shell=True)
    subprocess.run(["git", "push", "-u", "origin", "main"], shell=True)

if __name__ == "__main__":
    main()
