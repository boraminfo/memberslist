import os
import subprocess
from pathlib import Path
from datetime import datetime

USERS = {
    "1": {
        "name": "boraminfo",
        "email": "boraminfo@gmail.com",
        "remote": "git@github-boraminfo:boraminfo/members_list_boram.git",
        "host": "github-boraminfo"
    },
    "2": {
        "name": "ehlhappyday",
        "email": "ehlhappyday@gmail.com",
        "remote": "git@github-ehlhappyday:ehlhappyday/members_list_ehlhappyday.git",
        "host": "github-ehlhappyday"
    },
    "3": {
        "name": "sohee4463",
        "email": "sohee4463@gmail.com",
        "remote": "git@github-sohee4463:sohee4463/members_list_sohee4463.git",
        "host": "github-sohee4463"
    },
    "4": {
        "name": "boraminfo",
        "email": "boraminfo2@gmail.com",
        "remote": "git@github-boraminfo:boraminfo/memberslist.git",
        "host": "github-boraminfo"
    }
}

SSH_CONFIG_PATH = Path("C:/ChatGPT/ssh_config")

def select_user():
    print("\n==============================")
    print("🔐 Git 사용자 계정을 선택하세요:")
    for k, v in USERS.items():
        print(f"[{k}] {v['name']} ({v['email']})")
    print("==============================")
    choice = input("번호를 입력하세요 (1~4): ").strip()
    return USERS.get(choice)

def get_current_branch():
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True, text=True, check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return "main"  # 기본값 main

def setup_git(user):
    os.environ["GIT_SSH_COMMAND"] = f'ssh -F "{SSH_CONFIG_PATH}"'

    # Git 사용자 정보 적용
    subprocess.run(["git", "config", "--local", "user.name", user["name"]])
    subprocess.run(["git", "config", "--local", "user.email", user["email"]])

    # 항상 origin 새로 등록
    subprocess.run(["git", "remote", "remove", "origin"], check=False)
    subprocess.run(["git", "remote", "add", "origin", user["remote"]], check=True)

    branch = get_current_branch()
    print(f"\n✅ [{user['name']}] 설정 완료 (origin={user['remote']}, branch={branch})")
    return branch

def show_changes():
    result = subprocess.run(["git", "status", "--short"], capture_output=True, text=True)
    changes = result.stdout.strip()
    if not changes:
        print("✅ 변경 사항 없음.")
        return False
    print("\n📄 변경된 파일 목록:")
    print(changes)
    return True

def git_commit_and_push(branch):
    if not show_changes():
        return

    commit_msg = input("\n💬 커밋 메시지를 입력하세요 (비우면 자동 메시지 사용): ").strip()
    if not commit_msg:
        commit_msg = f"자동 커밋 {datetime.now().strftime('%Y-%m-%d %H:%M')}"

    subprocess.run(["git", "add", "."])
    subprocess.run(["git", "commit", "-m", commit_msg])

    print("\n📥 pull 실행 중...")
    result = subprocess.run(["git", "pull", "origin", branch])
    if result.returncode != 0:
        print("⚠️ pull 과정에서 충돌이 발생했습니다. 수동으로 해결 후 다시 실행하세요.")
        return

    subprocess.run(["git", "push", "origin", branch, "--force"])  # 강제 push
    print("\n🚀 Push 완료!")

def main():
    user = select_user()
    if not user:
        print("❌ 잘못된 입력입니다.")
        return
    branch = setup_git(user)
    git_commit_and_push(branch)

if __name__ == "__main__":
    main()
