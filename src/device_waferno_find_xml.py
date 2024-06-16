import os

def find_xml_files(directories, device, wafer_nos):
    device = device.strip().upper()
    wafer_no_input = wafer_nos.strip().upper()
    xml_files = []

    valid_devices = ['LMZC', 'LMZO', 'ALL']
    valid_wafer_nos = ['D07', 'D08', 'D23', 'D24']

    if device not in valid_devices:
        print("잘못된 device 입력. 'LMZC', 'LMZO', 또는 'ALL'만 지원됩니다.")
        return []

    if wafer_no_input not in valid_wafer_nos and wafer_no_input != 'ALL':
        print(f"잘못된 wafer 번호 입력. {', '.join(valid_wafer_nos)} 또는 'ALL'을 입력해주세요.")
        return []

    if wafer_no_input == 'ALL':
        wafer_nos = valid_wafer_nos
    else:
        wafer_nos = [wafer_no_input]

    files_found = False

    for directory in directories:
        try:
            wafer_no = directory.split('/')[2]  # 디렉토리에서 웨이퍼 번호 추출
            if wafer_no in wafer_nos:
                file_list = os.listdir(directory)
                if device == 'LMZC':
                    matching_files = [os.path.join(directory, file) for file in file_list if 'LMZC' in file and file.endswith(".xml")]
                elif device == 'LMZO':
                    matching_files = [os.path.join(directory, file) for file in file_list if 'LMZO' in file and file.endswith(".xml")]
                elif device == 'ALL':
                    matching_files = [os.path.join(directory, file) for file in file_list if ('LMZC' in file or 'LMZO' in file) and file.endswith(".xml")]

                if matching_files:
                    xml_files.extend(matching_files)
                    files_found = True
        except FileNotFoundError:
            print(f"디렉토리를 찾을 수 없습니다: {directory}")

    if not files_found:
        print(f"지정된 device ({device}) 파일이 {', '.join(wafer_nos)} 웨이퍼에서 발견되지 않았습니다.")

    return xml_files


