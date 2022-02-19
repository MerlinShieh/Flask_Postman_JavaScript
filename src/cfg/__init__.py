import configparser
import os
# 拿到根目录文件路径
config_path = os.path.dirname(__file__)
config = configparser.ConfigParser()
config.read(os.path.join(config_path, r'config.ini'), encoding='UTF-8')

if __name__ == '__main__':
	print(config_path)
	print(config.sections())