import os
import xml.etree.ElementTree as ET
import lmfit
import numpy as np
import matplotlib.pyplot as plt
#
# 데이터를 그래프에 그리는 함수
def plot_transmission_spectra(ax, root):
    # ref WavelengthSweep 요소 선택
    WavelengthSweep = list(root.findall('.//WavelengthSweep'))[6]

    # LengthUnit과 transmission 요소의 text 값 가져오기
    length_values = []
    measured_transmission_values = []
    for L in WavelengthSweep.findall('.//L'):
        length_text = L.text
        length_text = length_text.replace(',', ' ')
        length_values.extend([float(value) for value in length_text.split() if value.strip()])

    for IL in WavelengthSweep.findall('.//IL'):
        measured_transmission_text = IL.text
        measured_transmission_text = measured_transmission_text.replace(',', ' ')
        measured_transmission_values.extend(
            [float(value) for value in measured_transmission_text.split() if value.strip()])

    # 원래 데이터를 검은색 점으로 그리기
    ax.scatter(length_values, measured_transmission_values, color='black', label='Measured Data')

    # 다항식 차수 범위 설정
    poly_degrees = range(1, 7)

    # 각 차수에 대한 fitting 결과 저장할 리스트 초기화
    fitting_results = []

    # 1차부터 6차까지의 fitting 결과 저장
    for degree in range(1, 7):
        coeffs = np.polyfit(length_values, measured_transmission_values, degree)
        p = np.poly1d(coeffs)
        yhat = p(length_values)
        ybar = np.sum(measured_transmission_values) / len(measured_transmission_values)
        ssreg = np.sum((yhat - ybar) ** 2)
        sstot = np.sum((measured_transmission_values - ybar) ** 2)
        r_squared = ssreg / sstot
        fitting_results.append((coeffs, r_squared))

    # 각 차수에 대한 fitting 그래프 그리기
    for degree, coeffs in enumerate(fitting_results, start=1):
        p = np.poly1d(coeffs[0])
        x_values = np.linspace(min(length_values), max(length_values), 5000)
        y_values = p(x_values)
        ax.plot(x_values, y_values, label=f'{degree} degree fit')

        best_degree = np.argmax([result[1] for result in fitting_results]) + 1
        best_coeffs = fitting_results[best_degree - 1][0]

    # 근사식과 R 제곱 값 출력
    equation_parts = [f'{round(coeff, 2)}*x^{best_degree - i}' for i, coeff in enumerate(best_coeffs[::-1])]
    # 수식 항 3개당 줄바꿈
    equation = '\n'.join([' + '.join(equation_parts[i:i + 3]) for i in range(0, len(equation_parts), 3)])
    plt.text(1540, -13, f'Fitted Equation:\n{equation}', fontsize='small', color='red')


    r_squared_text = f'R^2: {round(fitting_results[best_degree - 1][1], 3)}, Degree: {best_degree}'
    plt.text(1540, -14, r_squared_text, fontsize='small', color='red')

    ax.set_xlabel('Wavelength [nm]')
    ax.set_ylabel('Measured Transmission [dB]')
    ax.set_title(f'Transmission Spectra - Processed and fitting')
    ax.legend(loc='lower left', bbox_to_anchor=(-0.5, -0.5), ncol=4, fontsize='small')
    ax.grid(True)


# 여러 디렉토리 경로
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
