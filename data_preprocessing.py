# -*- coding: utf-8 -*-
import os  
from xml.dom import minidom  
from urllib.parse import urlparse
import codecs  
# import importlib,sys  
# default_encoding = 'utf-8'  
# if sys.getdefaultencoding() != default_encoding:  
#     importlib.reload(sys)  
#     sys.setdefaultencoding(default_encoding)  
  
def file_fill(file_dir): #得到文本.txt的路径  
    for root, dirs, files in os.walk(file_dir):
        # print(files)
        for f in files:  
            tmp_dir = '.\sogou_after' + '\\' + f  # 加上标签后的文本

            text_init_dir = file_dir + '\\' + f  #原始文本
            print(text_init_dir)
            print(tmp_dir) 
            # print(text_init_dir)
            file_source = codecs.open(text_init_dir, 'r', 'ansi')  
            ok_file = codecs.open(tmp_dir, 'w', 'utf-8')  
            start = '<docs>\n'  
            end = '</docs>'  
            line_content = file_source.readlines()  
            ok_file.write(start)  
            for lines in line_content:  
                text_temp = lines.replace('&', '.')
                text = text_temp.replace(' ', '')
                ok_file.write(text)  
            ok_file.write('\n' + end)  
  
            file_source.close()  
            ok_file.close()  


def file_read(file_dir):
    #建立url和类别的映射词典,可以参考搜狗实验室的对照.txt,有18类，这里增加了奥运，减少了社会、国内和国际新闻
    dicurl = {'auto.sohu.com':'qiche','it.sohu.com':'hulianwang','health.sohu.com':'jiankang','sports.sohu.com':'tiyu',
    'travel.sohu.com':'lvyou','learning.sohu.com':'jiaoyu','career.sohu.com':'zhaopin','cul.sohu.com':'wenhua',
    'mil.news.sohu.com':'junshi','house.sohu.com':'fangchan','yule.sohu.com':'yule','women.sohu.com':'shishang',
    'media.sohu.com':'chuanmei','gongyi.sohu.com':'gongyi','2008.sohu.com':'aoyun', 'business.sohu.com': 'shangye'} 
    
    path = ".\sogou_grouped\\"

    for root, dirs, files in os.walk(file_dir):  
        for f in files:
            print(f)
            doc = minidom.parse(file_dir + "\\" + f)  
            root = doc.documentElement  
            claimtext = root.getElementsByTagName("content")  
            claimurl = root.getElementsByTagName("url")  
            for index in range(0, len(claimurl)):  
                if (claimtext[index].firstChild == None):  
                    continue  
                url = urlparse(claimurl[index].firstChild.data)  
                if url.hostname in dicurl:  
                    if not os.path.exists(path + dicurl[url.hostname]):  
                        os.makedirs(path + dicurl[url.hostname])  
                    fp_in = open(path + dicurl[url.hostname] + "\%d.txt" % (len(os.listdir(path + dicurl[url.hostname])) + 1),"w")  
                    temp_bytescontent = (claimtext[index].firstChild.data).encode('GBK','ignore')   #这里的ignore是说，如果编码过程中有GBK不认识的字符可以忽略
                    fp_in.write(temp_bytescontent.decode('GBK','ignore'))
    print('finished!')

  
   
if __name__=="__main__":  
    print("Program begin...")
    # file_fill(".\SogouCS.reduced")

    file_read(".\sogou_after") 