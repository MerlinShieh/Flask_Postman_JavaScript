import base64
import os
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

# 配置文件上传
__UPLOAD_FOLDER = r'./files/uploads'
__ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
__MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB


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


def _log(msg: any, level='debug', ):
	lel = level.lower()
	logger.info(msg) if \
		lel == 'info' or 'log' else logger.warning(msg) if \
		lel == 'warn' else logger.error(msg) if \
		lel == 'error' else logger.debug(msg)
	return True


@app.route('/log', methods=['POST'])
async def log():
	"""
	支持三个Content Type
	:return:
	"""
	if request.method == 'POST':
		if RespHeaders.ContentType.is_form_data():
			level = str(request.form['level'])
			message = str(request.form['message'])
		elif RespHeaders.ContentType.is_json():
			level = str(dict(request.get_json())['level'])
			message = str(dict(request.get_json())['message'])
		elif RespHeaders.ContentType.is_form_urlencoded():
			level = str(dict(request.values)['level'])
			message = str(dict(request.values)['message'])
		else:
			level = 'error'
			message = '不支持的格式'
		_log('远程日志为：{}, {}'.format(level, message))
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
	_log(req + "：\n环境变量变化为：" + str(json.dumps(msg).encode('utf-8').decode("unicode_escape")) + "\n")
	return msg


@app.route('/check_environment', methods=['POST'])
def check_environment():
	"""
	只支持 form格式
	:return:
	"""
	if request.method == 'POST' and RespHeaders.ContentType.is_form_data():
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
	"""
	支持json form form-urlencoded 三种
	:return:
	"""
	__methods = request.method
	if True if __methods == 'POST' or 'GET' else False:
		# noinspection PyBroadException
		try:
			# 判断请求的格式，json form form-urlencoded
			# print(RespHeaders.ContentType.is_json())
			# print(RespHeaders.ContentType.is_form_data())
			# print(RespHeaders.ContentType.is_form_urlencoded())

			data = (request.get_json() if
					RespHeaders.ContentType.is_json() else dict(request.form) if
			RespHeaders.ContentType.is_form_data() else dict(request.values))
			_log('is_json' + str(RespHeaders.ContentType.is_json()))
			_log('is_form_data' + str(RespHeaders.ContentType.is_form_data()))
			_log('is_form_urlendecoded' + str(RespHeaders.ContentType.is_form_urlencoded()))
			return RespResult.success(data=data)
		except:
			return RespResult.error(data=traceback.extract_stack())
	else:
		return RespResult.error()


def allowed_file(filename):
	_log('检查文件上传的格式，文件为：{}，检查格式为：{}'.format(filename, __ALLOWED_EXTENSIONS))
	return '.' in filename and filename.rsplit('.', 1)[1] in __ALLOWED_EXTENSIONS


@app.route('/uploadfiles', methods=['POST', 'PUT'])
def uploadfiles():
	"""
	设置上传限制
	:return:
	"""
	__methods = request.method
	_log('检查到文件上传，方式为：'+__methods)
	if True if __methods == 'POST' or 'PUT' else False:
		# 获取文件类型的参数
		try:
			file = request.files['file']
			if file and allowed_file(file.filename):
				# filename = secure_filename(file.filename)
				file.save(os.path.join(__UPLOAD_FOLDER, file.filename))
				_log('文件上传成功！路径为：'+os.path.join(__UPLOAD_FOLDER, file.filename))
			# 获取上传文件的二进制流
			# print(f"request.files.get('file_name').read(): {request.files.get('file_name').read()}")
			return RespResult.success()
		except:
			return RespResult.error(data=traceback.extract_stack())


"""
文件展示没有弄好

@app.route('/show/<filename>', methods=['POST', 'GET'])
def show_file(filename):
	if True if request.method == 'POST' or 'GET' else False:
		filename = request.values.get(filename)
		with open(__UPLOAD_FOLDER+r'/'+filename, 'wb') as f:
			file_base64 = base64.b64encode(f.read())
			print(file_base64)
			return RespResult.success(data=file_base64)
"""

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8801, debug=True, use_reloader=True)
