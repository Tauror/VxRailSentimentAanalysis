import xlrd
import xlwt
import numpy as np
from collections import defaultdict


# get 'year-month' colunm and 'level' colunm,
# and set defaultdict of year-month, insert the coresponding levels,
# then get the levels' mean to each year-month,
# finally, save the defaultdict to new .xls file

xls_file = './SentimentAanalysis/data-without blanks.xls'
workbook = xlrd.open_workbook(xls_file)  # 打开工作簿
sheets = workbook.sheet_names()  # 获取工作簿中的所有表格
worksheet = workbook.sheet_by_name(sheets[0])  # 获取工作簿中所有表格中的的第一个表格
rows = worksheet.nrows  # 获取表格中已存在的数据的行数
cols = worksheet.ncols  # 获取表格中已存在的数据的行数

month_level = defaultdict(list)
for row in range(1, rows):
    m = worksheet.cell_value(row, 8)
    l = worksheet.cell_value(row, 10)
    month_level[m].append(l)

j = 1
result = []
wb = xlwt.Workbook()
ws = wb.add_sheet('month_level')
ws.write(0, 0, 'month')
ws.write(0, 1, 'level')
for i in month_level.items():
    result.append([i[0], np.mean(i[1])])
    ws.write(j, 0, i[0])
    ws.write(j, 1, np.mean(i[1]))
    j = j+1

wb.save('./SentimentAanalysis/mean_sentiments.xls')


