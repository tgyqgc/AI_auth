
    Feature: ['交易确认记录', 'SKII']
    servers:http://10.244.23.117
    接口描述：Web端-交易管理-Admin交易确认-确认交易
    Scenario:
        # 接口契约描述
        # -------------------------------------------------------------
        parameters:
        {'type': 'object', 'properties': {'confirmedDate': {'type': 'integer', 'format': 'int64'}, 'adminName': {'type': 'string'}, 'counterIds': {'type': 'array', 'items': {'type': 'string'}}}}
        # -------------------------------------------------------------
        responses:
        {'type': 'object', 'properties': {'code': {'type': 'integer', 'format': 'int32'}, 'msg': {'type': 'string'}, 'data': {'type': 'boolean'}, 'errData': {'type': 'string'}}}
        abnormal responses:
        {'400': {'type': 'object', 'properties': {'errorCode': {'type': 'integer', 'format': 'int32'}, 'errorMessage': {'type': 'string'}, 'requestId': {'type': 'string'}}}, '408': {'type': 'object', 'properties': {'errorCode': {'type': 'integer', 'format': 'int32'}, 'errorMessage': {'type': 'string'}, 'requestId': {'type': 'string'}}}}
        # -------------------------------------------------------------
        Given path '/api/v1/transaction/record/admin/confirm'
        When method put
        Then status 200
        请求体中的None
          Background固定为
    * url karate.get('baseUrl')
    * header Authorization = karate.get('websiteToken')
    * header X-BUSINESS-BRAND = 'skii'
    * header Content-Type = 'application/json'
    * header Auth-Type = 'ssofed'
    * param subscription-key = karate.get('subscriptionKey')
    * def isSortingBy = read('classpath:pg-functions/sortingFunctions.js')   正确响应校验示例为    
        And match response.code == 20000
        And match response.msg == "success"
        And match response.data != null
        根据提供的条件尽可能多的生成karate测试用例
        