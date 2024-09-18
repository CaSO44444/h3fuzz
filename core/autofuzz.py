import json

from lib.deduplication import generate_signature
from lib.read_json import read_data_from_file, write_data_to_file

unique_requests = []
seen_signatures = set()

file_path = "request_response_pairs.json"
data = read_data_from_file(file_path)

for request in data:
    signature = generate_signature(request)
    if signature not in seen_signatures:
        seen_signatures.add(signature)
        unique_requests.append(request)

# 如果需要，也可以将去重后的数据写回到另一个文件
output_file_path = 'unique_requests.json'
write_data_to_file(output_file_path, unique_requests)