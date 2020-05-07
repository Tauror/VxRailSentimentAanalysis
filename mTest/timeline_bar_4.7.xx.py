import xlrd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime


def get_excel_date(t):
    t_as_datetime = datetime(*xlrd.xldate_as_tuple(t, workbook.datemode))
    date = str(t_as_datetime.year)+'-'+str(t_as_datetime.month)+'-'+str(t_as_datetime.day)
    return date


# read the defaultdict and plot it
xls_file = './SentimentAanalysis/mean_sentiments.xls'
workbook = xlrd.open_workbook(xls_file)  # 打开工作簿
sheets = workbook.sheet_names()  # 获取工作簿中的所有表格

# 获取工作簿中所有表格中的的第1个表格数据
worksheet0 = workbook.sheet_by_name(sheets[0])  
rows = worksheet0.nrows
cols = worksheet0.ncols
sentiment_months = [worksheet0.cell_value(i, 0) for i in range(1, rows)]
sentiment_scores = [round(worksheet0.cell_value(i, 1),1) for i in range(1, rows)]
# Convert date strings (e.g. 2014-10-18) to datetime
sentiment_months = [datetime.strptime(m, "%Y-%m") for m in sentiment_months]

# Create figure and plot a stem plot with the date
fig, ax = plt.subplots()
# fig, ax = plt.subplots(figsize=(8.8, 4), constrained_layout=True)
ax.set(title="Sentiment Survey of VxRail on Reddit")
#################################################
plt.plot(sentiment_months, sentiment_scores, 'b', linewidth=1, label='sentiment level')
plt.plot(sentiment_months, sentiment_scores, 'bo')
plt.plot(sentiment_months, np.ones((len(sentiment_months)))*3, 'r--', label='standard line')
ax.set_ylim([-3, 9])
plt.ylabel('Satisfaction level')
#################################################
# 第6个表格数据4.7.xxx：画层叠柱状图
worksheet4 = workbook.sheet_by_name(sheets[5])
rows = worksheet4.nrows
cols = worksheet4.ncols
installbase47_date = [get_excel_date(worksheet4.cell_value(i, 0)) for i in range(1, rows)]
installbase47000 = [int(worksheet4.cell_value(i, 1)) for i in range(1, rows)]
installbase47001 = [int(worksheet4.cell_value(i, 2)) for i in range(1, rows)]
installbase47100 = [int(worksheet4.cell_value(i, 3)) for i in range(1, rows)]
installbase47110 = [int(worksheet4.cell_value(i, 4)) for i in range(1, rows)]
installbase47111 = [int(worksheet4.cell_value(i, 5)) for i in range(1, rows)]
installbase47200 = [int(worksheet4.cell_value(i, 6)) for i in range(1, rows)]
installbase47211 = [int(worksheet4.cell_value(i, 7)) for i in range(1, rows)]
installbase47212 = [int(worksheet4.cell_value(i, 8)) for i in range(1, rows)]
# Convert date strings (e.g. 2014-10-18) to datetime
installbase47_date = [datetime.strptime(d, "%Y-%m-%d") for d in installbase47_date]

b1 = [installbase47000[i] + installbase47001[i] for i in range(len(installbase47000))]
b2 = [b1[i] + installbase47100[i] for i in range(len(installbase47100))]
b3 = [b2[i] + installbase47110[i] for i in range(len(installbase47110))]
b4 = [b3[i] + installbase47111[i] for i in range(len(installbase47111))]
b5 = [b4[i] + installbase47200[i] for i in range(len(installbase47200))]
b6 = [b5[i] + installbase47211[i] for i in range(len(installbase47211))]


ax2 = ax.twinx()  # this is the important function
ax2.get_xaxis().set_major_locator(mdates.MonthLocator(interval=1))
plt.bar(installbase47_date, installbase47000, width=15, label='4.7.000', fc='blue', zorder=1)
plt.bar(installbase47_date, installbase47001, width=15, bottom=installbase47000, label='4.7.001', fc='yellow', zorder=1)
plt.bar(installbase47_date, installbase47100, width=15, bottom=b1, label='4.7.100', fc='green', zorder=1)
plt.bar(installbase47_date, installbase47110, width=15, bottom=b2, label='4.7.110', fc='hotpink', zorder=1)
plt.bar(installbase47_date, installbase47111, width=15, bottom=b3, label='4.7.111', fc='orange', zorder=1)
plt.bar(installbase47_date, installbase47200, width=15, bottom=b4, label='4.7.200', fc='royalblue', zorder=1)
plt.bar(installbase47_date, installbase47211, width=15, bottom=b5, label='4.7.211', fc='gold', zorder=1)
plt.bar(installbase47_date, installbase47212, width=15, bottom=b6, label='4.7.212', fc='lawngreen', zorder=1)
ax2.set_ylim([0, 8000])
ax2.set_ylabel('Install Base')


# for i in range(1,4):
#################################################
# 获取4.7.xxx release信息
worksheet1 = workbook.sheet_by_name(sheets[3])
rows = worksheet1.nrows
cols = worksheet1.ncols
release_no40 = [str(worksheet1.cell_value(i, 0)).strip(u'\u200b') for i in range(1, rows)]
release_date40 = [get_excel_date(worksheet1.cell_value(i, 1)) for i in range(1, rows)]
# Convert date strings (e.g. 2014-10-18) to datetime
release_date40 = [datetime.strptime(d, "%Y-%m-%d") for d in release_date40]


# Choose some nice levels
levels = np.tile([-2, 8, -1, 7, 0, 6, 1, 5, 2, 4], int(np.ceil(len(release_date40)/6)))[:len(release_date40)]

markerline, stemline, baseline = ax.stem(release_date40, levels, bottom=3, linefmt="y:", basefmt=" ", use_line_collection=True, label='release version')
baseline.set_ydata(3)
# Shift the markers to the baseline by replacing the y-data by zeros.
# markerline.set_ydata(np.ones((len(release_date40)))*3)

# setp(): Set a property on an artist object.
plt.setp(markerline, mec="k", mfc="w", zorder=3)


# annotate lines
vert = np.array(['top', 'bottom'])[(levels > 3).astype(int)]
for d, l, r, va in zip(release_date40, levels, release_no40, vert):
    ax.annotate(r, xy=(d, l), xytext=(-3, np.sign(l)*3),
                textcoords="offset points", va=va, ha="right")



##########################################################################################
# format xaxis with 1 month intervals
# ax.xaxis.set_major_formatter(mdates.DateFormatter('%-m')) 
ax.get_xaxis().set_major_locator(mdates.MonthLocator(interval=1))
ax.get_xaxis().set_major_formatter(mdates.DateFormatter("%b %Y"))
plt.setp(ax.get_xticklabels(), rotation=30, ha="right")

# remove y axis and spines
# ax.get_yaxis().set_visible(False)
for spine in ["top", "right"]:
    ax.spines[spine].set_visible(False)

ax.margins(y=0.1)

plt.tight_layout()
plt.legend()
plt.show()
