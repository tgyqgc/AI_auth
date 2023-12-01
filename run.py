from execute.obtain_file_json import *
"""
直接运行此文件即可根据对应的swagger文件生成prompt指令的feature文件
swagger_file_path为读取的swagger文件地址
"""
swagger_file_path = "swagger/webswagger1.json"
# 指定目录的路径

my_dict = load_swagger_file(swagger_file_path)

# 调用函数创建提取文件
create_subdirectories_from_dict_keys(my_dict)



