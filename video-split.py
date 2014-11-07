#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import signal
import os
import subprocess
from PyQt4.QtCore import *
from PyQt4.QtGui import *


class FormWidget(QWidget):

	def __init__(self, parent):
		super(FormWidget, self).__init__(parent)
		self.__layout()

	def __layout(self):
		self.vbox = QVBoxLayout()

		self.toolbar = QToolBar()
		self.toolbar.addAction(QIcon.fromTheme('list-add'), 'Add Videos')
		self.toolbar.addAction(QIcon.fromTheme('edit-clear'), 'Clear Video List')
		self.help = QLabel('Welcome to Video Splitter. To get started, add videos to the list using the button above.')
		self.fileListView = QListView()
		self.fpsLabel = QLabel('Frames Per Second (play around to find a balance between capturing best poses and number of frames exported).')
		self.fps = QSpinBox()
		self.fps.setMinimum(1);
		self.fps.setMaximum(200);
		self.fps.setValue(5);
		self.outdirLabel = QLabel('Output folder (where to create the frame folders for each video)')
		self.outdirLayout = QHBoxLayout()
		self.outdirInput = QLineEdit()
		self.outdirInput.setText(os.environ['HOME'])
		self.outdirButton = QPushButton('Browse')
		self.outdirLayout.addWidget(self.outdirInput)
		self.outdirLayout.addWidget(self.outdirButton)
		self.button = QPushButton('Split videos into frames')
		self.logTextLabel = QLabel('Debug information')

		pal = QPalette()
		bgc = QColor(0, 0, 0)
		pal.setColor(QPalette.Base, bgc)
		textc = QColor(255, 255, 255)
		pal.setColor(QPalette.Text, textc)
		self.logText = QTextEdit()
		self.logText.setReadOnly(True)
		self.logText.setPalette(pal)

		self.vbox.addWidget(self.toolbar)
		self.vbox.addWidget(self.help)
		self.vbox.addWidget(self.fileListView)
		self.vbox.addWidget(self.fpsLabel)
		self.vbox.addWidget(self.fps)
		self.vbox.addWidget(self.outdirLabel)
		self.vbox.addLayout(self.outdirLayout)
		self.vbox.addWidget(self.button)
		self.vbox.addWidget(self.logTextLabel)
		self.vbox.addWidget(self.logText)
		self.setLayout(self.vbox)


class VideoSplitter(QMainWindow):

	def __init__(self):
		super(VideoSplitter, self).__init__()

		self.initUI()

	def initUI(self):

		self.layout = FormWidget(self)

		self.layout.button.clicked.connect(self.doSplitting)
		self.layout.toolbar.actionTriggered.connect(self.actionClicked)

		self.layout.outdirButton.clicked.connect(self.showOutputDialog)

		self.setCentralWidget(self.layout)
		self.statusBar()

		self.dialog = QMessageBox()

		self.outdir = os.environ['HOME'];

		self.setGeometry(450, 100, 800, 700)
		self.setWindowTitle('Video Splitter')
		self.show()

	def actionClicked(self, action):
		a = action.text()
		if a == 'Add Videos':
			self.showFileDialog()
		elif a == 'Clear Video List':
			self.clearList()

	def clearList(self):
		self.model.clear()

	def showOutputDialog(self):
		self.outdir = str(QFileDialog.getExistingDirectory(self, 'Choose output folder for video frames', os.environ['HOME']))
		self.layout.outdirInput.setText(self.outdir)

	def showFileDialog(self):

		fnames = QFileDialog.getOpenFileNames(self, 'Open file', os.environ['HOME'])
		self.model = QStandardItemModel()

		self.fileCount = 0
		for fname in fnames:
			item = QStandardItem()
			item.setText(fname)
			item.setCheckable(True)
			item.setCheckState(2)
			self.model.appendRow(item)
			self.fileCount += 1

		self.layout.fileListView.setModel(self.model)

	def doSplitting(self):
		self.completionCount = 0

		for i in range(0, self.fileCount):
			f = self.model.item(i)

			if f.checkState() != 2:
				continue;

			fin = str(f.text())
			print os.path.basename(fin)
			outdir = os.path.join(self.outdir, os.path.basename(fin) + '-frames')
			fname = os.path.join(outdir, 'image%03d.jpg')

			if not os.path.isdir(outdir):
				try:
					os.mkdir(outdir)
				except OSError:
					if not os.path.isdir(outdir):
						self.showPermissionDialog()
						raise

			# QProcess object for external ffmpeg/avconv command
			self.process = QProcess(self)
			# Just to prevent accidentally running multiple times
			# Disable the button when process starts, and enable it when it finishes
			self.process.started.connect(self.startedSplit)
			self.process.finished.connect(self.finishedSplit)
			# QProcess emits signals when there is output to be read
			self.process.readyReadStandardOutput.connect(self.writeLog)
			self.process.readyReadStandardError.connect(self.writeLog)

			self.process.start('avconv', ['-i', fin, '-r', self.layout.fps.text(), fname])

	def startedSplit(self):
		self.layout.button.setEnabled(False)

	def finishedSplit(self):
		self.completionCount += 1
		if (self.completionCount >= self.model.rowCount()):
			self.dialog.setIcon(1)
			self.dialog.setWindowTitle('Splitting finished')
			self.dialog.setText('All videos have been split into frames. The frames have been exported into the output folder you chose, with a sub-folder for each video. If you can\'t see some/any frames, or have any other problems, check the log output below, and feel free to raise an issue at https://github.com/itsravenous/videosplitter/issues')
			self.dialog.open()
			self.layout.button.setEnabled(True)

	def showPermissionDialog(self):
		self.dialog.setIcon(2)
		self.dialog.setWindowTitle('Can\'t write frames')
		self.dialog.setText('The folder in which one or more of your videos resides is not writeable. Please check you own the folder, and it is not read-only.')
		self.dialog.open()

	def writeLog(self):
		self.layout.logText.append(str(self.process.readAllStandardOutput()))
		self.layout.logText.append(str(self.process.readAllStandardError()))

	def confirmQuit(self):
		self.quit()

	def quit(self):
		sys.exit()


def main():

	app = QApplication(sys.argv)
	ex = VideoSplitter()
	sys.exit(app.exec_())


if __name__ == '__main__':
	main()
