import os
import subprocess

def install_missing_modules(filename='requirements.txt'):
    # 현재 파일의 경로에서 requirements.txt 파일의 절대 경로 설정
    current_dir = os.path.dirname(os.path.abspath(__file__))
    abs_file_path = os.path.normpath(os.path.join(current_dir, filename))

    if os.path.exists(abs_file_path):
        with open(abs_file_path) as f:
            modules = f.read().splitlines()

        for module in modules:
            try:
                __import__(module)
                print(f"{module} 모듈이 설치되어 있습니다. 계속 진행합니다.")
            except ImportError:
                print(f"{module} 모듈이 설치되어 있지 않습니다. 자동으로 설치합니다...")
                subprocess.call(['pip', 'install', module])
    else:
        print(f"파일 '{abs_file_path}'을(를) 찾을 수 없습니다. 패키지 설치를 스킵합니다.")
