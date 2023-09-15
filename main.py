import re

import jieba
def arrive_file_contents(path):  #读取文件
    str = ''
    f = open(path,'r',encoding = 'UTF-8')
    line = f.readline()
    while line:
        str = str + line
        line = f.readline()
        f.close()
        return str

def distinguish(str):  #分词
    str = jieba.lcut(str)
    result = []
    for tags in str :
        if re.match(u"[a-zA-Z0-9\u4e00-\u9fa5]",tags):
            result.append(tags)
        else:
            pass
        return result

def main(path1,path2):  #主函数
    save_path = 'D:\\1\\3121005101\\result.txt'  #输出路径
    str1 = arrive_file_contents(path1)
    str2 = arrive_file_contents(path2)
    text1 = distinguish(str1)
    text2 = distinguish(str2)