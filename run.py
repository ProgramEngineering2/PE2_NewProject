import os
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
from src.ivcurve import plot_iv_data
from src.transmission import plot_transmission_spectra_all
from src.ref_transmission import plot_transmission_spectra
from src.flat_transmission import plot_flat_transmission_spectra
import src.pandas_frame

directories = [
    'dat/HY202103/D07/20190715_190855',
    'dat/HY202103/D08/20190526_082853',
    'dat/HY202103/D08/20190528_001012',
    'dat/HY202103/D08/20190712_113254',
    'dat/HY202103/D23/20190528_101900',
    'dat/HY202103/D23/20190531_072042',
    'dat/HY202103/D23/20190603_204847',
    'dat/HY202103/D24/20190528_105459',
    'dat/HY202103/D24/20190528_111731',
    'dat/HY202103/D24/20190531_151815',
    'dat/HY202103/D24/20190603_225101'
]


def find_xml_files(directories):
    device = input("Device (LMZC, LMZO, or all): ").strip().upper()
    wafer_no_input = input("Wafer no (D07, D08, D23, D24, or all): ").strip().upper()
    xml_files = []

    if device not in ['LMZC', 'LMZO', 'all']:
        print("잘못된 device 입력. 'LMZC', 'LMZO', 또는 'all'만 지원됩니다.")
        return []

    if wafer_no_input == 'all':
        wafer_nos = ['D07', 'D08', 'D23', 'D24']
    else:
        wafer_nos = [wafer_no_input]

    for directory in directories:
        try:
            wafer_no = directory.split('/')[2]
            if wafer_no in wafer_nos:
                file_list = os.listdir(directory)
                if device == 'LMZC':
                    xml_files.extend([os.path.join(directory, file) for file in file_list if
                                      'LMZC' in file and file.endswith(".xml")])
                elif device == 'LMZO':
                    xml_files.extend([os.path.join(directory, file) for file in file_list if
                                      'LMZO' in file and file.endswith(".xml")])
                elif device == 'ALL':
                    xml_files.extend([os.path.join(directory, file) for file in file_list if
                                      ('LMZC' in file or 'LMZO' in file) and file.endswith(".xml")])
        except FileNotFoundError:
            print(f"디렉토리를 찾을 수 없습니다: {directory}")

    return xml_files


##
def main():

    # excel 파일을 저장할 디렉토리 경로
    excel_directory = os.path.join('res', 'CSV')
    if not os.path.exists(excel_directory):
        os.makedirs(excel_directory)

    final_df = src.pandas_frame.pandas_data()
    print(final_df)
    excel_file_path = os.path.join(excel_directory, 'pandas.xlsx')  # res/CSV 디렉토리에 있는 pandas.csv 파일 경로
    final_df.to_excel(excel_file_path, index=False)


    xml_files = find_xml_files(directories)
    if not xml_files:
        print("XML 파일을 찾을 수 없습니다.")
        return

    for xml_file in xml_files:
        fig, axs = plt.subplots(2, 2, figsize=(15, 10))

        tree = ET.parse(xml_file)
        root = tree.getroot()

        plot_iv_data(axs[0, 0], root)
        plot_transmission_spectra(axs[0, 1], root)
        plot_transmission_spectra_all(axs[1, 0], root)
        plot_flat_transmission_spectra(axs[1, 1], root)

        # 파일 경로 설정
        jpgs_directory = os.path.join('res', 'jpgs')
        if not os.path.exists(jpgs_directory):
            os.makedirs(jpgs_directory)

        # JPG 파일로 저장
        filename = os.path.splitext(os.path.basename(xml_file))[0] + '.jpg'
        plt.savefig(os.path.join(jpgs_directory, filename))
        plt.close()  # 그래프 초기화


if __name__ == "__main__":
    main()