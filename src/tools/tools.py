import base64
import json
import json_tools
from PIL import Image
from src import logger as log
from src.com import config


def show_img(data):
	image_data = base64.b64decode(data.split(',')[1])
	with open('PayQRCode.jpeg', 'wb') as f:
		f.write(image_data)
	img = Image.open('PayQRCode.jpeg')
	img.show()
	return True


def check_environment(env, glo, req):
	with open('../../files/~glo_data.cache', 'a+', encoding='utf-8') as f:
		try:
			f.seek(0)
			# 文件指针移至开头，进行读取就能获取所有数据
			last_glo = ((f.readlines())[-1])[:-1]
		except IndexError:
			last_glo = '{}'
		f.seek(2)
		# 文件指针移至末尾，这样写入数据就是追加写入
		f.write(glo + '\n')
	with open('../../files/~env_data.cache', 'a+', encoding='utf-8') as f:
		try:
			f.seek(0)
			last_env = ((f.readlines())[-1])[:-1]
		except IndexError:
			last_env = '{}'
		f.seek(2)
		f.write(env + '\n')
	msg = {"env": json_tools.diff(last_env, env), "glo": json_tools.diff(last_glo, glo)}
	log.info(req + "：\n环境变量变化为：" + str(json.dumps(msg).encode('utf-8').decode("unicode_escape")) + "\n")
	return msg


def allowed_file(filename):
	log.debug('检查文件上传的格式，文件为：{}，检查格式为：{}'.format(filename, config.flask_config['__ALLOWED_EXTENSIONS']))
	return '.' in filename and filename.rsplit('.', 1)[1] in config.flask_config['__ALLOWED_EXTENSIONS']
