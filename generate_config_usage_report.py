import os
import re

# config.py 내부에서 관리 중인 주요 변수
CONFIG_VARS = [
    "GOOGLE_SHEET_TITLE",
    "GOOGLE_SHEET_KEY",
    "GOOGLE_CREDENTIALS_PATH",
    "OPENAI_API_KEY"
]

def scan_usage(root_dir=".", skip_files=("config.py",)):
    usage_report = {var: [] for var in CONFIG_VARS}

    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith(".py") and filename not in skip_files:
                full_path = os.path.join(dirpath, filename)
                try:
                    with open(full_path, "r", encoding="utf-8") as f:
                        content = f.read()
                        for var in CONFIG_VARS:
                            # 단어 경계까지 고려
                            if re.search(rf"\b{var}\b", content):
                                usage_report[var].append(full_path)
                except Exception as e:
                    print(f"⚠️ 파일 읽기 실패: {full_path} → {e}")
    return usage_report

def print_report(report):
    print("\n📊 config.py 변수 사용 리포트:")
    for var, files in report.items():
        if files:
            print(f"\n🔹 {var} 사용됨:")
            for f in files:
                print(f"   - {f}")
        else:
            print(f"\n⚠️ {var}는 사용된 파일이 없습니다.")

if __name__ == "__main__":
    report = scan_usage(".")
    print_report(report)
