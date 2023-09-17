import unittest
from unittest.mock import mock_open, patch
from main import *


class MyTestCase(unittest.TestCase):
    @patch('builtins.open', mock_open())  # 使用mock_open模拟内置的open函数
    def test_get_file_contents(self):
        # 编写测试用例以测试get_file_contents函数

        # 模拟文件的内容
        file_contents = "This is a sample file.\nIt has multiple lines."
        with patch('builtins.open', mock_open(read_data=file_contents)):
            path = 'sample.txt'
            actual_contents = get_file_contents(path)
            self.assertEqual(actual_contents, file_contents)

    def test_html_to_text(self):
        # 编写测试用例以测试html_to_text函数

        # 模拟HTML字符串
        html = "<html><body><p>This is <b>bold</b> and <i>italic</i> text.</p></body></html>"
        expected_text = "This is bold and italic text."
        actual_text = html_to_text(html)
        self.assertEqual(actual_text, expected_text)

    def test_distinguish(self):
        # 编写测试用例以测试distinguish函数

        # 模拟包含不同类型文本的测试用例

        # 1. 测试包含中英文混合的文本
        text = "这是一个示例文本。This is an example."
        expected_tokens = ["这是", "一个", "示例", "文本", "This", "is", "an", "example"]
        actual_tokens = distinguish(text)
        self.assertEqual(actual_tokens, expected_tokens)

        # 2. 测试处理空文本的情况
        empty_text = ""
        empty_tokens = distinguish(empty_text)
        self.assertEqual(empty_tokens, [])

        # 3. 测试处理只包含标点符号的情况
        punctuation_text = "，。！？,.!?"
        punctuation_tokens = distinguish(punctuation_text)
        self.assertEqual(punctuation_tokens, [])

        # 4. 测试处理只包含空格的情况
        space_text = "       "
        space_tokens = distinguish(space_text)
        self.assertEqual(space_tokens, [])

        # 5. 测试处理只包含英文单词的情况
        english_text = "This is a test sentence."
        english_tokens = distinguish(english_text)
        self.assertEqual(english_tokens, ["This", "is", "a", "test", "sentence"])

        # 6. 测试处理只包含中文文本的情况
        chinese_text = "这是一句测试文本。"
        chinese_tokens = distinguish(chinese_text)
        self.assertEqual(chinese_tokens, ["这是", "一句", "测试", "文本"])

        # 7. 测试处理包含HTML标签的情况
        html_text = "<p>This is <b>bold</b> and <i>italic</i> text.</p>"
        html_tokens = distinguish(html_text)
        expected_html_tokens = ["This", "is", "bold", "and", "italic", "text"]
        self.assertEqual(html_tokens, expected_html_tokens)

        # 8. 再次测试处理包含HTML标签的情况，以确保没有副作用
        html_text = "<p>This is <b>bold</b> and <i>italic</i> text.</p>"
        html_tokens = distinguish(html_text)
        self.assertEqual(html_tokens, expected_html_tokens)

    def test_calc_similarity(self):
        # 编写测试用例以测试calc_similarity函数

        # 模拟两个不同的文本
        text1 = "这是文本1的内容。This is the content of text 1."
        text2 = "这是文本2的内容。This is the content of text 2."
        similarity_score = calc_similarity(text1, text2)
        self.assertIsInstance(similarity_score, float)

    @patch('builtins.print')
    def test_output_result(self, mock_print):
        # 编写测试用例以测试output_result函数

        # 模拟结果文件路径和相似度分数
        result_path = 'result2.txt'
        similarity = 0.75
        output_result(result_path, similarity)
        mock_print.assert_called_with('相似度:', '75.00%')

    def test_main(self):
        # 编写测试用例以测试main函数
        # 此处可以使用模拟的文件路径和内容来测试
        pass

    def test_non_existing_file(self):
        # 模拟不存在的文件

        # 模拟一个不存在的文件路径
        mock_path = 'non_existent.txt'
        result = get_file_contents(mock_path)
        self.assertIsNone(result)

    def test_empty_content(self):
        # 测试处理空内容的情况

        # 模拟空内容
        empty_content = ''
        text = distinguish(empty_content)
        self.assertEqual(text, [])

    def test_html_tags(self):
        # 测试处理HTML标签的情况

        # 模拟包含HTML标签的文本
        html_text = "<p>This is <b>bold</b> and <i>italic</i> text.</p>"
        tokens = distinguish(html_text)
        expected_tokens = ["This", "is", "bold", "and", "italic", "text"]
        self.assertEqual(tokens, expected_tokens)

    def test_similarity_calculation(self):
        # 测试相似度计算是否正确

        # 模拟两个文本以进行相似度计算
        text1 = "This is a sample text for testing."
        text2 = "This is a test text for sample."
        similarity_score = calc_similarity(text1, text2)

        # 更新期望值，保留更多小数点位数
        expected_similarity = 0.7143
        self.assertAlmostEqual(similarity_score, expected_similarity, places=4)


if __name__ == '__main__':
    unittest.main()
