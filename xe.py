from xlutils.copy import copy
import xlrd
import xlwt,os,sys
print(os.system("pwd"))
workbook = xlrd.open_workbook("a.xlsx")
# print(os.system("dir"))
# names = workbook.sheet_names()
sheet2_name = workbook.sheet_names()[2]
sheet_names = workbook.sheet_names()
for sheet2_name in sheet_names[2:]:
    sheet2 = workbook.sheet_by_name(sheet2_name)
    print(sheet2.name,sheet2.nrows)
    for i in range(3,sheet2.nrows-1):
        row_data = sheet2.row_values(i)
        print(row_data)
        user = row_data[-2]
        if not os.path.isfile('dest/{}.xls'.format(user)):
            w = xlwt.Workbook()
            ws = w.add_sheet(sheet2_name)
            w.save('dest/{}.xls'.format(user))
        print(' open dest/{}.xls'.format(user))
        rexcel = xlrd.open_workbook('dest/{}.xls'.format(user))
        excel = copy(rexcel)
        print(rexcel.sheet_names())
        if not sheet2_name  in rexcel.sheet_names():
            print("create")
            excel.add_sheet(sheet2_name)
            excel.save('dest/{}.xls'.format(user))
            rexcel = xlrd.open_workbook('dest/{}.xls'.format(user))
            excel = copy(rexcel)
        rows =rexcel.sheet_by_name(sheet2_name).nrows

        table = excel.get_sheet(sheet2_name)
        row = rows
        for index,value in enumerate(row_data):
            table.write(row,index,value)
        excel.save('dest/{}.xls'.format(user))
        print(' close dest/{}.xls'.format(user))