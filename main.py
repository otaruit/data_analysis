import pandas as pd
import japanize_matplotlib
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import warnings


# # ファイルのエンコーディングを変換するスクリプト
input_file = "Tokyo_20232_20241.csv"
output_file = "Tokyo_20232_20241_utf8.csv"

# # Shift_JIS から UTF-8 に変換
# with open(input_file, 'r', encoding='shift_jis', errors='replace') as f_in:
#     content = f_in.read()

# with open(output_file, 'w', encoding='utf-8') as f_out:
#     f_out.write(content)

# print("エンコーディングの変換が完了しました。")

# データを読み込む
df = pd.read_csv(output_file)

# 現在の列名を表示
# print("現在の列名:\n", df.columns)

# 列名をリネームする
df.rename(columns={'延床面積（�u）': '延床面積（㎡）'}, inplace=True)

# リネーム後の列名を表示して確認
print("リネーム後の列名:\n", df.columns)

# 必要なデータ操作を行う
# 例: 延床面積（㎡）のデータを数値型に変換
floor_area = {
    "10m^2未満": 9,
    "2000㎡以上": 2000,
    "2,000�u以上": 2000,
    "2,000㎡以上": 2000
}

# 文字列の置換を行い、カンマを削除してから数値に変換する
df["延床面積（㎡）"] = df["延床面積（㎡）"].replace(floor_area)
df["延床面積（㎡）"] = df["延床面積（㎡）"].str.replace('�u', '㎡')
df["延床面積（㎡）"] = df["延床面積（㎡）"].str.replace('㎡', '')
df["延床面積（㎡）"] = df["延床面積（㎡）"].str.replace(',', '')
df["延床面積（㎡）"] = pd.to_numeric(df["延床面積（㎡）"], errors='coerce')

# 変更後のデータを表示
print(df.head())

# 他の列も同様に置換する
dicto = {
    "30分?60分": 45,
    "30分〜60分": 45,
    "1H?1H30": 75,
    "2H?": 120,
    "2H〜": 120,
    "1H〜1H30": 105,
    "1H30〜2H": 105
}

df['最寄駅：距離（分）'] = df['最寄駅：距離（分）'].replace(dicto).astype(float)

# 最終的なデータの確認
# print(df.describe())

# df_tmp = df.groupby("種類").sum()
# df_tmp["取引価格（総額）"].plot.pie(y="取引価格（総額）")
# plt.show()

# df_tmp = df.groupby("種類").sum().reset_index()
# sns.barplot(x="種類", y="取引価格（総額）", data=df_tmp)
# plt.show()

df_tmp = df.groupby("種類")["取引価格（総額）"].agg(["mean", "min", "max", "median", "std"])

df_tmp = df.groupby("種類").sum()
df_tmp    