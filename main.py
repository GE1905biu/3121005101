def arrive_file_contents(path):
    str = ''
    f = open(path,'r',encoding = 'UTF-8')
    line = f.readline()
    while line:
        str = str + line
        line = f.readline()
        f.close()
        return str
def main(path1,path2):
    save_path = 'D:\\1\\3121005101\\result.txt'  #输出路径
    str1 = arrive_file_contents(path1)
    str2 = arrive_file_contents(path2)