import os.path
import re
import gensim as gensim
import jieba
from line_profiler import LineProfiler
from bs4 import BeautifulSoup


def get_file_contents(path):
    str = ''
    f = open(path,'r',encoding = 'UTF-8')
    line = f.readline()
    while line:
        str = str + line
        line = f.readline()
    f.close()
    return str

def html_to_text(html):
    soup = BeautifulSoup(html,'html.parser')
    text = soup.get_text()
    return text

def distinguish(str):  #分词
    str = jieba.lcut(str)
    result = []
    for tags in str :
        if re.match(u"[a-zA-Z0-9\u4e00-\u9fa5]",tags):
            result.append(tags)
        else:
            pass
    return result

def calc_similarity(text1,text2):
    texts = [text1,text2]
    dictionary = gensim.corpora.Dictionary(texts)
    corpus = [dictionary.doc2bow(text)for text in texts]
    similarity = gensim.similarities.Similarity('-Similarity-index',corpus,num_features = len(dictionary))
    test_corpus_1 = dictionary.doc2bow(text1)
    cosine_sim = similarity[test_corpus_1][1]
    return cosine_sim

def main(path1,path2):  #主函数
    save_path = 'D:\\1\\3121005101\\result.txt'  #输出路径
    str1 = get_file_contents(path1)
    str2 = get_file_contents(path2)

    #将html转换成txt格式
    text1 = html_to_text(str1)
    text2 = html_to_text(str2)

    text1 = distinguish(str1)
    text2 = distinguish(str2)
    similarity = calc_similarity(text1,text2)
    print("论文相似度：%.2f"%similarity)
    f = open(save_path,'w',encoding = "utf-8")
    f.write("论文相似度：%.2f"%similarity)
    f.close()

if __name__ == '__main__':
     path1 = input("输入论文原文的文件绝对路径：")
     path2 = input("输入要检测论文的文件绝对路径：")
     if not os.path.exists(path1):
         print("论文原文文件不存在")
         exit()
     if not os.path.exists(path2):
         print("论文要检测文件不存在")
         exit()
     main(path1, path2)
     p = LineProfiler()
     p.add_function(get_file_contents)
     p.add_function(distinguish)
     p.add_function(calc_similarity)
     p_wrap = p(main)
     p_wrap(path1,path2)
     p.print_stats()
     p.dump_stats('saveName.lprof')
