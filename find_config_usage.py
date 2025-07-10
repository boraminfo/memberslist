import os

CONFIG_IMPORT_KEYWORDS = [
    "from utils.config import",
    "import utils.config",
    "from ..config import",  # 상대경로도 고려
]

def find_config_usage(root_dir=".", target_file="config.py"):
    found = []

    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith(".py") and filename != target_file:
                file_path = os.path.join(dirpath, filename)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                        for keyword in CONFIG_IMPORT_KEYWORDS:
                            if keyword in content:
                                found.append((file_path, keyword))
                except Exception as e:
                    print(f"⚠️ 파일 읽기 실패: {file_path} → {e}")

    return found


if __name__ == "__main__":
    results = find_config_usage(".")

    if results:
        print("✅ config.py를 사용하고 있는 파일 목록:")
        for path, keyword in results:
            print(f"  - {path}  (→ 포함된 구문: `{keyword}`)")
    else:
        print("❌ config.py를 사용한 파일이 없습니다.")
