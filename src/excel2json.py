import pandas as pd
import json

# 读取 Excel 文件路径
file_path = "data/questions_full.xlsx"
output_json_path = "data/output/questions.json"


# 加载 Excel 的第一个工作表
df = pd.read_excel(file_path)

# 定义需要处理为列表的字段
fields_to_list = ["类型", "领域"]

# 处理数据：将指定字段中包含 ',' 的值转换为列表
def process_field(value):
    if isinstance(value, str) and ',' in value:
        return [item.strip() for item in value.split(',')]
    return value

for field in fields_to_list:
    if field in df.columns:
        df[field] = df[field].apply(process_field)

# 将数据框转换为 JSON
data = df.to_dict(orient='records')

# 保存为 JSON 文件
with open(output_json_path, 'w', encoding='utf-8') as json_file:
    json.dump(data, json_file, ensure_ascii=False, indent=4)

print(f"JSON 文件已保存到 {output_json_path}")
