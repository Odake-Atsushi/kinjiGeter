from scipy.optimize import curve_fit
import csv


def read_csv(filePath, v_in, v_ff, v_out):
    skip_data = 1
    # CSVファイルから読み取った値を格納する．
    v_in_csv = []
    v_ff_csv = []
    v_out_csv = []
    # ファイルを開いてデータを抽出する．
    with open(str(filePath)) as f:
        reader = csv.reader(f)
        for row in reader:
            v_in_csv.append(float(row[int(v_in)]))
            v_ff_csv.append(float(row[int(v_ff)]))
            v_out_csv.append(float(row[int(v_out)]))
    return  v_in_csv[skip_data:],\
            v_ff_csv[skip_data:],\
            v_out_csv[skip_data:]


############################################################################
def func(v_t, v_ff, vk_1, vk_2, vk_3, vk_ff):
    output = 0
    #フィードフォワード制御器
    output += vk_1 * v_t + vk_2 * v_t**2 + vk_3 * v_t**3
    #フィードバック制御器
    output += (v_t - v_ff) * vk_ff
    return output


############################################################################
# main
############################################################################
CSV_file_Path = "data.csv"

#制御器　近似曲線算出
# M0
V_target, V_ff, V_out = read_csv(CSV_file_Path, 0, 4, 8)
popt_0, pcov = curve_fit(func, (V_target, V_ff), V_out)
# M1
V_target, V_ff, V_out = read_csv(CSV_file_Path, 1, 5, 9)
popt_1, pcov = curve_fit(func, (V_target, V_ff), V_out)
# M2
V_target, V_ff, V_out = read_csv(CSV_file_Path, 2, 6, 10)
popt_2, pcov = curve_fit(func, (V_target, V_ff), V_out)
# M3
V_target, V_ff, V_out = read_csv(CSV_file_Path, 3, 7, 11)
popt_3, pcov = curve_fit(func, (V_target, V_ff), V_out)

print("制御器 ", "=" * 20)
print("１次の係数, ２次の係数, ３次の係数, フィードバックの係数")
print("M0: ", popt_0)
print("M1: ", popt_1)
print("M2: ", popt_2)
print("M3: ", popt_3)
