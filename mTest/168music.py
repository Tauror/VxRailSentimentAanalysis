import xlrd
import numpy as np
import matplotlib.pyplot as plt


# read the defaultdict and plot it
xls_file1 = './SentimentAanalysis/mean_sentiments.xls'
workbook = xlrd.open_workbook(xls_file1)  # 打开工作簿
sheets = workbook.sheet_names()  # 获取工作簿中的所有表格
worksheet = workbook.sheet_by_name(sheets[0])  # 获取工作簿中所有表格中的的第一个表格
rows = worksheet.nrows  # 获取表格中已存在的数据的行数
cols = worksheet.ncols  # 获取表格中已存在的数据的行数

months = [worksheet.cell_value(i, 0) for i in range(1, rows)]
levels = [round(worksheet.cell_value(i, 1),1) for i in range(1, rows)]
crtc = np.ones((len(months)))*3

plt.subplots(1)
plt.plot(months, levels, 'r', linewidth=1, label='satisfaction level')
plt.plot(months, crtc, 'y--', linewidth=1, label='standard line')
plt.plot(months, levels, 'bo')
plt.ylim(2, 4)
m_ticks = np.arange(1, 5.5, 0.5)
plt.yticks(m_ticks)
plt.xticks(rotation=70)
plt.title('Sentiment Survey of VxRail on Reddit')
plt.xlabel('Timeline')
plt.ylabel('Satisfaction level')
plt.legend()
plt.tight_layout()
plt.show()

print('-----------------------')
