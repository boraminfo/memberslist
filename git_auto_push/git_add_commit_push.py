import os
import sys
import subprocess
import shutil
from pathlib import Path
from datetime import datetime



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
    base_dir = Path(__file__).parent  # git_auto_push 폴더 기준
    env_file_name = select_pc_env()
    env_file_path = base_dir / env_file_name

    if not env_file_path.exists():
        print(f"❌ .env 파일이 존재하지 않습니다: {env_file_path}")
        return

    env_vars = load_env(env_file_path)
    user = select_user(env_vars)

  
    # ✅ GIT_SSH_COMMAND 환경변수 설정
    git_env = os.environ.copy()
    git_env["GIT_SSH_COMMAND"] = f'ssh -i "{user["ssh"]}"'

    # ✅ 기존 .git 폴더 삭제
    subprocess.run(["git", "init"], shell=True)
    subprocess.run(["git", "checkout", "-B", "main"], shell=True)

    # ✅ 사용자별 Git 설정 (로컬로)
    subprocess.run(["git", "config", "--local", "user.name", user["name"]], shell=True)
    subprocess.run(["git", "config", "--local", "user.email", user["email"]], shell=True)

    # ✅ 최소 한 번 커밋 (필수!)
    subprocess.run(["git", "add", "."], shell=True)
    subprocess.run(["git", "commit", "-m", "최초 커밋"], shell=True)

    # ✅ 리모트 재설정
    subprocess.run(["git", "remote", "remove", "origin"], shell=True)
    subprocess.run(["git", "remote", "add", "origin", user["remote"]], shell=True)

    # ✅ Pull 시도 (병합 허용)
    print("📥 git pull 실행 중...")
    pull_result = subprocess.run(
        ["git", "pull", "origin", "main", "--allow-unrelated-histories"],
        shell=True,
        env=git_env
    )
    if pull_result.returncode != 0:
        print("⚠️ git pull 중 충돌이 발생했을 수 있습니다.")
        print("🛠 수동 병합 후 add + commit을 수행하세요.")




    # 변경된 파일명 추출
    diff_result = subprocess.run(["git", "diff", "--name-only"], capture_output=True, text=True)
    changed_files = diff_result.stdout.strip().replace("\n", ", ")





    # ✅ 변경사항 확인 및 메시지 출력 (커밋 전!)
    status = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
    if not status.stdout.strip():
        print("ℹ️ 커밋할 변경 사항이 없습니다.")
    else:
        print("📝 변경 사항이 감지되어 커밋을 수행합니다.")

        # 변경된 파일명 추출
        diff_result = subprocess.run(["git", "diff", "--name-only"], capture_output=True, text=True)
        changed_files = diff_result.stdout.strip().replace("\n", ", ")

        # 커밋 메시지 입력
        commit_msg = input("\n💬 커밋 메시지를 입력하세요 (기본값: 자동 커밋): ").strip()
        if not commit_msg:
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            commit_msg = f"자동 커밋: {now}"
            if changed_files:
                commit_msg += f" | 수정 파일: {changed_files}"

        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        print("✅ 변경 사항이 커밋되었습니다.")

    print("✅ Git 초기화 및 커밋 완료!)")
    




    # git push 명령어 실행
    print("📤 최종 Push 중...")
    subprocess.run(["git", "push", "-u", "origin", "main"], shell=True, env=git_env)

    print("✅ Git push 완료!")

if __name__ == "__main__":
    main()


