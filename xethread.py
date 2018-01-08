from xlutils.copy import copy
from concurrent import futures
import xlrd
import xlwt,os,sys,time
workbook = xlrd.open_workbook("a.xlsx")
sheet_names = workbook.sheet_names()

def insert_one_row(sheet_content,row_number,sheet_name):
    row_data = sheet_content.row_values(row_number)
    sheet_header_data = sheet_content.row_values(2)
    print(row_data)
    user = row_data[-2]
    if user:
        if not os.path.isfile('dest/{}.xls'.format(user)):
            w = xlwt.Workbook()
            ws = w.add_sheet(sheet_name)
            w.save('dest/{}.xls'.format(user))
        # print('open dest/{}.xls'.format(user))
        rexcel = xlrd.open_workbook('dest/{}.xls'.format(user))
        excel = copy(rexcel)
        print(rexcel.sheet_names())
        if not sheet_name  in rexcel.sheet_names():
            # print("create")
            excel.add_sheet(sheet_name)
            excel.save('dest/{}.xls'.format(user))
            rexcel = xlrd.open_workbook('dest/{}.xls'.format(user))
            excel = copy(rexcel)
            # for index,value in enumerate(sheet_header_data):
            #     table.write(0,index,value)
        rows =rexcel.sheet_by_name(sheet_name).nrows
        table = excel.get_sheet(sheet_name)
        row = rows
        if row == 0:
            for index,value in enumerate(sheet_header_data):
                table.write(row,index,value)
            row +=1
        for index,value in enumerate(row_data):
            table.write(row,index,value)
        excel.save('dest/{}.xls'.format(user))
        # print(' close dest/{}.xls'.format(user))



    # ips = ["192.168.100.{}".format(ip) for ip in range(2,255)]
    # hostList=[]
    # with futures.ThreadPoolExecutor(max_workers=50) as excutor:
    #     hosts = [excutor.submit(scanSingleHost,ip,hostList) for ip in ips]
    # for future in futures.as_completed(hosts):
    #     pass
    #     # print future.result()
    #     # excutor.map(scanSingleHost,ips)
    # print len(hostList)
    # servers=[]
    # for host in hostList:
    #     print host['ip']
    #     syncSingleHost(host,servers)
    # print len(servers)


start = time.time()
for sheet_name in sheet_names[2:]:
    sheet_content = workbook.sheet_by_name(sheet_name)
    print(sheet_content.name,sheet_content.nrows)
    # with futures.ThreadPoolExecutor(max_workers=8) as excutor:
    #     rows = [excutor.submit(insert_one_row(sheet_content,row,sheet_name,)) for row in range(3,sheet_content.nrows-1)]
    # for future in futures.as_completed(rows):
    #     pass
    for row in range(3,sheet_content.nrows-1):
        insert_one_row(sheet_content,row,sheet_name,)
print(time.time()-start)
