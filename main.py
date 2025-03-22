import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import medfilt
from scipy.signal import savgol_filter
from sklearn.preprocessing import MinMaxScaler


global_variable = "背"

# 读取 Excel 文件
excel_file = pd.ExcelFile(f'{global_variable}.xlsx')
# 获取指定工作表中的数据
df = excel_file.parse('Sheet1')
print(df.shape)

# 设置图表大小
plt.figure(figsize=(10, 6))
# 设置中文字体支持
plt.rcParams['font.sans-serif'] = ['Heiti TC']  # 使用黑体
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

data = df.iloc[:, 1:-1]
# 提取波长，即列名，并转换为数值类型
wavelength = pd.to_numeric(data.columns)

# 筛选波长范围为 1200 - 2400 的数据
selected_wavelength_mask = (wavelength >= 1200) & (wavelength <= 2400)
selected_wavelength = wavelength[selected_wavelength_mask]
selected_data = data.loc[:, selected_wavelength_mask]

# 对每个样本的折射率数据进行去噪、平滑和归一化处理
processed_data = []
for i in range(selected_data.shape[0]):
    # 获取当前样本在筛选波长下的折射率数据
    refractive_index = selected_data.iloc[i].values.astype(float)
    # 使用库函数处理
    denoised = medfilt(refractive_index, kernel_size=7)  # 去噪
    smoothed = savgol_filter(denoised, window_length=11, polyorder=3)  # 平滑
    normalized = MinMaxScaler().fit_transform(smoothed.reshape(-1, 1)).flatten()  # 归一化
    processed_data.append(normalized)

# 将处理后的数据转换为 DataFrame 对象
processed_data = pd.DataFrame(processed_data, columns=selected_wavelength)

import os

# 将处理后的数据保存为新的 Excel 文件，使用相对路径
save_dir = '处理后的数据'
if not os.path.exists(save_dir):
    os.makedirs(save_dir)
file_name = os.path.join(save_dir, f'{global_variable}部-处理后的数据.xlsx')
processed_data.to_excel(file_name)

# 绘制每个样本的折射率随波长变化的折线图
for i in range(processed_data.shape[0]):
    plt.plot(selected_wavelength, processed_data.iloc[i], label=df['样本ID'][i])

# 设置 x 轴范围，使 1200 位于原点
plt.xlim(left=1200)
# 设置图表标题和坐标轴标签
plt.title('反射率随波长变化图')
plt.xlabel('波长（nm）')
plt.xticks(rotation=45)
plt.ylabel('反射率')

# 设置图例
plt.legend()

import os
if not os.path.exists('pcitures'):
    os.makedirs('pcitures')


# 显示图表# 保存图表为图片文件
plt.savefig(f'pcitures/{global_variable}部-反射率随波长变化图.png')

# 显示图表
plt.show()

plt.show()

