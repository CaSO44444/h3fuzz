import json
import requests
from bs4 import BeautifulSoup

# 爬取数据
with open('../config/test.json', 'r',encoding="utf-8") as file:
    for line in file:
        try:
            item = json.loads(line.strip())
            link = item['link']

            # 访问页面
            response = requests.get(link,timeout=2)
            soup = BeautifulSoup(response.content, 'html.parser')

            # 提取非隐藏和非复选框的 input 字段及其属性(除了 style)
            inputs = soup.find_all('input', type=lambda x: x not in ['hidden', 'checkbox'])
            with open('input_attributes.txt', 'a') as output_file:
                for input_field in inputs:
                    input_attrs = ' '.join(
                        [f"{key}='{value}'" for key, value in input_field.attrs.items() if key != 'style'])
                    output_file.write(f"Link: {link}, Input Attributes: {input_attrs}\n")
                    print(f"Link: {link}")
        except (ValueError, KeyError):
            # 如果解析 JSON 或提取 link 字段出错,继续处理下一行
            continue
        except:
            # 如果访问页面出错,继续处理下一个链接
            continue

# from mlxtend.preprocessing import TransactionEncoder
# from mlxtend.frequent_patterns import apriori, association_rules
# import pandas as pd
#
# # 假设你的文件名为 data.txt
# file_name = 'input_attributes.txt'
#
#
# # 读取文件并提取属性
# def extract_attributes(file_name):
#     with open(file_name, 'r') as file:
#         lines = file.readlines()
#     attributes_list = []
#     for line in lines:
#         if 'Input Attributes:' in line:
#             start_index = line.find('Input Attributes:') + len('Input Attributes:')
#             attributes = line[start_index:].strip()
#             attributes_list.append(attributes)
#     return attributes_list
#
#
# # 将属性字符串转换为交易列表
# def parse_attributes(attributes_list):
#     transactions = []
#     for attributes in attributes_list:
#         values = [item.split('=')[1].strip().strip("'") for item in attributes.split() if '=' in item and item.split('=')[1].strip().strip("'")]
#         transactions.append(values)
#     return transactions
#
#
# # 主函数
# def main():
#     attributes_list = extract_attributes(file_name)
#     transactions = parse_attributes(attributes_list)
#     print(transactions)
#     # 检查是否提取到任何交易
#     if not transactions:
#         print("No transactions found.")
#         return
#     # 使用TransactionEncoder进行一键式编码
#     te = TransactionEncoder()
#     te_ary = te.fit(transactions).transform(transactions)
#     df = pd.DataFrame(te_ary, columns=te.columns_)
#
#     # 检查数据框是否为空
#     if df.empty:
#         print("The DataFrame is empty after one-hot encoding.")
#         return
#     # 应用Apriori算法
#     frequent_itemsets = apriori(df, min_support=0.01, use_colnames=True)
#
#     # 检查是否找到频繁项集
#     if frequent_itemsets.empty:
#         print("No frequent itemsets found. Please check the min_support value.")
#         return
#
#     # 生成关联规则
#     rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=0.01)
#
#     # 打印频繁项集和关联规则
#
#     rules.to_csv('association_rules.csv', index=False)
#
#
# if __name__ == "__main__":
#     main()