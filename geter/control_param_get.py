from scipy.optimize import curve_fit
import csv


def read_csv(filePath, x_in, y_in, a_in, x_ff, y_ff, a_ff, x_out, y_out,
             a_out):
    skip_data = 1
    # CSVファイルから読み取った値を格納する．
    x_in_csv = []
    y_in_csv = []
    a_in_csv = []
    x_ff_csv = []
    y_ff_csv = []
    a_ff_csv = []
    x_out_csv = []
    y_out_csv = []
    a_out_csv = []
    # ファイルを開いてデータを抽出する．
    with open(str(filePath)) as f:
        reader = csv.reader(f)
        for row in reader:
            x_in_csv.append(float(row[int(x_in)]))
            y_in_csv.append(float(row[int(y_in)]))
            a_in_csv.append(float(row[int(a_in)]))
            x_ff_csv.append(float(row[int(x_ff)]))
            y_ff_csv.append(float(row[int(y_ff)]))
            a_ff_csv.append(float(row[int(a_ff)]))
            x_out_csv.append(float(row[int(x_out)]))
            y_out_csv.append(float(row[int(y_out)]))
            a_out_csv.append(float(row[int(a_out)]))
    return x_in_csv[skip_data:], y_in_csv[skip_data:], a_in_csv[
        skip_data:], x_ff_csv[skip_data:], y_ff_csv[skip_data:], a_ff_csv[
            skip_data:], x_out_csv[skip_data:], y_out_csv[
                skip_data:], a_out_csv[skip_data:]


############################################################################
def func_FF(vX_t, vY_t, vA_t, x_1, x_2, x_3, x_4, x_5, y_1, y_2, y_3, y_4, y_5,
            a_1, a_2, a_3, a_4, a_5):
    output = 0
    #フィードフォワード制御器
    output += x_1 * vX_t + x_2 * vX_t**2 + x_3 * vX_t**3 + x_4 * vX_t**4 + x_5 * vX_t**5
    output += y_1 * vY_t + y_2 * vY_t**2 + y_3 * vY_t**3 + y_4 * vY_t**4 + y_5 * vY_t**5
    output += a_1 * vA_t + a_2 * vA_t**2 + a_3 * vA_t**3 + a_4 * vA_t**4 + a_5 * vA_t**5
    return output


def func_FB(vX_t, vY_t, vA_t, vX_ff, vY_ff, vA_ff, x_ff, y_ff, a_ff):
    output = 0
    #フィードバック制御器
    output += (vX_t - vX_ff) * x_ff
    output += (vY_t - vY_ff) * y_ff
    output += (vA_t - vA_ff) * a_ff
    return output


############################################################################
# main
############################################################################
CSV_file_Path = "data.csv"

#制御器　近似曲線算出
Vx_target, Vy_target, Va_target, Vx_ff, Vy_ff, Va_ff, Vx, Vy, Va = read_csv(
    CSV_file_Path, 0, 1, 2, 3, 4, 5, 6, 7, 8)
# X
popt_x_ff, pcov = curve_fit(func_FF, (Vx_target, Vy_target, Va_target), Vx)
v_out_buff = []
for i in range(len(Vx_target)):
    v_out_buff.append(Vx[i] - func_FF(
        Vx_target[i], Vy_target[i], Va_target[i], popt_x_ff[0], popt_x_ff[1],
        popt_x_ff[2], popt_x_ff[3], popt_x_ff[4], popt_x_ff[5], popt_x_ff[6],
        popt_x_ff[7], popt_x_ff[8], popt_x_ff[9], popt_x_ff[10], popt_x_ff[11],
        popt_x_ff[12], popt_x_ff[13], popt_x_ff[14]))
popt_x_fb, pcov = curve_fit(
    func_FB, (Vx_target, Vy_target, Va_target, Vx_ff, Vy_ff, Va_ff),
    v_out_buff)

# Y
popt_y_ff, pcov = curve_fit(func_FF, (Vx_target, Vy_target, Va_target), Vy)
v_out_buff = []
for i in range(len(Vx_target)):
    v_out_buff.append(Vy[i] - func_FF(
        Vx_target[i], Vy_target[i], Va_target[i], popt_y_ff[0], popt_y_ff[1],
        popt_y_ff[2], popt_y_ff[3], popt_y_ff[4], popt_y_ff[5], popt_y_ff[6],
        popt_y_ff[7], popt_y_ff[8], popt_y_ff[9], popt_y_ff[10], popt_y_ff[11],
        popt_y_ff[12], popt_y_ff[13], popt_y_ff[14]))
popt_y_fb, pcov = curve_fit(
    func_FB, (Vx_target, Vy_target, Va_target, Vx_ff, Vy_ff, Va_ff),
    v_out_buff)

# A
popt_a_ff, pcov = curve_fit(func_FF, (Vx_target, Vy_target, Va_target), Va)
v_out_buff = []
for i in range(len(Vx_target)):
    v_out_buff.append(Va[i] - func_FF(
        Vx_target[i], Vy_target[i], Va_target[i], popt_a_ff[0], popt_a_ff[1],
        popt_a_ff[2], popt_a_ff[3], popt_a_ff[4], popt_a_ff[5], popt_a_ff[6],
        popt_a_ff[7], popt_a_ff[8], popt_a_ff[9], popt_a_ff[10], popt_a_ff[11],
        popt_a_ff[12], popt_a_ff[13], popt_a_ff[14]))
popt_a_fb, pcov = curve_fit(
    func_FB, (Vx_target, Vy_target, Va_target, Vx_ff, Vy_ff, Va_ff),
    v_out_buff)

# 結果
print("制御器 ", "=" * 20)
print("[１次の係数, ２次の係数, ３次の係数, ４次の係数, ５次の係数, フィードバックの係数](x, y, a)")
print("X: FF -> ", popt_x_ff, ", FB -> ", popt_x_fb)
print("Y: FF -> ", popt_y_ff, ", FB -> ", popt_y_fb)
print("A: FF -> ", popt_a_ff, ", FB -> ", popt_a_fb)
