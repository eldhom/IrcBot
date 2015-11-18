import time

class Timer:
	def __init__(self, timer=0):
		self._start = 0
		self._timer	= timer
		
	def start(self, timer):
		self._start = time.time()
		self._timer	= timer
	
	def reset(self):
		self._start = time.time()
	
	def isDone(self):
		if time.time() - self._start > self._timer:
			return True
		return False