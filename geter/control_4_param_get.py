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
#フィードフォワード制御器
def func_FF(v_t, vk_1, vk_2, vk_3):
    output = 0
    output += vk_1 * v_t + vk_2 * v_t**2 + vk_3 * v_t**3
    return output


#フィードバック制御器
def func_FB(v_t, v_ff, vk_ff):
    output = 0
    output += (v_t - v_ff) * vk_ff
    return output


############################################################################
# main
############################################################################
CSV_file_Path = "data.csv"

#制御器　近似曲線算出
# M0
V_target, V_ff, V_out = read_csv(CSV_file_Path, 0, 3, 6)
popt_0_ff, pcov_0_ff = curve_fit(func_FF, V_target, V_out)
v_out_buff = []
for i in range(len(V_target)):
    v_out_buff.append(
        V_out[i] -
        func_FF(V_target[i], popt_0_ff[0], popt_0_ff[1], popt_0_ff[2]))
popt_0_fb, pcov_0_fb = curve_fit(func_FB, (V_target, V_ff), v_out_buff)
# M1
V_target, V_ff, V_out = read_csv(CSV_file_Path, 1, 4, 7)
popt_1_ff, pcov_1_ff = curve_fit(func_FF, V_target, V_out)
v_out_buff = []
for i in range(len(V_target)):
    v_out_buff.append(
        V_out[i] -
        func_FF(V_target[i], popt_1_ff[0], popt_1_ff[1], popt_1_ff[2]))
popt_1_fb, pcov_1_fb = curve_fit(func_FB, (V_target, V_ff), v_out_buff)
# M2
V_target, V_ff, V_out = read_csv(CSV_file_Path, 2, 5, 8)
popt_2_ff, pcov_2_ff = curve_fit(func_FF, V_target, V_out)
v_out_buff = []
for i in range(len(V_target)):
    v_out_buff.append(
        V_out[i] -
        func_FF(V_target[i], popt_2_ff[0], popt_2_ff[1], popt_2_ff[2]))
popt_2_fb, pcov_2_fb = curve_fit(func_FB, (V_target, V_ff), v_out_buff)
# M3
V_target, V_ff, V_out = read_csv(CSV_file_Path, 2, 5, 8)
popt_3_ff, pcov_3_ff = curve_fit(func_FF, V_target, V_out)
v_out_buff = []
for i in range(len(V_target)):
    v_out_buff.append(
        V_out[i] -
        func_FF(V_target[i], popt_3_ff[0], popt_3_ff[1], popt_3_ff[2]))
popt_3_fb, pcov_3_fb = curve_fit(func_FB, (V_target, V_ff), v_out_buff)

# 結果
print("制御器 ", "=" * 20)
print("１次の係数, ２次の係数, ３次の係数, フィードバックの係数")
print("M0: FF -> ", popt_0_ff, ", FB -> ", popt_0_fb)
print("M1: FF -> ", popt_1_ff, ", FB -> ", popt_1_fb)
print("M2: FF -> ", popt_2_ff, ", FB -> ", popt_2_fb)
print("M3: FF -> ", popt_3_ff, ", FB -> ", popt_3_fb)