import xlrd
import xlwt
import datetime
import numpy as np
from xlutils.copy import copy
from textblob import TextBlob

'''
Reading the xls file to get the comments,
then generate the sentiment of each comment,
finally, save(append) the sentiment to xls file
'''

xls_file = './SentimentAanalysis/data-without blanks.xls'

workbook = xlrd.open_workbook(xls_file)  # 打开工作簿
sheets = workbook.sheet_names()  # 获取工作簿中的所有表格
worksheet = workbook.sheet_by_name(sheets[0])  # 获取工作簿中所有表格中的的第一个表格
rows = worksheet.nrows  # 获取表格中已存在的数据的行数
cols_old = worksheet.ncols  # 获取表格中已存在的数据的行数


years = []
dates = []
year_months = []
comments = [worksheet.cell_value(i, 4) for i in range(rows)]
for row in range(1, rows):
    t = worksheet.cell_value(row, 3)
    t_as_datetime = datetime.datetime(*xlrd.xldate_as_tuple(t, workbook.datemode))
    year = str(t_as_datetime.year)
    year_month = str(t_as_datetime.year)+'-'+str(t_as_datetime.month)
    date = str(t_as_datetime.year)+'-'+str(t_as_datetime.month)+'-'+str(t_as_datetime.day)
    years.append(year)
    dates.append(date)
    year_months.append(year_month)

years.insert(0, 'year')
dates.insert(0, 'date')
year_months.insert(0, 'year_months')

stmt = [TextBlob(comment).sentiment for comment in comments]

new_workbook = copy(workbook)  # 将xlrd对象拷贝转化为xlwt对象
new_worksheet = new_workbook.get_sheet(0)  # 获取转化后工作簿中的第一个表格
for i in range(1, rows):
    for j in range(0, 2):
        new_worksheet.write(i, cols_old+j, stmt[i][j])
    new_worksheet.write(i, cols_old+2, years[i])
    new_worksheet.write(i, cols_old+3, dates[i])
    if stmt[i][0]>=0.6:
        level = 5
    elif stmt[i][0]>=0.4 and stmt[i][0]<0.6:
        level = 4
    elif stmt[i][0]>=0 and stmt[i][0]<0.4:
        level = 3
    elif stmt[i][0]>=-0.4 and stmt[i][0]<0:
        level = 2
    else:
        level = 1
    new_worksheet.write(i, cols_old+4, level)
    new_worksheet.write(i, cols_old+5, year_months[i])

new_workbook.save(xls_file)

# print('-----------------------')

