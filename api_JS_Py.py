import base64
import json_tools
import json
import time
import traceback
from flask import Flask, request
from PIL import Image
from concurrent.futures import ThreadPoolExecutor
from log import Log

logger = Log().logger
# 初始化logger
executor = ThreadPoolExecutor(5)
# 初始化线程池 5
app = Flask(__name__)


# 初始化flask


class RespResult:
	"""
	重构 response
	"""

	@classmethod
	def error(cls, message='error', data=None):
		return {'code': 500, 'message': message, 'data': data}

	@classmethod
	def success(cls, message='success', data=None):
		return {'code': 200, 'message': message, 'data': data}


class RespHeaders:
	@classmethod
	def getheaders(cls, key=None):
		print(request.headers)
		if key:
			return request.headers[key]
		return dict(request.headers)

	class ContentType:
		@classmethod
		def is_json(cls):
			return 'application/json' in request.headers['Content-Type'] \
				if 'Content-Type' in dict(request.headers).keys() else False

		@classmethod
		def is_form_data(cls):
			return 'multipart/form-data' in request.headers['Content-Type'] \
				if 'Content-Type' in dict(request.headers).keys() else False

		@classmethod
		def is_form_urlencoded(cls):
			return 'application/x-www-form-urlencoded' in request.headers['Content-Type'] \
				if 'Content-Type' in dict(request.headers).keys() else False


def show_img(data):
	image_data = base64.b64decode(data.split(',')[1])
	with open('PayQRCode.jpeg', 'wb') as f:
		f.write(image_data)
	img = Image.open('PayQRCode.jpeg')
	img.show()
	return True


@app.route('/translate_img', methods=['POST'])
async def translate_img():
	if request.method == 'POST':
		resp = str(request.form['img'])
		executor.submit(show_img, resp)
		return RespResult.success()
	else:
		return RespResult.error()


def _log(level: str, msg: any):
	lel = level.lower()
	logger.info(msg) if \
		lel == 'info' or 'log' else logger.warning(msg) if \
		lel == 'warn' else logger.error(msg) if \
		lel == 'error' else logger.debug(msg)
	return True


@app.route('/log', methods=['POST'])
async def log():
	if request.method == 'POST':
		level = str(request.form['level'])
		message = str(request.form['message'])
		executor.submit(_log, level, message)
		return RespResult.success(data={"logger_name": logger.name})
	else:
		return RespResult.error()


def _check_environment(env, glo, req):
	with open('~glo_data.cache', 'a+', encoding='utf-8') as f:
		try:
			f.seek(0)
			# 文件指针移至开头，进行读取就能获取所有数据
			last_glo = ((f.readlines())[-1])[:-1]
		except IndexError:
			last_glo = '{}'
		f.seek(2)
		# 文件指针移至末尾，这样写入数据就是追加写入
		f.write(glo + '\n')
	with open('~env_data.cache', 'a+', encoding='utf-8') as f:
		try:
			f.seek(0)
			last_env = ((f.readlines())[-1])[:-1]
		except IndexError:
			last_env = '{}'
		f.seek(2)
		f.write(env + '\n')
	msg = {"env": json_tools.diff(last_env, env), "glo": json_tools.diff(last_glo, glo)}
	_log('log', req + "：\n环境变量变化为：" + str(json.dumps(msg).encode('utf-8').decode("unicode_escape")) + "\n")
	return msg


@app.route('/check_environment', methods=['POST'])
def check_environment():
	if request.method == 'POST':
		env = str(request.form['environment'])
		glo = str(request.form['globals'])
		req = str(request.form['request'])
		diff = _check_environment(env, glo, req)
		# return {'code': 200, 'message': 'success', "data": {"req_name": req, "diff": diff}}
		return RespResult.success(data={"req_name": req, "diff": diff})
	else:
		return RespResult.error()


@app.route('/test', methods=['POST', 'GET'])
def test():
	__methods = request.method
	if True if __methods == 'POST' or 'GET' else False:
		# noinspection PyBroadException
		try:
			# 判断请求的格式，json form form-urlencoded

			# print(RespHeaders.ContentType.is_json())
			# print(RespHeaders.ContentType.is_form_data())
			# print(RespHeaders.ContentType.is_form_urlencoded())

			data = (request.get_json() if RespHeaders.ContentType.is_json() else dict(request.form) if RespHeaders.ContentType.is_form_data() else dict(request.values))
			print(data)
			return RespResult.success(data=data)
		except:
			return RespResult.error(data=traceback.extract_stack())
	else:
		return RespResult.error()


if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8801, debug=True, use_reloader=True)
