# -*- coding: utf-8 -*-

try:
	from PyQt5.QtGui import *
	from PyQt5.QtSvg import *
	from PyQt5.QtCore import *
	from PyQt5.QtWidgets import *
except ModuleNotFoundError:
	try:
		from PySide2.QtGui import *
		from PySide2.QtSvg import *
		from PySide2.QtCore import *
		from PySide2.QtWidgets import *
	except ModuleNotFoundError:
		exit("The PyQt5 graphics library is not installed. Install it in the command-line using 'pip3 install PyQt5'.")

import _thread
import math


class TopBar(QGroupBox):
	class Button(QSvgWidget):
		def __init__(self, parent):
			super(TopBar.Button, self).__init__(parent=parent)

	def __init__(self, parent):
		super(TopBar, self).__init__(parent=parent)
		self.setLayout(QHBoxLayout())
		self.setStyleSheet("background-color: transparent;")
		# self.close_button =


class Widget(QPushButton):
	def __init__(self, parent):
		super(Widget, self).__init__(parent=parent)
		self.setMinimumSize(QSize(100, 100))
		self.setStyleSheet("Widget { background-color: rgba(255, 255, 255, 0.4); border-radius: 5px; }")


class Clock(Widget):
	def __init__(self, parent):
		super(Clock, self).__init__(parent=parent)
		self.timer = QTimer(self)
		self.timer.setInterval(1000)
		self.timer.timeout.connect(self.updateTime)
		self.timer.start()
		self.time = QTime().currentTime()
		self.clock = QLabel(self.time.toString("hh:mm"), self)
		self.clock.adjustSize()
		self.clock_seconds = QLabel(self.time.toString("ss"), self)
	
	def updateTime(self):
		self.time = QTime().currentTime()
		self.clock.setText(self.time.toString("hh:mm"))
		self.clock_seconds.setText(self.time.toString("ss"))
	
	def resizeEvent(self, event):
		self.clock.setFont(QFont(bebas_neue, math.floor(min(self.height(), self.width()) / 2.5) - 5))
		self.clock.adjustSize()
		self.clock.move(QPoint(5, 5))
		self.clock_seconds.setFont(QFont(bebas_neue, math.floor(min(self.height(), self.width()) / 2.5) - 15))
		self.clock_seconds.adjustSize()
		self.clock_seconds.move(QPoint(self.clock.width() + 10, 9))
		super(Clock, self).resizeEvent(event)


class Window(QMainWindow):
	def __init__(self):
		super(Window, self).__init__(flags=Qt.FramelessWindowHint | Qt.WindowTransparentForInput)
		self.setMinimumSize(QSize(200, 200))
		self.setAttribute(Qt.WA_TranslucentBackground)
		self.top_bar = TopBar(self)
		self.top_bar.hide()
		self.clock = Clock(self)
		self.show()
		self.leaveEvent = lambda event: super(Window, self).leaveEvent(event)
	
	def resizeEvent(self, event):
		#
		super(Window, self).resizeEvent(event)
	
	def enterEvent(self, event):
		self.top_bar.show()
		self.resize(QSize(self.width(), self.height() + self.top_bar.height()))

		def leaveEvent(event_):
			self.top_bar.hide()
			self.resize(QSize(self.width(), self.height() - self.top_bar.height()))
			super(Window, self).leaveEvent(event_)

		self.leaveEvent = leaveEvent
		super(Window, self).enterEvent(event)


application = QApplication([])
bebas_neue = QFontDatabase.applicationFontFamilies(QFontDatabase.addApplicationFont(QDir.currentPath() + "/fonts/Bebas_Neue/BebasNeue-Regular.ttf"))[0]
window = Window()


print("Close the window by entering 'quit' in this console.")


def check_input():
	while True:
		user_input = input()
		if user_input.lower() == "quit":
			QApplication.quit()
			exit()

	
_thread.start_new_thread(check_input, ())
application.exec_()
