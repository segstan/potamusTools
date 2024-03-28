# -*- coding: utf-8 -*-
##################################################################################################################
############## 								Environment Library 	  							##############
##################################################################################################################

import os

from PySide2 import QtGui, QtCore, QtWidgets , QtUiTools

try:
	import nuke
	in_nuke = True
except:
	in_nuke= False
if in_nuke==False:
	try:
		##To attach the window to maya, sip is going to translate for pyqt some function
		import maya.OpenMayaUI as omu
		from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
		in_maya = True
	except:
		in_maya = False

	try:
		import hou
		in_hou= True
	except:
		in_hou= False

##import sip
try:
	from shiboken import wrapInstance
except:
	from shiboken2 import wrapInstance

import sg_uiProgressBar
from sg_uiProgressBar import Ui_windowSGProgressBarLibrary
reload(sg_uiProgressBar)


	## My window and its functions
class sgProgressBarLibrary(QtWidgets.QMainWindow, Ui_windowSGProgressBarLibrary):
	def __init__(self, parent = None):
		QtWidgets.QMainWindow.__init__(self, parent, QtCore.Qt.WindowStaysOnTopHint)
		self.setupUi(self)
		self.show()

	def setValue(self, val,text): # Sets value
		self.progressBar_sgLoadEnvWin.setProperty("value", val)
		self.label_sgProgressBarWin.setText(text)

def main():
	app = QtWidgets.QApplication(sys.argv)      # A new instance of QApplication
	form = sgProgressBarLibrary('pbar')                        # We set the form to be our MainWindow (design)
	app.exec_()                                 # and execute the app

if __name__ == '__main__':                      # if we're running file directly and not importing it
	main()