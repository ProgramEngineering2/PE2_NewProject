import matplotlib.pyplot as plt
import os
import src.pandas_frame
#
def main():
    # excel 파일을 저장할 디렉토리 경로
    excel_directory = os.path.join('res', 'CSV')
    if not os.path.exists(excel_directory):
        os.makedirs(excel_directory)

    final_df = src.pandas_frame.pandas_data()
    print(final_df)
    excel_file_path = os.path.join(excel_directory, 'pandas.xlsx')  # res/CSV 디렉토리에 있는 pandas.csv 파일 경로
    final_df.to_excel(excel_file_path, index=False)


if __name__ == "__main__":
    main()

import src.ivcurve
import src.transmission
import src.ref_transmission
import src.flat_transmission

# 파일 경로 설정
jpgs_directory = os.path.join('res', 'jpgs')
if not os.path.exists(jpgs_directory):
    os.makedirs(jpgs_directory)

# 그래프 생성
fig, ax = plt.subplots()

# JPG 파일로 저장
jpg_file_path = os.path.join(jpgs_directory, 'graphs.jpg')
plt.savefig(jpg_file_path)

print(f"그래프가 {jpg_file_path}에 저장되었습니다.")
