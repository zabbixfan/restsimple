#!/usr/bin/env python
#coding:utf-8
from xlutils.copy import copy
from concurrent import futures
import collections
import xlrd
import xlwt,os,sys,time
workbook = xlrd.open_workbook("a.xlsx")
sheet_names = workbook.sheet_names()
total_data = []
total_header = {}
total_header = collections.OrderedDict()

def aggregation_data(sheet_content,row_number,sheet_name):
    row_data = sheet_content.row_values(row_number)
    sheet_header_data = sheet_content.row_values(2)
    user = row_data[-2]
    dept = row_data[-3]
    if user:
        row_data.append(sheet_name)
        total_data.append(row_data)
        total_header[sheet_name] = sheet_header_data
def create_single_user(user):
    user_proucts= {}
    #将用户按产品分成各个字典
    for item in total_data_dict[user]:
        if item[-1] not in user_proucts.keys():
            user_proucts[item[-1]]=[]
            user_proucts[item[-1]].append(item)
        else:
            user_proucts[item[-1]].append(item)
    #创建用户的excel,
    w = xlwt.Workbook()
    for sheet_name in total_header:
        if sheet_name in user_proucts.keys():
            ws = w.add_sheet(sheet_name)
    w.save('dest/{}.xls'.format(user))
    rexcel = xlrd.open_workbook('dest/{}.xls'.format(user))
    excel = copy(rexcel)
    for sheet_name in user_proucts.keys():
        table = excel.get_sheet(sheet_name)
        for index,value in enumerate(total_header[sheet_name]):
            table.write(0, index, value)
        row=1
        for row_data in user_proucts[sheet_name]:
            for index,value in enumerate(row_data[:-1]):
                table.write(row,index,value)
            row+=1
    excel.save('dest/{}.xls'.format(user))

def insert_one_row(sheet_content,row_number,sheet_name):
    row_data = sheet_content.row_values(row_number)
    sheet_header_data = sheet_content.row_values(2)
    user = row_data[-2]
    if user:
        print(row_data)
        print(row_number)
    #     if not os.path.isfile('dest/{}.xls'.format(user)):
    #         w = xlwt.Workbook()
    #         ws = w.add_sheet(sheet_name)
    #         w.save('dest/{}.xls'.format(user))
    #     # print('open dest/{}.xls'.format(user))
    #     rexcel = xlrd.open_workbook('dest/{}.xls'.format(user))
    #     excel = copy(rexcel)
    #     print(rexcel.sheet_names())
    #     if not sheet_name  in rexcel.sheet_names():
    #         # print("create")
    #         excel.add_sheet(sheet_name)
    #         excel.save('dest/{}.xls'.format(user))
    #         rexcel = xlrd.open_workbook('dest/{}.xls'.format(user))
    #         excel = copy(rexcel)
    #         # for index,value in enumerate(sheet_header_data):
    #         #     table.write(0,index,value)
    #     rows =rexcel.sheet_by_name(sheet_name).nrows
    #     table = excel.get_sheet(sheet_name)
    #     row = rows
    #     if row == 0:
    #         for index,value in enumerate(sheet_header_data):
    #             table.write(row,index,value)
    #         row +=1
    #     for index,value in enumerate(row_data):
    #         table.write(row,index,value)
    #     excel.save('dest/{}.xls'.format(user))
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
    for row in range(3,sheet_content.nrows):
        aggregation_data(sheet_content,row,sheet_name)

#
user_sorted_data = sorted(total_data,key=lambda x:x[-3],reverse=True)
total_data_dict = {}
for single_user in user_sorted_data:
    if single_user[-3] not in total_data_dict.keys():
        total_data_dict[single_user[-3]]=[]
        total_data_dict[single_user[-3]].append(single_user)
    else:
        total_data_dict[single_user[-3]].append(single_user)

for key in total_data_dict:
    print(key)
    create_single_user(key)
