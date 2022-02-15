import pyautogui
import traceback
from pynput.keyboard import Key, Listener
from concurrent.futures import ThreadPoolExecutor

executor = ThreadPoolExecutor(5)
# 初始化线程池 5

print('Enter input T activate autoScriptclks')
print('Press Ctrl-C or enter ESC to quit.')


# try:
# 	while True:
# 		# Get and print the mouse coordinates.
# 		x, y = pyautogui.position()
# 		positionStr = 'X:' + str(x).rjust(4) + ' Y:' + str(y).rjust(4)
# 		pix = pyautogui.screenshot().getpixel((x, y))  # 获取鼠标所在屏幕点的RGB颜色
# 		positionStr += ' RGB:(' + str(pix[0]).rjust(3) + ',' + str(pix[1]).rjust(3) + ',' + str(pix[2]).rjust(3) + ')'
# 		print(positionStr, end='')  # end='' 替换了默认的换行
# 		print('\b' * len(positionStr), end='', flush=True)  # 连续退格键并刷新，删除之前打印的坐标，就像直接更新坐标效果
# except KeyboardInterrupt:  # 处理 Ctrl-C 按键
# 	print('\nDone.')
# except Exception as e:
# 	print(traceback.extract_stack(e))


def auto_shooting():
	try:
		print('开始射击')
		for i in range(3):
			x, y = pyautogui.position()
			print(x, y)
			pyautogui.click(x=x, y=y)
			print("射击第{}次".format(i + 1))

	except KeyboardInterrupt:  # 处理 Ctrl-C 按键
		print('\nDone.')
	except Exception as e:
		print(traceback.extract_stack(e))


def test_():
	try:
		print('开始测试')
		pyautogui.press('w')
	except:
		pass


def on_press(key):
	if str(key) == "'t'":
		print(key)
		auto_shooting()
		print('自动射击代码已启动')
	if str(key) == "'y'":
		test_()


# print('退出 on_press ')


def on_release(key):
	if key == Key.esc:
		# Stop listener
		# print(k for k in Key)
		return False


# Collect events until released
with Listener(
		on_press=on_press,
		on_release=on_release) as listener:
	listener.join()
