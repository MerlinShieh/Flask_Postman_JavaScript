import os
import json_tools
import json
import traceback

from concurrent.futures import ThreadPoolExecutor
from src import app, logger as log, Response, Request, request, config
from src.tools import tools

executor = ThreadPoolExecutor(5)
# 初始化线程池 5


@app.route('/translate_img', methods=['POST'])
async def translate_img():
	if request.method == 'POST':
		resp = str(request.form['img'])
		executor.submit(tools.show_img, resp)
		return Response.success()
	else:
		return Response.error()


@app.route('/log', methods=['POST'])
def _log():
	if request.method == 'POST':
		if Request.Headers.ContentType.is_form_data():
			level = str(request.form['level'])
			message = str(request.form['message'])
		elif Request.Headers.ContentType.is_json():
			level = str(dict(request.get_json())['level'])
			message = str(dict(request.get_json())['message'])
		elif Request.Headers.ContentType.is_form_urlencoded():
			level = str(dict(request.values)['level'])
			message = str(dict(request.values)['message'])
		else:
			level = 'error'
			message = '不支持的格式'
		executor.submit(eval('log.level'), message)
		log.info('远程日志为: {}, {}'.format(level, message))

		return Response.success(data={"logger_name": log.name})
	else:
		return Response.error()


@app.route('/check_environment', methods=['POST'])
def check_environment():
	if request.method == 'POST' and Request.Headers.ContentType.is_form_data():
		env = str(request.form['environment'])
		glo = str(request.form['globals'])
		req = str(request.form['request'])
		diff = tools.check_environment(env, glo, req)
		return Response.success(data={"req_name": req, "diff": diff})
	else:
		return Response.error()


@app.route('/test', methods=['POST', 'GET'])
def test():
	__methods = request.method
	if __methods == 'POST' or 'GET':
		log.info('__method:' + __methods)
		try:
			data = (request.get_json()
					if Request.Headers.ContentType.is_json() else dict(request.form)
			if Request.Headers.ContentType.is_form_data() else dict(request.values))
			log.info('ContentType' + str(Request.Headers.ContentType))
			return Response.success(data=data)
		except:
			log.error(traceback.extract_stack())
			return Response.error(data=traceback.extract_stack())
	else:
		return Response.error()


@app.route('/uploadfiles', methods=['POST', 'PUT'])
def uploadfiles():
	__methods = request.method
	log.info('检查到文件上传，方式为：' + __methods)
	if __methods == 'POST' or 'PUT':
		# 获取文件类型的参数
		try:
			file = request.files['file']
			if file and tools.allowed_file(file.filename):
				file.save(os.path.join(config.flask_config['__UPLOAD_FOLDER'], file.filename))
				log.debug('文件上传成功！路径为：' + os.path.join(config.flask_config['__UPLOAD_FOLDER'], file.filename))
			return Response.success()
		except:
			return Response.error(data=traceback.extract_stack())


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
