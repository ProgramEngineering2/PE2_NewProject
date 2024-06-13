import os
import xml.etree.ElementTree as ET
import lmfit
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import UnivariateSpline
#
# IV 데이터를 그래프에 그리는 함수
def plot_iv_data(ax,root):
    # IVMeasurement 요소 찾기
    iv_measurement_element = root.find('.//IVMeasurement')

    # Voltage 및 Current 요소의 텍스트 값을 파싱하여 출력
    voltage_text = iv_measurement_element.find('.//Voltage').text
    current_text = iv_measurement_element.find('.//Current').text

    # Voltage 및 Current 텍스트 값을 파싱하여 실수형 리스트로 변환
    voltage_values = np.array([float(value) for value in voltage_text.split(',')])
    current_values = np.array([float(value) for value in current_text.split(',')])
    current_abs = np.abs(current_values)

    def diode_equation(V, Is, n, Vt, V_linear, Ilinear):
        current = []
        for v in V:
            if v >= V_linear:
                current.append(Is * (np.exp(v / (n * Vt)) - 1))
            else:
                current.append(Ilinear * v)
        return current

    # 초기 추정값 설정
    Is_guess = current_abs[0]
    n_guess = 1.0
    Vt_guess = 0.0256
    Ilinear_guess = 0.0
    Vlinear_guess = 0.0

    # 매개변수 및 초기 추정값 정의
    params = lmfit.Parameters()
    params.add('Is', value=Is_guess, min=0)  # 포화 전류
    params.add('n', value=n_guess, min=1)  # 이상성 지수
    params.add('Vt', value=Vt_guess, min=0)  # 열전압
    params.add('Ilinear', value=Ilinear_guess)  # 음수 전압 영역에서의 전류
    params.add('V_linear', value=Vlinear_guess)  # 음수 전압 영역에서의 선형 근사 전압

    # 적합 실행 (알고리즘 변경)
    result = lmfit.minimize(
        # 잔차 함수
        lambda params, x, y: np.array(diode_equation(x, **params)) - np.array(y),
        # 매개변수 및 데이터
        params, args=(voltage_values, current_values),
        # 알고리즘 변경
        method='least_squares'
    )

    # 적합된 값 얻기
    best_fit = np.abs(current_values) + result.residual

    # 스플라인 피팅
    spline = UnivariateSpline(voltage_values, current_abs, s=0)  # s 값은 필요에 따라 조절

    # R-squared 값 계산
    ss_residual = np.sum(result.residual ** 2)
    ss_total = np.sum(np.abs(current_values) - np.abs(np.mean(current_values)) ** 2)
    r_squared = 1 - (ss_residual / ss_total)


    # 데이터를 그래프에 그리기
    ax.scatter(voltage_values, np.abs(current_values), label='Original Data')
    ax.plot(voltage_values, spline(voltage_values), color='blue', linestyle='--', label='Spline Fit')
    ax.plot(voltage_values, best_fit, color='red',
            label=f'Fitted Polynomial \n R-squared: {round(r_squared, 3)}')
    ax.set_yscale('log')  # y축 로그 스케일로 변경
    ax.set_xlabel('Voltage [V]')
    ax.set_ylabel('Absolute Current [A]')
    ax.set_title('IV raw dat & fitted dat')
    ax.legend()



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

