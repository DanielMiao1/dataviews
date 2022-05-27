# -*- coding: utf-8 -*-

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class Window(QMainWindow):
	def __init__(self):
		super(Window, self).__init__()
		self.text = QLabel("hi", self)
		self.show()


application, window = QApplication([]), Window()
application.exec_()
