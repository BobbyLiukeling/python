
# a = {3.5:[88,84,90,90],1:[86,],3:[69,74,92,93,68,74],4:[84],0.5:[90,92,80],0.3:[88,89]}
# print(a.keys())
# print(type(a.keys()))
#
# totle = 0
# count = 0
# for key,value in a.items():
#     for i in value:
#         totle = i*key+totle
#     count = len(value)*key+count
# print(totle)
# print(count)
# print(totle/count)

import os
from moviepy.editor import VideoFileClip
# files = os.listdir(r'F:\各种软件下载目录\BaiduNetdiskDownload\03 2019韦林恋恋有词【新版】')
files = os.listdir(r'F:\各种软件下载目录\BaiduNetdiskDownload\02.恋练不忘-词组背多分【完】')
# print(type(files[0]))
# print(files[0])
# if files[0].endswith('.mp4'):
#     print('dddd')

# print(files)
# print(type(files))
# print(files[0])
# clip = VideoFileClip(r'F:\各种软件下载目录\BaiduNetdiskDownload\03 2019韦林恋恋有词【新版】'+'\\'+'044 19恋练有词Unit10（3）.mp4')
# print(clip.duration)


count = 0.0
for file in files:
    if file.endswith('.mp4'):
        try:
            # print(file)
            times = VideoFileClip(r'F:\各种软件下载目录\BaiduNetdiskDownload\02.恋练不忘-词组背多分【完】'+'\\'+file)
            s = int(times.duration)
            count = s+count
            times.close()#如果不清除缓存，则很快将会溢出从而出现异常
        except Exception as e:

            print(file)
            print(e)
            pass
# print(count)
print(int(count/3600))

