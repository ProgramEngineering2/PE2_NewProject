from src.install_missing_modules import install_missing_modules
from src.process_data import process_data

def main():
    device = 'LMZC'  # 디바이스 설정('LMZC', 'LMZO', 'ALL') *대소문자 구별X
    wafer_nos = 'D07'  # 웨이퍼 번호 설정 ('D07', 'D08', 'D23', 'D24', 'ALL')

    # 필요한 경우 모듈 설치
    install_missing_modules('requirements.txt')

    # 데이터 처리 및 그래프 생성
    process_data(device, wafer_nos)

if __name__ == "__main__":
    main()
