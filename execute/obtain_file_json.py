from common import *
import os


def get_json_pointer(json_pointer, openapi_spec):  # 解析JSON 指针并获得对应的请求或响应结构,openapi_specs是组件层级数据
    # 解析 JSON 指针
    pointer_parts = json_pointer.lstrip("#/").split("/")
    # 根据 JSON 指针获取值
    current_value = openapi_spec
    for part in pointer_parts:
        if part in current_value:
            current_value = current_value[part]
        else:
            current_value = None
            break
    return current_value


def process_dict(dictionary, in_data):
    """
    Recursively find keys with a specific value in a nested dictionary,
    call AAA method with the key, and replace the value with the result.
    遍历字典所有层级数据，并找到所有值为“$ref”的key，并用key作为一个方法###的入场获取返回值###，并用返回值替换掉key的值
    Parameters:
    - dictionary: The input dictionary.

    Returns:
    - A new dictionary with replaced values.
    """
    modified_dict = dictionary.copy()

    for key, value in modified_dict.items():
        if key == '$ref':
            # Call AAA method with the key
            bb = get_json_pointer(value, in_data)
            # modified_dict[key] = bb
            dictionary = bb

        if isinstance(value, dict):
            # Recursively process nested dictionaries
            nested_result = process_dict(value, in_data)
            # modified_dict[key] = nested_result
            dictionary[key] = nested_result

    return dictionary


def get_any_datas(in_dict, in_data):
    keys_to_extract_list = ['openapi', 'info', 'servers', 'tags', 'requestBody', 'parameters', 'responses', 'summary', 'comments']
    data_file = extract_data(in_dict, keys_to_extract_list)
    # decoded_str = codecs.decode(data_file.get("tags")[0], 'unicode_escape')
    # decoded_string = bytes(data_file.get("tags")[0], 'utf-8').decode('unicode_escape')
    # data_file = replace_key_values(data_file, {"tags": decoded_str})
    # data_requestBody = process_dict(data_file1.get("requestBody"))
    # data_responses = process_dict(data_file1.get("responses"))
    # sample_dict = {
    #     "requestBody": data_requestBody,
    #     "responses": data_responses
    # }
    # data_file = replace_key_values(data_file1, sample_dict)
    modified_dict = process_dict(data_file, in_data)
    modified_dict = process_dict(modified_dict, in_data)
    modified_dict = process_dict(modified_dict, in_data)
    return modified_dict


def generate_feature(key, data_file, subdirectory_path):
    json_file_path = os.path.join(subdirectory_path, str(key + ".feature"))
    file_servers = data_file.get("servers")
    file_url = data_file.get("url")
    file_tags = data_file.get("tags")
    file_responses = data_file.get("responses")
    summary = data_file.get("summary")
    file_comments = data_file.get("comments")
    responses = find_value_by_key(file_responses.get("200"), "schema")
    file_responses_abnormal = {}
    for k, v in file_responses.items():
        if k != "200":
            abnormal_name = str(k)
            file_responses_abnormal[abnormal_name] = find_value_by_key(v, "schema")

    file_request_name = "request"
    file_request = None
    if key == "get":
        file_request_name = "parameters"
        try:
            file_request = find_value_by_key(data_file.get("parameters"), "schema")
        except Exception as e:
            print(e)
            file_request = data_file.get("parameters")

    elif key == "post":
        try:
            file_request = find_value_by_key(data_file.get("requestBody"), "schema")
        except Exception as e:
            file_request = data_file.get("requestBody")
    elif key == "put":
        try:
            file_request_name = "parameters"
            file_request = find_value_by_key(data_file.get("parameters"), "schema")
        except Exception as e:
            print(f'发现异常：{e}')
            try:
                file_request = find_value_by_key(data_file.get("requestBody"), "schema")
            except Exception as e:
                print(e)
                try:
                    file_request = data_file.get("requestBody")
                except Exception as e:
                    file_request = data_file.get("parameters")
    elif key == "head":
        file_request = None
    elif key == "delete":
        try:
            file_request = find_value_by_key(data_file.get("requestBody"), "schema")
        except Exception as e:
            print(e)
            file_request = data_file.get("requestBody")
    # new_dict_request = extract_description_keys(file_request, 'comments')
    # request_str = get_str(new_dict_request)
    responses_str = {}
    request_str = {}
    try:
        responses_str = f'{file_comments}'
        request_str = data_file.get("requestBody").get('comments')
        request_str = f'请求体中的{request_str}'
    except Exception as e:
        print(f'此接口无comments{e}')
    # responses_str = get_str(responses_dict)
    karate_scenario = f"""
    Feature: {file_tags}
    servers:{file_servers}
    接口描述：{summary}
    Scenario:
        # 接口契约描述
        # -------------------------------------------------------------
        {file_request_name}:
        {file_request}
        # -------------------------------------------------------------
        responses:
        {responses}
        abnormal responses:
        {file_responses_abnormal}
        # -------------------------------------------------------------
        Given path '{file_url}'
        When method {key}
        Then status 200
        {request_str}
        {responses_str}
        根据提供的条件尽可能多的生成karate测试用例
        """
    # with open(json_file_path, 'w', encoding='utf-8') as json_file:
    #     json.dump(karate_scenario, json_file, indent=4)
    with open(json_file_path, 'w', encoding='utf-8') as file:
        file.write(karate_scenario)

    print(f"OpenAPI JSON file has been created: {json_file_path}")


