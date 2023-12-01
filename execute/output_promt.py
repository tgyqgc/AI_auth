from common import *


def get_interface_types(interface):
    global types_interface
    if "get" in interface:
        types_interface = "get"
    if "post" in interface:
        types_interface = "post"
    if "put" in interface:
        types_interface = "put"
    if "delete" in interface:
        types_interface = "delete"
    if "trace" in interface:
        types_interface = "head"
    return types_interface


def output_file(filename_list):
    name_output = '，进行有效性检查，校验请求参数和响应参数的格式、类型'
    file_list = []
    for items in filename_list:
        types_interface = get_interface_types(items)
        items = load_swagger_file(items)
        file_openapi = items.get("openapi")
        file_info = items.get("info")
        file_servers = items.get("servers")
        file_url = items.get("url")
        file_tags = items.get("tags")
        file_cookie = items.get("cookie")
        file_responses = items.get("responses")
        file_responses_abnormal = {}
        for k, v in file_responses.items():
            if k != "200":
                name = "file_responses" + str(k)
                try:
                    file_responses_abnormal[name] = v.get("content").get("*/*").get("schema").get("ref_body")
                except Exception as e:
                    file_responses_abnormal[name] = v
        try:
            file_responses_200 = items.get("responses").get("200").get("content").get("*/*").get("schema").get("ref_body")
        except Exception as e:
            file_responses_200 = items.get("responses").get("200")
        if types_interface == "get":
            file_parameters = items.get("parameters")
            statement = f"根据openapi{file_openapi}规范，接口信息为{file_info}，服务器信息为{file_servers}，url={file_url},cookie={file_cookie},接口描述为{file_tags},parameters={file_parameters},正确响应为{file_responses_200},异常响应包括：{file_responses_abnormal}，使用{types_interface}请求写一个接口测试用例{name_output}"
            file_list.append(statement)
        elif types_interface == "post":
            file_request = items.get("requestBody")
            statement = f"根据openapi{file_openapi}规范，接口信息为{file_info}，服务器信息为{file_servers}，url={file_url},cookie={file_cookie},接口描述为{file_tags},request={file_request},正确响应为{file_responses_200},异常响应包括：{file_responses_abnormal}，使用{types_interface}请求写一个接口测试用例{name_output}"
            file_list.append(statement)
        elif types_interface == "put":
            file_parameters = items.get("parameters")
            statement = f"根据openapi{file_openapi}规范，接口信息为{file_info}，服务器信息为{file_servers}，url={file_url},cookie={file_cookie},接口描述为{file_tags},parameters={file_parameters},正确响应为{file_responses_200},异常响应包括：{file_responses_abnormal}，使用{types_interface}请求写一个接口测试用例{name_output}"
            file_list.append(statement)
        elif types_interface == "head":
            statement = f"根据openapi{file_openapi}规范，接口信息为{file_info}，服务器信息为{file_servers}，url={file_url},cookie={file_cookie},接口描述为{file_tags},正确响应为{file_responses_200},异常响应包括：{file_responses_abnormal}，使用{types_interface}请求写一个接口测试用例{name_output}"
            file_list.append(statement)
        elif types_interface == "delete":
            file_request = items.get("requestBody")
            statement = f"根据openapi{file_openapi}规范，接口信息为{file_info}，服务器信息为{file_servers}，url={file_url},cookie={file_cookie},接口描述为{file_tags},request={file_request},正确响应为{file_responses_200},异常响应包括：{file_responses_abnormal}，使用{types_interface}请求写一个接口测试用例{name_output}"
            file_list.append(statement)
        else:
            print("未知的接口请求类型："+types_interface)
    return file_list


