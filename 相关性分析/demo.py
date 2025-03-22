import os
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import pearsonr
import pandas as pd

global_variable = '尾部'

# 读取 Excel 文件
excel_file = pd.ExcelFile(f'./处理后的数据/{global_variable}-处理后的数据.xlsx')
# 重新读取数据，设置第一行数据为表头
df = excel_file.parse('Sheet1', header=0)

# 将温度列转换为数值类型
df['温度/波长'] = df['温度/波长'].str.extract('(\d+)').astype(int)

# 初始化空列表来存储每个波长的相关系数和 p 值
correlation_coefficients = []
p_values = []

# 遍历每个波长列（除了温度列）
for column in df.columns[1:]:
    corr, p = pearsonr(df['温度/波长'], df[column])
    correlation_coefficients.append(corr)
    p_values.append(p)

# 提取波长信息
wavelengths = [float(col) for col in df.columns[1:]]


# 设置图表大小
plt.figure(figsize=(10, 6))
plt.rcParams['font.sans-serif'] = ['Heiti TC']  # 使用黑体
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

# 创建一个包含两个子图的画布
fig, axes = plt.subplots(2, 1, figsize=(10, 8))

# 绘制相关系数折线图
sns.lineplot(x=wavelengths, y=correlation_coefficients, ax=axes[0])
axes[0].set_title(f'{global_variable}相关系数随波长变化')
axes[0].set_ylabel('相关系数')

# 找出 P 值小于 0.05 的点并标记
for i in range(len(wavelengths)):
    if p_values[i] < 0.05:
        axes[0].scatter(wavelengths[i], correlation_coefficients[i], color='red', zorder=5)
        print(f"P 值小于 0.05 的点: 波长 {wavelengths[i]}, 相关系数 {correlation_coefficients[i]}, P 值 {p_values[i]}")

# 绘制 p 值折线图
sns.lineplot(x=wavelengths, y=p_values, ax=axes[1])
axes[1].set_title(f'{global_variable}P 值随波长变化')
axes[1].set_xlabel('波长')
axes[1].set_ylabel('P 值')

plt.tight_layout()


# 显示图表# 保存图表为图片文件
plt.savefig(f'pcitures/{global_variable}-相关性变化图.png')

# 输出结果
result_df = pd.DataFrame({
    '波长': wavelengths, 
    '相关系数': correlation_coefficients, 
    'P 值': p_values
})




# 保存结果到 Excel 文件
result_df.to_excel(f'{global_variable}-correlation_results.xlsx', index=False)
