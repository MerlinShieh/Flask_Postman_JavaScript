import json, time

class RespResult:
	Error = {'code': 500, 'message': 'error', 'data': ''}
	Success = {'code': 200, 'message': 'success', 'data': '{}'}
# print(RespResult.Error)
# print(type(RespResult.Error))
# print(json.dumps(RespResult.Error))
# print(type(json.dumps(RespResult.Error)))

print(time.asctime())