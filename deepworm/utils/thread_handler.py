from threading import Thread


class ThreadHandler(Thread):

	def __init__(
			self,
			group=None, target=None, name=None, verbose=None,  # args required by threading.Thread
			func=None,on_finished=None,
			*args, **kwargs):

		super(ThreadHandler, self).__init__(
			group=group, target=target, name=name)

		# do whatever you want with args list and kwargs dict
		self.args = args
		self.kwargs = kwargs

		if func is not None:
			self.func = func
		else:
			self.func = lambda: None

		if on_finished is not None:
			self.on_finished = on_finished
		else:
			self.on_finished = lambda: None

		# handle the thread process result
		self._result = None
		self._is_finished = False

		# I prefer start threads directly, but that's my choice ;-)
		self.start()

	def run(self):
		try:
			self._result = self.func()
			self.on_finished()
			self._is_finished = True
		except Exception as e:
			print(e)

	@property
	def is_finished(self):
		return self._is_finished

	@property
	def result(self):
		return self._result
