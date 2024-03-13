import json
import os

# 定义读取和保存文件的路径
input_file_path = 'catalina-rong/rotate_env'
output_file_path = 'catalina-rong/rotate_env-simple'
json_name = 'light_transform.json'
interval = 5

# 读取JSON文件
with open(os.path.join(input_file_path, json_name), 'r') as json_file:
    raw_data = json.load(json_file)

# 仅保留trajectory中10的倍数编号的条目
if json_name == 'light_transform.json':
    my_str = "transform"
elif json_name == 'trajectory.json':
    my_str = "trajectory"
filtered_trajectory = {int(key) // interval: value for key, value in raw_data[my_str].items() if int(key) % interval == 0}

# 更新原始数据结构中的trajectory部分
raw_data[my_str] = filtered_trajectory

# 保存到新的JSON文件
with open(os.path.join(output_file_path, json_name), 'w') as json_file:
    json.dump(raw_data, json_file, indent=4)

print("Filtered JSON data has been saved to filtered_data.json.")