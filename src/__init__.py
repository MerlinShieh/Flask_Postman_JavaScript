import os
import logging
from flask import Flask, request
from tools.log import Log
from cfg import config


_ROOT_PATH = os.path.dirname(os.path.dirname(__file__))

# print(config.get('path', 'is_update'))
if config.get('path', 'is_update') == 'True':
	"""
	判断是否需要更新配置 不需要的话就从配置读取 需要的话就写入配置
	"""
	log_path = os.path.join(_ROOT_PATH, r'files\log')
	L = Log(directory=log_path)
	
	config.set('path', 'log_path', log_path)
	config.set('path', 'logger', L.logger_name)
	config.write(open(os.path.join(_ROOT_PATH, r'src\cfg\config.ini'), 'w'))
else:
	log_path = config.get('path', 'log_path')
	logger_name = config.get('path', 'logger')
	L = Log(directory=log_path, log_name=logger_name)

log = L.logger

app = Flask(__name__)


class Response:
	@classmethod
	def error(cls, message='error', data=None):
		return {'code': 500, 'message': message, 'data': data}
	
	@classmethod
	def success(cls, message='success', data=None):
		return {'code': 200, 'message': message, 'data': data}


class Request:
	class Headers:
		@classmethod
		def get_headers(cls, key=None):
			# print(request.headers)
			if key:
				return request.headers[key]
			return dict(request.headers)
		
		class Cookie:
			@classmethod
			def get_cookies(cls, key=None):
				if key:
					return request.cookies[key]
				return dict(request.cookies)
		
		class ContentType:
			@classmethod
			def get_content_type(cls):
				return dict(request.headers['Content-Type'])
			
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


if __name__ == '__main__':
	print(os.path.dirname(os.path.dirname(__file__)))
	print(config.sections())
