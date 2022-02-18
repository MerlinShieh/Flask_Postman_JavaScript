import configparser
import logging
from flask import Flask, request
from src.tools.log import Log
import os

# 读取config.ini

# BASE_PATH = os.getcwd().split('\\')[:-1]
#
# BASE_PATH = str('\\'.join(BASE_PATH))
# print(BASE_PATH)


def get_root_path(numb=2):
	return '\\'.join(os.getcwd().split('\\')[:-numb])

logger = Log(directory='../log').logger

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
