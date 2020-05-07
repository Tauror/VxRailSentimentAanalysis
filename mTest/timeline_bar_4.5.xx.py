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
# 第5个表格数据4.5.xxx：画层叠柱状图
worksheet4 = workbook.sheet_by_name(sheets[4])
rows = worksheet4.nrows
cols = worksheet4.ncols
installbase45_date = [get_excel_date(worksheet4.cell_value(i, 0)) for i in range(1, rows)]
installbase45300 = [int(worksheet4.cell_value(i, 1)) for i in range(1, rows)]
installbase45310 = [int(worksheet4.cell_value(i, 2)) for i in range(1, rows)]
installbase45311 = [int(worksheet4.cell_value(i, 3)) for i in range(1, rows)]
installbase45314 = [int(worksheet4.cell_value(i, 4)) for i in range(1, rows)]
installbase45400 = [int(worksheet4.cell_value(i, 5)) for i in range(1, rows)]
# Convert date strings (e.g. 2014-10-18) to datetime
installbase45_date = [datetime.strptime(d, "%Y-%m-%d") for d in installbase45_date]

b1 = [installbase45300[i] + installbase45310[i] for i in range(len(installbase45300))]
b2 = [b1[i] + installbase45311[i] for i in range(len(installbase45311))]
b3 = [b2[i] + installbase45314[i] for i in range(len(installbase45314))]

ax2 = ax.twinx()  # this is the important function
ax2.get_xaxis().set_major_locator(mdates.MonthLocator(interval=1))
plt.bar(installbase45_date, installbase45300, width=15, label='4.5.300', fc='blue', zorder=1)
plt.bar(installbase45_date, installbase45310, width=15, bottom=installbase45300, label='4.5.310', fc='yellow', zorder=1)
plt.bar(installbase45_date, installbase45311, width=15, bottom=b1, label='4.5.311', fc='green', zorder=1)
plt.bar(installbase45_date, installbase45314, width=15, bottom=b2, label='4.5.314', fc='hotpink', zorder=1)
plt.bar(installbase45_date, installbase45400, width=15, bottom=b3, label='4.5.400', fc='orange', zorder=1)
ax2.set_ylim([0, 8000])
ax2.set_ylabel('Install Base')


# for i in range(1,4):
#################################################
# 获取工作簿中所有表格中的的第2个表格数据
worksheet1 = workbook.sheet_by_name(sheets[2])
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
