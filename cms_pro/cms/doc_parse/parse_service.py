import json
import os

from langchain_community.document_loaders import PyPDFLoader
from zhipuai import ZhipuAI


def summarize_paper(pdf_path):
    # 1. 提取PDF内容并转换成JSON格式
    loader = PyPDFLoader(pdf_path)
    docs = loader.load()
    print(f"处理文件路径为：{os.path.abspath(pdf_path)}")
    datas = [{'page': index + 1, 'page_content': doc.page_content} for index, doc in enumerate(docs)]
    res = json.dumps(datas, ensure_ascii=False, indent=4)

    # 2. 准备提示词
    prompt = f"""请根据以下JSON格式的论文内容，按照提供的结构总结论文的关键要点。需要包括研究背景及动机、研究问题、方法和技术、实验和结果、结论和贡献、挑战和不足等部分。

    JSON输入数据:
    {res}

    总结输出结构:
    1. **研究背景及动机**：
       - 简要描述研究背景。
       - 论文研究的主要动机是什么？

    2. **研究问题**：
       - 论文试图解决的主要问题是什么？

    3. **方法和技术**：
       - 论文中使用的主要研究方法和技术有哪些？
       - 这些方法的关键步骤和具体实现是什么？

    4. **实验和结果**：
       - 概述主要实验设计和测试。
       - 主要的实验结果和发现是什么？

    5. **结论和贡献**：
       - 论文得出了哪些主要结论？
       - 论文的主要贡献和创新点是什么？
       - 这些贡献和创新如何推动了领域的发展？

    6. **挑战和不足**：
       - 论文提到的主要挑战和不足有哪些？

    请根据以上结构，详细总结每个部分的内容。"""

    # 3. 使用生成的提示词向语言模型发送请求
    client = ZhipuAI(api_key="26ff506e4e8ef9b787251f1914532aaa.50TvJVih12un2iiw")
    response = client.chat.completions.create(
        model="glm-4-0520",
        messages=[
            {"role": "user", "content": prompt},
        ],
    )
    res = response.choices[0].message.content
    print(f"处理结束，处理结果为为：{res}")

    # 4. 输出模型的响应结果
    return res


# 示例调用

