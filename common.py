import json
import os


def load_swagger_file(swagger_file_path):
    with open(swagger_file_path, 'r', encoding='utf-8') as file:
        in_data = json.load(file)
    return in_data


def extract_data(input_dict, keys_to_extract):
    """
    Extract data from a dictionary based on specified keys.
     #提取字典中的某些数据，仅限于字典下的第一层
    Parameters:
    - input_dict: The input dictionary.
    - keys_to_extract: A list of keys to extract from the dictionary.

    Returns:
    - A new dictionary containing only the specified keys and their corresponding values.
    """
    extracted_data = {key: input_dict[key] for key in keys_to_extract if key in input_dict}
    return extracted_data


def replace_key_values(input_dict, key_value_mapping):
    """
    Replace values of specified keys in a dictionary.
    替换输入字典中指定键的值
    Parameters:
    - input_dict: The input dictionary.
    - key_value_mapping: A dictionary where keys are the keys to replace,
      and values are the new values to set for those keys.

    Returns:
    - A new dictionary with replaced values.
    """
    modified_dict = input_dict.copy()
    for key, new_value in key_value_mapping.items():
        if key in modified_dict:
            modified_dict[key] = new_value
    return modified_dict


def replace_slash_with_dot(input_string):
    # 使用 replace 方法替换斜杠
    result_string = input_string.replace("/", ".")
    return result_string


def find_value_by_key(dictionary, target_key):
    """
    在嵌套字典中查找指定键的值。

    Parameters:
    - dictionary (dict): 要搜索的嵌套字典。
    - target_key (str): 要查找的键。

    Returns:
    - 如果找到，返回对应键的值；否则返回 None。
    """
    for key, value in dictionary.items():
        if key == target_key:
            return value
        elif isinstance(value, dict):
            # 如果值是字典，递归调用函数
            result = find_value_by_key(value, target_key)
            if result is not None:
                return result
    return None


def check_and_create_directory(directory_path):
    # 检查目录是否存在
    if not os.path.exists(directory_path):
        # 如果目录不存在，则创建新目录
        os.makedirs(directory_path)
        print(f"Directory created: {directory_path}")
    else:
        print(f"Directory already exists: {directory_path}")


def remove_key(dictionary, key_to_remove):
    if not isinstance(dictionary, dict):
        return dictionary

    new_dict = {}
    for key, value in dictionary.items():
        if key == key_to_remove:
            continue
        if isinstance(value, dict):
            new_dict[key] = remove_key(value, key_to_remove)
        else:
            new_dict[key] = value

    return new_dict


def extract(dictionary, extract_key):
    result_dict = {}

    for key, value in dictionary.items():
        if key == extract_key:
            result_dict[key] = value
        elif isinstance(value, dict):
            nested_result = extract(value, extract_key)
            if nested_result:
                result_dict[key] = nested_result

    return result_dict


def extract_description_keys(data, description_keys):
    result_dict = {}

    for key, value in data.items():
        if isinstance(value, dict):
            # 递归处理嵌套字典
            nested_result = extract_description_keys(value, description_keys)
            if nested_result:
                result_dict.update({f"{key}.{k}": v for k, v in nested_result.items()})
        elif isinstance(value, list):
            # 如果值是列表，递归处理每个元素
            for i, item in enumerate(value):
                if isinstance(item, dict):
                    nested_result = extract_description_keys(item, description_keys)
                    if nested_result:
                        result_dict.update({f"{key}[{i}].{k}": v for k, v in nested_result.items()})
        elif key == description_keys:
            # 如果当前键是"description"，将其上一级的键和值添加到结果字典中
            result_dict[key] = value

    return result_dict


def get_str(result_dict):
    str_new_dict = ""
    # try:
    for k, v in result_dict.items():
        str_a = f'{k}{v}；'
        str_new_dict = str_new_dict+str_a
        str_new_dict = str_new_dict.replace('.comments', '')
        str_new_dict = str_new_dict.replace('items.', '')
        str_new_dict = str_new_dict.replace('properties.', '')
    # except Exception as e:
    #     print(f'不存在包含’description‘的字段:{e}')
    return str_new_dict


