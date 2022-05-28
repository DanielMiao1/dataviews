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

import math


class TopBar(QGroupBox):
	class CloseButton(QSvgWidget):
		"""<?xml version="1.0" encoding="UTF-8" standalone="no"?><svg xmlns="http://www.w3.org/2000/svg" width="2" height="2" fill="currentColor"><line x1="0.18" y1="0.18" x2="1.82" y2="1.82" style="stroke: rgb(0, 0, 0); stroke-width: 0.5"/><line x1="1.82" y1="0.18" x2="0.18" y2="1.82" style="stroke: rgb(0, 0, 0); stroke-width: 0.5"/></svg>"""
		def __init__(self, parent):
			super(TopBar.CloseButton, self).__init__(parent=parent)
			self.updateColor(QColor("black"))
			self.setFixedSize(QSize(15, 15))
			self.move(QPoint(5, 5))
			self.animation = None
			self.setCursor(Qt.CursorShape.PointingHandCursor)
		
		def enterEvent(self, event):
			self.animation = QPropertyAnimation(self, b"color")
			self.animation.setStartValue(QColor("black"))
			self.animation.setEndValue(QColor("#383838"))
			self.animation.setDuration(200)
			self.animation.start()
			super(TopBar.CloseButton, self).enterEvent(event)
		
		def leaveEvent(self, event) -> None:
			self.animation = QPropertyAnimation(self, b"color")
			self.animation.setStartValue(QColor("#383838"))
			self.animation.setEndValue(QColor("black"))
			self.animation.setDuration(200)
			self.animation.start()
			super(TopBar.CloseButton, self).leaveEvent(event)
		
		def mousePressEvent(self, event) -> None:
			QApplication.quit()
			super(TopBar.CloseButton, self).mousePressEvent(event)
		
		def updateColor(self, color: QColor):
			self.renderer().load(bytearray(f'<?xml version="1.0" encoding="UTF-8" standalone="no"?><svg xmlns="http://www.w3.org/2000/svg" width="2" height="2" fill="currentColor"><path style="stroke:{color.name()};stroke-width:.5" d="m.18.18 1.64 1.64m0-1.64L.18 1.82"/></svg>', encoding="utf-8"))
		
		color = pyqtProperty(QColor, fset=updateColor)

	def __init__(self, parent):
		super(TopBar, self).__init__(parent=parent)
		self.setLayout(QHBoxLayout())
		self.setStyleSheet("TopBar { background-color: rgba(255, 255, 255, 0.4); border-radius: 5px; }")
		self.close_button = TopBar.CloseButton(self)


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
		super(Window, self).__init__(flags=Qt.FramelessWindowHint)
		self.setMinimumSize(QSize(200, 200))
		self.setAttribute(Qt.WA_TranslucentBackground)
		self.main_wrapper = QWidget(self)
		self.top_bar = TopBar(self)
		self.top_bar.hide()
		self.clock = Clock(self.main_wrapper)
		self.show()
		self.leaveEvent = lambda event: super(Window, self).leaveEvent(event)
	
	def resizeEvent(self, event):
		self.main_wrapper.resize(event.size())
		self.top_bar.resize(QSize(event.size().width(), 25))
		super(Window, self).resizeEvent(event)
	
	def enterEvent(self, event):
		self.top_bar.show()
		self.resize(QSize(self.width(), self.height() + self.top_bar.height() + 10))
		self.main_wrapper.move(QPoint(0, self.top_bar.height() + 10))

		def leaveEvent(event_):
			self.top_bar.hide()
			self.resize(QSize(self.width(), self.height() - self.top_bar.height()))
			self.main_wrapper.move(QPoint(0, 0))
			super(Window, self).leaveEvent(event_)

		self.leaveEvent = leaveEvent
		super(Window, self).enterEvent(event)


application = QApplication([])
bebas_neue = QFontDatabase.applicationFontFamilies(QFontDatabase.addApplicationFont(QDir.currentPath() + "/fonts/Bebas_Neue/BebasNeue-Regular.ttf"))[0]
window = Window()
application.exec_()
