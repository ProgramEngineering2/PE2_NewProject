import os
import pandas as pd
from src.flat_transmission import plot_flat_transmission_spectra
from src.ivcurve import plot_iv_data
from src.pandas_frame import pandas_data, save_to_excel
from src.ref_transmission import plot_transmission_spectra
from src.transmission import plot_transmission_spectra_all
from src.device_waferno_find_xml import find_xml_files
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt

def process_data(device, wafer_nos):

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

    # Excel 파일 저장
    excel_directory = os.path.join('res', 'CSV')
    final_df = pandas_data(device, wafer_nos)
    save_to_excel(final_df, excel_directory, 'pandas.xlsx')

    # XML 파일 찾기
    xml_files = find_xml_files(directories, device, wafer_nos)
    if not xml_files:
        print("XML 파일을 찾을 수 없습니다.")
        return

    # 그래프 생성 및 저장
    jpgs_directory = os.path.join('res', 'jpgs')
    for xml_file in xml_files:
        fig, axs = plt.subplots(2, 2, figsize=(15, 10))

        tree = ET.parse(xml_file)
        root = tree.getroot()

        plot_iv_data(axs[0, 0], root)
        plot_transmission_spectra(axs[0, 1], root)
        plot_transmission_spectra_all(axs[1, 0], root)
        plot_flat_transmission_spectra(axs[1, 1], root)

        # 파일명에서 9번~12번 글자 추출
        filename = os.path.basename(xml_file)
        wafer_id = filename[9:12]

        # 파일 경로 설정
        jpgs_wafer_directory = os.path.join(jpgs_directory, wafer_id)
        if not os.path.exists(jpgs_wafer_directory):
            os.makedirs(jpgs_wafer_directory)

        # JPG 파일로 저장
        jpg_filename = os.path.splitext(filename)[0] + '.jpg'
        plt.savefig(os.path.join(jpgs_wafer_directory, jpg_filename))
        plt.close()  # 그래프 초기화
