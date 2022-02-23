# -*- coding: utf-8 -*-
# @Time : 2021/3/20 0020 13:20
# @Author : Bobby_Liukeling
# @File : connect_mysql.py
# 1. 连接数据库，
import pymysql
import pdb
# conn = pymysql.connect(
#     host='localhost',
#     user='root',
#     password='867425',
#     db='rabies',
#     charset='utf8',
#        # autocommit=True,    # 如果插入数据，， 是否自动提交? 和conn.commit()功能一致。
# )
# # ****python, 必须有一个游标对象， 用来给数据库发送sql语句， 并执行的.
# # 2. 创建游标对象，
# cur = conn.cursor()



list_dict = {'恩施土家族苗族自治州' : 'Enshi Tujia and Miao Autonomous Prefecture',
                        '鄂州市' : 'Ezhou city',
                        '黄冈市' : 'Huanggang city',
                        '黄石市' : 'Huangshi city',
                        '荆门市' : 'Jingmen city',
                        '荆州市' : 'Jingzhou city',
                        '潜江市' : 'Qianjiang city',
                        '神农架林区' : 'Shennongjia Forestry District',
                        '十堰市' : 'Shiyan city',
                        '随州市' : 'Suizhou city',
                        '天门市' : 'Tianmen city',
                        '武汉市' : 'Wuhan city',
                        '襄阳市' : 'Xiangyang city',
                        '咸宁市' : 'Xianning city',
                        '仙桃市' : 'Xiantao city',
                        '孝感市' : 'Xiaogan city',
                        '宜昌市' : 'Yichang city'}

# for key,value in list_dict.items():
#     name = value.split(' ')[0]
    # sql_uv = "SELECT county,county_en from rabies_in_county where area_name = %s GROUP BY county"
    # # 执行查询语句
    # cur.execute(sql_uv,name)
    # rows = cur.fetchall()
    # print("..........分割线.............")

    # print('case "'+name+'":')
    # print("    return "+name+"Map;")
    # for i in rows:
    #     # print(i)
    #     print("'"+i[0]+"':'"+i[1]+"',")
    #     # pdb.set_trace()

s = []
for key,value in list_dict.items():
    s.append(value.split(' ')[0])
print(s)







# sql_uv="SELECT county,county_en from rabies_in_county where area_name = 'Enshi' GROUP BY county"
# # 执行查询语句
# cur.execute(sql_uv)
# print(cur.fetchall())