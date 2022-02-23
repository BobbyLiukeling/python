import xlsxwriter

workbook = xlsxwriter.Workbook('Demo1.xlsx')    # 创建一个名为‘Demo1.xlsx’的工作表
worksheet = workbook.add_worksheet()            # 创建一个工作表对象

worksheet.set_column('A:A', 20)                 # 设定第一列（A）的宽度为20px
# bold = workbook.add_format({'blod': True})

worksheet.write('A1', 'Hello World！')           # A1单元格写入‘Hello World！’
worksheet.write('A2', '你好，世界！')             # A2单元格写入‘你好，世界！’

# 行列表示法的单元格下标以0作为起始值，如‘3,0’等价于‘A3’
worksheet.write(2, 0, 123)              # 使用列行表示法写入数字‘123’
worksheet.write(3, 0, 456)              # 使用列行表示法写入数字‘456’
worksheet.write(4, 0, '=SUM(A3:A4)')    # 求A3:A4的和，并写入‘4,0’，即‘A5’

worksheet.insert_image('A5', 'img1.jpg')        # 在A5单元格插入图片
workbook.close()        # 关闭Excel文件