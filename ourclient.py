import requests
from PyQt5.QtCore import QTimer

from client import QueryImage, RunningScreen

HOST = '192.168.2.106'
PORT = '8080'
BASE_URL = 'http://' + HOST + ':'+ PORT + '/'


def start_stream(self):
	"""Start to receive the stream

	With this function called, the QTimer start timing, while time up, call reflash_frame() function,
	the frame will be reflashed.

	Args:
		None
	"""
	# creat an object queryImage with the HOST
	self.queryImage = QueryImage(HOST)
	self.timer = QTimer(timeout=self.reflash_frame)  # Qt timer, time up, run reflash_frame()
	self.timer.start(RunningScreen.TIMEOUT)  # start timer
	# init the position
	run_action('fwready')
	run_action('bwready')
	run_action('camready')


def stop_stream(self):
	self.timer.stop()  # stop timer, so the receive of stream also stop


def run_action(cmd):
	"""Ask server to do sth, use in running mode

	Post requests to server, server will do what client want to do according to the url.
	This function for running mode

	Args:
		# ============== Back wheels =============
		'bwready' | 'forward' | 'backward' | 'stop'

		# ============== Front wheels =============
		'fwready' | 'fwleft' | 'fwright' |  'fwstraight'

		# ================ Camera =================
		'camready' | 'camleft' | 'camright' | 'camup' | 'camdown'
	"""
	# set the url include action information
	url = BASE_URL + 'run/?action=' + cmd
	print('url: %s'% url)
	# post request with url
	__request__(url)


def __request__(url, times=10):
	for x in range(times):
		try:
			requests.get(url)
			return 0
		except :
			print("Connection error, try again")
	print("Abort")
	return -1

running1 = RunningScreen()
