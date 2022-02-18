
config = configparser.ConfigParser()
config.read('config.ini', encoding='UTF-8')
if __name__ == '__main__':
	# app.run(host='0.0.0.0', port=8801, debug=True, use_reloader=True)
	from src._test import add_data
	print(__name__, add_data())