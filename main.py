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
import typing


class Label(QLabel):
	@typing.overload
	def __init__(self, parent, selectable=True):
		super(Label, self).__init__(parent)
		self.selectable = selectable
		self.initialize()

	def __init__(self, text="", parent: typing.Any = None, selectable=True):
		super(Label, self).__init__(text, parent)
		self.selectable = selectable
		self.initialize()
	
	def initialize(self):
		if self.selectable:
			self.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)

		self.setContextMenuPolicy(Qt.ContextMenuPolicy.NoContextMenu)


class TopBar(QGroupBox):
	class CloseButton(QSvgWidget):
		"""
		<?xml version="1.0" encoding="UTF-8" standalone="no"?>
		<svg xmlns="http://www.w3.org/2000/svg" width="2" height="2" fill="currentColor">
			<line x1="0.18" y1="0.18" x2="1.82" y2="1.82" style="stroke: rgb(0, 0, 0); stroke-width: 0.5"/>
			<line x1="1.82" y1="0.18" x2="0.18" y2="1.82" style="stroke: rgb(0, 0, 0); stroke-width: 0.5"/>
		</svg>"""
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
	
	class SettingsButton(QSvgWidget):
		"""
		<?xml version="1.0" encoding="UTF-8" standalone="no"?>
		<svg xmlns="http://www.w3.org/2000/svg" width="8" height="8" fill="currentColor">
		  <circle cx="4" cy="4" r="1.45" stroke="black" fill="none" stroke-width="0.85px"/>
		  <rect x="3.4" y="1.375" width="1.2" height="1" rx="0.2" fill="black"/>
		  <rect x="3.4" y="5.625" width="1.2" height="1" rx="0.2" fill="black"/>
		  <rect x="3.4" y="1.375" width="1.2" height="1" rx="0.2" fill="black" transform="rotate(90)" transform-origin="center"/>
		  <rect x="3.4" y="5.625" width="1.2" height="1" rx="0.2" fill="black" transform="rotate(90)" transform-origin="center"/>
		  <rect x="3.4" y="1.375" width="1.2" height="1" rx="0.2" fill="black" transform="rotate(45)" transform-origin="center"/>
		  <rect x="3.4" y="5.625" width="1.2" height="1" rx="0.2" fill="black" transform="rotate(45)" transform-origin="center"/>
		  <rect x="3.4" y="1.375" width="1.2" height="1" rx="0.2" fill="black" transform="rotate(135)" transform-origin="center"/>
		  <rect x="3.4" y="5.625" width="1.2" height="1" rx="0.2" fill="black" transform="rotate(135)" transform-origin="center"/>
		</svg>
		"""
		def __init__(self, parent):
			super(TopBar.SettingsButton, self).__init__(parent=parent)
			self.updateColor(QColor("black"))
			self.setFixedSize(QSize(15, 15))
			self.move(QPoint(25, 5))
			self.animation = None
			self.setCursor(Qt.CursorShape.PointingHandCursor)
		
		def enterEvent(self, event):
			self.animation = QPropertyAnimation(self, b"color")
			self.animation.setStartValue(QColor("black"))
			self.animation.setEndValue(QColor("#383838"))
			self.animation.setDuration(200)
			self.animation.start()
			super(TopBar.SettingsButton, self).enterEvent(event)
		
		def leaveEvent(self, event) -> None:
			self.animation = QPropertyAnimation(self, b"color")
			self.animation.setStartValue(QColor("#383838"))
			self.animation.setEndValue(QColor("black"))
			self.animation.setDuration(200)
			self.animation.start()
			super(TopBar.SettingsButton, self).leaveEvent(event)
		
		def mousePressEvent(self, event) -> None:
			QApplication.quit()
			super(TopBar.SettingsButton, self).mousePressEvent(event)
		
		def updateColor(self, color: QColor):
			self.renderer().load(bytearray(f'<?xml version="1.0" encoding="utf-8" standalone="no"?><svg xmlns="http://www.w3.org/2000/svg" width="122.88" height="122.878"><path fill="{color.name()}" fill-rule="evenodd" d="m101.589 14.7 8.818 8.819c2.321 2.321 2.321 6.118 0 8.439l-7.101 7.101a47.216 47.216 0 0 1 4.405 11.752h9.199c3.283 0 5.969 2.686 5.969 5.968V69.25c0 3.283-2.686 5.969-5.969 5.969h-10.039a47.194 47.194 0 0 1-5.204 11.418l6.512 6.51c2.321 2.323 2.321 6.12 0 8.44l-8.818 8.819c-2.321 2.32-6.119 2.32-8.439 0l-7.102-7.102a47.118 47.118 0 0 1-11.753 4.406v9.199c0 3.282-2.685 5.968-5.968 5.968h-12.47c-3.283 0-5.969-2.686-5.969-5.968V106.87a47.21 47.21 0 0 1-11.417-5.205l-6.511 6.512c-2.323 2.321-6.12 2.321-8.441 0l-8.818-8.818c-2.321-2.321-2.321-6.118 0-8.439l7.102-7.102a47.077 47.077 0 0 1-4.405-11.751H5.968C2.686 72.067 0 69.382 0 66.099V53.628c0-3.283 2.686-5.968 5.968-5.968h10.039a47.27 47.27 0 0 1 5.204-11.418l-6.511-6.51c-2.321-2.322-2.321-6.12 0-8.44l8.819-8.819c2.321-2.321 6.118-2.321 8.439 0l7.101 7.101a47.133 47.133 0 0 1 11.753-4.406V5.969C50.812 2.686 53.498 0 56.78 0h12.471c3.282 0 5.968 2.686 5.968 5.969v10.036a47.239 47.239 0 0 1 11.422 5.204l6.507-6.509c2.323-2.321 6.12-2.321 8.441 0zM61.44 36.92c13.54 0 24.519 10.98 24.519 24.519 0 13.538-10.979 24.519-24.519 24.519-13.539 0-24.519-10.98-24.519-24.519 0-13.539 10.98-24.519 24.519-24.519z"/></svg>', encoding="utf-8"))
		
		color = pyqtProperty(QColor, fset=updateColor)

	def __init__(self, parent):
		super(TopBar, self).__init__(parent=parent)
		self.setLayout(QHBoxLayout())
		self.setStyleSheet("TopBar { background-color: rgba(255, 255, 255, 0.4); border-radius: 5px; }")
		self.close_button = TopBar.CloseButton(self)
		self.close_button = TopBar.SettingsButton(self)


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
		self.day = QDate().currentDate()
		self.clock = Label(self.time.toString("hh:mm"), self)
		self.clock_seconds = Label(self.time.toString("ss"), self)
		self.date = Label(self.day.toString("dddd, MMMM d yyyy"), self)
	
	def updateTime(self):
		self.time = QTime().currentTime()
		self.day = QDate().currentDate()
		self.clock.setText(self.time.toString("hh:mm"))
		self.clock_seconds.setText(self.time.toString("ss"))
		self.date.setText(self.day.toString("dddd, MMMM d yyyy"))

	def resizeEvent(self, event):
		self.clock.setFont(QFont(bebas_neue, (min(self.height(), self.width()) // 2) - 5))
		self.clock.adjustSize()
		self.clock.move(QPoint(5, 5))
		self.clock_seconds.setFont(QFont(bebas_neue, math.floor(min(self.height(), self.width()) / 2.5) - 15))
		self.clock_seconds.adjustSize()
		self.clock_seconds.move(QPoint(self.clock.width() + 10, 9))
		self.date.setFont(QFont(barlow_condensed, (min(self.height(), self.width()) // 4) - 5))
		self.date.move(QPoint(7, 5 + self.clock.height()))
		self.date.adjustSize()
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
		self.clock.resize(QSize(event.size().width(), self.clock.height()))
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
barlow_condensed = QFontDatabase.applicationFontFamilies(QFontDatabase.addApplicationFont(QDir.currentPath() + "/fonts/Barlow_Condensed/BarlowCondensed-SemiBold.ttf"))[0]
window = Window()
application.exec_()
