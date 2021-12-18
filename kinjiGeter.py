from scipy.optimize import curve_fit
import PySimpleGUI as sg
import matplotlib.pyplot as plt
import numpy as np
import csv
import os
import sys


def read_csv(filePath, x_i, y_i):
    # CSVファイルから読み取った値を格納する．
    x_csv = []
    y_csv = []
    # ファイルを開いてデータを抽出する．
    with open(str(filePath)) as f:
        reader = csv.reader(f)
        for row in reader:
            x_csv.append(float(row[int(x_i)]))
            y_csv.append(float(row[int(y_i)]))
    return np.array(x_csv), np.array(y_csv)


def draw_plot(x, y, fit, text, r):
    print("OK")
    # plt.rcParams['text.usetex'] = True
    plt.scatter(x, y)
    plt.plot(x, fit, color="red")
    plt.title(str(text) + " :" + str(r))
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.show(block=True)


#
# 多項式近似
#
def func_polynomial(X, *params):
    Y = np.zeros_like(X)
    for i, param in enumerate(params):
        Y = Y + np.array(param * X**i)
    return Y


def curveFit_polynomial(x_data, y_data, func_order, genntenn=False):
    f_o = [1] * int(func_order)  #多項式の次数
    if genntenn:
        f_o[0] = 0
    popt, pcov = curve_fit(func_polynomial, x_data, y_data, p0=f_o)
    print(popt)
    return popt, pcov**2  # 算出された係数，決定係数


def print_polynomial(p):
    output_tex = ""
    for i, param in enumerate(p):
        if i == 0:
            output_tex = str(param)
        else:
            output_tex = str(param) + "X^" + str(i) + " + " + output_tex
    return str(output_tex)


#
# 対数近似
#
def func_log(X, a, b):
    Y = a + b * np.log(X)
    return Y


def curveFit_log(x_data, y_data):
    popt, pcov = curve_fit(func_log, x_data, y_data)
    return popt, pcov**2  # 算出された係数，決定係数


def print_log(p):
    return str(p[0]) + " + " + str(p[1]) + "log(X)"


#
# 指数近似
#
def func_exp(X, a, b):
    Y = a * np.exp(b * X)
    return Y


def curveFit_exp(x_data, y_data):
    popt, pcov = curve_fit(func_exp, x_data, y_data)
    return popt, pcov**2  # 算出された係数，決定係数


def print_exp(p):
    return str(p[0]) + "exp(" + str(p[1]) + "X)"


#
# 累乗近似
#
def func_pow(X, a, b):
    Y = a * (X**b)
    return Y


def curveFit_pow(x_data, y_data):
    popt, pcov = curve_fit(func_pow, x_data, y_data)
    return popt, pcov**2  # 算出された係数，決定係数


def print_pow(p):
    return str(p[0]) + "X^" + str(p[1])


# エラー
def error_window(msg):
    error_layout = [[sg.Text(msg, key='error')],
                    [sg.Button('OK', key='ok', expand_x=True)]]
    sub_window = sg.Window('エラー',
                           error_layout,
                           modal=True,
                           keep_on_top=True,
                           auto_size_text=True)
    while True:
        sub_event, sub_value = sub_window.read()
        sub_window['error'].update(msg)
        if sub_event == sg.WIN_CLOSED:  #ウィンドウのXボタンを押したときの処理
            break
        if sub_event == 'ok':
            break
    sub_window.close()


# def resource_path(relative):  #アイコン表示用にアイコンファイルのパスを取得する．
#     if hasattr(sys, '_MEIPASS'):
#         return os.path.join(sys._MEIPASS, relative)
#     return path.join(path.abspath('.'), relative)

sg.theme('Default')

main_layout = [[sg.Text('CSVファイルとフィッティング関数を選択してください．')],
               [
                   sg.Text('ファイル'),
                   sg.InputText('', key='inputFilePath', expand_x=True),
                   sg.FileBrowse('ファイルを選択',
                                 target='inputFilePath',
                                 file_types=(('データファイル', '*.csv'), ))
               ],
               [
                   sg.Text('フィッティング関数'),
                   sg.Combo(('多項式近似', '対数近似', '指数近似', '累乗近似'),
                            size=(11, 1),
                            default_value='多項式近似',
                            key='fit_func'),
                   sg.Text(' X'),
                   sg.InputText('0', size=(3, 1), key='csv_x'),
                   sg.Text(' Y'),
                   sg.InputText('1', size=(3, 1), key='csv_y')
               ], [sg.Text('以下，多項式近似の場合のみ有効')],
               [
                   sg.Text('次数'),
                   sg.InputText('1', size=(3, 1), key='func_order'),
                   sg.Text('原点'),
                   sg.Combo(('通る', '通らない'),
                            size=(8, 1),
                            default_value='通る',
                            key='genntenn')
               ], [sg.Button('実行', key='go', expand_x=True)]]

# icon_path = resource_path("InouTadataka.ico")

main_window = sg.Window(
    'フィッティング',
    main_layout,
    resizable=True,
    auto_size_buttons=True,
    auto_size_text=True,
    finalize=True,
    # icon=icon_path
)

main_window.set_min_size((470, 200))

while True:
    event, values = main_window.read()

    if event == sg.WIN_CLOSED:  #ウィンドウのXボタンを押したときの処理
        break

    if event == 'go':
        if not values['inputFilePath']:
            error_window('CSVファイル\nが選択されていません．')
        elif not values['csv_x'] or not values['csv_y']:
            error_window('CSVファイルの抽出先（X,Y）\nが指定されていません．')
        elif values['fit_func'] == '多項式近似' and (not values['func_order']):
            error_window('次数\nが指定されていません．')
        else:
            if values['fit_func'] == '多項式近似':
                X_d, Y_d = read_csv(values['inputFilePath'], values['csv_x'],
                                    values['csv_y'])
                f_o = True
                if values['genntenn'] == '通る':
                    f_o = True
                else:
                    f_o = False
                k, r = curveFit_polynomial(X_d, Y_d, values['func_order'], f_o)
                p_tex = print_polynomial(k)
                draw_plot(X_d, Y_d, func_polynomial(X_d, k), p_tex, r)
            elif values['fit_func'] == '対数近似':
                X_d, Y_d = read_csv(values['inputFilePath'], values['csv_x'],
                                    values['csv_y'])
                k, r = curveFit_log(X_d, Y_d)
                p_tex = print_log(k)
                draw_plot(X_d, Y_d, func_log(X_d, k), p_tex, r)
            elif values['fit_func'] == '指数近似':
                X_d, Y_d = read_csv(values['inputFilePath'], values['csv_x'],
                                    values['csv_y'])
                k, r = curveFit_exp(X_d, Y_d)
                p_tex = print_exp(k)
                draw_plot(X_d, Y_d, func_exp(X_d, k), p_tex, r)
            elif values['fit_func'] == '累乗近似':
                X_d, Y_d = read_csv(values['inputFilePath'], values['csv_x'],
                                    values['csv_y'])
                k, r = curveFit_pow(X_d, Y_d)
                p_tex = print_pow(k)
                draw_plot(X_d, Y_d, func_pow(X_d, k), p_tex, r)

main_window.close()