def generate_json(key, data_file, subdirectory_path):
    json_file_path = os.path.join(subdirectory_path, str(key + ".json"))
    file_responses = data_file.get("responses")
    responses = find_value_by_key(file_responses.get("200"), "schema")
    data_file["responses"] = responses
    file_responses_abnormal = {}
    for k, v in file_responses.items():
        if k != "200":
            abnormal_name = str(k)
            file_responses_abnormal[abnormal_name] = find_value_by_key(v, "schema")
    data_file["responses_abnormal"] = file_responses_abnormal
    # with open(json_file_path, 'w', encoding='utf-8') as json_file:
    #     json.dump(karate_scenario, json_file, indent=4)
    with open(json_file_path, 'w', encoding='utf-8') as file:
        file.write(data_file)

    print(f"OpenAPI JSON file has been created: {json_file_path}")


def create_subdirectories_from_dict_keys(dictionary):
    file_paths = {}
    name = dictionary.get("tags")[0].get("name")
    check_and_create_directory(name)
    try:
        file_paths = dictionary.get("paths")
    except Exception as e:
        print(f'未找到paths：{e}')
    file_openapi = {}
    try:
        file_openapi = dictionary.get("openapi")
    except Exception as e:
        print(f'未找到openapi：{e}')
    file_info = {}
    try:
        file_info = dictionary.get("info")
    except Exception as e:
        print(f'未找到info：{e}')
    file_servers = {}
    try:
        file_servers = dictionary.get("servers")[0].get("url")
    except Exception as e:
        print(f'未找到servers：{e}')
    file_cookie = {}
    try:
        file_cookie = dictionary.get("cookie")
    except Exception as e:
        print(f'未找到cookie：{e}')
    file_comments = ""
    try:
        file_comments = dictionary.get("comments")
    except Exception as e:
        print(f'未找到comments：{e}')
    # 遍历字典的键
    for key, value in file_paths.items():
        # 构造子目录路径
        subdirectory_path = os.path.join(name, str(replace_slash_with_dot(key)))
        subdirectory_path = "prompt_files\\" + subdirectory_path
        key_name = key
        # 创建子目录
        os.makedirs(subdirectory_path, exist_ok=True)
        print(f"Created subdirectory: {subdirectory_path}")
        for key, value in value.items():  # get/post/下的层级
            # 构造次子目录openapi文件路径
            files_data = {"openapi": file_openapi, "info": file_info, "servers": file_servers, "cookie": file_cookie, "comments": file_comments}
            files_data.update(value)
            data_file = get_any_datas(files_data, dictionary)
            new_data_file = {"url": key_name}
            new_data_file.update(data_file)
            remove_key(new_data_file, "format")
            generate_feature(key, new_data_file, subdirectory_path)   # 生成feature文件的promt
            # generate_json(key, new_data_file, subdirectory_path)    # 生成json文件的各种参数



