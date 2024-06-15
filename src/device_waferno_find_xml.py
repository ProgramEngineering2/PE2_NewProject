import os

def find_xml_files(directories, device, wafer_nos):
    device = device.strip().upper()
    wafer_no_input = wafer_nos.strip().upper()
    xml_files = []

    if device not in ['LMZC', 'LMZO', 'ALL']:
        print("잘못된 device 입력. 'LMZC', 'LMZO', 또는 'ALL'만 지원됩니다.")
        return []

    if wafer_no_input == 'ALL':
        wafer_nos = ['D07', 'D08', 'D23', 'D24']
    else:
        wafer_nos = [wafer_no_input]

    for directory in directories:
        try:
            wafer_no = directory.split('/')[2]  # 디렉토리에서 웨이퍼 번호 추출
            if wafer_no in wafer_nos:
                file_list = os.listdir(directory)
                if device == 'LMZC':
                    xml_files.extend([os.path.join(directory, file) for file in file_list if 'LMZC' in file and file.endswith(".xml")])
                elif device == 'LMZO':
                    xml_files.extend([os.path.join(directory, file) for file in file_list if 'LMZO' in file and file.endswith(".xml")])
                elif device == 'ALL':
                    xml_files.extend([os.path.join(directory, file) for file in file_list if ('LMZC' in file or 'LMZO' in file) and file.endswith(".xml")])
        except FileNotFoundError:
            print(f"디렉토리를 찾을 수 없습니다: {directory}")

    return xml_files
