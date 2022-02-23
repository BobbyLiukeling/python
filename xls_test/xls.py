import xlsxwriter

workbook=xlsxwriter.Workbook("demo.xlsx")#创建一个工作表,注意Workbook的大小写
worksheet=workbook.add_worksheet()#创建一个工作表对象

worksheet.set_column("A:A",20)#设置第一行的宽度为20px
worksheet.write("A1","hello world")#将数据写入单元格，位置是A1
worksheet.write("A2","python")

#第二种将数据写入单元格方法
worksheet.write(2,0,123)#位置：A3
worksheet.write(3,0,231)#位置：A4
worksheet.write(4,0,"=SUM(A3:A4)")#求和并写入

#写入图片
worksheet.insert_image("A5","img1.jpg")
workbook.close()
