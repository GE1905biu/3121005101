import os.path
import re
import gensim as gensim
import jieba
import difflib
from line_profiler import LineProfiler
from bs4 import BeautifulSoup


# 用于获取文件内容的函数
def get_file_contents(path):
    str = ''  # 用于存储文件内容的字符串
    f = open(path, 'r', encoding='UTF-8')  # 打开文件，使用UTF-8编码读取
    line = f.readline()  # 逐行读取文件内容
    while line:
        str = str + line  # 将每一行的内容拼接到str中
        line = f.readline()
    f.close()  # 关闭文件
    return str  # 返回文件内容的字符串


# 用于将HTML转换为纯文本的函数
def html_to_text(html):
    soup = BeautifulSoup(html, 'html.parser')  # 使用BeautifulSoup解析HTML
    text = soup.get_text()  # 获取纯文本内容
    return text  # 返回纯文本


# 用于分词的函数
def distinguish(text):
    words = jieba.lcut(text)  # 使用jieba库进行中文分词
    # 仅保留包含字母、数字、汉字或HTML标签的词语
    result = [word for word in words if re.match(u"[a-zA-Z0-9\u4e00-\u9fa5]", word) or re.match(r'<[^>]+>', word)]
    return result  # 返回分词结果


# 计算文本相似度的函数
def calc_similarity(text1, text2):
    texts = [text1, text2]  # 将两个文本组成列表
    dictionary = gensim.corpora.Dictionary(texts)  # 创建文本词典
    corpus = [dictionary.doc2bow(text) for text in texts]  # 将文本转换为词袋模型
    similarity = gensim.similarities.Similarity('-Similarity-index', corpus, num_features=len(dictionary))  # 计算相似度
    test_corpus_1 = dictionary.doc2bow(text1)  # 将第一个文本转换为词袋模型
    cosine_sim = similarity[test_corpus_1][1]  # 计算余弦相似度
    return cosine_sim  # 返回相似度值


# 主函数
def main(path1, path2):
    save_path = 'D:\\1\\3121005101\\result.txt'  # 输出结果保存路径
    str1 = get_file_contents(path1)  # 获取第一个文件的内容
    str2 = get_file_contents(path2)  # 获取第二个文件的内容

    if not str1 or not str2:
        return None  # 如果任一文件内容为空，返回None表示处理失败

    # 将HTML转换为纯文本
    text1 = html_to_text(str1)
    text2 = html_to_text(str2)

    # 对文本进行分词处理
    text1 = distinguish(text1)
    text2 = distinguish(text2)

    # 计算文本相似度
    similarity = calc_similarity(text1, text2)

    print("论文相似度：%.4f" % similarity)

    # 将相似度结果写入文件
    with open(save_path, 'w', encoding="utf-8") as f:
        f.write("论文相似度：%.4f" % similarity)

    return similarity  # 返回相似性值


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
    p_wrap(path1, path2)
    p.print_stats()
    p.dump_stats('saveName.lprof')
