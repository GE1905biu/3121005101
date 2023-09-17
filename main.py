import numpy as np
import os.path
import logging
import re
import gensim as gensim
import jieba.analyse
import jieba
from gensim import corpora, similarities
from line_profiler import LineProfiler
from bs4 import BeautifulSoup

# 将jieba的日志级别设置为ERROR，禁止输出信息
jieba.setLogLevel(logging.ERROR)


# 用于获取文件内容的函数
def get_file_contents(path):
    try:
        with open(path, 'r', encoding='UTF-8') as file:
            return file.read()
    except FileNotFoundError:
        return None


# 用于将HTML转换为纯文本的函数
def html_to_text(html):
    soup = BeautifulSoup(html, 'html.parser')  # 使用BeautifulSoup解析HTML
    text = soup.get_text()  # 获取纯文本内容
    return text  # 返回纯文本


# 用于分词的函数
def distinguish(text):
    # 使用正则表达式将HTML标签从文本中删除
    text_without_html = re.sub(r'<[^>]+>', '', text)

    # 使用正则表达式将英文单词与标点符号之间的空格替换为特殊字符
    text_without_html = re.sub(r'([a-zA-Z0-9]+)([，。、！？,.!?\n])', r'\1\2', text_without_html)

    # 使用jieba库进行中文分词，同时保留英文单词
    words = list(jieba.cut(text_without_html, cut_all=False, HMM=True))

    # 恢复特殊字符为原始空格
    result = [word.replace('_', ' ') if '_' in word else word for word in words if
              re.match(u"[a-zA-Z0-9\u4e00-\u9fa5]", word)]

    return result  # 返回分词结果
# 计算文本相似度的函数
def calc_similarity(text1, text2):
    # 将输入的文本转换为字符串，如果它们已经是列表
    if isinstance(text1, list):
        text1 = ' '.join(text1)
    if isinstance(text2, list):
        text2 = ' '.join(text2)

    # 将两个文本拆分为词语列表
    texts = [text1.split(), text2.split()]

    dictionary = corpora.Dictionary(texts)  # 创建文本词典
    corpus = [dictionary.doc2bow(text) for text in texts]  # 将文本转换为词袋模型
    similarity = similarities.Similarity('-Similarity-index', corpus, num_features=len(dictionary))  # 计算相似度
    test_corpus_1 = dictionary.doc2bow(text1.split())  # 将第一个文本转换为词袋模型
    cosine_sim = similarity[test_corpus_1][1]  # 计算余弦相似度
    return float(cosine_sim)  # 返回相似度值作为浮点数

def output_result(result_path, similarity):
    try:
        result_file = open(result_path, 'w', encoding='utf-8')
    except (FileNotFoundError, PermissionError):
        print('输出文件路径错误')
        return FileNotFoundError, PermissionError
    result_file.write('相似度:' + str("%.2f%%" % (similarity * 100)))
    result_file.close()
    print('相似度:', ("%.2f%%" % (similarity * 100)))


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
        print("文件地址出错，无法找到文件计算相似度")
        print("论文要检测文件不存在")
        exit()
    main(path1, path2)
