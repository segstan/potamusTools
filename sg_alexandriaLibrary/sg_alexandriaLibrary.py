
########################################################################################################################
################# 									Alexandria library									################
#################									  Version 2.0.1										################
########################################################################################################################
import sys
import os

pythonVersion = (sys.version_info[0])
if pythonVersion == 3:
	import imp

########################################################################################################################
########################################################################################################################

print("\n")
print(" =================================================================== ")
print(" ------------------------- Alexandria Library ------------------------- ")
print(" =================================================================== ")
print("\n")

################################################ Software Detection #####################################################
fileDir = os.path.dirname(os.path.abspath(__file__))
pathDetectSoftware = os.path.abspath(os.path.join(fileDir, '../sg_findSoftware/'))
sys.path.append( pathDetectSoftware )

import sg_findSoftware
if pythonVersion == 2:
	reload(sg_findSoftware)
elif  pythonVersion == 3:
	imp.reload(sg_findSoftware)

def detectSoftware():
	# Get Software
	findSoftware = sg_findSoftware.sgFindSoftware()
	softwareUsed = findSoftware.softwareUsed()
	return softwareUsed

findSoftware = sg_findSoftware.sgFindSoftware()
softwareUsed = detectSoftware()
in_nuke = findSoftware.isNuke()
in_katana = findSoftware.isKatana()
in_mari = findSoftware.isMari()
in_maya = findSoftware.isMaya()
in_hou = findSoftware.isHoudini()
in_blen = findSoftware.isBlender()
in_unreal = findSoftware.isUnreal()

####################################################### Log ############################################################
import logging
import logging.config

# logging.basicConfig( level=logging.INFO, format='%(asctime)s %(name)s %(levelname)s:%(message)s')

########################################################################################################################
######################################### Load all the needed modules per software #####################################
########################################################################################################################

if in_nuke:
	import nuke
	import sg_nukeLibraryCommands
	if pythonVersion == 2:
		reload(sg_nukeLibraryCommands)
	elif pythonVersion == 3:
		imp.reload(sg_nukeLibraryCommands)
	import nukescripts
	print(" ---- In Nuke ---- ")
elif in_mari:
	import mari
	import sg_mariLibraryCommands
	reload(sg_mariLibraryCommands)
	print(" ---- In Mari ---- ")
elif in_katana:
	import Katana
	from Katana import NodegraphAPI
	import sg_katanaLibraryCommands
	import sg_katanaRenderman
	from Katana import UI4

	if pythonVersion == 2:
		reload(sg_katanaLibraryCommands)
		reload(sg_katanaRenderman)
	elif pythonVersion == 3:
		imp.reload(sg_katanaLibraryCommands)
		imp.reload(sg_katanaRenderman)
	print(" ---- In Katana ---- ")
elif in_maya:
	import maya.cmds as cmds
	import maya.utils
	import maya.mel as mm

	from shiboken2 import wrapInstance

	import sg_mayaRenderman
	import sg_mayaArnold
	import sg_mayaLibraryCommands

	if pythonVersion == 2:
		reload(sg_mayaRenderman)
		reload(sg_mayaArnold)
		reload(sg_mayaLibraryCommands)
	elif pythonVersion == 3:
		imp.reload(sg_mayaRenderman)
		imp.reload(sg_mayaArnold)
		imp.reload(sg_mayaLibraryCommands)

	import pymel.core as pm

	if not cmds.pluginInfo('fbxmaya', q=True, l=True):
			cmds.loadPlugin("fbxmaya") # LOAD PLUGIN

	from mtoa.core import createStandIn, createVolume
	import maya.OpenMayaUI as apiUI
	from maya.app.general.mayaMixin import MayaQWidgetDockableMixin

	dock = MayaQWidgetDockableMixin
	##To attach the window to maya, sip is going to translate for pyqt some function
	import maya.OpenMayaUI as omu
	print(" ---- In Maya ---- ")
elif in_hou:
	import hou
	import sg_houdiniRenderman
	import sg_houdiniMantra
	import sg_houdiniLibraryCommands
	
	if pythonVersion == 2:
		reload(sg_houdiniRenderman)
		reload(sg_houdiniMantra)
		reload(sg_houdiniLibraryCommands)
	elif pythonVersion == 3:
		imp.reload(sg_houdiniRenderman)
		imp.reload(sg_houdiniMantra)
		imp.reload(sg_houdiniLibraryCommands)

	import hdefereval
	print(" ---- In Houdini ---- ")
elif in_blen:
	import bpy
	import sg_blenderLibraryCommands
	imp.reload(sg_blenderLibraryCommands)
	print(" ---- In Blender ---- ")
elif in_unreal:
	if in_nuke == True:
		import nuke
		in_unreal = False
		print(" ---- In Nuke with Unreal ---- ")
	else:
		import unreal
		import sg_unrealLibraryCommands
		imp.reload(sg_unrealLibraryCommands)
		print(" ---- In Unreal ---- ")

print (" -- Loading Python Modules ... -- ")

import platform
import time
from datetime import datetime,timedelta
from collections import OrderedDict

import subprocess
import shutil
import json
import zipfile
import threading
import math
import inspect
import tempfile
import random
import re
import glob
import traceback
import uuid

from functools import partial
from shutil import copyfile
from shutil import copytree

#from mpc.amanda.client.amandaProxy import amandaProxy
#_services = amandaProxy()

if in_katana == True :
	from PyQt5 import QtWidgets,QtGui, QtCore, QtWidgets , uic 
	from PyQt5.QtGui import QMovie
else:
	from PySide2 import QtGui, QtCore, QtWidgets , QtUiTools
	from PySide2.QtUiTools import QUiLoader
	from PySide2.QtCore import QFile, QObject
	from PySide2.QtCore import QEvent
	from PySide2.QtGui import QMovie

################################################# PIL Library ##########################################################
try:
	import PIL
	from PIL import Image as pilimage
	pilLoaded = True
	print (" - PIL Library loaded - ")
except :
	print (" - PIL Library didn't load, Ignore - ")
	pilLoaded = False
	pass

try:
	# Crash Mari
	if not in_mari:
		import sg_contactSheet
		if pythonVersion == 2:
			reload(sg_contactSheet)
		elif pythonVersion == 3:
			imp.reload(sg_contactSheet)
	print (" - ContactSheet Module Loaded - ")
except:
	print (" - ContactSheet module didn't load, Ignore - ")
	print("     Error Contact sheet:" , sys.exc_info())
	pass

import sg_functions as fcn
if pythonVersion == 2:
	reload(fcn)
elif pythonVersion == 3:
	imp.reload(fcn)

########################################################################################################################
######################################### Loading Batch Texture Convert ################################################
########################################################################################################################

# def loadBTC():
# 	fileDir = os.path.dirname(os.path.abspath(__file__))
# 	pathBTC = os.path.abspath(os.path.join(fileDir, '../sg_batchTextureConvert/'))
# 	sys.path.append( pathBTC )

# 	return pathBTC

# loadBTC()
# import sg_batchTextureConvert
# if pythonVersion == 2:
# 	reload(sg_batchTextureConvert)
# elif pythonVersion == 3:
# 	imp.reload(sg_batchTextureConvert)

############################################## Import Add to Collection ################################################

import sg_collectionsCreation
if pythonVersion == 2 :
	reload(sg_collectionsCreation)
elif pythonVersion == 3 :
	imp.reload(sg_collectionsCreation)

############################################ Loading Batch Texture Convert #############################################
## Crash in Mari and Katana
try:
	#if in_maya or in_blen:
	import sg_addBatchTextureToAlexandria
	if pythonVersion == 2 :
		reload(sg_addBatchTextureToAlexandria)
	elif pythonVersion == 3 :
		imp.reload(sg_addBatchTextureToAlexandria)
	print(" - Batch Texture Module Loaded")
except:
	print(" - Could not load sg_addBatchTextureToAlexandria")
	print(sys.exc_info())
	pass

######################################### Attach the window to Software Used ###########################################
def software_main_window():
	if in_maya == True:
		if pythonVersion == 2:
			mayaPtr = omu.MQtUtil.mainWindow()
			mainWindow = wrapInstance(long(mayaPtr),QtWidgets.QWidget)
		elif pythonVersion == 3:
			mainWindow = QtWidgets.QApplication.activeWindow()
	elif in_hou == True:
			mainWindow = hou.qt.mainWindow()
	elif in_nuke ==True or in_mari == True or in_katana == True:
			mainWindow = QtWidgets.QApplication.activeWindow()
			mainWindow.setAcceptDrops(True)
	elif in_blen == True:
		mainWindow = QtWidgets.QApplication.activeWindow()
	elif in_unreal == True:
		mainWindow = None
	else:
		mainWindow = None

	return mainWindow

########################################################################################################################
########################################################################################################################

################################################ Progress bar ##########################################################
class sgProgressBarLibrary(QtWidgets.QMainWindow):
	def __init__(self, parent = software_main_window()):
		super(sgProgressBarLibrary, self).__init__(parent)
		self.fileDir = os.path.dirname(os.path.abspath(__file__))
		file_progressBar = os.path.abspath(self.fileDir+ "/ui/ui_sgEnvProgressBar.ui")

		if  not in_katana :
			self.loaderP = QUiLoader()
			self.progressWidget = self.loaderP.load(file_progressBar,self)
		else:
			self.progressWidget = uic.loadUi(file_progressBar)
		
		self.resize(425,100)
		self.setWindowTitle("Loading Megascans Library")

	def setValue(self, val,text): # Sets value
		self.progressWidget.progressBar_sgLoadEnvWin.setProperty("value", val)
		self.progressWidget.label_sgProgressBarWin.setText(text)

	def finishBar(self,timeFade):
		self.progressWidget.progressBar_sgLoadEnvWin.setProperty("value", 100)
		time.sleep(timeFade)
		self.close()

############################################## Input Name Dialog #######################################################
class sgInputNameDialog(QtWidgets.QDialog):
	'''
	This is for when you need to get some user input text
	'''
	def __init__(self, parent=None, title='Add Category', label='Name:', text=''):
		super(sgInputNameDialog,self).__init__(parent)

		#--Layout Stuff---------------------------#
		mainLayout = QtWidgets.QVBoxLayout()

		layout = QtWidgets.QHBoxLayout()
		self.label = QtWidgets.QLabel()
		self.label.setText(label)
		layout.addWidget(self.label)

		self.text = QtWidgets.QLineEdit(text)
		layout.addWidget(self.text)

		mainLayout.addLayout(layout)

		#--The Button------------------------------#
		layout = QtWidgets.QHBoxLayout()
		button = QtWidgets.QPushButton("OK") #string or icon
		self.connect(button, QtCore.SIGNAL("clicked()"), self.close)
		layout.addWidget(button)

		mainLayout.addLayout(layout)
		self.setLayout(mainLayout)

		self.resize(400, 60)
		self.setWindowTitle(title)

############################################## Remove Item  #######################################################
class sgRemoveItemConfirmDialog(QtWidgets.QMessageBox):
	'''
	This is for when you need to get some user input text
	'''
	def __init__(self, parent=None, title='Remove Item(s):', label='', text=''):
		super(sgRemoveItemConfirmDialog,self).__init__(parent)

		self.setStandardButtons(QtWidgets.QMessageBox.Ok|QtWidgets.QMessageBox.Cancel)
		#self.buttonClicked.connect(self.buttonPressed)

		self.resize(400, 60)
		self.setWindowTitle(title)

	def setTextRemoval(self,label):
		self.setText(label)

############################################## Show Message User   #######################################################
class sgShowMessageUser(QtWidgets.QMessageBox):
	'''
	This is for when you need to get some user input text
	'''
	def __init__(self, parent=None, title='Message:', label='', text=''):
		super(sgShowMessageUser,self).__init__(parent)

		self.setStandardButtons(QtWidgets.QMessageBox.Ok)

		self.resize(400, 120)
		self.setFixedSize(400, 120)
		self.setWindowTitle(title)

	def setMessage(self,label):
		self.setText(label)

##############################################  Confirmation User   #######################################################
class sgConfirmationMessage(QtWidgets.QMessageBox):
	'''
	This is for when you need to get some user input text
	'''
	def __init__(self, parent=None, title='Confirm Action:', label='', text=''):
		super(sgConfirmationMessage,self).__init__(parent)

		self.setStandardButtons(QtWidgets.QMessageBox.Ok|QtWidgets.QMessageBox.Cancel)

		self.resize(400, 60)
		self.setWindowTitle(title)

	def setMessage(self,label):
		self.setText(label)

############################################# Add To Collection ########################################################
class sgAddCollection(QtWidgets.QDialog):
	'''
	UI to add selected item to a Collection
	'''
	def __init__(self, parent= software_main_window(),title='Manage Collection', label='Manage Collection'):
		super(sgAddCollection,self).__init__(parent)

		#self.fileDir = os.path.dirname(os.path.abspath(inspect.stack()[0][1]))
		self.fileDir = os.path.dirname(os.path.abspath(__file__))
		file_customAddCollection = os.path.abspath(self.fileDir+ "/ui/ui_sgCustomAddCollection.ui")
		file_customAddCollectionKatana = os.path.abspath(self.fileDir+ "/ui/ui_sgCustomAddCollection_Katana.ui")
		self.stylesheetUnreal = os.path.abspath(self.fileDir+ "/themes/unreal_qtStyle.ssh")
		
		self.pathToCollection =""

		if  not in_katana :
			self.loaderP = QUiLoader()
			self.addToCollectionWidget = self.loaderP.load(file_customAddCollection,self)

		else:
			self.addToCollectionWidget = uic.loadUi(file_customAddCollection,self)
			
		self.addToCollectionWidget.setWindowTitle("Add to Collection")
		self.setFixedSize(400,820)

		self.data= {}
		self.jsonInfoFileExtension = "_infos.json"

		if in_unreal:
			# self.main_widget.libraryTab.setTabEnabled(1,False)
			with open(self.stylesheetUnreal,"r") as unrealStyleSheet:
				self.setStyleSheet(unrealStyleSheet.read())
			self.addToCollectionWidget.setStyle(QtWidgets.QStyleFactory.create("Fusion"))

		self.listCollectionWidget = self.addToCollectionWidget.listWidget_sgListCollection
		
		self.addToCollectionWidget.pushButton_sgAddToCollection.clicked.connect(self.accept)
		self.addToCollectionWidget.pushButton_sgCancelCollection.clicked.connect(self.close)
		self.addToCollectionWidget.listWidget_sgListCollection.itemDoubleClicked.connect(self.accept)

		self.addToCollectionWidget.pushButton_sgopenIconFinder.clicked.connect(self.selectIcon)
		self.addToCollectionWidget.pushButton_sgCreateNewCollection.clicked.connect(self.createNewCollection)

		self.addToCollectionWidget.groupBox_sgCreateCollection.toggled.connect(self.toggleCreateCollectionUI)

	def saveAddToCollection(self):
		return self.data

	def generateUUID(self):
		return str(uuid.uuid1())+"----" 

	def createNewCollection(self):
		nameNewCollection = self.addToCollectionWidget.lineEdit_sgNewCollectionName.text()
		if nameNewCollection != "":
			uuid = self.generateUUID()
			self.createNewFolder(self.pathToCollection + nameNewCollection)
			iconPath = self.addToCollectionWidget.lineEdit_sgPathIcon.text()
			extension = iconPath.split(".")[-1]
			icon = uuid+nameNewCollection+"_Preview."+ extension
			iconName = nameNewCollection+"_Preview."+ extension
			jsonFileInfos = nameNewCollection+ self.jsonInfoFileExtension
			fullPath = os.path.join(self.pathToCollection,nameNewCollection)
			tags = ""
			notes = self.addToCollectionWidget.lineEdit_sgCollectionNotes.text()
			if iconPath:
				savedIcon = self.pathToCollection + nameNewCollection + "/" + uuid+nameNewCollection+"_Preview." + extension
				self.copyFile(iconPath,savedIcon)
			self.createJsonFromNote(self.pathToCollection + nameNewCollection+"/" + nameNewCollection+ self.jsonInfoFileExtension)
			self.listCollection.append(self.pathToCollection + nameNewCollection+"/")
			self.listCollection.sort()

			self.addToCollectionWidget.listWidget_sgListCollection.clear()
			self.addToCollectionWidget.lineEdit_sgNewCollectionName.clear()
			self.appendUI(self.listCollection)

			print ("Collection Added: " + nameNewCollection)
			self.data = fcn.addEntryToAssetDictionary(nameNewCollection,icon,iconName,uuid,jsonFileInfos,fullPath,"Collections",time.time(),notes,tags)

		else:
			print("No valid name for the collection")

	def setPathCollection(self,path):
		self.pathToCollection = path

	def getListCollections(self,listCollection):
		self.listCollection = listCollection

	def createNewFolder(self,newpath):
		if not os.path.exists(newpath):
			os.umask(0)
			folderCreated = os.makedirs(newpath,0o777)
		else:
			folderCreated = "Already Exist"
		return folderCreated
	
	def selectIcon(self):
		selected_icon = QtWidgets.QFileDialog.getOpenFileName(self,"Choose an icon file","","*.jpg *.png")
		#selected_icon.setFixedSize(1000,600)
		self.addToCollectionWidget.lineEdit_sgPathIcon.setText(str(selected_icon[0]))

	def createJsonFromNote(self,jsonFilepath):
		notes = self.addToCollectionWidget.lineEdit_sgCollectionNotes.text()
		tags = ""
		name = self.addToCollectionWidget.lineEdit_sgNewCollectionName.text()
		listFileExtension = []
		listTextures=[]
		version = ""
		ocio = "Unknown"
		date = ""
		meta = ""
		
		self.writeJsonCollectionInfos(jsonFilepath,name,notes,tags)

	def copyFile(self, inFile, outFile):
		try:
			copyfile(inFile, outFile)
		except:
			print("Couldn't Create Icon")
			pass
		return outFile

	def updateUI(self,listName):
		for item in listName:
			self.addToCollectionWidget.listWidget_sgListCollection.addItem(item)

	def appendUI(self,listCollection):
		## Get a path and convert to the name of the folder
		for item in listCollection:
			path =os.path.dirname(item)
			self.addToCollectionWidget.listWidget_sgListCollection.addItem(os.path.basename(path))

	def toggleCreateCollectionUI(self,toggle):
		if toggle == True:
			self.addToCollectionWidget.groupBox_sgCreateCollection.setMaximumHeight(300)
		elif toggle == False:
			self.addToCollectionWidget.groupBox_sgCreateCollection.setMaximumHeight(50)

	def toggleDeleteCollectionUI(self,toggle):
		if toggle == True:
			self.addToCollectionWidget.groupBox_sgDeleteCollection.setMaximumHeight(300)
		elif toggle == False:
			self.addToCollectionWidget.groupBox_sgDeleteCollection.setMaximumHeight(50)

	def writeJsonCollectionInfos(self,jsonFilepath,name,notes,tags):
		data = {}
		data["releaseInfos"]= []
		data["releaseInfos"].append({
		'author': os.getenv("USER"),
		'timeEntry': time.time(),
		'lock':False,
		'version':"1",
		'ocio':"",
		'name':name,
		'extension': [],
		'textures' :[],
		'tags':tags,
		'meta': "",
		'note':notes
		})

		with open(jsonFilepath,'w') as outJson:
			json.dump(data,outJson,indent = 4)

########################################### Pick LOD UI ################################################################
class sgPickLOD(QtWidgets.QDialog):
	'''
	UI to pick LODs
	'''
	def __init__(self,parent=software_main_window()):
		super(sgPickLOD,self).__init__(parent)

		#self.fileDir = os.path.dirname(os.path.abspath(inspect.stack()[0][1]))
		self.fileDir = os.path.dirname(os.path.abspath(__file__))
		file_customPickLOD = os.path.abspath(self.fileDir+ "/ui/ui_sgPickLOD.ui")
		file_customPickLODKatana = os.path.abspath(self.fileDir+ "/ui/ui_sgPickLOD_Katana.ui")
		self.stylesheetUnreal = os.path.abspath(self.fileDir+ "/themes/unreal_qtStyle.ssh")

		if  not in_katana :
			self.loaderP = QUiLoader()
			self.pickLODWidget = self.loaderP.load(file_customPickLOD,self)
			
		else:
			self.pickLODWidget = uic.loadUi(file_customPickLOD,self)

		self.setWindowTitle("Pick LOD to load")

		if in_unreal:
			# self.main_widget.libraryTab.setTabEnabled(1,False)
			with open(self.stylesheetUnreal,"r") as unrealStyleSheet:
					self.setStyleSheet(unrealStyleSheet.read())
			self.pickLODWidget.setStyle(QtWidgets.QStyleFactory.create("Fusion"))

		self.setFixedSize(300,350)
		self.pickLODWidget.pushButton_sgOkLOD.clicked.connect(self.accept)
		self.pickLODWidget.pushButton_sgCancelLOD.clicked.connect(self.close)

		self.listLODWidget = self.pickLODWidget.listWidget_sgListPickLOD

	def appendUI(self,listLODs):
		for item in listLODs:
			self.pickLODWidget.listWidget_sgListPickLOD.addItem(item)

################################################ Edit Notes ############################################################
class sgEditInfos(QtWidgets.QDialog):
	'''
	UI to edit json infos from asset ( not tested on megascans )
	'''
	def __init__(self,parent = software_main_window()):
		super(sgEditInfos,self).__init__(parent)
		
		self.fileDir = os.path.dirname(os.path.abspath(__file__))
		file_customEditInfos = os.path.abspath(self.fileDir+ "/ui/ui_sgEditInfos.ui")
		file_customEditInfosKatana = os.path.abspath(self.fileDir+ "/ui/ui_sgEditInfos_Katana.ui")
		self.stylesheetUnreal = os.path.abspath(self.fileDir+ "/themes/unreal_qtStyle.ssh")
		if not in_katana :
			self.loaderP = QUiLoader()
			self.editInfosWidget = self.loaderP.load(file_customEditInfos,self)
			
		else:
			self.editInfosWidget = uic.loadUi(file_customEditInfos,self)

		self.setWindowTitle("Edit Information of Selected Asset")
		self.setFixedSize(500,740)
		self.setWindowIcon(QtGui.QIcon(self.fileDir+"/icons/sg_alexandriaLibrary_icon64.png"))
		# self.resize(500,450)

		self.pb_icon = self.editInfosWidget.pb_icon
		self.textEdit_author = self.editInfosWidget.textEdit_author
		self.textEdit_tags = self.editInfosWidget.textEdit_tags
		self.textEdit_note = self.editInfosWidget.textEdit_note
		self.textEdit_meta = self.editInfosWidget.textEdit_meta
		self.textEdit_files = self.editInfosWidget.textEdit_files
		self.comboBox_ocio = self.editInfosWidget.comboBox_ocio

		self.editInfosWidget.pb_icon.clicked.connect(self.updateIcon)

		self.editInfosWidget.pushButton_sgOkEditInfos.clicked.connect(self.accept)
		self.editInfosWidget.pushButton_sgCancelEditInfos.clicked.connect(self.close)

		if in_unreal:
			# self.main_widget.libraryTab.setTabEnabled(1,False)
			with open(self.stylesheetUnreal,"r") as unrealStyleSheet:
				self.setStyleSheet(unrealStyleSheet.read())
			self.editInfosWidget.setStyle(QtWidgets.QStyleFactory.create("Fusion"))

	def updateIcon(self):
		selectedIconBrowser = QtWidgets.QFileDialog.getOpenFileName(self,"Choose a new icon","","*.jpg *.png *.gif")
		
		if selectedIconBrowser[0] != "":
			self.setIcon(selectedIconBrowser[0])
			self.editInfosWidget.pb_icon.setToolTip(selectedIconBrowser[0])

	def createNewIcon(self):
		icon = QtGui.QIcon()
		return icon

	def setIcon(self,iconPath):
		icon = self.createNewIcon()
		icon.addPixmap(QtGui.QPixmap(iconPath), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.editInfosWidget.pb_icon.setIcon(icon)
		self.editInfosWidget.pb_icon.setIconSize(QtCore.QSize(128, 128))

		self.editInfosWidget.pb_icon.setToolTip(iconPath)

	def setOCIOCombobox(self,listOCIO):
		self.editInfosWidget.comboBox_ocio.addItems(listOCIO)

	def setWindowsTitle(self,nameAsset):
		self.setWindowTitle("Edit Information of: " + nameAsset)

	def infoInUI(self,iconPath,tags,meta,author,files,notes,ocio):
		self.setIcon(iconPath)
		self.editInfosWidget.textEdit_tags.setPlainText(tags)
		self.editInfosWidget.textEdit_author.setPlainText(author)
		self.editInfosWidget.textEdit_note.setPlainText(notes)
		self.editInfosWidget.textEdit_meta.setPlainText(meta)
		self.editInfosWidget.textEdit_files.setPlainText(files)
		#QtCore.Qt.MatchContains
		#QtCore.Qt.MatchFixedString
		index = self.editInfosWidget.comboBox_ocio.findText(ocio,QtCore.Qt.MatchFixedString)
		self.editInfosWidget.comboBox_ocio.setCurrentIndex(index)

################################################ Show Asset Infos ######################################################
class sgAssetInfos(QtWidgets.QDialog):
	'''
	UI to edit json infos from asset ( not tested on megascans )
	'''
	def __init__(self,parent = software_main_window()):
		super(sgAssetInfos,self).__init__(parent)
		
		self.fileDir = os.path.dirname(os.path.abspath(__file__))
		file_customAssetInfos = os.path.abspath(self.fileDir+ "/ui/ui_sgDialogInfos.ui")
		print(file_customAssetInfos)
		#file_customAssetInfosKatana = os.path.abspath(self.fileDir+ "/ui/ui_sgDialogInfos_Katana.ui")
		self.stylesheetUnreal = os.path.abspath(self.fileDir+ "/themes/unreal_qtStyle.ssh")
		if  not in_katana :
			self.loaderP = QUiLoader()
			self.assetInfosWidget = self.loaderP.load(file_customAssetInfos,self)
		else:
			self.assetInfosWidget = uic.loadUi(file_customAssetInfos,self)

		self.setWindowTitle("Asset Information")
		self.setFixedSize(450,700)

		self.assetInfosWidget.pushButton_sgOkAssetInfos.clicked.connect(self.accept)
		#self.assetInfosWidget.pushButton_sgCancelAssetInfos.clicked.connect(self.close)
		#self.textEdit_author = self.editInfosWidget.textEdit_author

		if in_unreal:
			with open(self.stylesheetUnreal,"r") as unrealStyleSheet:
					self.setStyleSheet(unrealStyleSheet.read())
			self.editInfosWidget.setStyle(QtWidgets.QStyleFactory.create("Fusion"))

		# self.listLODWidget = self.pickLODWidget.listWidget_sgListPickLOD

	def infoInUI(self,dicData):
		self.assetInfosWidget.labelBrowser.setText(json.dumps(dicData,indent = 4))

################################################ Folder Dialog	 #######################################################

class sgFolderDialog(QtWidgets.QDialog):
	def __init__(self,parent = None):
		super(sgFolderDialog,self).__init__(parent)
		dialogFolder = QtWidgets.QFileDialog(None,"Pick Folder")
		dialogFolder.setFileMode(QtWidgets.QFileDialog.Directory)
		dialogFolder.setOption(QtWidgets.QFileDialog.DontUseNativeDialog,True)
		dialogFolder.setOption(QtWidgets.QFileDialog.ShowDirsOnly,False)

	def closeEvent(self,event):

		# Save Geometry and position on Screen
		self.settings.setValue("geometry",self.saveGeometry())
		self.settings.setValue("windowState",self.saveState())

		event.accept()

########################################################################################################################
#######################################  Window Library and its functions ##############################################
########################################################################################################################

# To get Katana embeded in the UI / to check in Linux. Path must be added as an env variable in KATANA_RESOURCES, it will 
# load if script is in a subfolder named Tabs 
if not in_katana:
	widget = QtWidgets.QMainWindow
elif in_katana:
	widget = QtWidgets.QMainWindow
	#widget = UI4.Tabs.BaseTab

class sgAlexandriaLibrary(widget):
	def __init__(self, parent = software_main_window()):
		super(sgAlexandriaLibrary, self).__init__(parent)
		#if not in_katana:
		#	super(sgAlexandriaLibrary, self).__init__(parent)
		#elif in_katana:
		#	UI4.Tabs.BaseTab.__init__(self,parent)

		# Load in your UI file.
		self.platform = sys.platform
		self.fileDir = os.path.dirname(os.path.abspath(__file__))
		file_interface = os.path.abspath(self.fileDir+ "/ui/ui_sgAlexandriaLibrary.ui")
		file_interfaceKatana = os.path.abspath(self.fileDir+ "/ui/ui_sgAlexandriaLibrary_Katana.ui")
		stylesheetBlender = os.path.abspath(self.fileDir+ "/themes/qtStyle.ssh")
		self.stylesheetUnreal = os.path.abspath(self.fileDir+ "/themes/unreal_qtStyle.ssh")

		self.defaulPathJson =  os.path.abspath(self.fileDir+"/setup/defaultPath.json")
		self.defaulPathJson = self.defaulPathJson.replace(os.sep,"/")
		## TODO Check it is really necessary
		# if self.platform == "win32" or self.platform == "win64":
		# 	self.defaulPathJson.replace("jobs","J:/")
		# if self.platform == "linux2" or self.platform == "linux":
		# 	self.defaulPathJson.replace("J:/","jobs")

		print("Library default path file: " + self.defaulPathJson)

		## Set The UI size
		if not in_katana:
			self.loader = QUiLoader()
			self.main_widget = self.loader.load(file_interface,self)
			self.setObjectName("sgAlexandriaLibrary")
			if in_maya:
				self.resize(1150,1080)
			if in_hou:
				self.resize(1020,1080)
			if in_nuke:
				self.resize(1020,1080)
			if in_mari:
				self.resize(980,1080)
			if in_blen:
				self.overrideBlenderContext = bpy.context.copy()
				self.resize(980,1080)
			if in_unreal:
				self.resize(980,1080)

		else:
			self.main_widget = uic.loadUi(file_interfaceKatana,self)
			self.main_widget.resize(1040,1160)
		
		self.setWindowTitle("Library v2.0.1")
		self.setWindowIcon(QtGui.QIcon(self.fileDir+"/icons/sg_alexandriaLibrary_icon64.png"))
		self.installEventFilter(self)

		# Inherit Houdinis Style Sheet.
		if in_hou == True:
			stylesheet = hou.qt.styleSheet()
			self.setStyleSheet(stylesheet)
		# Disable Icons per Software
		if in_nuke:
			self.main_widget.checkBox_sgTextureSharedUV.setEnabled(False)
			#self.main_widget.checkBox_sgTextureTriplanar.setEnabled(False)
		if in_mari:
			self.main_widget.libraryTab.setTabEnabled(2,False)
			self.main_widget.libraryTab.setTabEnabled(3,False)
			self.main_widget.checkBox_sgTextureSharedUV.setEnabled(False)
			self.main_widget.checkBox_sgTextureTriplanar.setEnabled(False)
		#if in_katana:
			#self.main_widget.libraryTab.setTabEnabled(2,False)
			#self.main_widget.libraryTab.setTabEnabled(3,True)
		if in_blen:
			with open(stylesheetBlender,"r") as blenderStyleSheet:
				self.setStyleSheet(blenderStyleSheet.read())
		if in_unreal:
			# self.main_widget.libraryTab.setTabEnabled(1,False)
			with open(self.stylesheetUnreal,"r") as unrealStyleSheet:
				self.setStyleSheet(unrealStyleSheet.read())
			self.main_widget.setStyle(QtWidgets.QStyleFactory.create("Fusion"))

		self.pilLoaded = pilLoaded
		
		## Blender
		self.blenderContext = "VIEW_3D"

		########### Batch Convert #############
		try:
			pathBTC = os.path.abspath(os.path.join(self.fileDir, '../sg_batchTextureConvert/'))
			sys.path.append( pathBTC )
			import sg_batchTextureConvert
			if pythonVersion ==2:
				reload(sg_batchTextureConvert)
			elif pythonVersion ==3:
				imp.reload(sg_batchTextureConvert)
			print(" - Batch Convert has been loaded - ")
		except:
			# TODO Disable Button ? 
			print(" - Batch Convert has not been loaded - ")
			print(sys.exc_info())
			pass

		########### Book Convert ##############

		try:
			pathBook = os.path.abspath(os.path.join(self.fileDir, '../sg_convertToBook/'))
			sys.path.append(pathBook)

			import sg_convertToBook
			if pythonVersion ==2:
				reload(sg_convertToBook)
			elif pythonVersion ==3:
				imp.reload(sg_convertToBook)
			print(" - Book Convert has been loaded - ")
		except:
			# TODO Disable Button ?
			print(" - Book Convert has not been loaded - ")
			print(sys.exc_info())
			pass

		########### Init Procedure ############
		## To check maya, nuke or houdini have different way to get the env variable
		if self.platform == "win32" or self.platform == "win64":
			if in_mari or in_katana or in_blen or in_unreal or in_maya or in_nuke or in_hou:
				self.userPreferenceFolder = os.path.abspath(os.path.join( os.environ['HOMEDRIVE'],os.environ['HOMEPATH'])) + "/"
			else:
				self.userPreferenceFolder = os.environ['HOME'] + "/"

			self.userPreferenceFolder = self.userPreferenceFolder.replace(os.sep,"/")
		elif self.platform == "linux2" or self.platform == "linux":
			self.userPreferenceFolder = os.environ['HOME'] + "/"
		self.userPrefJson = "sg_alexandriaLibrary_pref.json"
		print("User Preference Folder: " + self.userPreferenceFolder)

		self.initPathsLibrary()
		self.main_widget.tableWidget_sgSearchBrowser.setVisible(False)

		##################### Main Tab
		self.main_widget.treeWidget_sgLibrary.itemClicked.connect(self.launchBrowsing)
		self.main_widget.tableWidget_sgElementBrowser.currentCellChanged.connect(self.cellClicked)
		self.main_widget.tableWidget_sgElementBrowser.cellDoubleClicked.connect(self.doubleClickCommandBrowser)
		self.main_widget.tableWidget_sgSearchBrowser.cellDoubleClicked.connect(self.doubleClickCommandBrowser)
		self.main_widget.tableWidget_sgCollectionBrowser.cellDoubleClicked.connect(self.doubleClickCommandBrowser)

		## Collections Tab
		self.main_widget.tableWidget_sgCollectionBrowser.currentCellChanged.connect(self.cellClicked)

		## Tab
		self.main_widget.libraryTab.currentChanged.connect(self.changeTab)

		## Icons Preview
		self.main_widget.pb_iconInfos08.clicked.connect(self.showAssetInfos)
		self.main_widget.pb_iconInfos01.toggled.connect(self.buttonItemLock)
		#partial(self.buttonItemLock,iconPathLock,iconPathUnlock)

		##################### Create New Entry 
		## Model/Shader 
		self.buttonModel = self.main_widget.pushButton_sgAddEntry
		self.main_widget.pushButton_sgAddEntry.clicked.connect(lambda:self.addNewEntry(self.buttonModel))
		self.main_widget.checkBox_sgUseFileDisc.toggled.connect(self.toggleUseDiscThumbnail)
		self.main_widget.sg_thumbnailFile_toolButton.clicked.connect(self.selectThumbnailFile)
		self.main_widget.pushButton_sgPreviewThumbnail.clicked.connect(partial(self.thumbnailsCreator,"",True))
		self.main_widget.comboBox_sgPreviewRes.currentTextChanged.connect(self.setResThumbnailNewEntry)

		## Texture
		self.main_widget.pushButton_sg_PickFolderTexturesEntry.clicked.connect(lambda:self.selectFolderUIUpdate(self.main_widget.pushButton_sg_PickFolderTexturesEntry))
		self.main_widget.radioButton_sgUniqueEntryText.clicked.connect(self.updateTextureEntryTypeUI)
		self.main_widget.radioButton_sgGroupEntryText.clicked.connect(self.updateTextureEntryTypeUI)
		self.main_widget.pushButton_sgCreateEntryDirectoryTextures.clicked.connect(self.launchBatchTextureTool)

		## DMP
		self.main_widget.pushButton_sg_PickDMPFolderEntry.clicked.connect(lambda:self.selectFolderUIUpdate(self.main_widget.pushButton_sg_PickDMPFolderEntry))
		self.main_widget.pushButton_sgCreateEntryDirectoryDMP.clicked.connect(self.addNewEntryDMP)
		self.main_widget.radioButton_sgDMPCopyImgs.clicked.connect(self.updateDMPEntryTypeUI)
		self.main_widget.radioButton_sgDMPLinkToOriginal.clicked.connect(self.updateDMPEntryTypeUI)

		self.main_widget.pushButton_sgDMPContactsheet01.clicked.connect(lambda:self.updateNewEntryIcons(self.main_widget.pushButton_sgDMPContactsheet01))
		self.main_widget.pushButton_sgDMPContactsheet02.clicked.connect(lambda:self.updateNewEntryIcons(self.main_widget.pushButton_sgDMPContactsheet02))
		self.main_widget.pushButton_sgDMPContactsheet03.clicked.connect(lambda:self.updateNewEntryIcons(self.main_widget.pushButton_sgDMPContactsheet03))
		self.main_widget.pushButton_sgDMPContactsheet04.clicked.connect(lambda:self.updateNewEntryIcons(self.main_widget.pushButton_sgDMPContactsheet04))

		## IES
		self.main_widget.pushButton_sg_PickFolderIESEntry.clicked.connect(lambda:self.selectFolderUIUpdate(self.main_widget.pushButton_sg_PickFolderIESEntry))
		self.main_widget.pushButton_sgCreateEntryIES.clicked.connect(self.addNewEntryIES)
		self.main_widget.pushButton_sgIESPreview.clicked.connect(self.selectThumbnailIES)
		self.main_widget.pushButton_sgIESFoundFile.clicked.connect(partial( self.openFileInExplorer,self.folderNewIES))
		self.main_widget.pushButton_sgIESFoundJson.clicked.connect(partial( self.openFileInExplorer,self.folderNewIES))

		## VDB
		self.buttonVDB = self.main_widget.pushButton_sgVDBAddEntry
		self.main_widget.pushButton_sgVDBAddEntry.clicked.connect(lambda:self.addNewEntry(self.buttonVDB))
		self.main_widget.checkBox_sgVDBUseFileDisc.toggled.connect(self.toggleVDBUseDiscThumbnail)
		self.main_widget.sg_VDBthumbnailFile_toolButton.clicked.connect(self.selectVDBThumbnailFile)
		self.main_widget.pushButton_sgVDBPreviewThumbnail.clicked.connect(partial(self.thumbnailsCreator,"",True))
		self.main_widget.comboBox_sgVDBPreviewRes.currentTextChanged.connect(self.setResThumbnailNewEntry)
		self.main_widget.pushButton_sg_PickFolderVDBEntry.clicked.connect(self.selectVDBFile)

		## ArtBooks/Tutorials
		self.main_widget.pushButton_sg_PickABTFolderEntry.clicked.connect(lambda:self.selectFolderUIUpdate(self.main_widget.pushButton_sg_PickABTFolderEntry))
		self.main_widget.pushButton_sgCreateEntryArtBooks.clicked.connect(self.addNewEntryATB)
		self.main_widget.radioButton_sgABTCopyImgs.clicked.connect(self.updateATBEntryTypeUI)
		self.main_widget.radioButton_sgABTLinkToOriginal.clicked.connect(self.updateATBEntryTypeUI)
		self.main_widget.pushButton_sgABTContactsheet01.clicked.connect(lambda:self.updateNewEntryIcons(self.main_widget.pushButton_sgABTContactsheet01))
		
		## Path Library
		self.main_widget.comboBox_sgDefaultLibrary.currentIndexChanged.connect(self.setDefaultPath)
		self.main_widget.button_sgPathLibrary.clicked.connect(partial(self.openFileInExplorer,self.libraryPath))

		##################### SETTINGS
		self.main_widget.comboBox_sgDefaultLibrary.currentIndexChanged.connect(self.userPreferencesWrite)
		self.main_widget.lineEdit_sgPathUnzipMegascans.textChanged.connect(self.userPreferencesWrite)
		self.main_widget.pb_sgPathUnzipMegascans.clicked.connect(self.selectUnzipFolder)
		self.main_widget.lineEdit_sgPathBrowser_lin.textChanged.connect(self.userPreferencesWrite)
		self.main_widget.pb_sgPathBrowser_lin.clicked.connect(lambda:self.selectImageOrPDFBrowser(self.main_widget.pb_sgPathBrowser_lin))
		self.main_widget.lineEdit_sgPathBrowser_win.textChanged.connect(self.userPreferencesWrite)
		self.main_widget.pb_sgPathBrowser_win.clicked.connect(lambda:self.selectImageOrPDFBrowser(self.main_widget.pb_sgPathBrowser_win))
		self.main_widget.lineEdit_sgPDFPathBrowser_lin.textChanged.connect(self.userPreferencesWrite)
		self.main_widget.pb_sgPDFPathBrowser_lin.clicked.connect(lambda:self.selectImageOrPDFBrowser(self.main_widget.pb_sgPDFPathBrowser_lin))
		self.main_widget.lineEdit_sgPDFPathBrowser_win.textChanged.connect(self.userPreferencesWrite)
		self.main_widget.pb_sgPDFPathBrowser_win.clicked.connect(lambda:self.selectImageOrPDFBrowser(self.main_widget.pb_sgPDFPathBrowser_win))
		self.main_widget.pushButton_megascansPath.clicked.connect(partial( self.openFileInExplorer,self.megascanZIPLibraryPath))

		self.main_widget.checkBox_sgMegAutoSync.toggled.connect(self.initMegascansSync)

		self.main_widget.sgGlobalSettings_Verbosity.currentIndexChanged.connect(self.userPreferencesWrite)
		self.main_widget.sgBlenderSettings_LOD.currentIndexChanged.connect(self.userPreferencesWrite)
		self.main_widget.sgHoudiniSettings_convertionT.currentIndexChanged.connect(self.userPreferencesWrite)
		self.main_widget.sgHoudiniSettings_LOD.currentIndexChanged.connect(self.userPreferencesWrite)
		self.main_widget.sgHoudiniSettings_Settings.currentIndexChanged.connect(self.userPreferencesWrite)
		self.main_widget.sgMariSettings_Shader.currentIndexChanged.connect(self.userPreferencesWrite)
		self.main_widget.sgMariSettings_ColorSpace.currentIndexChanged.connect(self.userPreferencesWrite)
		self.main_widget.sgMayaSettings_LOD.currentIndexChanged.connect(self.userPreferencesWrite)
		self.main_widget.sgNukeSettings_LOD.currentIndexChanged.connect(self.userPreferencesWrite)
		self.main_widget.sgNukeSettings_3D.currentIndexChanged.connect(self.userPreferencesWrite)
		self.main_widget.sgUnrealSettings_LOD.currentIndexChanged.connect(self.userPreferencesWrite)
		self.main_widget.checkBox_sgUnrealSettingsDisplacement.stateChanged.connect(self.userPreferencesWrite)

		##################### SEARCH BAR
		self.main_widget.lineEdit_sgPergamonLibrary_search.returnPressed.connect(self.searchLibrary)
		self.main_widget.tableWidget_sgSearchBrowser.currentCellChanged.connect(self.cellSearchClicked)
		
		##################### TOOLS
		self.main_widget.pushButton_sgNewLibraryTree.clicked.connect(partial(self.createNewLibrary,False,"",""))
		self.main_widget.pushButton_sgRefreshLibrary.clicked.connect(self.refreshTreeView)
		self.main_widget.pushButton_sgDeleteLibraryTree.clicked.connect(self.removeLibrary)
		
		self.main_widget.pushButton_sg_viewLog.clicked.connect(self.viewLog)
		self.main_widget.pushButton_sgSuperUserFile.clicked.connect(partial( self.openFileInExplorer,self.superUsersJson))
		self.main_widget.pushButton_sgSuperUserNameAdd.clicked.connect(partial( self.manageSuperUserFile,"add"))
		self.main_widget.pushButton_sgSuperUserNameRemove.clicked.connect(partial( self.manageSuperUserFile,"remove"))
		self.main_widget.pushButton_sgTagFile.clicked.connect(partial( self.openFileInExplorer,self.tagsJsonFile))
		self.main_widget.pushButton_sgTagMngmtAdd.clicked.connect(partial( self.manageTagFile,"add"))
		self.main_widget.pushButton_sgTagMngmtRemove.clicked.connect(partial( self.manageTagFile,"remove"))

		self.main_widget.pushButton_sgLogPath.clicked.connect(partial( self.openFileInExplorer,self.pathLogFile))
		self.main_widget.pushButton_sgLogViewIni.clicked.connect(partial( self.openFileInExplorer,self.pathLogIni))
		self.main_widget.pushButton_sgUserPrefPath.clicked.connect(partial( self.openFileInExplorer,os.path.join(self.userPreferenceFolder,self.userPrefJson)))
		self.main_widget.pushButton_sgPathSetup.clicked.connect(partial( self.openFileInExplorer,self.defaulPathJson))
		
		self.main_widget.pushButton_sgUpdateJsonInfos.clicked.connect(self.updateOldJsonInfosFiles)
		
		self.main_widget.pushButton_sgErroredZip.clicked.connect(self.openMegascansErroredInExplorer)
		self.main_widget.sg_PathNewLibrary_toolButton.clicked.connect(self.selectFolderNewLibrary)
		
		self.main_widget.pushButton_sgConvertBatch.clicked.connect(self.loadConvertToTexUI)
		self.main_widget.pushButton_sgConvertBook.clicked.connect(self.loadConvertToBookUI)

		self.main_widget.pushButton_sgRebuildDatabase.clicked.connect(self.launchBuildDatabase)
		self.main_widget.pushButton_sgRebuildMegDatabase.clicked.connect(self.launchRebuildMegascansDatabase)
		self.main_widget.pushButton_sgCleanupDatabase.clicked.connect(self.launchCleanUpDatabase)
		self.main_widget.pushButton_sgViewGlobalDatabase.clicked.connect(partial( self.openFileInExplorer,self.databaseJson))
		self.main_widget.pushButton_sgViewAssetDatabase.clicked.connect(partial( self.openFileInExplorer,self.databaseAssetsJson))
		self.main_widget.pushButton_sgViewMegascansDatabase.clicked.connect(partial( self.openFileInExplorer,self.databaseMegascansJson))
		self.main_widget.pushButton_sgDiagnoseDatabase.clicked.connect(self.diagnoseDatabaseUI)
		self.main_widget.pushButton_sgSyncZips.clicked.connect(self.syncAll)

		self.initLoadingDatabase()
		self.initBuildingMegascansLibrary()

		###################################### Create UI Elements ######################################################
		self.main_widget.treeWidget_sgLibrary.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)  
		self.main_widget.treeWidget_sgLibrary.customContextMenuRequested.connect(self.actionCategoryUI)

		## Button UISetup
		self.main_widget.checkBox_sgTextureSharedUV.clicked.connect(self.buttonUVShare)
		self.main_widget.checkBox_sgTextureTriplanar.clicked.connect(self.buttonTriplanar)
		self.main_widget.checkBox_sgShaderLama.clicked.connect(self.buttonLamaShader)

		self.main_widget.checkBox_sgTextureSharedUV.setChecked(True)
		self.buttonUVShare()
		self.buttonTriplanar()
		self.buttonLamaShader()
		self.buttonItemLock()
		
		############################################ UI Zoom ############################################################
		self.main_widget.treeWidget_sgLibrary.viewport().installEventFilter(self)
		## Library Browser
		self.main_widget.tableWidget_sgElementBrowser.setMouseTracking(True)
		self.main_widget.tableWidget_sgElementBrowser.viewport().installEventFilter(self)
		self.main_widget.tableWidget_sgElementBrowser.cellEntered.connect(self.cellEnteredThumbnail)
		## Search Browser
		self.main_widget.tableWidget_sgSearchBrowser.setMouseTracking(True)
		self.main_widget.tableWidget_sgSearchBrowser.cellEntered.connect(self.cellEnteredThumbnail)
		self.main_widget.tableWidget_sgSearchBrowser.viewport().installEventFilter(self)
		## Collection Browser
		self.main_widget.tableWidget_sgCollectionBrowser.setMouseTracking(True)
		self.main_widget.tableWidget_sgCollectionBrowser.cellEntered.connect(self.cellEnteredThumbnail)
		self.main_widget.tableWidget_sgCollectionBrowser.viewport().installEventFilter(self)

		self.actionMenuUI()
		self.actionSearchMenuUI()
		self.actionCollectionMenuUI()
		self.zoomWindowUI()
		self.createPixmapUI()
		self.fillOCIOComboBox()
		# Crash Mari
		if not in_mari:
			self.initSearchCompleter()
					
#######################################################################################################################
######################################### INIT ALL THE USEFUL PATHS ###################################################
#######################################################################################################################

	def initVariables(self):
		###### System
		self.platform = sys.platform
		global objectScroll

		self.elementBrowserWidth = self.main_widget.tableWidget_sgElementBrowser.width()

		self.listSupportedSoftware = ["blender","houdini","katana","mari","maya","nuke","unreal"]

		############## Library
		## ArtBooks
		self.artBookLibraryPath = self.libraryPath + "ArtBooks/"
		## Collections
		self.collectionLibraryPath = self.libraryPath + "Collections/"
		## DMP
		self.dmpLibraryPath = self.libraryPath + "DMP/"
		## IES
		self.iesLibraryPath = self.libraryPath + "IES/"
		## LightRigs
		self.lightrigLibraryPath = self.libraryPath + "Lightrigs/"
		## Models
		self.modelLibraryPath = self.libraryPath + "Models/"
		## Textures
		self.textureLibraryPath = self.libraryPath + "Textures/"
		## Shader
		self.shaderLibraryPath = self.libraryPath + "Shaders/"
		## MetaHumans
		self.metaHumanLibraryPath = self.libraryPath + "MetaHumans/"
		## Megascans
		self.megascanLibraryPath = self.libraryPath + "Megascans/"
		## VDB
		self.vdbLibraryPath = self.libraryPath + "VDB/"

		self.softwareInAction = softwareUsed.lower()

		self.listDefaultFolders = ["ArtBooks","Megascans","MetaHumans","Models","Lightrigs","Textures","Shaders","IES","VDB","DMP","Collections"]
		self.libraryWritableContext = ["ArtBooks","Models","Lightrigs","Textures","Shaders","IES","VDB","DMP"]

		self.jsonAttachmentShader = "attachment"+".json"
		
		self.nameDMPSource = "dmpSources/"
		self.nameATBSource = "sources/"

		## Dictionnary for Path
		self.dicPaths = {}
		self.dicCollectionPaths = {}
		self.dicElementPaths= {}
		self.dataAssetSelected = {}

		## DataBase
		self.dicAllDatabase={}
		self.dicAssetDatabase={}
		self.dicMegascansZip={}
		self.databaseFilename = "database.json"
		self.databaseJson = self.libraryPath + "database.json"
		self.databaseAssetFilename = "databaseAssets.json" 
		self.databaseAssetsJson = self.libraryPath + "databaseAssets.json"
		self.databaseMegascansJson = self.megascanLibraryPath+ "megascans.json"
		self.databaseMegascansFilename = "megascans.json"
		self.databaseSeparator = "----"

		## Global Dic with all in one
		self.dicLibraryPaths= {
			"ArtBooks": self.artBookLibraryPath,
			"Collection": self.collectionLibraryPath,
			"DMP": self.dmpLibraryPath,
			"IES": self.iesLibraryPath,
			"LightRigs": self.lightrigLibraryPath,
			"Models": self.modelLibraryPath,
			"Textures": self.textureLibraryPath,
			"Shaders": self.shaderLibraryPath,
			"MetaHumans": self.metaHumanLibraryPath,
			"Megascans": self.megascanLibraryPath,
			"VDB": self.vdbLibraryPath,
		}

		self.dicLibraryDatabasePaths={
			'Global_Json_Database': self.databaseJson,
			'Asset_Json_Database':self.databaseAssetsJson,
			'Megascans_Json_Database': self.databaseMegascansJson
		}

		## Menu
		self.jsonMenuAction =  os.path.abspath(self.fileDir + "/setup/menuAction.json")
		self.dicMenuAction = self.readJsonInfos(self.jsonMenuAction)

		## Default Shaders Library
		self.initialLibraryShaders = os.path.abspath(self.fileDir + "/installation/Shaders")

		print("\n")
		print(" =================================================================== ")
		print("\n")
		print(" ---- User Infos ---- ")

		###################################### Current Workspace ###########################################
		if os.getenv("DISCIPLINE") == "3ddmp":
			self.discipline = "env"
		elif os.getenv("DISCIPLINE") == "":
			print ("No discipline set, please job in with a discipline")
		else :
			self.discipline = os.getenv("DISCIPLINE")
		
		### Username
		if self.platform == "win32" or self.platform == "win64":
			self.username = os.getenv("USERNAME")
		elif self.platform == "linux2" or self.platform == "linux":
			if pythonVersion == 2:
				self.username = os.getenv("USER")
			elif pythonVersion == 3:
				## Used to be USERNAME
				self.username = os.getenv("USER")
		print("Username: " + str(self.username))

		#### Job/Project
		self.job = os.getenv("JOB")
		self.sequence = os.environ.get("SHOT")
		if self.sequence:
			self.shot = self.sequence.split("/")[-1]
		else:
			self.shot = None

		## Get user folder crossplatform
		self.userFolder = os.path.expanduser("~")

		## set Default Size
		self.sizeSelectedElmt = 1

		## Get Log, Tag and Super user
		self.superUserFilename = "resurepus.json"
		self.tagsJsonFilename = "tags.json"
		if self.platform == "win32" or self.platform == "win64":
			self.pathLogFile = self.libraryPath.replace("/jobs","J:") + "sg_alexandriaLibrary_logs.log"
			self.tagsJsonFile = self.libraryPath.replace("/jobs","J:") + "tags.json"
			# Log Init file
			self.pathLogIniWindows = self.libraryPath.replace("/jobs","J:") + "/logging_win.ini"
			self.pathLogIniLinux = self.libraryPath + "/logging_linux.ini"
			self.pathLogIni = self.pathLogIniWindows
			## Super users 
			self.superUsersJson = self.libraryPath.replace("/jobs","J:") + "resurepus.json"
		if self.platform == "linux2" or self.platform == "linux":
			self.pathLogFile = self.libraryPath + "/sg_alexandriaLibrary_logs.log"
			self.tagsJsonFile = self.libraryPath + "tags.json"
			# Log Init file
			self.pathLogIniWindows = self.libraryPath.replace("/jobs","J:") + "/logging_win.ini"
			self.pathLogIniLinux = self.libraryPath + "/logging_linux.ini"
			self.pathLogIni = self.pathLogIniLinux
			## Super users
			self.superUsersJson = self.libraryPath + "resurepus.json"

		## Megascan ZIP Library Path
		self.main_widget.pushButton_megascansPath.setText(self.megascanZIPLibraryPath)
		self.main_widget.pushButton_megascansPath.setStyleSheet("QPushButton { text-align:left;} ")

		self.initButtonLook()

		####### Log Recorder #########
		# self.logInfos()

		## Search Tab
		self.searchMode= False

		## Sync
		self.sitesMPC = ["bang","london","monw"]
		self.dicSyncFile= {}

		## Temp Folder Path
		if in_maya== True:
			self.pathTempFolder = cmds.internalVar(userTmpDir=True)
			##self.result_available = threading.Event()
		else:
			self.pathTempFolder = os.path.abspath(tempfile.gettempdir())
			##self.pathTempFolder = os.path.abspath(os.getcwd())
			##self.result_available = threading.Event()

		## Set QPixmap Cache in Mb
		QtGui.QPixmapCache.setCacheLimit(40960)

		## Detect event on Qlabel
		self.main_widget.label_sgThumbnail.installEventFilter(self)

		## Drag and Drop
		self.objectsToDrop = []
		self.mouseButtonUsed = ""

		## Init path QTreeView Selection
		self.selectedPath = ["","",""]

		## Files
		self.depth= 0
		self.fileExtension = ""

		## Tags
		self.separator = ","

		####  Check Plugins:
		self.RfM = True
		self.MtoA = True
		if in_maya:
			try:
				self.RfM_version = float(cmds.pluginInfo("RenderMan_for_Maya.py", query=True, version=True)[:4])
			except:
				self.RfM_version = 0.0
				pass
			if not (cmds.pluginInfo("RenderMan_for_Maya.py", query=True, loaded=True)) or self.RfM_version < 22.0:
				print("RfM not available/loaded or unsupported version, the tool support RfM from v22.0, loaded version is: " + str(self.RfM_version))
				self.RfM = False
			if not (cmds.pluginInfo("mtoa.mll", query=True, loaded=True)):
				print("Arnold Render not available")
				self.MtoA = False
			if not (cmds.pluginInfo("fbxmaya.mll", query=True, loaded=True)):
				cmds.loadPlugin("fbxmaya.mll")
			if not (cmds.pluginInfo("AbcImport.mll", query=True, loaded=True)):
				cmds.loadPlugin("AbcImport.mll")
		# Needs a check for all the software
		if in_hou:
			if hou.getenv("RFHTREE") :
				self.RfM = True
				self.RfM_version = float(hou.getenv("RFHTREE").split("-")[-1])
			else:
				self.RfM = False
			self.MtoA = False
		if in_blen:
			self.RfM = True
			self.MtoA = False
		if in_katana:
			self.RfM = True
			self.MtoA = False
		if in_mari:
			self.RfM = True
			self.MtoA = False

		## Sync - will be updated later on by Init
		self.amandaServices = False

		## Unreal - Copy Utility Node for current project
		if in_unreal:
			try:
				pathLibrary = os.path.join(self.shaderLibraryPath.replace("/jobs","J:"),"unreal/megascans/")
				sg_unrealLibraryCommands.copyUnrealShaderLibrary(pathLibrary)
				print("Unreal Initialisation: Done")
			except:
				pass

		self.unrealLOD = self.main_widget.sgUnrealSettings_LOD.itemText(self.main_widget.sgUnrealSettings_LOD.currentIndex())
		self.unrealDisplacement = self.main_widget.checkBox_sgUnrealSettingsDisplacement.isChecked()

		## Nuke - Check if Eddy is available
		self.EddyForNuke = False
		if in_nuke:
			for p in nuke.plugins():
				if "eddy" in p.lower():
					self.EddyForNuke = True
		## MARI -
		self.mariShader = self.main_widget.sgMariSettings_Shader.itemText( self.main_widget.sgMariSettings_Shader.currentIndex())
		self.mariColorspace = self.main_widget.sgMariSettings_ColorSpace.itemText(self.main_widget.sgMariSettings_ColorSpace.currentIndex())
		self.mariHDR = self.main_widget.sgMariSettings_EnvMap.itemText(self.main_widget.sgMariSettings_EnvMap.currentIndex())
		# Find available colorspace close to mpc_lin
		if in_mari:
			self.mariColorspaceAvailable = sg_mariLibraryCommands.allColorSpaces()
			# Find a linear color space if selected one in default setting doesn't exist
			if self.mariColorspace not in self.mariColorspaceAvailable:
				for cs in self.mariColorspaceAvailable:
					if cs.endswith("_lin"):
						self.mariColorspace = cs
						break
			print("ColorSpace to use: " + self.mariColorspace)

		## UI Behaviour
		self.resized = False
		self.resizeEventHappened = False
		self.lazyLoading = False
		self.currentUITab = self.main_widget.libraryTab.currentIndex()
		self.context = ""
		self.subContext = ""
		self.categoryContext = ""

		self.elementBrowserWidth = self.main_widget.tableWidget_sgElementBrowser.width()
		self.elementBrowserHeight = self.main_widget.tableWidget_sgElementBrowser.height()
		self.collectionBrowserWidth = self.main_widget.tableWidget_sgCollectionBrowser.width()

		self.collectionSelection = ""
		self.picturePath = ""
		self.collectionPicture = ""

		self.allSearchTags = []

		self.selectedIconName = ""

		## Time Limit to consider a Directory New in days
		self.freshTimeLimit = 5

		## UI Color
		self.itemBGFreshColor = QtGui.QColor(80,130,80,180)
		self.itemBGDefaultColor = QtGui.QColor(0,0,0,0)

		self.fontFreshDirectoryColor = QtGui.QColor(80,130,80,255)
		self.fontNormalDirectoryColor = QtGui.QColor(255,255,255,255)

		## Find Screen Resolution
		self.screenWidth =0
		if in_katana:
			self.amountScreen = QtGui.QGuiApplication.screens()
			for screen in self.amountScreen:
				self.screenWidth +=QtGui.QScreen.availableGeometry(screen).width()
		else:
			self.amountScreen = QtWidgets.QDesktopWidget().numScreens()
			for screen in range(self.amountScreen):
				self.screenWidth += QtWidgets.QDesktopWidget().screenGeometry(screen).width()
			# self.screenWidth = QtWidgets.QDesktopWidget().screenGeometry(-1).width()
			# print(self.screenWidth)

		## FBX Import Settings
		if in_maya == True:
			mm.eval('FBXImportMode -v add')

		## Mari temp fix - Needs to have a job
		print("Jobbed in: " + str(self.job))
		print("Sequence: " + str(self.sequence))
		if self.job == None:
			self.job = "clfviz"

		####### New Entry Texture Init #######
		self.rbNewTextureEntryType = "radioButton_sgUniqueEntryText"
		self.rbNewDMPEntryType = "radioButton_sgDMPCopyImgs"
		self.rbNewATBEntryType = "radioButton_sgABTCopyImgs"

		## Restraint Function access to Super User
		self.superUserAccess()

		## Default Picture
		self.pictureDefaultPath = self.libraryPath+ "missing.png"

		## Json file Extension
		self.jsonInfoFileExtension = "_infos.json"
		self.jsonDMPLinkExtension = "_dmpLink.json"

		## Thumbnail
		self.thumbnailSuffix = "_Preview"

		## Depth of Folder to look into for adding element ot Library
		self.pathDepthReference= 0
		self.pathDepthReferenceModel = len(self.modelLibraryPath.split("/"))+1
		self.pathDepthReferenceShader = len(self.shaderLibraryPath.split("/"))+2

		# Megascan Thumbnail Resize Max
		self.megascansThumbnailResolution = 512

		## Variables fo Zoom Widget
		self.zoomSize = (384,384)
		self.resolutionThumbnail = 256

		## Number of Column in Items
		self.maxColumnModels= 4
		self.iconAmount =0
		self.amountOfRows = 0

		## Megascans
		if os.path.exists(self.megascanZIPLibraryPath):
			self.listAllMegascansZip =[]
			for file in os.listdir(self.megascanZIPLibraryPath):
				if file.endswith(".zip"):
					self.listAllMegascansZip.append(file)
			self.sizeMegascansLibrary = len(self.listAllMegascansZip)
		else:
			self.sizeMegascansLibrary = 50

		self.listErrorZip = ""

		self.textProgressUnzip = "Unzip Megascans"
		self.textProgressCopyTextures = "Copy Textures"

		########################### Files Type ########################################

		self.list3dFormat = ["abc","fbx","obj"]
		self.listExtraFormat = ["ztl","brush"]
		self.listImagesFormat = ["jpg","exr"] #Removed upper case format as I test in lowercase
		self.listImagefileExtension = ["jpg","tif","exr","png","hdr"]
		self.listdmpImagefileExtension = ["jpg","tif","exr","png","hdr","cr2","crw","nef","arw"]
		self.listRawImagesFormat = ["cr2","crw","nef","arw"]
		self.listHdrImagesFormat = ["exr","hdr"]
		self.thumbnailsfileExtension = ["jpg","png","gif"]
		self.listMariChannels = ["Albedo","Normal","Roughness","Specular","Cavity","Displacement","AO","Translucency"]
		self.listMegascansComponents = ["Albedo","Normal","Roughness","Specular","Cavity","Displacement","AO","Translucency","Opacity","Curvature","Fuzz","Transmission"]
		self.listRendermanLights = ['PxrEnvDayLight','PxrMeshLight','PxrSphereLight',"PxrDomeLight","PxrRectLight","PxrDistantLight","PxrDiskLight","PxrCylinderLight","PxrPortalLight","PxrAovLight","PxrBlockerLightFilter","PxrBarnLightFilter"]
		self.listArnoldLights = ['aiSkyDomeLight','aiAreaLight','aiPhotometricLight',"aiLightPortal","ambientLight","directionalLight","pointLight","spotLight","areaLight","volumeLight","aiPhysicalSky"]
		self.listMayaLights = ['aiSkyDomeLight','aiAreaLight','aiPhotometricLight',"aiLightPortal","ambientLight","directionalLight","pointLight","spotLight","areaLight","volumeLight","aiPhysicalSky"]
		
		self.defaultOCIO = ["sRGB","linear","AcesCG",""]

		self.dicSquareResolution = {"1K":"1024x1024","2K":"2048x2048","4K":"4096x4096","8K":"8192x8192"}

		## Button UI
		self.sharedUV =  self.main_widget.checkBox_sgTextureSharedUV.isChecked()
		self.triplanar =  self.main_widget.checkBox_sgTextureTriplanar.isChecked()
		self.shaderLama = self.main_widget.checkBox_sgShaderLama.isChecked()

		## Progrees Bar
		global progress
		self.progress = 0.00

		## UI Messages
		self.pbLoadingTextMegascans= "Loading Megascans Library:"
		self.pbCopyingFile= "Copying Files: "
		self.pbConvertingToPNG= "Converting Image(s): "
		self.pbCreatingContactsheet= "Creating Contactsheet: "
		self.pbLoadingTextExtract= "Extracting: "
		self.pbLoadingTextImport= "Importing: "
		self.pbTaskDone= " DONE "

		self.uiMessageEntryOverwriten = "- Entry Overwritten Successfully -"
		self.uiMessageOperationCancelled = 'Operation Cancelled by User'

		## Add Entry Tab
		self.nameNewEntry = self.main_widget.lineEdit_sgNameEntry.text()
		self.folderNewIES = ""
		self.iesFileNewEntry = ""
		self.iconIESNewEntry = ""

		## Snapshot Settings, hidding those huds
		self.hideUI = ['manipulators', 'grid', 'hud']

		## start time 
		self.libraryStartTime = time.time()
		self.getMTimeDatabase()
		print("Library Opened: " + str(datetime.fromtimestamp(self.libraryStartTime)))

		print("\n")

########################################################### Init ######################################################

	def printMessage(self):
		print("MESSAGE HERE!")

	def initPathsLibrary(self):
		nameDefaultLibraries=[]
		nameDeletableLibraries = []
		self.main_widget.comboBox_sgDefaultLibrary.clear()
		# Load User Settings
		with open(self.defaulPathJson) as jfile:
			self.dataPathDefaultLibraries = json.load(jfile)

		for key in self.dataPathDefaultLibraries:
			if key != "Generalist Library":
				nameDeletableLibraries.append(key)
			nameDefaultLibraries.append(key)

		nameDefaultLibraries.sort()
		nameDeletableLibraries.sort()

		self.main_widget.comboBox_sgDefaultLibrary.addItems(nameDefaultLibraries)
		self.main_widget.comboBox_sgDeleteLibrary.addItems(nameDeletableLibraries)
		# Load User Preferences
		self.userPreferencesRead()
		## Main Library is picked and variables initialise here
		self.setDefaultPath()
		self.initWorkspacePath()

		# check Sync
		self.initMegascansSync(self.megascansAutoSync)

	def initSearchCompleter(self):
		self.completerModel = QtCore.QStringListModel()
		if os.path.exists(self.tagsJsonFile):
			with open(self.tagsJsonFile) as standardTagsJsonFile:
				self.standardTags = json.load(standardTagsJsonFile)

		else:
			self.standardTags = ["concrete","plant","blue"]
			# Write file is doesn't exist
			self.writeJsonFile(self.tagsJsonFile,self.standardTags)

		self.setToolTipTagsUI()

		self.completerModel.setStringList(self.standardTags)
		self.uiCompleter= QtWidgets.QCompleter()
		self.uiCompleter.setModel(self.completerModel)

		self.main_widget.lineEdit_sgPergamonLibrary_search.setCompleter(self.uiCompleter)

	def initWorkspacePath(self):
		### Set Working Path
		updateZipPath = False
		if self.pathUnzipFolder != "" and os.path.exists(self.pathUnzipFolder):
			print("Keep UI entry for the unzip folder")
		else:
			updateZipPath = True
		try:
			if self.platform == "win32" or self.platform == "win64":
				if in_maya:
					self.pathWorkspaceFolder = cmds.workspace(q=True, rd=True)
					self.pathSceneFolder = self.pathWorkspaceFolder+"scenes/"
					if updateZipPath:
						self.pathUnzipFolder = self.pathWorkspaceFolder+"scenes/"
				elif in_hou:
					self.pathWorkspaceFolder = os.environ["HIP"]+"/"
					self.pathSceneFolder = self.pathWorkspaceFolder
					if updateZipPath:
						self.pathUnzipFolder = self.pathWorkspaceFolder+ "library/"
				elif in_katana:
					self.pathWorkspaceFolder = os.environ["HOMEPATH"]+"/"
					self.pathSceneFolder = self.pathWorkspaceFolder
					if updateZipPath:
						self.pathUnzipFolder = self.pathWorkspaceFolder+ "library/"
				elif in_nuke:
					self.pathWorkspaceFolder = os.environ['NUKE_TEMP_DIR']
					self.pathSceneFolder = self.pathWorkspaceFolder+"scenes/"
					if updateZipPath:
						self.pathUnzipFolder = self.pathWorkspaceFolder+"scenes/library/"
				elif in_mari:
					self.pathWorkspaceFolder = mari.projects.cachePath()
					self.pathSceneFolder = self.pathWorkspaceFolder+"library/"
					if updateZipPath:
						self.pathUnzipFolder = self.pathWorkspaceFolder+"library/"
				elif in_unreal:
					self.pathWorkspaceFolder = sg_unrealLibraryCommands.getAbsoluteProjectDir()
					self.pathSceneFolder = self.pathWorkspaceFolder+"library/"
					if updateZipPath:
						self.pathUnzipFolder = self.pathWorkspaceFolder+"library/"
				else:
					self.pathWorkspaceFolder = os.environ['NUKE_TEMP_DIR']
					self.pathSceneFolder = self.pathWorkspaceFolder+"scenes/"
					if updateZipPath:
						self.pathUnzipFolder = self.pathWorkspaceFolder+"scenes/library/"

			elif self.platform == "linux2" or self.platform == "linux":
				self.pathWorkspaceFolder = os.getenv("__ION_PASSENV_MAYA_PROJECT")
				self.pathSceneFolder = self.pathWorkspaceFolder+"/scenes/"+ self.discipline+"/"+self.username+"/"
				if updateZipPath:
					self.pathUnzipFolder = "/jobs/"+ self.job+ "/docs/library/"
		except:
			print(sys.exc_info())
			# MPC safe folder
			self.pathWorkspaceFolder = os.getcwd()
			self.pathSceneFolder = "/jobs/"+ self.job +"/docs/library/"
			if updateZipPath:
				self.pathUnzipFolder = "/jobs/"+ self.job+"/docs/library/"

		print("Workspace is : " + self.pathWorkspaceFolder)
		print("Scene will be saved in : " + self.pathSceneFolder)
		print("Megascans will be unzipped in: " + self.pathUnzipFolder)

	def initButtonLook(self):
		## Set Button Tool UI
		self.main_widget.button_sgPathLibrary.setText(self.libraryPath)
		self.main_widget.button_sgPathLibrary.setStyleSheet("QPushButton { text-align:left;} ")
		self.main_widget.pushButton_sgSuperUserFile.setText(self.superUsersJson)
		self.main_widget.pushButton_sgSuperUserFile.setStyleSheet("QPushButton { text-align:left;} ")
		self.main_widget.pushButton_sgTagFile.setText(self.tagsJsonFile)
		self.main_widget.pushButton_sgTagFile.setStyleSheet("QPushButton { text-align:left;} ")
		self.main_widget.pushButton_sgLogPath.setText(self.pathLogFile)
		self.main_widget.pushButton_sgLogPath.setStyleSheet("QPushButton { text-align:left;} ")
		self.main_widget.pushButton_sgUserPrefPath.setText(os.path.join(self.userPreferenceFolder,self.userPrefJson))
		self.main_widget.pushButton_sgUserPrefPath.setStyleSheet("QPushButton { text-align:left;} ")
		self.main_widget.pushButton_sgPathSetup.setText(self.defaulPathJson)
		self.main_widget.pushButton_sgPathSetup.setStyleSheet("QPushButton { text-align:left;} ")
		self.main_widget.pushButton_sgViewGlobalDatabase.setText(self.databaseJson)
		self.main_widget.pushButton_sgViewGlobalDatabase.setStyleSheet("QPushButton { text-align:left;} ")
		self.main_widget.pushButton_sgViewAssetDatabase.setText(self.databaseAssetsJson )
		self.main_widget.pushButton_sgViewAssetDatabase.setStyleSheet("QPushButton { text-align:left;} ")
		self.main_widget.pushButton_sgViewMegascansDatabase.setText(self.databaseMegascansJson )
		self.main_widget.pushButton_sgViewMegascansDatabase.setStyleSheet("QPushButton { text-align:left;} ")

		self.main_widget.label_sgPreviewInfo_name__.setStyleSheet('color: grey')
		self.main_widget.label_sgPreviewInfo_version__.setStyleSheet('color: grey')
		self.main_widget.label_sgPreviewInfo_author__.setStyleSheet('color: grey')
		self.main_widget.label_sgPreviewInfo_available__.setStyleSheet('color: grey')
		self.main_widget.label_sgPreviewInfo_ocio__.setStyleSheet('color: grey')
		self.main_widget.label_sgPreviewInfo_metadata__.setStyleSheet('color: grey')
		self.main_widget.label_sgPreviewInfo_notes__.setStyleSheet('color: grey')

		## Add Icons to the UI
		iconPathBCT = os.path.abspath(self.fileDir+ '/../sg_batchTextureConvert/icon/sg_batchConvertIcon_64.png')
		iconPathConvertBook = os.path.abspath(self.fileDir+ '/../sg_convertToBook/icons/sg_convertToBook_icon64.png')
		self.iconPathDefaultArtBooks = os.path.abspath(self.fileDir+ '/icons/defaultArtBooks.png')
		self.iconPathDefaultTutorials = os.path.abspath(self.fileDir+ '/icons/defaultTutorials.png')
		iconPathTriplanarOn = os.path.abspath(self.fileDir+ '/icons/sg_triplanar_On_icon64.png')
		iconPathTriplanarOff = os.path.abspath(self.fileDir+ '/icons/sg_triplanar_Off_icon64.png')
		iconPathSharedUVOn = os.path.abspath(self.fileDir+ '/icons/sg_sharedUV_On_icon64.png')
		iconPathSharedUVOff = os.path.abspath(self.fileDir+ '/icons/sg_sharedUV_Off_icon64.png')
		#iconPathShaderLamaOn = os.path.abspath(self.fileDir+ '/icons/sg_PLLama_On_icon128.png')
		iconPathShaderLamaOn = os.path.abspath(self.fileDir+ '/icons/sg_PLLama02_On_icon128.png')
		#iconPathShaderLamaOff = os.path.abspath(self.fileDir+ '/icons/sg_PLLama_Off_icon128.png')
		iconPathShaderLamaOff = os.path.abspath(self.fileDir+ '/icons/sg_PLLama02_Off_icon128.png')
		iconPathInfos = os.path.abspath(self.fileDir+ '/icons/sg_infosIcon_icon128.png')
		iconPathLock = os.path.abspath(self.fileDir+ '/icons/sg_lock_icon128.png')
		iconPathUnlock = os.path.abspath(self.fileDir+ '/icons/sg_unlock_icon128.png')

		iconPathMegascanSettings = os.path.abspath(self.fileDir+ '/icons/sg_megascansSettings.png')

		## Button Icons
		self.iconNewIES = self.createNewIcon()
		self.iconNewEmtpyIES = self.createNewIcon()

		self.iconDefaultArtbooks = self.createNewIcon()
		self.iconDefaultTutorials = self.createNewIcon()
		self.iconDefaultArtbooks.addPixmap(QtGui.QPixmap(self.iconPathDefaultArtBooks), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.iconDefaultTutorials.addPixmap(QtGui.QPixmap(self.iconPathDefaultTutorials), QtGui.QIcon.Normal, QtGui.QIcon.Off)

		iconBCT = self.createNewIcon()
		iconBCT.addPixmap(QtGui.QPixmap(iconPathBCT), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.main_widget.pushButton_sgConvertBatch.setIcon(iconBCT)
		self.main_widget.pushButton_sgConvertBatch.setIconSize(QtCore.QSize(32, 32))

		iconConvertBook = self.createNewIcon()
		iconConvertBook.addPixmap(QtGui.QPixmap(iconPathConvertBook), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.main_widget.pushButton_sgConvertBook.setIcon(iconConvertBook)
		self.main_widget.pushButton_sgConvertBook.setIconSize(QtCore.QSize(44, 44))

		self.iconSharedUVon = self.createNewIcon()
		self.iconSharedUVon.addPixmap(QtGui.QPixmap(iconPathSharedUVOn), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.iconSharedUVOff = self.createNewIcon()
		self.iconSharedUVOff.addPixmap(QtGui.QPixmap(iconPathSharedUVOff), QtGui.QIcon.Normal, QtGui.QIcon.Off)

		iconInfo = self.createNewIcon()
		iconInfo.addPixmap(QtGui.QPixmap(iconPathInfos), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.main_widget.pb_iconInfos08.setIcon(iconInfo)
		self.main_widget.pb_iconInfos08.setIconSize(QtCore.QSize(20, 20))

		self.iconTriplanarOn = self.createNewIcon()
		self.iconTriplanarOn.addPixmap(QtGui.QPixmap(iconPathTriplanarOn), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.iconTriplanarOff = self.createNewIcon()
		self.iconTriplanarOff.addPixmap(QtGui.QPixmap(iconPathTriplanarOff), QtGui.QIcon.Normal, QtGui.QIcon.Off)

		self.iconShaderLamaOn = self.createNewIcon()
		self.iconShaderLamaOn.addPixmap(QtGui.QPixmap(iconPathShaderLamaOn), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.iconShaderLamaOff = self.createNewIcon()
		self.iconShaderLamaOff.addPixmap(QtGui.QPixmap(iconPathShaderLamaOff), QtGui.QIcon.Normal, QtGui.QIcon.Off)

		self.iconDMPContactsheet01 = self.createNewIcon()
		self.iconDMPContactsheet02 = self.createNewIcon()
		self.iconDMPContactsheet03 = self.createNewIcon()
		self.iconDMPContactsheet04 = self.createNewIcon()
		self.listDMPContactsheetImg = ["","","",""]

		self.iconLock = self.createNewIcon()
		self.iconLock.addPixmap(QtGui.QPixmap(iconPathLock), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.iconUnlock = self.createNewIcon()
		self.iconUnlock.addPixmap(QtGui.QPixmap(iconPathUnlock), QtGui.QIcon.Normal, QtGui.QIcon.Off)

		#iconMegascanSettings = self.createNewIcon()
		#iconMegascanSettings.addPixmap(QtGui.QPixmap(iconPathMegascanSettings), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		pixmapMegascanSettings = QtGui.QPixmap(iconPathMegascanSettings).scaled(610, 610, QtCore.Qt.KeepAspectRatio,QtCore.Qt.SmoothTransformation)
		self.main_widget.label_sgMegascansSettings.setPixmap(pixmapMegascanSettings)
		self.main_widget.label_sgMegascansSettings.setAlignment(QtCore.Qt.AlignTop)

#######################################################################################################################
#################################################### Init Megascans ###################################################
#######################################################################################################################
 	
	def initBuildingMegascansLibrary(self):
		if os.path.exists(self.megascanZIPLibraryPath):
			## Launch Progress Bar
			self.pb = sgProgressBarLibrary()
			self.pb.show()

			##self.buildMegascansLibrary()
			if self.platform == "win32" or self.platform == "win64":
				listNewZip= self.buildMegascansLibrary()
				## Threading and Loading bar
				##self.my_threads = []
				##thread = threading.Thread(target=self.buildMegascansLibrary)
				##thread.start()
				##self.my_threads.append(thread)
			elif self.platform == "linux2" or self.platform == "linux":
				listNewZip = self.buildMegascansLibrary()

			## Sync Data to the main facilities
			if self.amandaServices == True:
				self.syncUpdate(listNewZip)

			## Finish Progress Bar
			## UI Progress Bar
			self.progress = 100.00
			self.pb.setValue(self.progress,self.pbLoadingTextMegascans)
			self.pb.finishBar(timeFade = 0.1)
		else:
			if in_maya:
				cmds.inViewMessage( amg="The Megascans Library path doesn't exist: " + self.megascanZIPLibraryPath, pos='botCenter', fade=True, fadeOutTime=500)
			print("The Megascans Library path doesn't exist: " + self.megascanZIPLibraryPath)

	def extractingZip(self,action):
		self.usedRenderer =  action
		self.queryPreferences()

		if in_maya:
			cmds.waitCursor( state=True )
			LodConfirm = maya.utils.executeInMainThreadWithResult(self.unzipMegascan)
			if LodConfirm != "Cancel" and self.usedRenderer != "mayaDrop":
				if self.usedRenderer != "unzip":
					maya.utils.executeInMainThreadWithResult(self.loadMegascans)
			else:
				cmds.inViewMessage( amg="LODs Choice Cancel by user", pos='botCenter', fade=True, fadeOutTime=500)
			# maya.utils.executeDeferred(self.loadMegascans)
			cmds.waitCursor( state = False )
		else:
			self.unzipMegascan()
			if self.usedRenderer != "unzip":
				self.loadMegascans()

	def buildMegascansLibrary(self):
		## That process, load the json file with all the megascans data, compare to the folder and
		## If difference will rebuild the entire "database"/json file
		## It simplifies the removal of elements but slow down the process when new zip are added
		print( "\n")
		print( " ---- Checking Megascans Library ---- ")
		try:
			logger.info(" ---- Checking Megascans Library ---- ")
		except:
			pass
		## UI
		self.progress = 0.0000
		if self.sizeMegascansLibrary != 0:
			percentage =  100.0000/(self.sizeMegascansLibrary*2)
		else:
			percentage = 100.0000

		## Load Meagascan Overal Json File
		self.listErrorZip = []
		listDuplicateZip = []
		listNewZip = []
		listFullNewZip=[]

		# Find only zip files
		listDatabaseZip = []
		for key in self.dicMegascansZip:
			listDatabaseZip.append(self.dicMegascansZip[key][0]["zipFile"].split("/")[-1])
			if ".zip" in key:
				print("Potential error in database:",key)

		## Compare the size of the database with the folder
		if self.sizeMegascansLibrary == len(self.dicMegascansZip.keys()):
			print( "No new Megascans detected in the library")
			print("There are " + str(len(self.dicMegascansZip.keys())) + " Megascans in the library")
			print("\n")
			if in_maya:
				cmds.inViewMessage( amg='There are ' +  str(self.sizeMegascansLibrary) + " elements in the Megascans library", pos='botCenter', fade=True, fadeOutTime=500)

		else:
			print(" - New entry found  - ")
			print("There are " + str(self.sizeMegascansLibrary) + " elements in the Megascans library")
			print("There are " + str(len(self.dicMegascansZip.keys())) + " elements in the Json database")
			try:
				logger.info("There are %s Megascans in the library",str(self.sizeMegascansLibrary))
			except:
				pass
			tempAList=[]
			tempBList=[]

			if in_maya:
				cmds.inViewMessage( amg='There are ' +  str(self.sizeMegascansLibrary) + " Megascans in the library", pos='botCenter', fade=True, fadeOutTime=500)

			temSizeList = []
			listSubFoldersToCreate=[]
			listMainFoldersToCreate=[]

			# Calculate Time Process
			startProcess = time.time()
			print("Adding New Entry to Megascans Library, now: " +  str(self.sizeMegascansLibrary) + " elements"+  "\n")

			self.listNewZip = list(set(self.listAllMegascansZip)-set(listDatabaseZip))
			self.listNewZip.sort()
			print("New Zip Discovered: ", self.listNewZip)

			if os.path.exists(self.megascanZIPLibraryPath):
					## Folder Creation
					for megaZip in sorted(self.listNewZip):
					# if megaZip not in self.dicMegascansZip.keys():
						try:
							subCategoryFolder = megaZip.split("_")[0]
							typeFolder = megaZip.split("_")[-2]
							tempAList.append(subCategoryFolder)
							tempBList.append(typeFolder)
							if not subCategoryFolder in tempAList:
								listSubFoldersToCreate.append(subCategoryFolder)
							if not typeFolder in tempBList:
								listMainFoldersToCreate.append(typeFolder)
						except:
							print("Probably not a megascan zip: " + megaZip)
							pass

					##Create Categories and SubCategories
					startFolderProcess = time.time()
					for mainFolder in listMainFoldersToCreate:
						if not os.path.exists(self.megascanLibraryPath+mainFolder):
							self.createNewFolder(self.megascanLibraryPath+mainFolder)
						for subfolder in listSubFoldersToCreate:
							if not os.path.exists(self.megascanLibraryPath+mainFolder+"/"+folder):
								self.createNewFolder(self.megascanLibraryPath+mainFolder+"/"+folder)
					endFolderProcess = time.time()

					## Extract Preview and json
					startZipProcess = time.time()
					for megascanZip in self.listNewZip:
						jsonZip = ""
						error = False
						iconZip = megascanZip
						zipFile = self.megascanZIPLibraryPath+ megascanZip
						modifiedTime = os.path.getmtime(self.megascanZIPLibraryPath+megascanZip)
						nameFile = megascanZip.split(".")[0]
						subType =  megascanZip.split(".")[0].split("_")[-2]
						if subType == "3dplant":
								subType ="3d"
						category =  megascanZip.split(".")[0].split("_")[0]
						typeAsset =  "Megascans"
						refPath = typeAsset+ "/" + subType + "/" + category
						resolutionZip = megascanZip.split("_")[-3]
						listLODs=[]
						listExtensionfiles = []
						list2Dfiles = []
						listExtrafiles = []

						if "surface" in megascanZip:
								self.extraMegascansPath = "surface/"
						elif "atlas" in megascanZip:
								self.extraMegascansPath = "atlas/"
						elif "3d" in megascanZip:
								self.extraMegascansPath = "3d/"
						elif "_brush" in megascanZip:
								self.extraMegascansPath = "brush/"

						try:
							## Read zip
							z= zipfile.ZipFile(self.megascanZIPLibraryPath+megascanZip, "r")
							for file in z.namelist():
								fileExtension= file.split("_")[-1].split(".")[1].lower()
								## Extract Preview
								if "Preview" in file:
									zipFile = self.megascanZIPLibraryPath+ megascanZip
									iconZip = file.replace(" ", "" )
									if not os.path.exists(self.megascanLibraryPath+self.extraMegascansPath+iconZip.split("_")[0]+"/"+iconZip):
										z.extract(file, self.megascanLibraryPath+self.extraMegascansPath+iconZip.split("_")[0]+"/")
										print("Adding New Element: " + iconZip )
										listNewZip.append(megascanZip)
										listFullNewZip.append(zipFile)
										## Resize thumbnail to speed up loading
										self.resizeThumbnailMegascans(self.megascanLibraryPath+self.extraMegascansPath+iconZip.split("_")[0]+"/"+file)
									if " " in file:
										if os.path.isfile(self.megascanLibraryPath+self.extraMegascansPath+iconZip.split("_")[0]+"/"+file):
											os.rename(self.megascanLibraryPath+self.extraMegascansPath+iconZip.split("_")[0]+"/"+file, self.megascanLibraryPath+self.extraMegascansPath+iconZip.split("_")[0]+"/"+iconZip )
											print("Renaming: " + self.megascanLibraryPath+self.extraMegascansPath+iconZip.split("_")[0]+"/"+file + " as " + self.megascanLibraryPath+self.extraMegascansPath+iconZip.split("_")[0]+"/"+iconZip )
								## Find and Extract Json / ISSUE with space in preview file name
								elif "json" in file:
									outpath = self.megascanLibraryPath+self.extraMegascansPath+megascanZip.split("_")[0]+"/"
									jsonZip = file
									if not os.path.exists(outpath+file):
										z.extract(file, outpath)
								## CG to add
								elif "fbx" in file.lower() or "obj" in file.lower() or "abc" in file.lower():
									lod = file.split("_")[-1].split(".")[0]
									if lod not in listLODs :
										listLODs.append(lod)
									if fileExtension not in listExtensionfiles :
										listExtensionfiles.append(fileExtension.lower())
								## Textures to add
								elif fileExtension.lower() in self.listImagesFormat:
									list2Dfiles.append(file)
									if fileExtension not in listExtensionfiles :
										listExtensionfiles.append(fileExtension.lower())
								## Extra to add
								elif fileExtension in self.listExtraFormat:
									listExtrafiles.append(file)
									if fileExtension not in listExtensionfiles :
										listExtensionfiles.append(fileExtension.lower())
						except :
							print(sys.exc_info())
							print(traceback.format_exc())
							self.listErrorZip.append(megascanZip)
							error = True
							pass
						## Close Zip File
						try:
							z.close()
						except:
							pass

						## Read json for tags
						if jsonZip != "":
							tagsStr = ""
							try:
								assetInfo = self.readJsonInfos(self.libraryPath + refPath + "/" + jsonZip)
								# print( " Reading json: " + self.libraryPath + refPath + "/" + jsonZip)
							
							except UnicodeDecodeError:
								#print(traceback.format_exc())
								#print("Potentially Weird characters in the file")
								assetInfo = {}
								self.listErrorZip.append(megascanZip)
								pass

							except:
								print(sys.exc_info())
								print(traceback.format_exc())
								assetInfo = {}
								self.listErrorZip.append(megascanZip)
								error = True
								pass

							if assetInfo:
								tagsStr = self.findTagsInMegascansJson(assetInfo)
							else:
								print("The json file associated with the zip is empty/corrupted - Will proceed, but you may need to check it manually")
							tags = tagsStr.split(",")
						else:
							tags = ""

						## Add to Dictionnary
						if error != True:
							if not iconZip in self.dicMegascansZip.keys() :
								self.dicMegascansZip[iconZip]= []
								self.dicMegascansZip[iconZip].append({
								'name':nameFile,
								'icon':iconZip,
								'timeEntry':modifiedTime,
								'resolution':resolutionZip,
								'refPath':refPath,
								'zipFile':zipFile,
								'json':jsonZip,
								'lods':listLODs,
								'extension':listExtensionfiles,
								'extraFiles' :listExtrafiles,
								'textures': list2Dfiles,
								'files':[],
								'tags':tags,
								'type':typeAsset,
								'subType': subType,
								'category': category
								})
								
							else:
								## Treat duplicate = Rough
								dicZip = self.dicMegascansZip[iconZip][0]["zipFile"]
								resolutionDicZip = dicZip.split("_")[-3]
								resolutionNewZip = megascanZip.split("_")[-3]
								if resolutionNewZip > resolutionDicZip or len(resolutionNewZip)>len(resolutionDicZip):
									print(megascanZip +  " has higher resolution than: " + dicZip.split("/")[-1] + " -Updating dictionary." + " -Deleting: " + dicZip)
									listDuplicateZip.append(dicZip.split("/")[-1])
									# Update Dictionary but assume some files are identic
									self.dicMegascansZip[iconZip][0]["zipFile"] = self.megascanZIPLibraryPath + megascanZip
									self.dicMegascansZip[iconZip][0]["name"] = megascanZip.split(".")[0]
									self.dicMegascansZip[iconZip][0]["resolution"] = resolutionNewZip
									try:
										os.remove( dicZip )
									except:
										print(" ### Can't remove from disc: " + dicZip)
								elif resolutionNewZip < resolutionDicZip or len(resolutionNewZip) < len(resolutionDicZip):
									print(megascanZip + " has smaller resolution than: " + dicZip.split("/")[-1] + " -Deleting: " + self.megascanLibraryPath + megascanZip)
									listDuplicateZip.append(megascanZip)
									try:
										os.remove(self.megascanZIPLibraryPath + megascanZip)
									except:
										print("### Can't remove from disc: " + self.megascanLibraryPath + megascanZip)
								else:
									print(megascanZip + " and " + dicZip.split("/")[-1] + " have the same resolution. Keep both duplicate, let the user choose")
									listDuplicateZip.append(megascanZip)

						## UI Progress Bar
						self.progress += percentage
						self.pb.setValue(self.progress,self.pbLoadingTextMegascans)

					## Save Megascan Database as a jsonfile
					startWriteJsonProcess = time.time()
					with open(self.databaseMegascansJson,'w') as outJson:
						json.dump(self.dicMegascansZip,outJson,indent = 4)

			## Database
			if len(self.dicAssetDatabase) == 0:
				 fcn.buildDatabase(self.jsonInfoFileExtension,self.databaseJson,self.dicAllDatabase,self.databaseAssetsJson,self.dicAssetDatabase,self.dicMegascansZip,self.libraryPath,self.artBookLibraryPath,self.collectionLibraryPath,self.iesLibraryPath,self.modelLibraryPath,self.lightrigLibraryPath,self.metaHumanLibraryPath,self.dmpLibraryPath,self.textureLibraryPath,self.shaderLibraryPath,self.vdbLibraryPath)
			else:
				self.dicAllDatabase = fcn.mergeDictionaries(self.dicAssetDatabase,self.dicMegascansZip)
				self.writeJsonFile(self.databaseJson,self.dicAllDatabase)

				## Time
				endProcess = time.time()

				## Refresh UI
				self.main_widget.treeWidget_sgLibrary.clear()
				self.libraryFolderStructure(self.libraryPath,self.main_widget.treeWidget_sgLibrary)
				
				print("\n")
				print("Megascans Added: " + str(len(listNewZip)) +"\n" + '\n'.join("- " + str(p) for p in sorted(listNewZip)))
				print("\n")
				print("Megascans Duplicated: "+"\n" + '\n'.join("- " + str(p) for p in sorted(listDuplicateZip)))
				print("\n")
				print("Megascans Errored: "+"\n" + '\n'.join("- " + str(p) for p in sorted(self.listErrorZip)))
				print("\n")
				print("Time Zip Processing Elapsed: " + str(timedelta(seconds=endProcess - startZipProcess)) )
				print("Time Folder Processing Elapsed: " + str(timedelta(seconds=endFolderProcess - startFolderProcess)) )
				print("Time Writing Json File Elapsed: " + str(timedelta(seconds=endProcess - startWriteJsonProcess)) )
				print("Time Total Elapsed: " + str(timedelta(seconds=endProcess - startProcess)) )
				print("\n")

		print(" ---- Refreshing UI ---- " + "\n")
		print("\n")
		print(" =================================================================== ")
		return listFullNewZip

##################################################### Super Users #####################################################

	def writeSuperUserBackup(self):
		# Write Super Users List
		superUserDic = {
		"superUsers" : [self.username]
		}
		self.writeJsonFile(self.superUsersJson,superUserDic)

	def superUserAccess(self):
		# Read List Super Users
		self.superUsersDic = self.readJsonInfos(self.superUsersJson)
		self.listSuperUsers = self.superUsersDic["superUsers"]
		#self.listSuperUsers = ["sebastien-g"]
			
		## Check for user privilege
		if self.username not in self.listSuperUsers:
			self.main_widget.libraryTab.setTabEnabled(2,False)
			self.main_widget.libraryTab.setTabEnabled(3,False)

		# Update ToolTip
		self.setToolTipSuperUserUI()

	def isSuperUser(self,user):
		if user in self.listSuperUsers:
			return True
		else:
			return False

################################################### UI Browser Tab ####################################################

	def buttonUVShare(self):
		self.sharedUV = self.main_widget.checkBox_sgTextureSharedUV.isChecked()

		if self.sharedUV:
			self.main_widget.checkBox_sgTextureSharedUV.setIcon(self.iconSharedUVon)
			self.main_widget.checkBox_sgTextureSharedUV.setIconSize(QtCore.QSize(30, 30))
			self.main_widget.checkBox_sgTextureSharedUV.setToolTip( "Manifold/2D Placements are shared between textures" )
		else:
			self.main_widget.checkBox_sgTextureSharedUV.setIcon(self.iconSharedUVOff)
			self.main_widget.checkBox_sgTextureSharedUV.setIconSize(QtCore.QSize(30, 30))
			self.main_widget.checkBox_sgTextureSharedUV.setToolTip( "Manifold/2D Placement are unique to each texture" )

	def buttonTriplanar(self):
		self.triplanar = self.main_widget.checkBox_sgTextureTriplanar.isChecked()

		if self.triplanar:
			self.main_widget.checkBox_sgTextureTriplanar.setIcon(self.iconTriplanarOn)
			self.main_widget.checkBox_sgTextureTriplanar.setIconSize(QtCore.QSize(30, 30))
			self.main_widget.checkBox_sgTextureTriplanar.setToolTip( "Create Projection/Tri-Planar Setup" )
		else:
			self.main_widget.checkBox_sgTextureTriplanar.setIcon(self.iconTriplanarOff)
			self.main_widget.checkBox_sgTextureTriplanar.setIconSize(QtCore.QSize(30, 30))
			self.main_widget.checkBox_sgTextureTriplanar.setToolTip( "Create UV Texture Nodes" )

	def buttonLamaShader(self):
		self.shaderLama = self.main_widget.checkBox_sgShaderLama.isChecked()

		if self.shaderLama:
			self.main_widget.checkBox_sgShaderLama.setIcon(self.iconShaderLamaOn)
			self.main_widget.checkBox_sgShaderLama.setIconSize(QtCore.QSize(45, 45))
			self.main_widget.checkBox_sgShaderLama.setToolTip( "Use Lama Shader with Prman" )
		else:
			self.main_widget.checkBox_sgShaderLama.setIcon(self.iconShaderLamaOff)
			self.main_widget.checkBox_sgShaderLama.setIconSize(QtCore.QSize(45, 45))
			self.main_widget.checkBox_sgShaderLama.setToolTip( "Use PxrSurface with Prman" )

	def buttonItemLock(self):
		self.itemLock = self.main_widget.pb_iconInfos01.isChecked()
		if self.itemLock:
			self.main_widget.pb_iconInfos01.setIcon(self.iconLock)
			self.main_widget.pb_iconInfos01.setIconSize(QtCore.QSize(20, 20))
			self.main_widget.pb_iconInfos01.setToolTip( "Use Lama Shader with Prman" )
		else:
			self.main_widget.pb_iconInfos01.setIcon(self.iconUnlock)
			self.main_widget.pb_iconInfos01.setIconSize(QtCore.QSize(20, 20))
			self.main_widget.pb_iconInfos01.setToolTip( "Use PxrSurface with Prman" )
	
	def userPreferencesWrite(self):
		prefFile = os.path.abspath(os.path.join(self.userPreferenceFolder, self.userPrefJson))
		prefFile = prefFile.replace(os.sep,"/")
		indexToSave = self.main_widget.comboBox_sgDefaultLibrary.currentIndex()
		nameToSave = self.main_widget.comboBox_sgDefaultLibrary.itemText(indexToSave)
		## GLOBAL
		self.pathUnzipFolder = self.main_widget.lineEdit_sgPathUnzipMegascans.text()
		self.imageBrowserPathLinux = self.main_widget.lineEdit_sgPathBrowser_lin.text()
		self.imageBrowserPathWindows = self.main_widget.lineEdit_sgPathBrowser_win.text()
		self.pdfBrowserPathLinux = self.main_widget.lineEdit_sgPDFPathBrowser_lin.text()
		self.pdfBrowserPathWindows = self.main_widget.lineEdit_sgPDFPathBrowser_win.text()
		verbosityLODIndex = self.main_widget.sgGlobalSettings_Verbosity.currentIndex()
		self.verbosityText = self.main_widget.sgGlobalSettings_Verbosity.itemText(verbosityLODIndex)
		## Sync
		self.megascansAutoSync = self.main_widget.checkBox_sgMegAutoSync.isChecked()
		## BLENDER
		blenderLODIndex = self.main_widget.sgBlenderSettings_LOD.currentIndex()
		self.blenderLOD = self.main_widget.sgBlenderSettings_LOD.itemText(blenderLODIndex)
		## MAYA
		mayaLODIndex = self.main_widget.sgMayaSettings_LOD.currentIndex()
		self.mayaLOD = self.main_widget.sgMayaSettings_LOD.itemText(mayaLODIndex)
		## HOUDINI
		houdiniSolarisIndex = self.main_widget.sgHoudiniSettings_Settings.currentIndex()
		self.houdiniSolaris = self.main_widget.sgHoudiniSettings_Settings.itemText(houdiniSolarisIndex)
		houdiniLODIndex = self.main_widget.sgHoudiniSettings_LOD.currentIndex()
		self.houdiniLOD = self.main_widget.sgHoudiniSettings_LOD.itemText(houdiniLODIndex)
		#self.houdiniLOD = "LOD0"
		houdiniTexConvertionIndex = self.main_widget.sgHoudiniSettings_convertionT.currentIndex()
		houdiniTexConvertion = self.main_widget.sgHoudiniSettings_convertionT.itemText(houdiniTexConvertionIndex)
		## KATANA
		self.katanaLOD = "LOD0"
		## MARI
		mariShaderIndex = self.main_widget.sgMariSettings_Shader.currentIndex()
		self.mariShader = self.main_widget.sgMariSettings_Shader.itemText(mariShaderIndex)
		mariColorspaceIndex = self.main_widget.sgMariSettings_ColorSpace.currentIndex()
		self.mariColorspace = self.main_widget.sgMariSettings_ColorSpace.itemText(mariColorspaceIndex)
		mariEnvMapIndex = self.main_widget.sgMariSettings_EnvMap.currentIndex()
		self.mariEnvMap = self.main_widget.sgMariSettings_EnvMap.itemText(mariEnvMapIndex)
		## NUKE
		nukeLODIndex = self.main_widget.sgNukeSettings_LOD.currentIndex()
		self.nukeLOD = self.main_widget.sgNukeSettings_LOD.itemText(nukeLODIndex)
		nuke3DIndex = self.main_widget.sgNukeSettings_3D.currentIndex()
		self.nuke3D = self.main_widget.sgNukeSettings_3D.itemText(nuke3DIndex)
		## UNREAL
		unrealLODIndex = self.main_widget.sgUnrealSettings_LOD.currentIndex()
		self.unrealLOD = self.main_widget.sgUnrealSettings_LOD.itemText(unrealLODIndex)
		self.unrealDisplacement = self.main_widget.checkBox_sgUnrealSettingsDisplacement.isChecked()

		print("Saving User Preferences to: " + prefFile)

		pref = {}
		pref["Preferences"]= []
		pref["Preferences"].append({
		'Library_Index':indexToSave,
		'Library_Name':nameToSave,
		'UnzipFolder':self.pathUnzipFolder,
		'ImgBrowserLinux':self.imageBrowserPathLinux,
		'ImgBrowserWindows':self.imageBrowserPathWindows,
		'PDFBrowserLinux':self.pdfBrowserPathLinux,
		'PDFBrowserWindows':self.pdfBrowserPathWindows,
		'Verbosity':verbosityLODIndex,
		'MEGASCANS_AutomaticSync':self.megascansAutoSync,
		'BLENDER_Lod':self.blenderLOD,
		'MAYA_Lod':self.mayaLOD,
		'HOUDINI_Convertion':houdiniTexConvertion,
		'HOUDINI_Solaris':self.houdiniSolaris,
		'HOUDINI_Lod':self.houdiniLOD,
		'MARI_Shader':self.mariShader,
		'MARI_Colorspace':self.mariColorspace,
		'MARI_EnvMap':self.mariEnvMap,
		'NUKE_3D':self.nuke3D,
		'NUKE_Lod':self.nukeLOD,
		'UNREAL_Lod':self.unrealLOD,
		'UNREAL_Disp':self.unrealDisplacement,
		})

		with open(prefFile,'w') as outJson:
			json.dump(pref,outJson,indent = 4)

	def userPreferencesRead(self):
		try:
			prefFile= os.path.abspath( os.path.join(self.userPreferenceFolder,self.userPrefJson ))
			prefFile = prefFile.replace(os.sep,"/")
			print ("Loading User Preferences from: " + prefFile)
			with open(prefFile) as jfile:
				preferences = json.load(jfile)
			print ("Preferences Loaded Successfully")
		except:
			preferences={}
			preferences["Preferences"]= []
			preferences["Preferences"].append({
			'Library_Index':0,
			'Library_Name':"Generalist Library",
			'UnzipFolder':"",
			'ImgBrowserLinux':"",
			'ImgBrowserWindows':"",
			'PDFBrowserLinux':"",
			'PDFBrowserWindows':"",
			'Verbosity':0,
			'MEGASCANS_AutomaticSync':False,
			'BLENDER_Lod':"LOD0",
			'HOUDINI_Convertion':"TEX (Prman)",
			'HOUDINI_Solaris':"MPC",
			'HOUDINI_Lod':"LOD0",
			'MAYA_Lod':"LOD0",
			'MARI_Shader':"Shaders/Vendor Shaders/Unreal",
			'MARI_Colorspace':"mpc_lin",
			'MARI_EnvMap':"Luxo",
			'NUKE_3D':"3D Classic",
			'NUKE_Lod':"LOD0",
			'UNREAL_Lod':"LOD0",
			'UNREAL_Disp':0,
			})
			print("** Set back to default preferences - Could not load user preferences **")
			print(sys.exc_info())

		try :
			## Set Library
			self.main_widget.comboBox_sgDefaultLibrary.setCurrentText(preferences["Preferences"][0]["Library_Name"])
		except:
			self.main_widget.comboBox_sgDefaultLibrary.setCurrentIndex(0)
			print ("Last selected library has been deleted, going back to the default one")
			# print(sys.exc_info())
			pass

		try:
			self.pathUnzipFolder = preferences["Preferences"][0]["UnzipFolder"]
			self.imageBrowserPathLinux = preferences["Preferences"][0]["ImgBrowserLinux"]
			self.imageBrowserPathWindows = preferences["Preferences"][0]["ImgBrowserWindows"]
			self.pdfBrowserPathLinux = preferences["Preferences"][0]["PDFBrowserLinux"]
			self.pdfBrowserPathWindows = preferences["Preferences"][0]["PDFBrowserWindows"]
		except:
			print ("** Image/PDF Browser didn't initialise properly **")
			pass

		try:
			# Global
			self.main_widget.lineEdit_sgPathUnzipMegascans.setText(self.pathUnzipFolder)
			self.main_widget.lineEdit_sgPathBrowser_lin.setText(self.imageBrowserPathLinux)
			self.main_widget.lineEdit_sgPathBrowser_win.setText(self.imageBrowserPathWindows)
			self.main_widget.lineEdit_sgPDFPathBrowser_lin.setText(self.pdfBrowserPathLinux)
			self.main_widget.lineEdit_sgPDFPathBrowser_win.setText(self.pdfBrowserPathWindows)
			# Sync
			self.megascansAutoSync = preferences["Preferences"][0]["MEGASCANS_AutomaticSync"]
			self.main_widget.checkBox_sgMegAutoSync.setChecked(self.megascansAutoSync)
			self.amandaServices = self.megascansAutoSync
			# Blender
			self.main_widget.sgGlobalSettings_Verbosity.setCurrentIndex(preferences["Preferences"][0]["Verbosity"])
			self.main_widget.sgBlenderSettings_LOD.setCurrentText(preferences["Preferences"][0]["BLENDER_Lod"])
			# Houdini
			self.main_widget.sgHoudiniSettings_convertionT.setCurrentText(preferences["Preferences"][0]["HOUDINI_Convertion"])
			self.main_widget.sgHoudiniSettings_LOD.setCurrentText(preferences["Preferences"][0]["HOUDINI_Lod"])
			self.main_widget.sgHoudiniSettings_Settings.setCurrentText(preferences["Preferences"][0]["HOUDINI_Solaris"])
			# Maya
			self.main_widget.sgMayaSettings_LOD.setCurrentText(preferences["Preferences"][0]["MAYA_Lod"])
			# Mari
			self.main_widget.sgMariSettings_Shader.setCurrentText(preferences["Preferences"][0]["MARI_Shader"])
			self.main_widget.sgMariSettings_ColorSpace.setCurrentText(preferences["Preferences"][0]["MARI_Colorspace"])
			self.main_widget.sgMariSettings_EnvMap.setCurrentText(preferences["Preferences"][0]["MARI_EnvMap"])
			# Nuke
			self.main_widget.sgNukeSettings_3D.setCurrentText(preferences["Preferences"][0]["NUKE_3D"])
			self.main_widget.sgNukeSettings_LOD.setCurrentText(preferences["Preferences"][0]["NUKE_Lod"])
			# Unreal
			self.main_widget.sgUnrealSettings_LOD.setCurrentText(preferences["Preferences"][0]["UNREAL_Lod"])
			self.main_widget.checkBox_sgUnrealSettingsDisplacement.setChecked(preferences["Preferences"][0]["UNREAL_Disp"])
		except:
			print("** Softwares specific settings could not be set in UI **")
			self.megascansAutoSync = False
			pass

	def queryPreferences(self):
		## Query UI
		self.pathUnzipFolder = self.main_widget.lineEdit_sgPathUnzipMegascans.text()
		self.imageBrowserPathLinux = self.main_widget.lineEdit_sgPathBrowser_lin.text()
		self.imageBrowserPathWindows = self.main_widget.lineEdit_sgPathBrowser_win.text()
		self.pdfBrowserPathLinux = self.main_widget.lineEdit_sgPDFPathBrowser_lin.text()
		self.pdfBrowserPathWindows = self.main_widget.lineEdit_sgPDFPathBrowser_win.text()
		verbosityLODIndex = self.main_widget.sgGlobalSettings_Verbosity.currentIndex()
		self.verbosityText = self.main_widget.sgGlobalSettings_Verbosity.itemText(verbosityLODIndex)
		self.megascansAutoSync = self.main_widget.checkBox_sgMegAutoSync.isChecked()
		blenderLODIndex = self.main_widget.sgBlenderSettings_LOD.currentIndex()
		self.blenderLOD = self.main_widget.sgBlenderSettings_LOD.itemText(blenderLODIndex)
		self.indexnukeLOD = self.main_widget.sgNukeSettings_LOD.currentIndex()
		self.nukeLOD = self.main_widget.sgNukeSettings_LOD.itemText(self.indexnukeLOD)
		mayaLODIndex = self.main_widget.sgMayaSettings_LOD.currentIndex()
		self.mayaLOD = self.main_widget.sgMayaSettings_LOD.itemText(mayaLODIndex)
		houdiniLODIndex = self.main_widget.sgHoudiniSettings_LOD.currentIndex()
		self.houdiniLOD = self.main_widget.sgHoudiniSettings_LOD.itemText(houdiniLODIndex)
		houdiniSolarisIndex = self.main_widget.sgHoudiniSettings_Settings.currentIndex()
		self.houdiniSolaris = self.main_widget.sgHoudiniSettings_Settings.itemText(houdiniSolarisIndex)

		self.katanaLOD="LOD0"
		self.mariLOD="LOD0"

		unrealLODIndex = self.main_widget.sgUnrealSettings_LOD.currentIndex()
		self.unrealLOD = self.main_widget.sgUnrealSettings_LOD.itemText(unrealLODIndex)

	def frameSyncColor(self,status):
		if status == "green":
			self.main_widget.frameMegAutoSync.setStyleSheet('color: green')
		elif status == "red":
			self.main_widget.frameMegAutoSync.setStyleSheet('color: red')
		elif status == "black":
			self.main_widget.frameMegAutoSync.setStyleSheet('color: black')

	def setDefaultPath(self):
		currentDefaultSelection = self.main_widget.comboBox_sgDefaultLibrary.currentText()
		self.megascanZIPLibraryWinPath = self.dataPathDefaultLibraries[currentDefaultSelection][0]["megascans_Windows"]
		self.megascanZIPLibraryLinPath = self.dataPathDefaultLibraries[currentDefaultSelection][0]["megascans_Linux"]
		if self.platform == "win32" or self.platform == "win64":
			self.libraryPath = self.dataPathDefaultLibraries[currentDefaultSelection][0]["path_Windows"]
			self.megascanZIPLibraryPath = self.dataPathDefaultLibraries[currentDefaultSelection][0]["megascans_Windows"]
		if self.platform == "linux2" or self.platform == "linux":
			self.libraryPath = self.dataPathDefaultLibraries[currentDefaultSelection][0]["path_Linux"]
			self.megascanZIPLibraryPath = self.dataPathDefaultLibraries[currentDefaultSelection][0]["megascans_Linux"]
		
		## Update UI Text
		self.main_widget.button_sgPathLibrary.setText(self.libraryPath)
		self.main_widget.button_sgPathLibrary.setStyleSheet("QPushButton { text-align:left;} ")
		self.main_widget.pushButton_megascansPath.setText(self.megascanZIPLibraryPath)
		self.main_widget.pushButton_megascansPath.setStyleSheet("QPushButton { text-align:left;} ")

		# Init all the variables
		self.initVariables()
		## Refresh UI
		self.main_widget.treeWidget_sgLibrary.clear()
		self.libraryFolderStructure(self.libraryPath,self.main_widget.treeWidget_sgLibrary)

	def show_progress_window(self ):
		w = sgProgressBarLibrary()
		w.show()

	def displayStatusMessage(self,message):
		self.main_widget.lineEdit_sgDisplayMessage.setText(message)
		# time.sleep(1)

	def displaySuperUserFile(self,filePath):
		self.main_widget.lineEdit_sgSuperUserFile.setText(filePath)
		# Update Tooltip
	
	def displayTagFile(self,filePath):
		self.main_widget.lineEdit_sgTagFile.setText(filePath)
		# Update Tooltip
		self.setToolTipTagsUI()

	def displayUserPrefFile(self,filePath):
		self.main_widget.label_sgLogPath.setText(filePath)

	def loadConvertToTexUI(self):
		import sg_batchTextureConvert
		sg_batchTextureConvert.showBatchConvertUI()

	def loadConvertToBookUI(self):
		import sg_convertToBook
		sg_convertToBook.sg_convertToBook_UI()

	def updateSearchCompleter(self):
		self.completerModel.setStringList(self.allSearchTags)
		self.uiCompleter.setModel(self.completerModel)

	def getLibContext(self):
		self.selectedPath = self.selectTreeItem()
		self.context = self.selectedPath[1]

		tmpContext = self.selectedPath[0].replace(self.libraryPath,"")

		if len(tmpContext.split("/")) == 4:
			self.subContext = self.selectedPath[0].split("/")[-3]
			self.categoryContext = self.selectedPath[0].split("/")[-2]
		elif len(tmpContext.split("/")) == 3:
			self.subContext = self.selectedPath[0].split("/")[-2]
			self.categoryContext = self.selectedPath[0].split("/")[-1]
		else:
			self.subContext = ""
			self.categoryContext = ""

	def diagnoseDatabaseUI(self):
		#
		self.main_widget.label_sgAmountEntryDatabase.setText("There are " +str(len(self.dicAllDatabase.keys()))+" entries in the database and " + str(len(self.dicMegascansZip.keys())) + " megascans")

#######################################################################################################################
################################################### ACTION MENU #######################################################
#######################################################################################################################
	
	def actionCategoryUI(self,point):
		try:
			self.getLibContext()
		except:
			pass
		## Build the add category Menu after a right click.
		if self.selectedPath[0] == self.libraryPath + self.context + "/"  :
			#print(self.selectedPath[0],self.context)
			if self.context != "Megascans" and self.context != "Models" and self.context != "Shaders" and self.context != "Collections" and self.context != "Lightrigs":
				text = "Add New Category to " + self.context
				self.createNewCategoryMenu(point,text)
		# Can't add a first subContext for Shaders,Models and Lightrigs
		elif self.selectedPath[0] == self.libraryPath + "Shaders/"+ self.subContext+"/":
			text = "Add New Category to " + self.context + "/" + self.subContext + "/"
			self.createNewCategoryMenu(point,text)
		elif self.selectedPath[0] == self.libraryPath + "Models/"+ self.subContext+"/":
			text = "Add New Category to " + self.context + "/" + self.subContext + "/"
			self.createNewCategoryMenu(point,text)
		elif self.selectedPath[0] == self.libraryPath + "Lightrigs/"+ self.subContext+"/":
			text = "Add New Category to " + self.context + "/" + self.subContext + "/"
			self.createNewCategoryMenu(point,text)
		# Remove Category
		elif self.selectedPath[0] == self.libraryPath + "Shaders/"+ self.subContext+"/"+self.categoryContext+"/":
			text = "Remove category named: " + self.context + "/" + self.subContext + "/"+self.categoryContext + " and its content"
			self.createRemoveCategoryMenu(point,text)
		elif self.selectedPath[0] == self.libraryPath + "Models/"+ self.subContext+"/"+self.categoryContext+"/":
			text = "Remove category named: " + self.context + "/" + self.subContext + "/"+self.categoryContext + " and its content"
			self.createRemoveCategoryMenu(point,text)
		elif self.selectedPath[0] == self.libraryPath + "Lightrigs/"+ self.subContext+"/"+self.categoryContext+"/":
			text = "Remove category named: " + self.context + "/" + self.subContext + "/"+self.categoryContext + " and its content"
			self.createRemoveCategoryMenu(point,text)
		elif self.selectedPath[0] == self.libraryPath + "Textures/"+ self.subContext+"/":
			text = "Remove category named: " +self.subContext + " and its content"
			self.createRemoveCategoryMenu(point,text)
		elif self.selectedPath[0] == self.libraryPath + "DMP/"+ self.subContext+"/" or self.selectedPath[0] == self.libraryPath + "VDB/"+ self.subContext+"/" or self.selectedPath[0] == self.libraryPath + "IES/"+ self.subContext+"/":
			text = "Remove category named: " + self.subContext + " and its content"
			self.createRemoveCategoryMenu(point,text)
		#else:
		#	print("Not fitting anything", self.selectedPath[0],self.context, self.subContext)

	def createNewCategoryMenu(self,point,text):
		# Infos about the menu selected.
		index =self.main_widget.treeWidget_sgLibrary.indexAt(point)
		
		if not index.isValid():
			return
		menu = QtWidgets.QMenu()

		self.addCategory = QtWidgets.QAction(text, self.main_widget.treeWidget_sgLibrary)
		separatorCategory = QtWidgets.QAction("______", self.main_widget.treeWidget_sgLibrary)
		self.actionCategory = menu.addAction(self.addCategory)
		separatorActionCategory = menu.addAction(separatorCategory)
		self.addCategory.triggered.connect(self.addNewCategoryFolder)
		separatorCategory.setSeparator(True)

		item = self.main_widget.treeWidget_sgLibrary.itemAt(point)
		name = item.text(0)

		menu.exec_( self.main_widget.treeWidget_sgLibrary.mapToGlobal(point))

	def createRemoveCategoryMenu(self,point,text):
		index =self.main_widget.treeWidget_sgLibrary.indexAt(point)
		
		if not index.isValid():
			return
		menu = QtWidgets.QMenu()

		self.removeCategory = QtWidgets.QAction(text, self.main_widget.treeWidget_sgLibrary)
		self.actionRemoveCategory = menu.addAction(self.removeCategory)
		self.removeCategory.triggered.connect(partial(self.removeCategoryFolder,self.context + "/" + self.subContext + "/"+self.categoryContext))

		item = self.main_widget.treeWidget_sgLibrary.itemAt(point)
		name = item.text(0)

		# Check if user is super user
		if self.isSuperUser(self.username) == True:
			self.removeCategory.setEnabled(True)
		else:
			self.removeCategory.setEnabled(False)

		menu.exec_( self.main_widget.treeWidget_sgLibrary.mapToGlobal(point))

	def actionMenuUI(self):
		# Create Actions
		self.actionImport00 = QtWidgets.QAction("", self.main_widget.tableWidget_sgElementBrowser)
		self.actionImport01 = QtWidgets.QAction("", self.main_widget.tableWidget_sgElementBrowser)
		self.actionImport02 = QtWidgets.QAction("", self.main_widget.tableWidget_sgElementBrowser)
		self.separator01 = QtWidgets.QAction("________________________",self.main_widget.tableWidget_sgElementBrowser)
		self.actionUnzip = QtWidgets.QAction("Unzip File", self.main_widget.tableWidget_sgElementBrowser)
		self.actionSelectZip = QtWidgets.QAction("View Zip", self.main_widget.tableWidget_sgElementBrowser)
		self.actionView = QtWidgets.QAction("View in Explorer", self.main_widget.tableWidget_sgElementBrowser)
		self.actionCopy = QtWidgets.QAction("Copy Path", self.main_widget.tableWidget_sgElementBrowser)
		self.separator02 = QtWidgets.QAction("________________________",self.main_widget.tableWidget_sgElementBrowser)
		self.actionAddToCollection = QtWidgets.QAction("Add to Collection", self.main_widget.tableWidget_sgElementBrowser)
		self.actionEditInfos = QtWidgets.QAction("Edit Infos", self.main_widget.tableWidget_sgElementBrowser)
		self.actionGenerateContactSheet = QtWidgets.QAction("Create Contact Sheet", self.main_widget.tableWidget_sgElementBrowser)
		self.separator03 = QtWidgets.QAction("________________________",self.main_widget.tableWidget_sgElementBrowser)
		self.actionDelete = QtWidgets.QAction("Delete", self.main_widget.tableWidget_sgElementBrowser)

		# Add Actions
		self.main_widget.tableWidget_sgElementBrowser.addAction(self.actionImport00)
		self.main_widget.tableWidget_sgElementBrowser.addAction(self.actionImport01)
		self.main_widget.tableWidget_sgElementBrowser.addAction(self.actionImport02)
		self.main_widget.tableWidget_sgElementBrowser.addAction(self.separator01)
		self.main_widget.tableWidget_sgElementBrowser.addAction(self.actionUnzip)
		self.main_widget.tableWidget_sgElementBrowser.addAction(self.actionSelectZip)
		self.main_widget.tableWidget_sgElementBrowser.addAction(self.actionView)
		self.main_widget.tableWidget_sgElementBrowser.addAction(self.actionCopy)
		self.main_widget.tableWidget_sgElementBrowser.addAction(self.separator02)
		self.main_widget.tableWidget_sgElementBrowser.addAction(self.actionAddToCollection)
		self.main_widget.tableWidget_sgElementBrowser.addAction(self.actionEditInfos)
		self.main_widget.tableWidget_sgElementBrowser.addAction(self.actionGenerateContactSheet)
		self.main_widget.tableWidget_sgElementBrowser.addAction(self.separator03)
		self.main_widget.tableWidget_sgElementBrowser.addAction(self.actionDelete)

		# Connect Signals
		self.actionImport00.triggered.connect(partial (self.extractingZip, ''))
		self.actionImport01.triggered.connect(partial (self.extractingZip, ''))
		self.actionImport02.triggered.connect(partial (self.extractingZip, ''))
		self.separator01.setSeparator(True)
		self.actionUnzip.triggered.connect(partial (self.extractingZip, ''))
		self.actionSelectZip.triggered.connect(self.openSelectFileInExplorer)
		self.actionView.triggered.connect(self.openExplorer)
		self.actionCopy.triggered.connect(self.copyPath)
		self.separator02.setSeparator(True)
		self.actionAddToCollection.triggered.connect(self.addToCollection)
		self.actionEditInfos.triggered.connect(self.launchEditInfosMenu)
		self.actionGenerateContactSheet.triggered.connect(self.createContactSheet)
		self.separator03.setSeparator(True)
		self.actionDelete.triggered.connect(self.deleteItemLibrary)

		self.actionUnzip.setEnabled(False)

	def actionSearchMenuUI(self):
		self.actionSearchImport00 = QtWidgets.QAction("", self.main_widget.tableWidget_sgSearchBrowser)
		self.actionSearchImport01 = QtWidgets.QAction("", self.main_widget.tableWidget_sgSearchBrowser)
		self.actionSearchImport02 = QtWidgets.QAction("", self.main_widget.tableWidget_sgSearchBrowser)
		self.searchSeparator01 = QtWidgets.QAction("________________________",self.main_widget.tableWidget_sgSearchBrowser)
		self.actionSearchUnzip = QtWidgets.QAction("Unzip File", self.main_widget.tableWidget_sgSearchBrowser)
		self.actionSearchSelectZip = QtWidgets.QAction("View Zip", self.main_widget.tableWidget_sgSearchBrowser)
		self.actionSearchView = QtWidgets.QAction("View in Explorer", self.main_widget.tableWidget_sgSearchBrowser)
		self.actionSearchCopy = QtWidgets.QAction("Copy Path", self.main_widget.tableWidget_sgSearchBrowser)
		self.searchSeparator02 = QtWidgets.QAction("________________________",self.main_widget.tableWidget_sgSearchBrowser)
		self.actionSearchAddToCollection = QtWidgets.QAction("Add to Collection", self.main_widget.tableWidget_sgSearchBrowser)
		self.actionSearchEditInfos = QtWidgets.QAction("Edit Asset Infos", self.main_widget.tableWidget_sgSearchBrowser)
		self.actionSearchGenerateContactSheet = QtWidgets.QAction("View Contact Sheet", self.main_widget.tableWidget_sgSearchBrowser)
		self.searchSeparator03 = QtWidgets.QAction("________________________",self.main_widget.tableWidget_sgSearchBrowser)
		self.actionSearchDelete = QtWidgets.QAction("Delete", self.main_widget.tableWidget_sgSearchBrowser)

		self.main_widget.tableWidget_sgSearchBrowser.addAction(self.actionSearchImport00)
		self.main_widget.tableWidget_sgSearchBrowser.addAction(self.actionSearchImport01)
		self.main_widget.tableWidget_sgSearchBrowser.addAction(self.actionSearchImport02)
		self.main_widget.tableWidget_sgSearchBrowser.addAction(self.searchSeparator01)
		self.main_widget.tableWidget_sgSearchBrowser.addAction(self.actionSearchUnzip)
		self.main_widget.tableWidget_sgSearchBrowser.addAction(self.actionSearchSelectZip)
		self.main_widget.tableWidget_sgSearchBrowser.addAction(self.actionSearchView)
		self.main_widget.tableWidget_sgSearchBrowser.addAction(self.actionSearchCopy)
		self.main_widget.tableWidget_sgSearchBrowser.addAction(self.searchSeparator02)
		self.main_widget.tableWidget_sgSearchBrowser.addAction(self.actionSearchAddToCollection)
		self.main_widget.tableWidget_sgSearchBrowser.addAction(self.actionSearchEditInfos)
		self.main_widget.tableWidget_sgSearchBrowser.addAction(self.actionSearchGenerateContactSheet)
		self.main_widget.tableWidget_sgSearchBrowser.addAction(self.searchSeparator03)
		self.main_widget.tableWidget_sgSearchBrowser.addAction(self.actionSearchDelete)

		self.actionSearchImport00.triggered.connect(partial (self.extractingZip, ''))
		self.actionSearchImport01.triggered.connect(partial (self.extractingZip, ''))
		self.actionSearchImport02.triggered.connect(partial (self.extractingZip, ''))
		self.searchSeparator01.setSeparator(True)
		self.actionSearchUnzip.triggered.connect(partial (self.extractingZip, ''))
		self.actionSearchSelectZip.triggered.connect(self.openSelectFileInExplorer)
		self.actionSearchView.triggered.connect(self.openExplorer)
		self.actionSearchCopy.triggered.connect(self.copyPath)
		self.searchSeparator02.setSeparator(True)
		self.actionSearchAddToCollection.triggered.connect(self.addToCollection)
		self.actionSearchEditInfos.triggered.connect(self.launchEditInfosMenu)
		self.actionSearchGenerateContactSheet.triggered.connect(self.createContactSheet)
		self.actionSearchDelete.triggered.connect(self.deleteItemLibrary)

		self.actionSearchUnzip.setEnabled(False)

	def actionCollectionMenuUI(self):
		self.actionColImport00 = QtWidgets.QAction("", self.main_widget.tableWidget_sgCollectionBrowser)
		self.actionColImport01 = QtWidgets.QAction("", self.main_widget.tableWidget_sgCollectionBrowser)
		self.actionColImport02 = QtWidgets.QAction("", self.main_widget.tableWidget_sgCollectionBrowser)
		self.colSeparator01 = QtWidgets.QAction("________________________",self.main_widget.tableWidget_sgCollectionBrowser)
		self.actionColUnzip = QtWidgets.QAction("Unzip File ", self.main_widget.tableWidget_sgCollectionBrowser)
		self.actionColSelectZip = QtWidgets.QAction("View Zip", self.main_widget.tableWidget_sgCollectionBrowser)
		self.actionColView = QtWidgets.QAction("View in Explorer", self.main_widget.tableWidget_sgCollectionBrowser)
		self.actionColCopy = QtWidgets.QAction("Copy Path", self.main_widget.tableWidget_sgCollectionBrowser)
		self.colSeparator02 = QtWidgets.QAction("________________________",self.main_widget.tableWidget_sgCollectionBrowser)
		self.actionColRemoveFromCollection = QtWidgets.QAction("Remove From Collection", self.main_widget.tableWidget_sgCollectionBrowser)
		self.actionColEditInfos = QtWidgets.QAction("Edit Infos", self.main_widget.tableWidget_sgCollectionBrowser)
		self.actionColGenerateContactSheet = QtWidgets.QAction("Create Contact Sheet", self.main_widget.tableWidget_sgCollectionBrowser)
		self.colSeparator03 = QtWidgets.QAction("________________________",self.main_widget.tableWidget_sgCollectionBrowser)
		self.actionColDelete = QtWidgets.QAction("Delete", self.main_widget.tableWidget_sgCollectionBrowser)

		self.main_widget.tableWidget_sgCollectionBrowser.addAction(self.actionColImport00)
		self.main_widget.tableWidget_sgCollectionBrowser.addAction(self.actionColImport01)
		self.main_widget.tableWidget_sgCollectionBrowser.addAction(self.actionColImport02)
		self.main_widget.tableWidget_sgCollectionBrowser.addAction(self.colSeparator01)
		self.main_widget.tableWidget_sgCollectionBrowser.addAction(self.actionColUnzip)
		self.main_widget.tableWidget_sgCollectionBrowser.addAction(self.actionColSelectZip)
		self.main_widget.tableWidget_sgCollectionBrowser.addAction(self.actionColView)
		self.main_widget.tableWidget_sgCollectionBrowser.addAction(self.actionColCopy)
		self.main_widget.tableWidget_sgCollectionBrowser.addAction(self.colSeparator02)
		self.main_widget.tableWidget_sgCollectionBrowser.addAction(self.actionColRemoveFromCollection)
		self.main_widget.tableWidget_sgCollectionBrowser.addAction(self.actionColEditInfos)
		self.main_widget.tableWidget_sgCollectionBrowser.addAction(self.actionColGenerateContactSheet)
		self.main_widget.tableWidget_sgCollectionBrowser.addAction(self.colSeparator03)
		self.main_widget.tableWidget_sgCollectionBrowser.addAction(self.actionColDelete)

		self.actionColImport00.triggered.connect(partial (self.extractingZip, ''))
		self.actionColImport01.triggered.connect(partial (self.extractingZip, ''))
		self.actionColImport02.triggered.connect(partial (self.extractingZip, ''))

		self.colSeparator01.setSeparator(True)
		self.actionColUnzip.triggered.connect(partial (self.extractingZip, ''))
		self.actionColSelectZip.triggered.connect(self.openSelectFileInExplorer)
		self.actionColView.triggered.connect(self.openExplorer)
		self.actionColCopy.triggered.connect(self.copyPath)
		self.colSeparator02.setSeparator(True)
		self.actionColRemoveFromCollection.triggered.connect(self.removeFromCollection)
		self.actionColEditInfos.triggered.connect(self.launchEditInfosMenu)
		self.actionColGenerateContactSheet.triggered.connect(self.createContactSheet)
		self.colSeparator03.setSeparator(True)
		self.actionColDelete.triggered.connect(self.deleteItemLibrary)

	def actionMenuUpdateUI(self):
		nameKeyIcon = self.picturePath.split("/")[-1]
		## Button clicked context
		self.selectedButtonContext = self.dicAllDatabase[nameKeyIcon][0]["type"]
		#self.softwareInAction = softwareUsed.lower()
		dictMenuAction = self.dicMenuAction[self.softwareInAction][self.selectedButtonContext]
		#print(self.softwareInAction,dictMenuAction)
		## Get action data
		import00Module = dictMenuAction["actionImport00_action"]["module"]
		import00Variable = dictMenuAction["actionImport00_action"]["variables"]
		import01Module = dictMenuAction["actionImport01_action"]["module"]
		import01Variable = dictMenuAction["actionImport01_action"]["variables"]
		import02Module = dictMenuAction["actionImport02_action"]["module"]
		import02Variable = dictMenuAction["actionImport02_action"]["variables"]
		unzipModule = dictMenuAction["actionUnzip_action"]["module"]
		unzipVariable = dictMenuAction["actionUnzip_action"]["variables"]
		if self.main_widget.libraryTab.currentIndex() == 0:
			# Main Tab
			if self.searchMode == False:
				try:
					self.actionImport00.triggered.disconnect()
				except:
					pass
				try:
					self.actionImport01.triggered.disconnect()
				except:
					pass
				try:
					self.actionImport02.triggered.disconnect()
				except:
					pass
				
				## Update UI
				self.actionImport00.setText(dictMenuAction["actionImport00_txt"])
				self.actionImport00.setVisible(dictMenuAction["actionImport00_vis"])
				if import00Variable == "rman":
					enable00 =  self.RfM 
				elif import00Variable == "arnold":
					enable00 = self.MtoA
				else:
					enable00 =  dictMenuAction["actionImport00_enabled"]
				self.actionImport00.setEnabled(enable00)

				self.actionImport01.setText(dictMenuAction["actionImport01_txt"])
				self.actionImport01.setVisible(dictMenuAction["actionImport01_vis"])
				if import01Variable == "rman":
					enable01 =  self.RfM 
				elif import00Variable == "arnold":
					enable01 = self.MtoA
				else:
					enable01 =  dictMenuAction["actionImport00_enabled"]
				self.actionImport01.setEnabled(enable01)

				self.actionImport02.setText(dictMenuAction["actionImport02_txt"])
				self.actionImport02.setVisible(dictMenuAction["actionImport02_vis"])
				if import02Variable == "rman":
					enable02 =  self.RfM 
				elif import00Variable == "arnold":
					enable02 = self.MtoA
				else:
					enable02 =  dictMenuAction["actionImport00_enabled"]
				self.actionImport02.setEnabled(enable02)

				self.actionUnzip.setVisible(dictMenuAction["actionUnzip_vis"])
				self.actionUnzip.setEnabled(dictMenuAction["actionUnzip_enabled"])

				self.actionSelectZip.setVisible(dictMenuAction["actionSelectZip_vis"])
				self.actionSelectZip.setEnabled(dictMenuAction["actionSelectZip_enabled"])
				self.actionView.setVisible(dictMenuAction["actionView_vis"])
				self.actionView.setEnabled(dictMenuAction["actionView_enabled"])
				self.actionCopy.setVisible(dictMenuAction["actionCopy_vis"])
				self.actionCopy.setEnabled(dictMenuAction["actionCopy_enabled"])
				self.actionAddToCollection.setVisible(dictMenuAction["actionAddToCollection_vis"])
				self.actionAddToCollection.setEnabled(dictMenuAction["actionAddToCollection_enabled"])
				self.actionEditInfos.setVisible(dictMenuAction["actionEditInfos_vis"])
				self.actionEditInfos.setEnabled(dictMenuAction["actionEditInfos_enabled"])
				self.actionGenerateContactSheet.setVisible(dictMenuAction["actionAddToCollection_vis"])
				
				if pilLoaded == True:
					self.actionGenerateContactSheet.setEnabled(dictMenuAction["actionGenerateContactSheet_enabled"])
				else:
					self.actionGenerateContactSheet.setEnabled(False)
				
				self.actionDelete.setVisible(True)

				if dictMenuAction["actionDelete_enabled"] == True:
					if self.lock == False:
						self.actionDelete.setEnabled(self.isSuperUser(self.username))
					else:
						self.actionDelete.setEnabled(False)
				else:
					self.actionDelete.setEnabled(dictMenuAction["actionDelete_enabled"])

				if import00Module == "extractingZip" :
					self.actionImport00.triggered.connect(partial(self.extractingZip,import00Variable))
				elif import00Module == "importModel" :
					self.actionImport00.triggered.connect(partial(self.importModel,import00Variable))
				elif import00Module == "importTexture" :
					self.actionImport00.triggered.connect(partial(self.importTexture,import00Variable))
				elif import00Module == "importShader" :
					self.actionImport00.triggered.connect(partial(self.importShader,import00Variable))
				elif import00Module == "assignShader" :
					self.actionImport00.triggered.connect(partial(self.assignShader,import00Variable))
				elif import00Module == "importLightrig" :
					self.actionImport00.triggered.connect(partial(self.importLightrig,import00Variable))	
				elif import00Module == "importVDB" :
					self.actionImport00.triggered.connect(partial(self.importVDB,import00Variable))
				elif import00Module == "doubleClickCommandBrowser" :
					self.actionImport00.triggered.connect(self.doubleClickCommandBrowser)
				elif import00Module == "viewFile" :
					self.actionImport00.triggered.connect(self.viewFile)
				elif import00Module== "browseImages":
					self.actionImport00.triggered.connect(partial(self.browseImages,import00Variable))
				elif import00Module== "browsePDF":
					self.actionImport00.triggered.connect(partial(self.browseImages,import00Variable))
				else:
					if import00Module !="":
						print("Didn't find Module: " + import00Module)

				if import01Module == "extractingZip" :
					self.actionImport01.triggered.connect(partial(self.extractingZip,import01Variable))
				elif import01Module == "importModel" :
					self.actionImport01.triggered.connect(partial(self.importModel,import01Variable))
				elif import01Module == "importTexture" :
					self.actionImport01.triggered.connect(partial(self.importTexture,import01Variable))
				elif import01Module == "importShader" :
					self.actionImport01.triggered.connect(partial(self.importShader,import01Variable))
				elif import01Module == "assignShader" :
					self.actionImport01.triggered.connect(partial(self.assignShader,import01Variable))
				elif import01Module == "importLightrig" :
					self.actionImport01.triggered.connect(partial(self.importLightrig,import01Variable))	
				elif import01Module == "importVDB" :
					self.actionImport01.triggered.connect(partial(self.importVDB,import01Variable))
				elif import01Module == "doubleClickCommandBrowser" :
					self.actionImport01.triggered.connect(self.doubleClickCommandBrowser)
				elif import01Module == "viewFile" :
					self.actionImport01.triggered.connect(self.viewFile)
				else:
					if import01Module !="":
						print("Didn't find Module: " + import01Module)

				if import02Module == "extractingZip" :
					self.actionImport02.triggered.connect(partial(self.extractingZip,import02Variable))
				elif import02Module == "importModel" :
					self.actionImport02.triggered.connect(partial(self.importModel,import02Variable))
				elif import02Module == "importTexture" :
					self.actionImport02.triggered.connect(partial(self.importTexture,import02Variable))
				elif import02Module == "importShader" :
					self.actionImport02.triggered.connect(partial(self.importShader,import02Variable))
				elif import02Module == "assignShader" :
					self.actionImport02.triggered.connect(partial(self.assignShader,import02Variable))
				elif import02Module == "importLightrig" :
					self.actionImport02.triggered.connect(partial(self.importLightrig,import02Variable))	
				elif import02Module == "importVDB" :
					self.actionImport02.triggered.connect(partial(self.importVDB,import02Variable))
				elif import02Module == "doubleClickCommandBrowser" :
					self.actionImport02.triggered.connect(self.doubleClickCommandBrowser)
				elif import02Module == "viewFile" :
					self.actionImport02.triggered.connect(self.viewFile)
				else:
					if import02Module !="":
						print("Didn't find Module: " + import02Module)
			## Search Mode
			elif self.searchMode == True:
				try:
					self.actionSearchImport00.triggered.disconnect()
				except:
					pass
				try:
					self.actionSearchImport01.triggered.disconnect()
				except:
					pass
				try:
					self.actionSearchImport02.triggered.disconnect()
				except:
					pass
				
				## Update UI
				self.actionSearchImport00.setText(dictMenuAction["actionImport00_txt"])
				self.actionSearchImport00.setVisible(dictMenuAction["actionImport00_vis"])
				self.actionSearchImport00.setEnabled(dictMenuAction["actionImport00_enabled"])

				self.actionSearchImport01.setText(dictMenuAction["actionImport01_txt"])
				self.actionSearchImport01.setVisible(dictMenuAction["actionImport01_vis"])
				self.actionSearchImport01.setEnabled(dictMenuAction["actionImport01_enabled"])

				self.actionSearchImport02.setText(dictMenuAction["actionImport02_txt"])
				self.actionSearchImport02.setVisible(dictMenuAction["actionImport02_vis"])
				self.actionSearchImport02.setEnabled(dictMenuAction["actionImport02_enabled"])

				self.actionSearchUnzip.setVisible(dictMenuAction["actionUnzip_vis"])
				self.actionSearchUnzip.setEnabled(dictMenuAction["actionUnzip_enabled"])

				self.actionSearchSelectZip.setVisible(dictMenuAction["actionSelectZip_vis"])
				self.actionSearchSelectZip.setEnabled(dictMenuAction["actionSelectZip_enabled"])
				self.actionSearchView.setVisible(dictMenuAction["actionView_vis"])
				self.actionSearchView.setEnabled(dictMenuAction["actionView_enabled"])
				self.actionSearchCopy.setVisible(dictMenuAction["actionCopy_vis"])
				self.actionSearchCopy.setEnabled(dictMenuAction["actionCopy_enabled"])
				self.actionSearchAddToCollection.setVisible(dictMenuAction["actionAddToCollection_vis"])
				self.actionSearchAddToCollection.setEnabled(dictMenuAction["actionAddToCollection_enabled"])
				self.actionSearchEditInfos.setVisible(dictMenuAction["actionEditInfos_vis"])
				self.actionSearchEditInfos.setEnabled(dictMenuAction["actionEditInfos_enabled"])
				
				if pilLoaded == True:
					self.actionSearchGenerateContactSheet.setEnabled(True)
				else:
					self.actionSearchGenerateContactSheet.setEnabled(False)
				
				self.actionSearchDelete.setVisible(True)
				if dictMenuAction["actionDelete_enabled"] == True:
					if self.lock == False:
						self.actionSearchDelete.setEnabled(self.isSuperUser(self.username))
					else:
						self.actionSearchDelete.setEnabled(False)
				else:
					self.actionSearchDelete.setEnabled(dictMenuAction["actionDelete_enabled"])

				if import00Module == "extractingZip" :
					self.actionSearchImport00.triggered.connect(partial(self.extractingZip,import00Variable))
				elif import00Module == "importModel" :
					self.actionSearchImport00.triggered.connect(partial(self.importModel,import00Variable))
				elif import00Module == "importTexture" :
					self.actionSearchImport00.triggered.connect(partial(self.importTexture,import00Variable))
				elif import00Module == "importShader" :
					self.actionSearchImport00.triggered.connect(partial(self.importShader,import00Variable))
				elif import00Module == "assignShader" :
					self.actionSearchImport00.triggered.connect(partial(self.assignShader,import00Variable))
				elif import00Module == "importLightrig" :
					self.actionSearchImport00.triggered.connect(partial(self.importLightrig,import00Variable))	
				elif import00Module == "importVDB" :
					self.actionSearchImport00.triggered.connect(partial(self.importVDB,import00Variable))
				elif import00Module == "doubleClickCommandBrowser" :
					self.actionSearchImport00.triggered.connect(self.doubleClickCommandBrowser)
				elif import00Module == "viewFile" :
					self.actionSearchImport00.triggered.connect(self.viewFile)
				else:
					if import00Module !="":
						print("Didn't find Module: " + import00Module)

				if import01Module == "extractingZip" :
					self.actionSearchImport01.triggered.connect(partial(self.extractingZip,import01Variable))
				elif import01Module == "importModel" :
					self.actionSearchImport01.triggered.connect(partial(self.importModel,import01Variable))
				elif import01Module == "importTexture" :
					self.actionSearchImport01.triggered.connect(partial(self.importTexture,import01Variable))
				elif import01Module == "importShader" :
					self.actionSearchImport01.triggered.connect(partial(self.importShader,import01Variable))
				elif import01Module == "assignShader" :
					self.actionSearchImport01.triggered.connect(partial(self.assignShader,import01Variable))
				elif import01Module == "importLightrig" :
					self.actionSearchImport01.triggered.connect(partial(self.importLightrig,import01Variable))	
				elif import01Module == "importVDB" :
					self.actionSearchImport01.triggered.connect(partial(self.importVDB,import01Variable))
				elif import01Module == "doubleClickCommandBrowser" :
					self.actionSearchImport01.triggered.connect(self.doubleClickCommandBrowser)
				elif import01Module == "viewFile" :
					self.actionSearchImport01.triggered.connect(self.viewFile)
				else:
					if import01Module !="":
						print("Didn't find Module: " + import01Module)

				if import02Module == "extractingZip" :
					self.actionSearchImport02.triggered.connect(partial(self.extractingZip,import02Variable))
				elif import02Module == "importModel" :
					self.actionSearchImport02.triggered.connect(partial(self.importModel,import02Variable))
				elif import02Module == "importTexture" :
					self.actionSearchImport02.triggered.connect(partial(self.importTexture,import02Variable))
				elif import02Module == "importShader" :
					self.actionSearchImport02.triggered.connect(partial(self.importShader,import02Variable))
				elif import02Module == "assignShader" :
					self.actionSearchImport02.triggered.connect(partial(self.assignShader,import02Variable))
				elif import02Module == "importLightrig" :
					self.actionSearchImport02.triggered.connect(partial(self.importLightrig,import02Variable))	
				elif import02Module == "importVDB" :
					self.actionSearchImport02.triggered.connect(partial(self.importVDB,import02Variable))
				elif import02Module == "doubleClickCommandBrowser" :
					self.actionSearchImport02.triggered.connect(self.doubleClickCommandBrowser)
				elif import02Module == "viewFile" :
					self.actionSearchImport02.triggered.connect(self.viewFile)
				else:
					if import02Module !="":
						print("Didn't find Module: " + import02Module)

		## IN COLLECTIONS
		elif self.main_widget.libraryTab.currentIndex() == 1:
			try:
				self.actionColImport00.triggered.disconnect()
			except:
				pass
			try:
				self.actionColImport01.triggered.disconnect()
			except:
				pass
			try:
				self.actionColImport02.triggered.disconnect()
			except:
				pass
			
			## Update UI
			self.actionColImport00.setText(dictMenuAction["actionImport00_txt"])
			self.actionColImport00.setVisible(dictMenuAction["actionImport00_vis"])
			self.actionColImport00.setEnabled(dictMenuAction["actionImport00_enabled"])

			self.actionColImport01.setText(dictMenuAction["actionImport01_txt"])
			self.actionColImport01.setVisible(dictMenuAction["actionImport01_vis"])
			self.actionColImport01.setEnabled(dictMenuAction["actionImport01_enabled"])

			self.actionColImport02.setText(dictMenuAction["actionImport02_txt"])
			self.actionColImport02.setVisible(dictMenuAction["actionImport02_vis"])
			self.actionColImport02.setEnabled(dictMenuAction["actionImport02_enabled"])

			self.actionColUnzip.setVisible(dictMenuAction["actionUnzip_vis"])
			self.actionColUnzip.setEnabled(dictMenuAction["actionUnzip_enabled"])

			self.actionColSelectZip.setVisible(dictMenuAction["actionSelectZip_vis"])
			self.actionColSelectZip.setEnabled(dictMenuAction["actionSelectZip_enabled"])
			self.actionColView.setVisible(dictMenuAction["actionView_vis"])
			self.actionColView.setEnabled(dictMenuAction["actionView_enabled"])
			self.actionColCopy.setVisible(dictMenuAction["actionCopy_vis"])
			self.actionColCopy.setEnabled(dictMenuAction["actionCopy_enabled"])
			self.actionColEditInfos.setVisible(dictMenuAction["actionEditInfos_vis"])
			self.actionColEditInfos.setEnabled(dictMenuAction["actionEditInfos_enabled"])
			
			if pilLoaded == True:
				self.actionColGenerateContactSheet.setEnabled(True)
			else:
				self.actionColGenerateContactSheet.setEnabled(False)
			
			self.actionColDelete.setVisible(True)
			if dictMenuAction["actionDelete_enabled"] == True:
				if self.lock == False:
					self.actionColDelete.setEnabled(self.isSuperUser(self.username))
				else:
					self.actionColDelete.setEnabled(False)
			else:
				self.actionColDelete.setEnabled(dictMenuAction["actionDelete_enabled"])

			if import00Module == "extractingZip" :
				self.actionColImport00.triggered.connect(partial(self.extractingZip,import00Variable))
			elif import00Module == "importModel" :
				self.actionColImport00.triggered.connect(partial(self.importModel,import00Variable))
			elif import00Module == "importTexture" :
				self.actionColImport00.triggered.connect(partial(self.importTexture,import00Variable))
			elif import00Module == "importShader" :
				self.actionColImport00.triggered.connect(partial(self.importShader,import00Variable))
			elif import00Module == "assignShader" :
				self.actionColImport00.triggered.connect(partial(self.assignShader,import00Variable))
			elif import00Module == "importLightrig" :
				self.actionColImport00.triggered.connect(partial(self.importLightrig,import00Variable))	
			elif import00Module == "importVDB" :
				self.actionColImport00.triggered.connect(partial(self.importVDB,import00Variable))
			elif import00Module == "doubleClickCommandBrowser" :
				self.actionColImport00.triggered.connect(self.doubleClickCommandBrowser)
			elif import00Module == "viewFile" :
				self.actionColImport00.triggered.connect(self.viewFile)
			else:
				if import00Module !="":
					print("Didn't find Module: " + import00Module)

			if import01Module == "extractingZip" :
				self.actionColImport01.triggered.connect(partial(self.extractingZip,import01Variable))
			elif import01Module == "importModel" :
				self.actionColImport01.triggered.connect(partial(self.importModel,import01Variable))
			elif import01Module == "importTexture" :
				self.actionColImport01.triggered.connect(partial(self.importTexture,import01Variable))
			elif import01Module == "importShader" :
				self.actionColImport01.triggered.connect(partial(self.importShader,import01Variable))
			elif import01Module == "assignShader" :
				self.actionColImport01.triggered.connect(partial(self.assignShader,import01Variable))
			elif import01Module == "importLightrig" :
				self.actionColImport01.triggered.connect(partial(self.importLightrig,import01Variable))	
			elif import01Module == "importVDB" :
				self.actionColImport01.triggered.connect(partial(self.importVDB,import01Variable))
			elif import01Module == "doubleClickCommandBrowser" :
				self.actionColImport01.triggered.connect(self.doubleClickCommandBrowser)
			elif import01Module == "viewFile" :
				self.actionColImport01.triggered.connect(self.viewFile)
			else:
				if import01Module !="":
					print("Didn't find Module: " + import01Module)

			if import02Module == "extractingZip" :
				self.actionColImport02.triggered.connect(partial(self.extractingZip,import02Variable))
			elif import02Module == "importModel" :
				self.actionColImport02.triggered.connect(partial(self.importModel,import02Variable))
			elif import02Module == "importTexture" :
				self.actionColImport02.triggered.connect(partial(self.importTexture,import02Variable))
			elif import02Module == "importShader" :
				self.actionColImport02.triggered.connect(partial(self.importShader,import02Variable))
			elif import02Module == "assignShader" :
				self.actionColImport02.triggered.connect(partial(self.assignShader,import02Variable))
			elif import02Module == "importLightrig" :
				self.actionColImport02.triggered.connect(partial(self.importLightrig,import02Variable))	
			elif import02Module == "importVDB" :
				self.actionColImport02.triggered.connect(partial(self.importVDB,import02Variable))
			elif import02Module == "doubleClickCommandBrowser" :
				self.actionColImport02.triggered.connect(self.doubleClickCommandBrowser)
			elif import02Module == "viewFile" :
				self.actionColImport02.triggered.connect(self.viewFile)
			else:
				if import02Module !="":
					print("Didn't find Module: " + import02Module)

			self.actionColRemoveFromCollection.triggered.connect(self.removeFromCollection)
			
#######################################################################################################################
#######################################################################################################################
	
	def zoomWindowUI(self):
		##Zoom widget
		self.zoomWidget = QtWidgets.QLabel()
		self.zoomWidget.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
		self.zoomWidget.setWindowFlags(QtCore.Qt.FramelessWindowHint)
		self.zoomLayout = QtWidgets.QGridLayout()
		self.zoomWidget.setLayout(self.zoomLayout)

		##Zoom pictures
		self.zoomPic = QtWidgets.QLabel(self)
		self.zoomPic.setFixedSize(self.zoomSize[0], self.zoomSize[1]  )
		self.zoomLayout.addWidget(self.zoomPic)

		## Color for All
		self.zoomWidget.setStyleSheet("background-color: rgb(58, 58, 58)")
		self.zoomPic.setStyleSheet("background-color: rgb(58, 58, 58)")

	def setCollectionHeaderUI(self):
		## GroupBox
		self.main_widget.groupBox_collections.setTitle("Collection: " + self.collectionSelection)
		self.main_widget.label_sgCollection.setFixedSize(self.collectionBrowserWidth, 60  )
		## Icon
		self.collectionHeadPic.load(self.collectionPicture)

		self.collectionHeadPic = self.collectionHeadPic.scaled(self.main_widget.label_sgCollection.width(),self.main_widget.label_sgCollection.height(), QtCore.Qt.KeepAspectRatioByExpanding,QtCore.Qt.FastTransformation)
		self.main_widget.label_sgCollection.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
		self.main_widget.label_sgCollection.setPixmap(self.collectionHeadPic)

	def thumbnailPreviewUI(self,thumbnail):
		##self.thumbPrevmap=QtGui.QPixmap(thumbnail).scaledToWidth(220)
		self.thumbPrevmap=QtGui.QPixmap(thumbnail).scaled(220, 220, QtCore.Qt.KeepAspectRatio,QtCore.Qt.SmoothTransformation)
		self.main_widget.label_sgThumbnail.setPixmap(self.thumbPrevmap)
		self.main_widget.label_sgThumbnail.setAlignment(QtCore.Qt.AlignCenter)

	def thumbnailAddPreview(self,thumbnail):
		##self.thumbPreview=QtGui.QPixmap(thumbnail).scaledToWidth(128)
		self.thumbPreview= QtGui.QPixmap(thumbnail).scaled (128, 128, QtCore.Qt.KeepAspectRatio,QtCore.Qt.SmoothTransformation)
		self.main_widget.label_sgPreview.setPixmap(self.thumbPreview)
		self.main_widget.label_sgPreview.setAlignment(QtCore.Qt.AlignCenter)

	def thumbnailAddVDBPreview(self,thumbnail):
		##self.thumbPreview=QtGui.QPixmap(thumbnail).scaledToWidth(128)
		self.thumbPreview=QtGui.QPixmap(thumbnail).scaled (128, 128, QtCore.Qt.KeepAspectRatio,QtCore.Qt.SmoothTransformation)
		self.main_widget.label_sgVDBPreview.setPixmap(self.thumbPreview)
		self.main_widget.label_sgVDBPreview.setAlignment(QtCore.Qt.AlignCenter)

	def iconLibrary(self,path,name,tagsName,recent):
		## Add Icon, Add tags, and status to the main UI
		##
		iconPic = QtGui.QIcon(path)
		item = QtWidgets.QTableWidgetItem(name+","+tagsName)
		item.setIcon(iconPic)
		item.setToolTip(name)
		item.setTextAlignment(QtCore.Qt.AlignBottom)

		if recent == True:
			item.setBackground(self.itemBGFreshColor)
		else:
			item.setBackground(self.itemBGDefaultColor)
		return item

	def getSelectedIcons(self):
		listIcons = []
		selectedItems = []
		if self.currentUITab == 0:
			if self.searchMode == False:
				selectedItems = self.main_widget.tableWidget_sgElementBrowser.selectedItems()
			elif self.searchMode == True:
				selectedItems = self.main_widget.tableWidget_sgSearchBrowser.selectedItems()
		elif self.currentUITab == 1:
			selectedItems = self.main_widget.tableWidget_sgCollectionBrowser.selectedItems()
		for item in selectedItems:
			if self.searchMode == False:
				pathImage = self.dicPaths[str(item.row())+str(item.column())][0]["preview"]
				nameAsset = self.dicPaths[str(item.row())+str(item.column())][0]["name"]
			else:
				pathImage = self.dicPathsSearch[str(item.row())+str(item.column())][0]["preview"]
				nameAsset = self.dicPathsSearch[str(item.row())+str(item.column())][0]["name"]

			nameFile = os.path.basename(os.path.realpath(pathImage))
			listIcons.append(nameFile)
		return listIcons

	def showZoomThumbnail(self,row,column):
		idCell = str(row)+str(column)
		if self.searchMode == False:
			self.picturePath = self.dicPaths[idCell][0]["preview"]
			self.nameSelection = self.dicPaths[idCell][0]["name"]
			self.folderSelection = self.dicPaths[idCell][0]["path"]
		else:
			self.picturePath = self.dicPathsSearch[idCell][0]["preview"]
			self.nameSelection = self.dicPathsSearch[idCell][0]["name"]
			self.folderSelection = self.dicPathsSearch[idCell][0]["path"]

		##self.main_widget.label_sgThumbnail.setMouseTracking(True)
		if self.pilLoaded == True:
			try:
				img = Image.open(self.picturePath)
				img.show()
			except:
				print ("PIL not installed")
	
	def searchLibrary(self):
		self.listSearch=[]
		if not self.main_widget.lineEdit_sgPergamonLibrary_search.text()== "":
			self.searchMode= True
			##self.main_widget.tableWidget_sgSearchBrowser.setFixedWidth(self.main_widget.tableWidget_sgElementBrowser.width())
			##self.main_widget.tableWidget_sgSearchBrowser.setFixedHeight(self.main_widget.tableWidget_sgElementBrowser.height())
			self.main_widget.tableWidget_sgSearchBrowser.setVisible(True)
			self.main_widget.tableWidget_sgSearchBrowser.setEnabled(True)
			self.main_widget.tableWidget_sgElementBrowser.setVisible(False)
			self.main_widget.tableWidget_sgElementBrowser.setEnabled(False)
			self.main_widget.tableWidget_sgElementBrowser.clearSelection()

			items = self.main_widget.tableWidget_sgElementBrowser.findItems(self.main_widget.lineEdit_sgPergamonLibrary_search.text(),QtCore.Qt.MatchContains)
			#QtCore.Qt.MatchContains
			#QtCore.Qt.MatchWildcard
			#QtCore.Qt.MatchFixedString
			# if items:
					# print ("Found a search")
			# else:
					# print("Found Nothing")
			for item in items:
				cell = str(item.row())+str(item.column())
				self.listSearch.append(self.dicPaths[cell][0]["preview"])

			self.librarySearchBrowser()
					##results = "\n".join('row %d column %d' % (item.row() + 1, item.column() + 1)for item in items)
					##print results
		else:
			self.searchMode = False
			self.main_widget.tableWidget_sgSearchBrowser.setVisible(False)
			self.main_widget.tableWidget_sgSearchBrowser.setEnabled(False)
			self.main_widget.tableWidget_sgSearchBrowser.clearSelection()
			self.main_widget.tableWidget_sgElementBrowser.setVisible(True)
			self.main_widget.tableWidget_sgElementBrowser.setEnabled(True)

			## UI Display Status back to default
			self.main_widget.lineEdit_sgDisplayMessage.setText("")

	def manageToolTipIcon(self,dataJsonMegascan):
		#
		self.main_widget.label_sgThumbnail.setToolTip(json.dumps(dataJsonMegascan,indent = 4))

	def updateTextureEntryTypeUI(self):
		# get the radio button the send the signal
		rb = self.sender()
		self.rbNewTextureEntryType = rb.objectName()
 
		# check if the radio button is checked
		# if rb.isChecked():
		# 	print(f'You selected {rb.text()}')

	def updateDMPEntryTypeUI(self):
		# get the radio button the send the signal
		rb = self.sender()
		self.rbNewDMPEntryType = rb.objectName()
 
		# check if the radio button is checked
		# if rb.isChecked():
		# 	print(f'You selected {rb.text()}')

	def updateATBEntryTypeUI(self):
		rb = self.sender()
		self.rbNewATBEntryType = rb.objectName()

	def fillOCIOComboBox(self):
		self.main_widget.comboBox_sgLTOCIO.addItems(self.defaultOCIO)
		self.main_widget.comboBox_sgDMPOCIO.addItems(self.defaultOCIO)

	def addNewCategoryFolder(self):
		## Launch UI
		self.inputNameDialog = sgInputNameDialog()
		self.inputNameDialog.exec_()
		## Get Result Input
		name = self.inputNameDialog.text.text()
		if name != "":
			self.createNewFolder(self.selectedPath[0]+name)
			# Refresh Library
			self.refreshLibrary()
			#self.refreshTreeView()
		else:
			print("Name invalid, please write a valid name")

	def removeCategoryFolder(self,path):
		# Get Confirmation
		confirm = self.getUserConfirmation("You are about to delete: " + path + " and all his content")
		if confirm :
			# Find the Preview Image
			listPreviewInFolder = glob.glob(os.path.join(self.libraryPath,path) + "/**/*_Preview.*",recursive = True)

			for filename in listPreviewInFolder:
				# Find Key
				nameToDelete = os.path.basename(filename)
				# Remove From Database
				deletedEntryAssetDic = self.removeItemFromAssetDatabase(nameToDelete)
				deletedEntryGlobalDic = self.removeItemFromGlobalDatabase(nameToDelete)
				if deletedEntryAssetDic:
					print("Removed element: " + nameToDelete + " - Successful")

			# Save Database
			fcn.saveAssetDatabase(self.databaseAssetsJson,self.dicAssetDatabase)
			self.dicAllDatabase = fcn.saveGlobalDatabase(self.dicAllDatabase,self.databaseJson,self.dicAssetDatabase,self.dicMegascansZip)
			# Remove Folder / For now no check
			deletedFolder = self.deleteFolderLibrary( os.path.join(self.libraryPath,path))
			print("Removed folder: " +  os.path.join(self.libraryPath,path) + " - Successful")
			# Update UI
			self.refreshTreeView()
		
#######################################################################################################################
################################################### OS Utils ##########################################################
#######################################################################################################################

	def listFolders(self,path):
		folders = glob.glob(path+ "*/")
		return folders

	def findNameFile(self,path):
		nameFile = os.path.basename(os.path.realpath(path))
		return nameFile

	def renameDuplicates(self):
		#Find all objects that have the same shortname as another for Maya
		#We can indentify them because they have | in the name
		duplicates = [f for f in cmds.ls(ln=False) if '|' in f]
		#Sort them by hierarchy so that we don't rename a parent before a child.
		duplicates.sort(key=lambda obj: obj.count('|'), reverse=True)

		#if we have duplicates, rename them
		if duplicates:
			for name in duplicates:
				# extract the base name
				m = re.compile("[^|]*$").search(name)
				shortname = m.group(0)
				# extract the numeric suffix
				m2 = re.compile(".*[^0-9]").match(shortname)
				if m2:
					stripSuffix = m2.group(0)
				else:
					stripSuffix = shortname

				digit = [int(s) for s in name.split() if s.isdigit()]
				lastLetter = name[-1]
				try:
					#rename, adding '#' as the suffix, which tells maya to find the next available number
					newname = cmds.rename(name, (stripSuffix + "##"))
					print("renamed %s to %s" % (name, newname))
				except:
					e = sys.exc_info()
					print(e)
					print("Couldn't rename: " + name)

	def sequencesStringifier(self,sequences):
		output_string = ''
		dictSequences = {}
		for key, seq_info in sequences.items():
			if not seq_info:
				output_string += '{}\n'.format(key)
				continue
			if in_maya:
				stringIndexSequence = "####"
			else:
				stringIndexSequence = "####"

			if seq_info['start_index'] == seq_info['end_index']:
				output_string += '{}.{}.{}\n'.format(key,
													stringIndexSequence,
													seq_info['ext'])
				continue
			# seq_info['start_index_str']
			output_string += '{}.{}.{}, [{}-{}]\n'.format(key,
														stringIndexSequence,
														seq_info['ext'],
														seq_info['start_index'],
														seq_info['end_index'])
			
			dictSequences[seq_info['path']+key+"."+stringIndexSequence+"."+seq_info['ext']] = {
				'path':seq_info['path'],
				'ext': seq_info['ext'],
				'start_index_str': stringIndexSequence,
				'start_index': seq_info['start_index'],
				'end_index': seq_info['end_index'],
				}

		return dictSequences

	def findImageSequences(self,directory):
		'''
		sequences get put into arrays like so:
		[x_folder, z_folder, [test_a.000.png, 0, 2], [test_b.000.tif, 0, 3], test_C.000.png]
		:return: [file1, file2, [first_file, seq_start, seq_end]]
		'''
		self.SEQUENCE_PATTERN = r'(.*)\.([0-9]+).(.{3,4})$'
		sequences = {}
		sorted_candidate_list = sorted(os.listdir(directory))

		for candidate_path in sorted_candidate_list:
			full_candidate_path = os.path.join(directory, candidate_path)
			if not os.path.isfile(full_candidate_path):
				sequences[candidate_path] = None
				continue

			matches = re.match(self.SEQUENCE_PATTERN, candidate_path)
			if not matches:
				sequences[candidate_path] = None
				continue

			filename = matches.group(1)
			sequence_index = matches.group(2)
			extension = matches.group(3)

			if not extension in self.listImagefileExtension:
				sequences[candidate_path] = None
				continue

			if not filename in sequences:
				sequences[filename] = {
				'path':directory,
				'ext': extension,
				'start_index_str': sequence_index,
				'start_index': int(sequence_index),
				'end_index': int(sequence_index),
				}
				continue

			sequences[filename]['end_index'] = int(sequence_index)

		return self.sequencesStringifier(sequences)

#######################################################################################################################
###################################################### Sync ###########################################################
#######################################################################################################################

	def startAmandaServices(self):
		try:
			from mpc.amanda.client.amandaProxy import amandaProxy
			global _services
			_services = amandaProxy()
			self.amandaServices = True
			print("Sync Services have started correctly")
		except:
			print("Sync Services not started")
			self.amandaServices = False

	def initMegascansSync(self,enabled):
		# Save status button
		self.userPreferencesWrite()
		# Start Services
		if enabled and self.amandaServices != True:
			self.startAmandaServices()

		if self.amandaServices == True and enabled == True:
			self.frameSyncColor("green")
		elif self.amandaServices == False and enabled == True:
			self.frameSyncColor("red")
		elif self.amandaServices == False and enabled == False:
			self.frameSyncColor("black")
		elif self.amandaServices == True and enabled == False:
			self.frameSyncColor("black")
		
	def syncAll(self):
		i = 0
		self.dicSyncFile= {}
		for key in sorted(self.dicMegascansZip.keys()):
			path = self.dicMegascansZip[key][0]["zipFile"]
			# if i < 6000:
			sourceSite = self.findSourceSite(path)
			if len(sourceSite) != len(self.sitesMPC):
				missingSite = list(set(self.sitesMPC).difference(set(sourceSite)))
				self.dicSyncFile[key] = {"zipFile":path, "sourceSite":sourceSite,"destinationSite":missingSite}
			# i += 1
		# print(self.dicSyncFile)

		syncIDs = self.syncData(self.dicSyncFile)
		print(syncIDs)

	def syncUpdate(self,listZip):
		self.dicSyncFile= {}
		if listZip:
			print("Megascan(s) syncing: ")
		for zipFile in listZip:
			sourceSite = self.findSourceSite(zipFile)
			if len(sourceSite) != len(self.sitesMPC):
				missingSite = list(set(self.sitesMPC).difference(set(sourceSite)))
				self.dicSyncFile[zipFile] = {"zipFile":zipFile, "sourceSite":sourceSite,"destinationSite":missingSite}
				print("- " + zipFile)
		syncIDs = self.syncData(self.dicSyncFile)
		if syncIDs:
			print("Sync ID(s): ")
			print(syncIDs)
			
	def findSourceSite(self,path):
		sourceSite = []
		for site in self.sitesMPC:
			checkSource = _services.MultisiteQueue.shouldSync([path],site)
			if not checkSource[path]:
				sourceSite.append(site)
				# print("Found site: " + site)
				# break
		return sourceSite

	def syncData(self,dictionarySync):
		syncIDs=[]
		for key in sorted(dictionarySync.keys()):
			zipFile = dictionarySync[key]["zipFile"]
			source = dictionarySync[key]["sourceSite"][0]
			destinations = dictionarySync[key]["destinationSite"]
			for destination in destinations:
				try:
					pathSyncStatusInfo =  _services.MultisiteQueue.queue_add_batch(user = self.username, sources = zipFile,targetSite = destination, sourceSite = source,priority = "9")
					for idx,status in enumerate(pathSyncStatusInfo):
						success = bool(status[0])
						if success:
							syncIDs.append(int(status[1]))
							# print(zipFile,int(status[1]))
						else:
							print(zipFile,int(status[0]))
				except:
					print("Could not sync: " + zipFile)
		return syncIDs

#######################################################################################################################
##################################################### Database ########################################################
#######################################################################################################################

	def generateUUID(self):
		return str(uuid.uuid1())+self.databaseSeparator 

	def launchBuildDatabase(self):
		self.dicAllDatabase,self.dicAssetDatabase = fcn.buildDatabase(self.jsonInfoFileExtension,self.databaseJson,self.dicAllDatabase,self.databaseAssetsJson,self.dicAssetDatabase,self.dicMegascansZip,self.libraryPath,self.artBookLibraryPath,self.collectionLibraryPath,self.iesLibraryPath,self.modelLibraryPath,self.lightrigLibraryPath,self.metaHumanLibraryPath,self.dmpLibraryPath,self.textureLibraryPath,self.shaderLibraryPath,self.vdbLibraryPath)

	def launchRebuildMegascansDatabase(self):
		fcn.rebuildMegascansLibrary(self.libraryPath,self.databaseMegascansJson)

	def launchCleanUpDatabase(self):
		fcn.cleanUpDatabase(self.dicMegascansZip)

	def loadDatabase(self,jsonFile):
		if os.path.exists(jsonFile):
			self.dicAllDatabase = self.readJsonInfos(jsonFile)
		else:
			print("Global Database Json File doesn't exist")

	def loadAssetDatabase(self,jsonFile):
		if os.path.exists(jsonFile):
			self.dicAssetDatabase = self.readJsonInfos(jsonFile)
		else:
			print("Assets Database Json File doesn't exist")

	def loadMegascansDatabase(self):
		# Load Megascans "Database" Need all the check here
		if os.path.exists(self.databaseMegascansJson):
			self.dicMegascansZip = self.readJsonInfos(self.databaseMegascansJson)
		else:
			print("Megascans Database Json File doesn't exist")

		# print(self.dicMegascansZip.keys())

	def initLoadingDatabase(self):
		print(' ---- Database Initialisation ---- ')
		print("Database path: " +  self.databaseJson)

		self.loadAssetDatabase(self.databaseAssetsJson)
		print('Asset Database Loaded ')

		self.loadMegascansDatabase()
		print('Megascans Database Loaded ' )

		self.loadDatabase(self.databaseJson)
		print('Global Database Loaded ')

	def reloadAllDatabase(self):
		self.loadAssetDatabase(self.databaseAssetsJson)
		self.loadMegascansDatabase()
		self.loadDatabase(self.databaseJson)

	def searchDictionary(self,dictionary,value):
		# time01 = time.time()
		keyList =[]
		itemList= dictionary.items()
		for itemKeys in itemList:
			for item in itemKeys[1][0].items():
					if item[0] == "refPath" and item[1]+"/" == value:
						keyList.append(self.libraryPath+ item[1] + "/" + itemKeys[0])

		time02 = time.time()
		# print(time02-time01)
		return keyList

	def removeItemFromAssetDatabase(self,key):
		del self.dicAssetDatabase[key]
		return True
		#print("Removed " + key)

	def removeItemFromGlobalDatabase(self,key):
		del self.dicAllDatabase[key]
		return True
		#print("Removed " + key)

	def addBatchTextureToDatabase(self,data,path,category,tags,notes,ocio):
		nameAsset = ""
		path = path.replace("//","/")
		path = path.replace(os.sep,"/")
		fullPathTmp = os.path.join(path,category)
		typeAsset = path.split("/")[-2]
		categoryDB = fullPathTmp.split(typeAsset)[-1].split("/")[0]
		timeEntry = time.time()
		extraFiles = []
		textures = []

		for key,value in data.items():
			listExtension = data[key][0]['extension']
			listTextures = data[key][0]['list textures']
			uuid = data[key][0]['uuid']
			icon =  uuid + key + "_Preview.png"
			iconName =  key + "_Preview.png" 
			jsonFile = key + self.jsonInfoFileExtension
			nameAsset = key
			fullPath = os.path.join(fullPathTmp,nameAsset)
			fullPath = fullPath.replace("//","/")
			fullPath = fullPath.replace(os.sep,"/")
			subType = fullPath.split(typeAsset)[-1].split(nameAsset)[0]

			print("Name: " + nameAsset,"Path: " + fullPath,"Type: " + typeAsset,"CatDB: " + categoryDB,"SubType: " + subType, "Icon: " + iconName)
			
			self.dicAssetDatabase= fcn.addEntryToAssetDatabase(self.dicAssetDatabase,self.databaseAssetsJson,self.libraryPath,nameAsset,icon,iconName,uuid,jsonFile,fullPath,typeAsset,timeEntry,listExtension,extraFiles,listTextures,tags,listTextures)

		# Save Database
		fcn.saveAssetDatabase(self.databaseAssetsJson,self.dicAssetDatabase)
		self.dicAllDatabase = fcn.saveGlobalDatabase(self.dicAllDatabase,self.databaseJson,self.dicAssetDatabase,self.dicMegascansZip)
		
		## Congrats
		message = "Congrats New Entry(ies) added to the library"
		self.sendMessage(message)

		# Refresh Library
		self.setBrowserTab()
		self.refreshLibrary()
		self.launchBrowsing()
		
	def getMTimeDatabase(self):
		self.assetDatabaseUpdate = os.path.getmtime(self.databaseAssetsJson)
		self.megascansDatabaseUpdate = os.path.getmtime(self.databaseMegascansJson)

	def checkTimeDatabases(self):
		updated = False
		if self.assetDatabaseUpdate != os.path.getmtime(self.databaseAssetsJson):
			self.loadAssetDatabase(self.databaseAssetsJson)
			updated = True
		if self.megascansDatabaseUpdate != os.path.getmtime(self.databaseMegascansJson):
			self.loadMegascansDatabase()
			updated = True
		if updated == True:
			print("Database Reloaded")
			## Reload database
			self.dicAllDatabase = fcn.mergeDictionaries(self.dicAssetDatabase,self.dicMegascansZip)
			# Update Time
			self.assetDatabaseUpdate = os.path.getmtime(self.databaseAssetsJson)
			self.megascansDatabaseUpdate = os.path.getmtime(self.databaseMegascansJson)
		
################################################# Open In Explorer ####################################################

	def openFileInExplorer(self,filepath):
		if self.platform == "win32" or self.platform == "win64" :
			os.popen('start explorer "%s" ' % os.path.abspath(filepath))
			# subprocess.Popen(f'explorer /select,"{filepath}"')
		elif self.platform == "linux2" or self.platform == "linux":
			print("Opening: ", filepath)
			if in_nuke:
				os.system('xdg-open "%s" ' % os.path.abspath(filepath))
			else:
				if os.path.isdir(os.path.abspath(filepath)):
					os.system('caja "%s" ' % os.path.abspath(filepath))
				elif os.path.isfile(os.path.abspath(filepath)):
					os.system('xdg-open "%s" ' % os.path.abspath(filepath))

	def openSelectFileInExplorer(self):
		# Find Zip
		if self.currentUITab == 0:
			item = self.main_widget.tableWidget_sgElementBrowser.selectedItems()
		elif self.currentUITab == 1:
			item = self.main_widget.tableWidget_sgCollectionBrowser.selectedItems()
		if self.searchMode == False:
			pathImage = self.dicPaths[str(item[0].row())+str(item[0].column())][0]["preview"]
		else:
			pathImage = self.dicPathsSearch[str(self.searchRow)+str(self.searchColumn)][0]["preview"]

		nameIcon= pathImage.split("/")[-1]
			
		## Find zip in dictionary - search in entire database
		pathZip = str(self.dicAllDatabase[nameIcon][0]["zipFile"] )

		# open explorer with file selected
		if self.platform == "win32" or self.platform == "win64" :
			os.popen('start explorer /select ,"%s" ' % os.path.abspath(pathZip))
		if self.platform == "linux" or self.platform == "linux2":
			os.system('nautilus --select "%s" ' % os.path.abspath(pathZip))
			#os.system('caja --select "%s" ' % os.path.abspath(pathZip))

	def openListFilesInExplorer(self,listPath):
		# open explorer from a list
		stringFile = '""' + ','.join(listPath) + '"'
		for pathZip in listPath:
			if self.platform == "win32" or self.platform == "win64" :
				os.popen('start explorer /select ,"%s" ' % os.path.abspath(pathZip))
			if self.platform == "linux" or self.platform == "linux2":
				os.system('caja --select "%s" ' % os.path.abspath(pathZip))
		# self.listErrorZip

	def openMegascansErroredInExplorer(self):
		self.megascanZIPLibraryPath
		listPath = [os.path.join(self.megascanZIPLibraryPath,m) for m in self.listErrorZip]

		self.openListFilesInExplorer(listPath)
		
#######################################################################################################################
################################################# Message To User #####################################################
#######################################################################################################################

	def sendMessage(self,message):
		## Launch Message UI
		self.messageDialog = sgShowMessageUser()
		self.messageDialog.setMessage(message)
		
		## Get Confirmation Dialog
		approval = self.messageDialog.exec_()
		if approval == QtWidgets.QMessageBox.Ok:
			return True
		elif approval == QtWidgets.QMessageBox.Cancel:
			return False

	def getUserConfirmation(self,message):
		## Launch Message UI
		self.confirmationDialog = sgConfirmationMessage()
		self.confirmationDialog.setMessage(message)
		
		## Get Confirmation Dialog
		approval = self.confirmationDialog.exec_()
		if approval == QtWidgets.QMessageBox.Ok:
			return True
		elif approval == QtWidgets.QMessageBox.Cancel:
			return False

#######################################################################################################################
################################################ Browser Management ###################################################
#######################################################################################################################

	def setBrowsers(self):
		## Reset Search as change of selection
		self.main_widget.lineEdit_sgPergamonLibrary_search.setText("")
		self.searchLibrary()
		## Element Browser
		self.elementBrowserWidth = self.main_widget.tableWidget_sgElementBrowser.width()
		self.maxColumnModels =  int(round(self.elementBrowserWidth/136))-1
		if self.context== "Collections":
			self.maxColumnModels =1
			# Element Browser
			# if self.searchMode == False:
			self.main_widget.tableWidget_sgElementBrowser.setColumnCount(2)
			self.main_widget.tableWidget_sgElementBrowser.horizontalHeader().setDefaultSectionSize( int(self.elementBrowserWidth/2-10))
			self.main_widget.tableWidget_sgElementBrowser.verticalHeader().setDefaultSectionSize( int(self.elementBrowserWidth/4))
			self.main_widget.tableWidget_sgElementBrowser.setIconSize(QtCore.QSize( int(self.elementBrowserWidth/2), int(self.elementBrowserWidth/2)))
			#Search Browser
			# elif self.searchMode == True:
			self.main_widget.tableWidget_sgSearchBrowser.setColumnCount(2)
			self.main_widget.tableWidget_sgSearchBrowser.horizontalHeader().setDefaultSectionSize( int(self.elementBrowserWidth/2-10))
			self.main_widget.tableWidget_sgSearchBrowser.verticalHeader().setDefaultSectionSize( int(self.elementBrowserWidth/4))
			self.main_widget.tableWidget_sgSearchBrowser.setIconSize(QtCore.QSize( int(self.elementBrowserWidth/2), int(self.elementBrowserWidth/2)))
		else:
			self.maxColumnModels = int(round(self.elementBrowserWidth/136))-1
			# Element Browser
			self.main_widget.tableWidget_sgElementBrowser.setColumnCount(self.maxColumnModels+1)
			self.main_widget.tableWidget_sgElementBrowser.horizontalHeader().setDefaultSectionSize(128)
			self.main_widget.tableWidget_sgElementBrowser.verticalHeader().setDefaultSectionSize( 128 )
			self.main_widget.tableWidget_sgElementBrowser.setIconSize(QtCore.QSize(128, 128))
			## Search Browser
			self.main_widget.tableWidget_sgSearchBrowser.setColumnCount(self.maxColumnModels+1)
			self.main_widget.tableWidget_sgSearchBrowser.horizontalHeader().setDefaultSectionSize(128)
			self.main_widget.tableWidget_sgSearchBrowser.verticalHeader().setDefaultSectionSize( 128 )
			self.main_widget.tableWidget_sgSearchBrowser.setIconSize(QtCore.QSize(128, 128))

		## Collections Browser is done in the libraryCollectionBrowser Module

	def launchBrowsing(self):
		if self.currentUITab == 1:
			self.main_widget.libraryTab.setCurrentIndex(0)
		self.getLibContext()
		self.libraryItemBrowser()
	
	def librarySearchBrowser(self):
		column = 0
		self.dicPathsSearch = {}

		self.main_widget.tableWidget_sgSearchBrowser.clearContents()
		self.main_widget.tableWidget_sgSearchBrowser.setRowCount(0)
		sizeFitem = len(self.listSearch)
		
		if len(self.listSearch)!=0:
			rowPosition = self.main_widget.tableWidget_sgSearchBrowser.rowCount()
			self.main_widget.tableWidget_sgSearchBrowser.insertRow(rowPosition)
			for icon in self.listSearch:
				assetName = os.path.basename(icon).split(self.thumbnailSuffix)[0].split(self.databaseSeparator)[-1]

				tags = ""
				if "Megascans" in icon:
					path = icon.split(assetName)[0]
				else:
					path = icon.split(assetName)[0]+assetName+"/"

				pathPreviewImage = icon
				recent = self.compareTimeModification(icon)
				item = self.iconLibrary(pathPreviewImage,assetName,tags,recent)

				self.main_widget.tableWidget_sgSearchBrowser.setItem(rowPosition, column, item)

				##Create my dictionnary with infos
				cell = str(rowPosition)+str(column)
				self.dicPathsSearch[cell]= []
				self.dicPathsSearch[cell].append({
				'preview':icon,
				'path':path,
				'name':assetName,
				})

				## Change Columns
				column +=1
				if column>self.maxColumnModels:
					column =0
					rowPosition = self.main_widget.tableWidget_sgSearchBrowser.rowCount()
					self.main_widget.tableWidget_sgSearchBrowser.insertRow(rowPosition)

		####################################### UI ############################################
		self.main_widget.tableWidget_sgSearchBrowser.setMouseTracking(True)
		self.main_widget.tableWidget_sgSearchBrowser.viewport().installEventFilter(self)
		self.main_widget.lineEdit_sgDisplayMessage.setText("Found: " + str(sizeFitem) + " item(s)" )
		
		#self.actionSearchMenuUpdateUI()

	def libraryItemBrowser(self):
		startTime = time.time()
		self.resizeEventHappened = False
		self.rowPosition = 0
		self.iconAmount = 0
		sizeFitem = 0
		column = 0
		self.listModelsIcons = []
		self.listModelsTags = []
		listDataTags = []
		listDir=[]
		self.dicElementPaths = {}
		self.modelPathsRC = []

		############################################### Clear UI #######################################################
		self.main_widget.tableWidget_sgElementBrowser.clearContents()
		self.main_widget.tableWidget_sgElementBrowser.setRowCount(0)

		################################################################################################################

		if self.main_widget.treeWidget_sgLibrary.currentItem() and self.main_widget.libraryTab.currentIndex() == 0:
			# Update selected treePath
			self.getLibContext()
			# Check if database has not been updated:
			self.checkTimeDatabases()
			exclude = [".mayaSwatches"]
			include = ["renderman","arnold","unreal","vray","prod","previs"]

			############## Change Size Icons For Collections
			self.setBrowsers()

			############### Parse folder to find the Preview file For Python2
			if os.path.exists(self.selectedPath[0]):
					##### Method 3 in between solution fastest so far but don't cover the all hierarchy
					folders = glob.glob(self.selectedPath[0]+"*/")
					if folders:
						for path in folders:
							path = path.replace(os.sep, '/')
							## Will list from Top Category
							if self.context == "IES" or self.context == "DMP" or self.context == "ArtBooks" or self.context == "VDB":
								if os.path.isdir(path):
									for subfolder in glob.glob(path+"*/"):
										if subfolder not in folders:
											folders.append(subfolder)
							elif self.subContext in include:
								if os.path.isdir(path):
									for subfolder in glob.glob(path+"*/"):
										if subfolder not in folders:
											folders.append(subfolder)
							for fileP in glob.glob(path +"/*_Preview.*"):
								## Windows fix
								fileP = fileP.replace(os.sep, '/')
								if ".uasset" not in fileP:
									self.listModelsIcons.append(fileP)
					else:
						for fileP in glob.glob(self.selectedPath[0]+"/*_Preview.*"):
							## Windows fix
							fileP = fileP.replace(os.sep, '/')
							self.listModelsIcons.append(fileP)

					##### Method 4 for python > 3.5
					# for path in glob.glob(self.selectedPath[0]+"*_Preview.*", recursve = True):
					# self.listModelsIcons.append(path)

					self.listModelsIcons.sort()
					amountTotalOfRows = math.ceil(len(self.listModelsIcons)/float(self.maxColumnModels+1))
					self.amountOfRows = amountTotalOfRows
					if amountTotalOfRows > 10:
						self.lazyLoading = True
					else:
						self.lazyLoading = False
					################################### UI Progress Bar #################################
					progressBarValue = 0
					sizeFitem = len(self.listModelsIcons)
					if sizeFitem != 0 :
						percentage = float(100/sizeFitem)
					else:
						percentage = 1
					self.main_widget.progressBar_sgLoading.setValue(progressBarValue)
					self.main_widget.progressBar_sgLoading.setTextVisible(True)
					self.main_widget.progressBar_sgLoading.setFormat("Loading... "+'%p%')
					self.main_widget.progressBar_sgLoading.setAlignment(QtCore.Qt.AlignCenter)

					######################################################################################
					
					self.main_widget.tableWidget_sgElementBrowser.setRowCount(self.amountOfRows)
					self.main_widget.tableWidget_sgElementBrowser.setSortingEnabled(False)
					sizeFitem = len(self.listModelsIcons)
					if sizeFitem!=0:
						self.rowPosition = 0
						for index in range(self.iconAmount,sizeFitem):
						# for icon in self.listModelsIcons:
							############################## Lazy Loading #########################
							# if self.lazyLoading == True and (self.maxColumnModels+1)*10 < self.iconAmount-self.maxColumnModels:
								# break
								# self.main_widget.tableWidget_sgElementBrowser.hideRow(self.rowPosition)
							icon = self.listModelsIcons[index]
							iconName = os.path.basename(icon)
							################################ UI #################################
							progressBarValue += percentage
							self.main_widget.progressBar_sgLoading.setValue(int(progressBarValue))
							#####################################################################
							idPos = str(self.rowPosition)+str(column)
							assetName = os.path.basename(icon).split(self.thumbnailSuffix)[0].split(self.databaseSeparator)[-1]
							tagsName = ""
							self.originalName = ""
							
							# If not in database will continue 
							if iconName in self.dicAllDatabase:
								if self.context =="Megascans":
									path = os.path.join(self.libraryPath, self.dicAllDatabase[iconName][0]["refPath"])+"/"
									tagsName = ",".join(self.dicAllDatabase[iconName][0]["tags"])	
								else:
									path = os.path.join(self.libraryPath, self.dicAllDatabase[iconName][0]["refPath"], assetName)+"/"
									path = path.replace(os.sep,"/")
									jsonFilename= assetName+self.jsonInfoFileExtension
									data = self.readJsonInfos(os.path.join(path,jsonFilename))
									if data:
										tagsName = data['releaseInfos'][0]['tags']
							else:
								continue

							######################################################################
							pathPreviewImage = icon
							recent = self.compareTimeModification(icon)
							if recent == True:
								tagsName += ",update,new"
							tagsName = tagsName.replace(" ", "")
							self.allSearchTags += tagsName.lower().split(",")
							item = self.iconLibrary(pathPreviewImage,assetName,tagsName,recent)
							##################### Check the action menu per object ###############
							# self.main_widget.tableWidget_sgElementBrowser.setCellWidget(rowPosition, column, item)
							self.main_widget.tableWidget_sgElementBrowser.setItem(self.rowPosition, column, item)
							####################### Create my dictionnary with infos ##############
							self.dicElementPaths[idPos]= []
							self.dicElementPaths[idPos].append({
							'preview':pathPreviewImage,
							'path':path,
							'name':assetName,
							})
							######################### Change Columns ##############################
							column +=1
							if column>self.maxColumnModels:
								column =0
								self.rowPosition += 1
							self.iconAmount +=1

			self.dicPaths = self.dicElementPaths
			self.allSearchTags = list(set(self.allSearchTags))
			###################### UI ##########################
			self.main_widget.progressBar_sgLoading.setValue(100)
			self.progressBarFinish(timeSleep = 0.02)
			endTime = time.time()
			elapsed= endTime-startTime
			self.main_widget.lineEdit_sgDisplayMessage.setText(str(self.iconAmount )+"/" + str(sizeFitem)+ " item(s) available, loaded in: " + str("%.3f" % elapsed) + " seconds")
			self.main_widget.tableWidget_sgElementBrowser.setSortingEnabled(True)

		else:
			try:
				self.selectedPath = self.selectTreeItem()
				self.context = self.selectedPath[1]

				tmpContext = self.selectedPath[0].replace(self.libraryPath,"")
				if len(tmpContext.split("/")) == 4:
					self.subContext = self.selectedPath[0].split("/")[-3]
					self.categoryContext = self.selectedPath[0].split("/")[-2]
				elif len(tmpContext.split("/")) == 3:
					self.subContext = self.selectedPath[0].split("/")[-2]
					self.categoryContext = os.path.basename(self.selectedPath[0])
					
				else:
					self.subContext = ""
					self.categoryContext = ""
			except:
				#print("No subcontext or category context selected")
				#print(sys.exc_info())
				pass

	def libraryCollectionBrowser(self):
		startTime = time.time()
		column = 0
		folders=[]
		self.listModelsIcons = []
		self.listModelsTags = []
		self.dicCollectionPaths = {}
		listDataTags = []
		self.modelPathsRC = []
		########################################## Clear UI ########################################################
		self.main_widget.tableWidget_sgCollectionBrowser.clearContents()
		self.main_widget.tableWidget_sgCollectionBrowser.setRowCount(0)

		## Collection Browser Set up Needs to be done here
		if self.currentUITab == 0 :
			self.collectionBrowserWidth = self.main_widget.tableWidget_sgElementBrowser.width()
		elif self.currentUITab ==1:
			self.collectionBrowserWidth = self.main_widget.tableWidget_sgCollectionBrowser.width()
			
		self.maxColumnModels = int(round(self.collectionBrowserWidth/136))-1

		self.main_widget.tableWidget_sgCollectionBrowser.setColumnCount(self.maxColumnModels+1)
		self.setCollectionHeaderUI()
		############################################################################################################

		self.context = "Collections"
		selectedPath = self.collectionLibraryPath + self.collectionSelection
		self.subContext = ""
		self.categoryContext = ""
		################################# Find Icons ############################
		if os.path.exists(selectedPath):
			jsonCollection = glob.glob(selectedPath+"/*ollection.json")
			if jsonCollection:
				dataCollection = self.readJsonInfos(jsonCollection[0])
				for key in dataCollection:
					## Get path of
					refPath = dataCollection[key][0]["refPath"]
					typeAsset = dataCollection[key][0]["type"]
					subTypeAsset = dataCollection[key][0]["subType"]
					category = dataCollection[key][0]["category"]
					name = dataCollection[key][0]["name"]
					previewImage = key
					if typeAsset == "Megascans":
						pathToAsset = self.libraryPath+"/"+ typeAsset+"/"+ subTypeAsset+"/"+ category + "/"
					else:
						pathToAsset = self.libraryPath+"/"+ refPath + "/"+ name + "/"
					self.listModelsIcons.append(os.path.join(pathToAsset,previewImage))
			else:
				dataCollection=""

			# self.listModelsIcons.sort()
			sizeFitem = len(self.listModelsIcons)
			if sizeFitem!=0:
				amountOfRows =math.ceil(len(self.listModelsIcons)/float(self.maxColumnModels+1))
			else:
				amountOfRows = 0

			############################### UI Progress Bar #####################################
			
			progressBarValue = 0
			if len(self.listModelsIcons) != 0 :
				percentage = float(100/sizeFitem)
			else:
				percentage = 1
			self.main_widget.progressBar_sgLoading.setValue(progressBarValue)
			self.main_widget.progressBar_sgLoading.setTextVisible(True)
			self.main_widget.progressBar_sgLoading.setFormat("Loading... "+'%p%')
			self.main_widget.progressBar_sgLoading.setAlignment(QtCore.Qt.AlignCenter)

			self.main_widget.tableWidget_sgCollectionBrowser.setRowCount(amountOfRows)
			self.main_widget.tableWidget_sgCollectionBrowser.setSortingEnabled(False)

			#####################################################################################
			if sizeFitem!=0:
				self.rowPosition = 0
				for icon in self.listModelsIcons:
					# Clean up path
					icon = icon.replace("//","/")
					########################## UI #########################
					progressBarValue += percentage
					self.main_widget.progressBar_sgLoading.setValue(int(progressBarValue))
					
					idPos = str(self.rowPosition)+str(column)
					imageName = os.path.basename(icon)
					assetName = imageName.split(self.thumbnailSuffix)[0].split(self.databaseSeparator)[-1]
					
					typeContextAsset = icon.split(self.libraryPath)[-1].split("/")[0]
					
					tagsName =""
					self.originalName = ""
					################### Get Data ##########################
					if typeContextAsset == "Megascans":
						path = icon.split(assetName)[0]
					else: 
						path = os.path.join(icon.split(assetName)[0],assetName)+"/"
						#path = os.path.join(self.libraryPath, self.dicAllDatabase[iconName][0]["refPath"])+"/"

					string = ""
					jsonFile = dataCollection[imageName][0]["json"]
					try:
						jsonFile = dataCollection[imageName][0]["json"]
						data = self.readJsonInfos(os.path.join(path,jsonFile))
					except:
						data = ""
						logger.error("Except %s cannot be read correctly, check corrupted json or image",icon)
						logger.error("The path of the icon us: %s",path)
					try:
						tagsName = ",".join(data['tags'])
					except:
						pass
					try:
						tagsName += ",".join(data['semanticTags']['contains'])
						tagsName += ",".join(data['semanticTags']['descriptive'])
						tagsName += ",".join(data['semanticTags']['theme'])
						self.originalName = ",".join(data['semanticTags']['name'])
					except:
						pass
					
					pathPreviewImage = icon
					recent = self.compareTimeModification(icon)
					item = self.iconLibrary(pathPreviewImage,assetName,tagsName,recent)

					##################### Check the action menu per object ###################################
					self.main_widget.tableWidget_sgCollectionBrowser.setItem(self.rowPosition, column, item)
					##################### Create my dictionnary with infos ###################################
					self.dicCollectionPaths[idPos]= []
					self.dicCollectionPaths[idPos].append({
					'preview':pathPreviewImage,
					'path':path,
					'name':assetName,
					})
					################## Change Columns and rowwhen at the end of the max columns ##############
					column +=1
					if column>self.maxColumnModels:
							column =0
							self.rowPosition += 1
			else:
				sizeFitem = 0
		self.dicPaths = self.dicCollectionPaths
		############################################ UI ######################################################
		self.main_widget.progressBar_sgLoading.setValue(100)
		# self.actionMenuUpdateUI()
		
		self.progressBarFinish(timeSleep = 0.02)
		endTime = time.time()
		timeElapsed = endTime-startTime
		self.main_widget.lineEdit_sgDisplayMessage.setText(str(sizeFitem)+ " item(s) available, loaded in: " +str("%.3f" % timeElapsed) + " seconds")

	def lazyLoadLibraryItems(self):
		#
		print (test)
	
	def changeTab(self):
		self.displayStatusMessage("")
		self.currentUITab = self.main_widget.libraryTab.currentIndex()
		if self.main_widget.libraryTab.currentIndex()== 0:
			self.dicPaths = self.dicElementPaths
		if self.main_widget.libraryTab.currentIndex()== 1:
			self.dicPaths = self.dicCollectionPaths

		if self.resizeEventHappened == True:
			self.resizeEventHappened = False

			## Update rest of UI
			if self.searchMode == False:
				self.libraryItemBrowser()
			elif self.searchMode == True:
				self.librarySearchBrowser()

		# Switch to the correct add tab
		if self.main_widget.libraryTab.currentIndex()== 2:
			self.setElementAddTab()

	def setElementAddTab(self):
		if self.context == ("Megascans"):
			self.main_widget.tabWidget_sgAddElement.setCurrentIndex(0)
		elif self.context == ("Models") or self.context == ("Lightrigs") or self.context == ("Shaders"):
			self.main_widget.tabWidget_sgAddElement.setCurrentIndex(1)
		elif self.context == ("Textures"):
			self.main_widget.tabWidget_sgAddElement.setCurrentIndex(2)
		elif self.context == ("DMP"):
			self.main_widget.tabWidget_sgAddElement.setCurrentIndex(3)
		elif self.context == ("IES"):
			self.main_widget.tabWidget_sgAddElement.setCurrentIndex(4)
		elif self.context == ("VDB"):
			self.main_widget.tabWidget_sgAddElement.setCurrentIndex(5)	
		elif self.context == ("ArtBooks") or self.context == ("Tutorials"):
			self.main_widget.tabWidget_sgAddElement.setCurrentIndex(6)		

	def refresh(self):
		print("ttt")

#######################################################################################################################
##################################################### ToolTab #########################################################
#######################################################################################################################

	def manageSuperUserFile(self,action):
		# Get UI 
		superUserUI = self.main_widget.lineEdit_sgSuperUserName.text()
		# Get List of super user
		self.listSuperUsers = self.superUsersDic["superUsers"]

		superUserDic = {}
		if action == "add":
			if superUserUI not in self.listSuperUsers and superUserUI != "":
				self.listSuperUsers.append(superUserUI)
				superUserDic = {
				"superUsers" : self.listSuperUsers
				}
				# Write file
				self.writeJsonFile(self.superUsersJson,superUserDic)

				print("Added Super User: " + superUserUI )
				self.displayStatusMessage("Added Super User: " + superUserUI )
			else:
				print("Super User already in list: " + superUserUI)
				self.displayStatusMessage("Super User already in list: " + superUserUI )

		elif action == "remove":
			if superUserUI in self.listSuperUsers and superUserUI != "":
				self.listSuperUsers.remove(superUserUI)
				superUserDic = {
				"superUsers" : self.listSuperUsers
				}
				# Write file
				self.writeJsonFile(self.superUsersJson,superUserDic)

				print("Removed Super User: " + superUserUI)
				self.displayStatusMessage("Removed Super User: " + superUserUI )
			else:
				print("Super User not in list: " + superUserUI)
				self.displayStatusMessage("Super User not in list: " + superUserUI )

	def manageTagFile(self,action):
		# Get UI 
		tagNameUI = self.main_widget.lineEdit_sgTagMngmt.text()
		# Get List of autocompleteTags
		listTags = self.standardTags
		if action == "add":
			if tagNameUI not in listTags and tagNameUI != "":
				listTags.append(tagNameUI)
				# Write file
				self.writeJsonFile(self.tagsJsonFile,listTags)
				# Reload
				self.initSearchCompleter()

				print("Added Tag: " + tagNameUI )
				self.displayStatusMessage("Added Tag: " + tagNameUI )
			else:
				print("Tag already in list: " + tagNameUI)
				self.displayStatusMessage("Tag already in list: " + tagNameUI )

		elif action == "remove":
			if tagNameUI in listTags and tagNameUI != "":
				listTags.remove(tagNameUI)
				# Write file
				self.writeJsonFile(self.tagsJsonFile,listTags)
				# Reload
				self.initSearchCompleter()

				print("Removed Tag: " + tagNameUI)
				self.displayStatusMessage("Removed Tag: " + tagNameUI )
			else:
				print("Super User not in list: " + tagNameUI)
				self.displayStatusMessage("Tag not in list: " + tagNameUI )

	def setToolTipSuperUserUI(self):
		#
		self.main_widget.lineEdit_sgSuperUserName.setToolTip(json.dumps(self.superUsersDic["superUsers"],indent = 4))
		self.main_widget.pushButton_sgSuperUserFile.setToolTip(json.dumps(self.superUsersDic["superUsers"],indent = 4))
		
	def setToolTipTagsUI(self):
		#
		self.main_widget.lineEdit_sgTagMngmt.setToolTip(json.dumps(self.standardTags,indent = 4))
		self.main_widget.pushButton_sgTagFile.setToolTip(json.dumps(self.standardTags,indent = 4))

	def selectUnzipFolder(self):
		selectedUnzipFolder = QtWidgets.QFileDialog.getExistingDirectory(self,"Choose folder to unzip files","",QtWidgets.QFileDialog.ShowDirsOnly)
		#selectedUnzipFolder.setFixedSize(1000,600)
		if selectedUnzipFolder != "":
			self.main_widget.lineEdit_sgPathUnzipMegascans.setText(str(selectedUnzipFolder)+"/")
			self.pathUnzipFolder = str(selectedUnzipFolder)+"/"
		else:
			self.pathUnzipFolder = self.main_widget.lineEdit_sgPathUnzipMegascans.text()

	def selectImageOrPDFBrowser(self,button):
		if button.objectName() == "pb_sgPathBrowser_lin":
			selectedAppBrowser = QtWidgets.QFileDialog.getOpenFileName(self,"Choose an application to browse images","","*.*")
			selectedAppBrowser.setFixedSize(1000,600)
			if selectedAppBrowser[0] != "":
				self.main_widget.lineEdit_sgPathBrowser_lin.setText(str(selectedAppBrowser[0]))
		elif button.objectName() == "pb_sgPathBrowser_win":
			selectedAppBrowser = QtWidgets.QFileDialog.getOpenFileName(self,"Choose an application to browse images","","*.exe")
			selectedAppBrowser.setFixedSize(1000,600)
			if selectedAppBrowser[0] != "":
				self.main_widget.lineEdit_sgPathBrowser_win.setText(str(selectedAppBrowser[0]))
		elif button.objectName() == "pb_sgPDFPathBrowser_lin":
			selectedAppBrowser = QtWidgets.QFileDialog.getOpenFileName(self,"Choose an application to open pdf or cbr","","*.exe")
			selectedAppBrowser.setFixedSize(1000,600)
			if selectedAppBrowser[0] != "":
				self.main_widget.lineEdit_sgPDFPathBrowser_lin.setText(str(selectedAppBrowser[0]))
		elif button.objectName() == "pb_sgPDFPathBrowser_win":
			selectedAppBrowser = QtWidgets.QFileDialog.getOpenFileName(self,"Choose an application to open pdf or cbr","","*.exe")
			selectedAppBrowser.setFixedSize(1000,600)
			if selectedAppBrowser[0] != "":
				self.main_widget.lineEdit_sgPDFPathBrowser_win.setText(str(selectedAppBrowser[0]))

	def removeLibrary(self):
		# Get UI
		selectedLibrary = self.main_widget.comboBox_sgDeleteLibrary.currentText()
		if selectedLibrary:
			# Confirm
			confirm = self.getUserConfirmation("Remove Access to Library: " + selectedLibrary + "\n" + "(It will not delete the library from the disk)")
			if confirm == True:
				# Remove Access Only
				fcn.deletePathLibrary(self.defaulPathJson,selectedLibrary)
				# Remove from UI
				itemIndex = self.main_widget.comboBox_sgDeleteLibrary.findText(selectedLibrary)
				self.main_widget.comboBox_sgDeleteLibrary.removeItem(itemIndex)

#######################################################################################################################
################################ Create a zoom picture of the icon when mouse hoover ##################################
#######################################################################################################################

	def createPixmapUI(self):
		self.pixmapMovie = QtGui.QMovie()
		self.pixmap = QtGui.QPixmap()
		self.collectionHeadPic = QtGui.QPixmap()

	def cellEnteredThumbnail(self, row, column):
		idCell = str(row)+str(column)
		try:
			if self.searchMode== False:
				picturePath = self.dicPaths[idCell][0]["preview"]
				pictureName = self.dicPaths[idCell][0]["name"]
			else:
				picturePath = self.dicPathsSearch[idCell][0]["preview"]
				pictureName = self.dicPathsSearch[idCell][0]["name"]
			
			## Switch icon from left to right of the UI
			if in_hou:
				xOffset = 25
			else:
				xOffset = 14
			## Get the position of the window in dockable and parented to a window
			gp = self.mapFromGlobal(QtCore.QPoint(0, 0))

			## Set X Position
			winXPos = abs(gp.x())
			xPos = winXPos + self.main_widget.tableWidget_sgElementBrowser.width()+ 50 + self.zoomSize[0]
			maxPos = self.screenWidth - self.main_widget.tableWidget_sgElementBrowser.width()
			
			if xPos > maxPos:
				xPos = winXPos-self.zoomSize[0]-xOffset

			## Set Y Position
			yPos = abs(gp.y())+300

			self.zoomWidget.setGeometry(xPos , yPos, self.zoomSize[0], self.zoomSize[1]+25)
			
			## Switch between gif and image
			if "gif" in picturePath:
				self.pixmapMovie.stop()
				self.pixmapMovie.setFileName(picturePath)
				self.pixmapMovie.setScaledSize(QtCore.QSize(self.zoomSize[1],self.zoomSize[1]))
				self.zoomPic.setMovie(self.pixmapMovie)
				self.pixmapMovie.start()
			else:
				self.pixmap.load(picturePath)
				self.pixmap = self.pixmap.scaled(self.zoomSize[1],self.zoomSize[1], QtCore.Qt.KeepAspectRatio,QtCore.Qt.SmoothTransformation)
				self.zoomPic.setPixmap(self.pixmap)
			self.zoomPic.setAlignment(QtCore.Qt.AlignCenter)
			self.zoomWidget.setText(pictureName)
			self.zoomWidget.show()
			
		except:
			e = sys.exc_info()
			#print(e)
			pass

	def createNewIcon(self):
		icon = QtGui.QIcon()
		return icon

#######################################################################################################################
################################################## EVENT FILTER #######################################################
#######################################################################################################################

	def eventFilter(self, widget, event):
		if event.type() is not event.Resize:
			self.timeElapse = 0
			try:
				self.timeElapse=time.time()-self.start
			except:
				pass
			if self.timeElapse > 0.2 and self.resized == True:
				self.resized = False
				self.manageResize()
		## Detext right click on QTree Item for better path init
		if event.type() is event.MouseButtonPress:
			if event.button() == QtCore.Qt.MouseButton.RightButton:
				self.mouseButtonUsed = "Right Button Used"
				#if self.main_widget.treeWidget_sgLibrary.viewport():
				#	print("Yeah!")
			elif event.button() == QtCore.Qt.MouseButton.LeftButton:
				self.mouseButtonUsed = "Left Button Used"
			# print(self.mouseButtonUsed)

		## Detect Click on Qlabel
		if event.type() is event.MouseButtonRelease or event.type() == 3:
			if widget is self.main_widget.label_sgThumbnail:
				self.openExplorer()

		## Drag and Drop temp
		if event.type() is event.DragEnter:
			print ("Drag Event")
			#self.dragEnterEvent(event)
		if event.type() is event.Drop:
			print ("Drop Event")
		if event.type() is event.DragLeave:
			print("Drag Leave")
			# self.dropEvent(event)

		## Zoom Window Closing
		if widget is self.main_widget.tableWidget_sgElementBrowser.viewport():
			if event.type() == QtCore.QEvent.Leave or event.type() == event.DragEnter:
				index = QtCore.QModelIndex()
				self.zoomWidget.close()
				QtGui.QPixmapCache.clear()
		if widget is self.main_widget.tableWidget_sgSearchBrowser.viewport():
			if event.type() == QtCore.QEvent.Leave or event.type() == event.DragEnter:
				index = QtCore.QModelIndex()
				self.zoomWidget.close()
				QtGui.QPixmapCache.clear()
		if widget is self.main_widget.tableWidget_sgCollectionBrowser.viewport():
			if event.type() == QtCore.QEvent.Leave:
				index = QtCore.QModelIndex()
				self.zoomWidget.close()
				# self.collectionWidget.close()
				QtGui.QPixmapCache.clear()
		return False

	def resizeEvent(self, event):
		self.resized = True
		self.start=time.time()

	def manageResize(self):
		self.changeTab()
		if self.currentUITab == 0:
			if self.searchMode == False:
					self.elementBrowserWidth = self.main_widget.tableWidget_sgElementBrowser.width()
					self.elementBrowserHeight = self.main_widget.tableWidget_sgElementBrowser.height()
					if self.context == "Collections":
						self.maxColumnModels = 1
					else:
						self.maxColumnModels =  int(round(self.elementBrowserWidth/136))-1
					self.setBrowsers()
					# self.libraryItemBrowser()
					# self.libraryCollectionBrowser()
			elif self.searchMode == True:
					self.searchBrowserWidth = self.main_widget.tableWidget_sgSearchBrowser.width()
					self.librarySearchBrowser()
					self.libraryCollectionBrowser()
		elif self.currentUITab == 1:
					self.collectionBrowserWidth = self.main_widget.tableWidget_sgCollectionBrowser.width()
					self.collectionBrowserHeight = self.main_widget.tableWidget_sgCollectionBrowser.height()
					self.setBrowsers()
					self.libraryCollectionBrowser()
		self.resizeEventHappened = True

#######################################################################################################################
################################################## ScreenGrab #########################################################
#######################################################################################################################

	def getScreenshot(self,imageSnapshot):
		# Default module to get a screenshot of the all screen under windows
		screen = QtWidgets.QApplication.primaryScreen()
		#screenshot = screen.grabWindow(0,0,0,250,250)
		screenshot = screen.grabWindow(QtWidgets.QApplication.desktop().winId())
		screenshot.save(imageSnapshot, 'jpg')

#######################################################################################################################
################################################ Drag and Drop ########################################################
#######################################################################################################################

	def dragEnterEvent(self, drag_event):
		objects = []
		if self.context == "Textures":
			if in_nuke:
					objects = self.importTexture("nukeDrop")
		if self.context == "Megascans":
			if in_nuke:
					self.extractingZip("nukeDrop")
			elif in_hou:
					self.extractingZip("houdiniDrop")
			elif in_maya:
					self.extractingZip("mayaDrop")
			objects = self.objectsToDrop
			##objects= ["/jobs/faces/docs/library/Antique_Architecture_ud4mbgtfa_3d/ud4mbgtfa_LOD1.fbx"]
		mime_data = drag_event.mimeData()
		print('\n'.join(objects))
		mime_data.setData("text/plain", str('\n'.join(objects)))
		if mime_data.hasFormat("text/plain") or mime_data.hasFormat("text/url-list"):
			drag_event.acceptProposedAction()

		self.progressBarFinish(timeSleep = 0.5)

	def dragLeaveEvent(self,drag_event):
		print("Leave Event")

	def dragMoveEvent(self,drag_event):
		print("Move Event")

	def dropEvent(self, drop_event):
		print( "Drop Event")
		objects = []
		if self.context == "Textures":
			if in_nuke:
					objects = self.importTexture("nukeDrop")
		if self.context == "Megascans":
			if in_nuke:
					self.extractingZip("nukeDrop")
			elif in_hou:
					self.extractingZip("houdiniDrop")
			elif in_maya:
					objects = "/jobs/faces/docs/library/Antique_Architecture_ud4mbgtfa_3d/ud4mbgtfa_LOD1.fbx"
					self.extractingZip("mayaDrop")
			objects = self.objectsToDrop
		mime_data = drop_event.mimeData()
		print('\n'.join(objects))

		mime_data.setData("text/plain", str('\n'.join(objects)))
		if mime_data.hasFormat("text/plain") or mime_data.hasFormat("text/url-list"):
			drop_event.acceptProposedAction()

		super(sgAlexandriaLibrary,self).dropEvent(drop_event)
		##self.addItem(drag_event.mimeData().text())

#######################################################################################################################
#######################################################################################################################
############################################## Update Asset Infos #####################################################
#######################################################################################################################
#######################################################################################################################
	
	def doubleClickCommandBrowser(self):
		if self.context == "Collections" :
			if self.main_widget.libraryTab.currentIndex() == 0:
				self.libraryCollectionBrowser()
				self.main_widget.libraryTab.setCurrentIndex(1)
			else:
				self.openExplorer()
		else:
			self.openExplorer()

	def showAssetInfos(self):
		self.assetInfosMenu = sgAssetInfos()
		self.assetInfosMenu.infoInUI(self.dataAssetSelected)
		# self.editInfosMenu.show()
		response = self.assetInfosMenu.exec_()
		return response

	def cellClicked(self, row, column):
		## Check Which tab you are in
		self.changeTab()
		self.idCell = str(row)+str(column)

		self.updateInfos()

	def cellSearchClicked(self, row, column):
		self.idSearchCell = str(row)+str(column)
		self.searchRow = row
		self.searchColumn = column
		self.updateSearchInfos()

	def updateInfos(self):
		## Check Which tab you are in
		self.changeTab()
		try:
			if self.idCell in self.dicPaths:
				self.picturePath = self.dicPaths[self.idCell][0]["preview"]
				self.nameSelection = self.dicPaths[self.idCell][0]["name"]
				self.folderSelection = self.dicPaths[self.idCell][0]["path"]
			else:
				return

			nameKeyIcon = os.path.basename(self.picturePath)
			nameCollection = nameKeyIcon.split(self.databaseSeparator)[-1].split(self.thumbnailSuffix)[0]
			jsonfile = os.path.join(self.folderSelection,nameKeyIcon.split(self.databaseSeparator)[-1].split(self.thumbnailSuffix)[0]+ self.jsonInfoFileExtension)
			# Browser
			if self.currentUITab == 0:
				if self.context == "Megascans":
					self.folderSelection = self.folderSelection.split(self.nameSelection)[0]
					self.jsonFile = os.path.join(self.folderSelection,self.dicMegascansZip[nameKeyIcon][0]["json"])
				elif self.context == "Collections":
					self.collectionSelection = nameCollection
					self.collectionPicture =  self.picturePath
					self.jsonFile = os.path.join(self.folderSelection,self.dicAllDatabase[nameKeyIcon][0]["json"])
				else:
					self.jsonFile = os.path.join(self.folderSelection,self.dicAllDatabase[nameKeyIcon][0]["json"])

			# Collection
			elif self.currentUITab ==1:
				self.folderSelection = self.folderSelection
				self.jsonFile = os.path.join(self.folderSelection, self.dicAllDatabase[nameKeyIcon][0]["json"])

			# Get Selected icon
			self.typeItemSelected = self.dicAllDatabase[nameKeyIcon][0]["type"]
			self.selectedIconName = self.picturePath
			## Update UI
			self.thumbnailPreviewUI(self.picturePath)
			self.collectItemInformation(self.jsonFile,self.typeItemSelected)

			self.actionMenuUpdateUI()

		except:
			print(sys.exc_info())
			print(traceback.format_exc())
			pass

	def updateSearchInfos(self):
		if self.idSearchCell in self.dicPathsSearch:
			self.picturePath = self.dicPathsSearch[self.idSearchCell][0]["preview"]
			self.nameSelection = self.dicPathsSearch[self.idSearchCell][0]["name"]
			self.folderSelection = self.dicPathsSearch[self.idSearchCell][0]["path"]
		else:
			return

		nameKeyIcon = os.path.basename(self.picturePath)
		nameCollection = nameKeyIcon.split(self.databaseSeparator)[-1].split(self.thumbnailSuffix)[0]

		if self.context == "Megascans":
			self.folderSelection = self.folderSelection.split(self.nameSelection)[0]
			self.jsonFile = os.path.join(self.folderSelection,self.dicMegascansZip[nameKeyIcon][0]["json"])
		elif self.context == "Collections":
			self.collectionSelection = nameCollection
			self.collectionPicture =  self.picturePath
			self.jsonFile = os.path.join(self.folderSelection,self.dicAllDatabase[nameKeyIcon][0]["json"])
		else:
			self.jsonFile = os.path.join(self.folderSelection,self.nameSelection+self.jsonInfoFileExtension)
		
		# Get Selected icon
		self.typeItemSelected = self.dicAllDatabase[nameKeyIcon][0]["type"]

		self.thumbnailPreviewUI(self.picturePath)
		self.collectItemInformation(self.jsonFile,self.typeItemSelected)
		self.actionMenuUpdateUI()

	def collectItemInformation(self,jsonFile,typeItemSelected):
		if os.path.exists(jsonFile):
			with open(jsonFile) as jfile:
				dictInfoItem = json.load(jfile)

			if typeItemSelected == "Megascans":
				nameImage = os.path.basename(self.picturePath)
				dataMegascans = self.gatherDataFromMegascanJson(dictInfoItem)
				name = self.nameSelection + " - " + dataMegascans[self.picturePath][0]["originalName"]
				author = "Megascans"
				date = 	time.ctime(self.dicMegascansZip[nameImage][0]["timeEntry"])
				version = date
				self.lock = False
				ocio = ""
				notes = "Physical Size: " + str(dataMegascans[self.picturePath][0]["physicalSize"]) + " ( in meters )" + " - Resolution: " + str(dataMegascans[self.picturePath][0]["resolution"])
				extension = self.separator.join(self.dicMegascansZip[nameImage][0]["lods"]) + self.separator + self.separator.join(self.dicMegascansZip[nameImage][0]["extension"])
				tags = self.separator.join(dataMegascans[self.picturePath][0]["tags"])
				metadata = "" #self.separator.join(dataMegascans[self.picturePath][0]["tags"])
				dataTooltip = dataMegascans
			else:
				dataTooltip = dictInfoItem
				for data in dictInfoItem['releaseInfos']:
					name = self.nameSelection
					author = data['author']
					date = time.ctime(data["timeEntry"])
					version = str(data['version']) + " - " + date
					self.lock = data['lock']
					ocio = data['ocio']
					notes = data['note']
					extension = self.separator.join(data['extension'])
					tags = data['tags']
					metadata = data['meta']	
		else:
			name = ""
			author = ""
			date = ""
			version = ""
			ocio = ""
			notes = ""
			self.lock = False
			extension = ""
			tags = ""
			metadata = ""
			dataTooltip = {}
			print("Json Infos file for selected item doesn't exist: ",jsonFile)

		# Update Tooltip Top Icon
		self.dataAssetSelected = dataTooltip
		#self.manageToolTipIcon(dataTooltip)
		self.updateUIInfo(name,author,version,ocio,notes,extension,metadata,self.lock)

	def updateUIInfo(self,name,author,version,ocio,notes,extension,metadata,lock):
		self.main_widget.label_sgPreviewInfo_name.setText( name)
		self.main_widget.label_sgPreviewInfo_author.setText(author )
		self.main_widget.label_sgPreviewInfo_version.setText( version )
		self.main_widget.label_sgPreviewInfo_ocio.setText( ocio )
		self.main_widget.label_sgPreviewInfo_notes.setText( notes )
		self.main_widget.label_sgPreviewInfo_available.setText( extension )
		self.main_widget.label_sgPreviewInfo_metadata.setText( metadata )
		self.main_widget.pb_iconInfos01.setChecked(lock)

	def gatherDataFromMegascanJson(self,dataDic):
		#print("- Gathering informations from selected megascan -" + "\n")
		tags = []
		size = ""
		averageColor = ""
		originalName = ""
		resolutionSquare = ""
		minSize = ""
		maxSize = ""
		maps = {}
		imageName = os.path.basename(self.picturePath)
		zipFile = resolutionZip = self.dicMegascansZip[imageName][0]['zipFile']
		resolutionZip = self.dicMegascansZip[imageName][0]['resolution']
		modifiedTimeZip = time.ctime(self.dicMegascansZip[imageName][0]['timeEntry'])
		components = self.dicMegascansZip[imageName][0]['textures']
		dictTexture,dictComponent = self.findTextureComponents(components)

		if resolutionZip in self.dicSquareResolution:
			resolutionSquare = self.dicSquareResolution[resolutionZip]
			# print("Found Resolution: " + resolutionSquare + " match the megascans resolution: " + resolutionZip )

		# Explore Json
		for key, value in self.recursiveMegascanJson(dataDic):
			# print(key, value)
			if key == "averageColor":
				averageColor = value
			elif key == "physicalSize":
				size = value
			elif key == "minSize":
				minSize = value
			elif key == "maxSize":
				maxSize = value
			elif key == "semanticTags" or key == "descriptive" or key == "contains" or key == "environment" or key == "theme" or key == "tags" or key == "name":
				if key != "name":
					if type(value) is list:
						tags += value
					else:
						tags.append(value)
				elif key == "name":
					originalName = value
			# Works for Surface
			elif key == "maps" :
				# print(key)
				# Check if list available
				if type(value) is list:
					for elmt in value:
						# print(elmt)
						if type(elmt) is dict:
							for keyElmt,valueElmt in elmt.items():
								# If texture name found in json add it to the simplified dictionary
								if keyElmt == "uri":
									if elmt["uri"] in dictTexture:
										maps[elmt["uri"]] = elmt
							# print(elmt.items())

			# Works for 3d Objects and Atlas
			elif key == "components":
				# print(key)
				if type(value) is list:
					for components in value:
						if type(components) is dict:
							if "name" in components:
								nameComponent = components["name"].replace("'","")
								if nameComponent in dictComponent :
									colorspaceComponent = components["colorSpace"]
									minIntensity = components["minIntensity"]
									maxIntensity = components["maxIntensity"]
									bitDepth = 0
									if dictComponent[nameComponent]['extension'] == "jpg":
										bitDepth = 8
									elif dictComponent[nameComponent]['extension'] == "exr":
										bitDepth = 16
									# print(json.dumps(components['uris'],indent=4))
									listJsonResComponent = components['uris']
									for dicJsonResComponent in listJsonResComponent:
										# print(dicJsonResComponent['resolutions'])
										for dicResComp in dicJsonResComponent['resolutions']:
											if dicResComp["resolution"] == resolutionSquare:
												# print(json.dumps(dicResComp,indent = 4))
												maps[dictComponent[nameComponent]['texture']] = {
												"mimeType": "image/" + dictComponent[nameComponent]['extension'],
												"minIntensity": minIntensity,
												"bitDepth": bitDepth,
												"name": nameComponent,
												"resolution": resolutionSquare,
												"contentLength": "",
												"colorSpace": colorspaceComponent,
												"uri": dictComponent[nameComponent]['texture'],
												"physicalSize": "",
												"maxIntensity": maxIntensity,
												"type": nameComponent.lower(),
												"averageColor": ""
												}
						# print(json.dumps(components,indent = 4)) 
				# print("\n")	
			if size == None :
				size = str(maxSize) + "x" + str(minSize)
		# Simplified dictionary
		dataJsonMegascan = {}
		dataJsonMegascan[self.picturePath] = []
		dataJsonMegascan[self.picturePath].append({
		'originalName': originalName,
		'zipFile':zipFile,
		'resolution': resolutionSquare ,
		'id': dataDic["id"],
		'tags':tags,
		'physicalSize':size,
		'minSize':minSize,
		'maxSize': maxSize,
		'averageColor': averageColor , 
		'maps':maps
		})
		# print(json.dumps(dataJsonMegascan,indent=4))

		return dataJsonMegascan
	
	def findTagsInMegascansJson(self,dataDic):
		tags = ""
		for key, value in self.recursiveMegascanJson(dataDic):
			if key == "semanticTags" or key == "descriptive" or key == "contains" or key == "environment" or key == "theme" or key == "tags" or key == "name":
				if key != "name":
					if type(value) is list:
						tags += ",".join(value)
					else:
						tags+= "," + value
		return tags

	def recursiveMegascanJson(self,dictionary):
		for key, value in dictionary.items():
			if type(value) is dict:
				# Python 2 Friendly
				for t in self.recursiveMegascanJson(value):
					yield t
				# Python 3
				#yield from self.recursiveMegascanJson(value)
				self.recursiveMegascanJson(value)
			else:
				yield (key, value)

	def findTextureComponents(self,listTexturesName):
		dictTexture = {}
		dictComponent = {}
		for texture in listTexturesName:
			noExtensionTexture = texture.split(".")[0]
			extension = texture.split(".")[-1]

			componentTexture = noExtensionTexture.split("_")
			for component in componentTexture:
				if component in self.listMegascansComponents and component not in dictComponent:
					dictTexture[texture] = {
					'texture': noExtensionTexture,
					'component':component,
					'extension':extension
					}
					dictComponent[component] = {
					'texture': texture,
					'component':component,
					'extension':extension
					}

		# print(json.dumps(dictComponent,indent=4))
		return dictTexture,dictComponent

	def launchEditInfosMenu(self):
		# Prepare UI
		tags = ""
		author = ""
		note = ""
		meta = ""
		extension = ""
		time = ""
		ocio = ""
		textures = []
		if self.dataAssetSelected["releaseInfos"][0]["tags"]:
			tags = self.dataAssetSelected["releaseInfos"][0]["tags"]
		if self.dataAssetSelected["releaseInfos"][0]["author"]:
			author = self.dataAssetSelected["releaseInfos"][0]["author"]
		if self.dataAssetSelected["releaseInfos"][0]["note"]:
			note = self.dataAssetSelected["releaseInfos"][0]["note"]
		if self.dataAssetSelected["releaseInfos"][0]["meta"]:
			meta = self.dataAssetSelected["releaseInfos"][0]["meta"]
		if self.dataAssetSelected["releaseInfos"][0]["extension"]:
			extension = self.dataAssetSelected["releaseInfos"][0]["extension"]
			if type(extension) == list:
				extension = ",".join(extension)
		if self.dataAssetSelected["releaseInfos"][0]["timeEntry"]:
			time = self.dataAssetSelected["releaseInfos"][0]["timeEntry"]
		if self.dataAssetSelected["releaseInfos"][0]["ocio"]:
			ocio = self.dataAssetSelected["releaseInfos"][0]["ocio"]
		if self.dataAssetSelected["releaseInfos"][0]["textures"]:
		 	textures = self.dataAssetSelected["releaseInfos"][0]["textures"]
		listToParse = self.findListSelectedItems()
		pathImage,nameAsset,pathToLookIn = self.getDataFromDicImport(listToParse[0])
		iconPath = pathImage

		## Launch UI
		self.editInfosMenu = sgEditInfos()
		self.editInfosMenu.setOCIOCombobox(self.defaultOCIO)
		self.editInfosMenu.infoInUI(iconPath,tags,meta,author,extension,note,ocio)
		self.editInfosMenu.setWindowsTitle(nameAsset)
		# self.editInfosMenu.show()
		response = self.editInfosMenu.exec_()

		if response == 1:
			## Get data from UI and from the json file
			iconPath = self.editInfosMenu.pb_icon.toolTip()
			author = self.editInfosMenu.textEdit_author.toPlainText()
			tags = self.editInfosMenu.textEdit_tags.toPlainText()
			note = self.editInfosMenu.textEdit_note.toPlainText()
			meta = self.editInfosMenu.textEdit_meta.toPlainText()
			ocio = self.editInfosMenu.comboBox_ocio.currentText()
			data = self.readJsonInfos(self.jsonFile)
			# Icon
			if iconPath != pathImage:
				self.simpleCopyFile(iconPath,pathImage)
				# Resize Thumbnail and resolution at 512
				self.resolutionThumbnail = 512
				self.resizeThumbnail(pathImage)
				
			# Json
			if data:
				## Update the dictionary
				data['releaseInfos'][0]['author'] = author
				data['releaseInfos'][0]['tags'] = tags
				data['releaseInfos'][0]['note'] = note
				data['releaseInfos'][0]['meta'] = meta
				data['releaseInfos'][0]['ocio'] = ocio
				if type(extension) != list:
					extension = extension.split(",")
				data['releaseInfos'][0]['extension'] = extension
				data['releaseInfos'][0]['timeEntry'] = time
				## Write the new infos file
				self.writeJsonFile(self.jsonFile,data)
			else:
				if os.getenv("USER"):
					user = os.getenv("USER")
				else:
					user = os.environ.get("USERNAME")
				## Write the new infos file
				self.writeJsonEntryInfos(self.jsonFile,self.nameSelection,extension,textures,note,"1",tags,ocio,time.time(),meta)

			# Update icon for display
			# TODO Update Selected cell
			self.updateInfos()
			self.launchBrowsing()
			# Update data for display
			self.dataAssetSelected = data
			try:
				self.collectItemInformation(self.jsonFile,self.typeItemSelected)
			except:
				print(sys.exc_info())
				pass

	def updateOldJsonInfosFiles(self):
		import sg_updateJsonInfos 
		if pythonVersion == 3:
			import imp
			imp.reload(sg_updateJsonInfos)

		## Launch Pick LOD UI
		updateOldJson = sg_updateJsonInfos.sgUpdateJsonInfos()
		updateOldJson.show()
		## Add LODs to listWidget
		updateOldJson.appendUI(self.libraryPath)
		
#######################################################################################################################
#######################################################################################################################
########################################### IMPORT ACTION WHEN RIGHT CLICK ############################################
#######################################################################################################################
#######################################################################################################################

	def findListSelectedItems(self):
		if self.main_widget.libraryTab.currentIndex()== 0:
			if self.searchMode == False:
				listToParse = self.main_widget.tableWidget_sgElementBrowser.selectedItems()
			else:
				listToParse = self.main_widget.tableWidget_sgSearchBrowser.selectedItems()
		elif self.main_widget.libraryTab.currentIndex()== 1:
			listToParse = self.main_widget.tableWidget_sgCollectionBrowser.selectedItems()
		return listToParse

	def getDataFromDicImport(self,item):
		if self.main_widget.libraryTab.currentIndex()== 0: 
			if self.searchMode == False:
				pathImage =  self.dicPaths[str(item.row())+str(item.column())][0]["preview"]
				nameAsset = self.dicPaths[str(item.row())+str(item.column())][0]["name"]
				pathToLookIn = self.dicPaths[str(item.row())+str(item.column())][0]["path"]
			else:
				pathImage =  self.dicPathsSearch[str(self.searchRow)+str(self.searchColumn)][0]["preview"]
				nameAsset = self.dicPathsSearch[str(self.searchRow)+str(self.searchColumn)][0]["name"]
				pathToLookIn = self.dicPathsSearch[str(self.searchRow)+str(self.searchColumn)][0]["path"]

		elif self.main_widget.libraryTab.currentIndex()== 1: 
			pathImage =  self.dicCollectionPaths[str(item.row())+str(item.column())][0]["preview"]
			nameAsset = self.dicCollectionPaths[str(item.row())+str(item.column())][0]["name"]
			pathToLookIn = self.dicCollectionPaths[str(item.row())+str(item.column())][0]["path"]

		return pathImage,nameAsset,pathToLookIn

	def findCells(self):
		if self.searchMode == False:
			listToParse = self.main_widget.tableWidget_sgElementBrowser.selectedItems()
		else:
			listToParse = self.main_widget.tableWidget_sgSearchBrowser.selectedItems()
		for item in listToParse:
			if self.searchMode ==False:
				pathImage =  self.dicPaths[str(item.row())+str(item.column())][0]["preview"]
				nameAsset = str(self.dicPaths[str(item.row())+str(item.column())][0]["name"])
				pathToLookIn = self.dicPaths[str(item.row())+str(item.column())][0]["path"]
			else:
				pathImage =  self.dicPathsSearch[str(item.row())+str(item.column())][0]["preview"]
				nameAsset = str(self.dicPathsSearch[str(item.row())+str(item.column())][0]["name"])
				pathToLookIn = self.dicPathsSearch[str(item.row())+str(item.column())][0]["path"]

	def importModel(self,action):
			modelFiles = []
			otherLODs = []
			try:
				logger.info(" ---- Model Import ---- ")
			except:
				pass

			if action =="ma":
				self.fileExtension = "ma"
				self.depth= 2
			elif action =="usd":
				self.fileExtension = "abc"
				self.depth= 3
			elif action =="fbx":
				self.fileExtension = "fbx"
				self.depth= 3
				nodeToCreate = 'file'
				attribute = 'file'
			elif action =="abc":
				self.fileExtension = "abc"
				self.depth= 3
				nodeToCreate = 'file'
				attribute = 'file'

			#  Find Selection in UI
			listToParse = self.findListSelectedItems()

			for item in listToParse:
				# Get Infos
				pathImage,nameAsset,pathToLookIn = self.getDataFromDicImport(item)
				nameIcon = os.path.basename(pathImage)

				for file in os.listdir(pathToLookIn):
					if file[-self.depth:] == self.fileExtension:
						modelFiles.append(file)
					
				if not modelFiles:
					print("Didn't find any files in " + pathToLookIn + " for command: " + action)
					return False

				#### Init per software
				if in_hou:
					houdiniNodeInfos = sg_houdiniLibraryCommands.getCurrentContextNode()
					houdiniContext = houdiniNodeInfos[1]
					houdiniNodePath = houdiniNodeInfos[2]
					houdiniContextPos = houdiniNodeInfos[3]
					self.houdiniSettings = self.main_widget.sgHoudiniSettings_Settings.itemText(self.main_widget.sgHoudiniSettings_Settings.currentIndex())
					if self.houdiniSettings == "MPC":
						self.houdiniMPC= True
					else:
						self.houdiniMPC = False
					if self.houdiniMPC == True and houdiniContext == "Lop":
						## Return master lop, model lop and shader lop
						self.assetLop = sg_houdiniLibraryCommands.importMPCMegascansLop(nameAsset)
				if len(modelFiles)!=0:
					modelPath = pathToLookIn + modelFiles[0]
					shaderPath = pathToLookIn + "shaders"
					texturePath = pathToLookIn + "sourceimages"
					if action == "ma" or action == "fbx" or action =="usd" or action =="obj" or action == "abc" :
						if in_maya==True:
								model = sg_mayaLibraryCommands.importModel(modelPath,action,nameAsset)
								self.renameDuplicates()
								if action == "abc":
									self.loadShader(shaderPath,nameAsset,"maya")
									sg_mayaLibraryCommands.deleteNamespace([nameAsset,])

						elif in_hou==True:
								## Create file node to load the geo
								if self.houdiniMPC:
									if houdiniContext == "Object" or houdiniContext == "Sop" and not "/stage" in houdiniNodePath:
											model = sg_houdiniLibraryCommands.importMegascansModel(modelPath,nameAsset, nameAsset,houdiniNodeInfos)
									elif  houdiniContext == "Lop":
											model = sg_houdiniLibraryCommands.importMPCMegascansModel(self.assetLop,modelPath,"LodA")
											sg_houdiniLibraryCommands.setLOPVariant(self.assetLop[1])
								else:
									model = sg_houdiniLibraryCommands.importMegascansModel(modelPath,nameAsset, nameAsset,houdiniNodeInfos)
								## Launch texture convertion
								self.listFullpathImages = [texturePath+"/"+f for f in os.listdir(texturePath) if os.path.isfile((os.path.join(texturePath,f))) and ".tex" not in f]
								## Automatically Launch tex convertion in Houdini
								print ("\n" + " ---- Converting Textures as TEX in Background ---- ")
								dataAutomaticTex = sg_houdiniLibraryCommands.convertTexAutomatic(self.listFullpathImages)
								sg_batchTextureConvert.makeTex(ui_obj=self,listTextures = self.listFullpathImages,commands = dataAutomaticTex[1],settings = dataAutomaticTex[2],bypass_UI = True)

								## Create and load the shader from the json file
								if action == "abc":
									self.loadShader(shaderPath,model,houdiniNodeInfos)
								## Organise Geo Container
								model[0].layoutChildren()

						elif in_nuke==True:
								sg_nukeLibraryCommands.clearSelection()
								model = sg_nukeLibraryCommands.importModel(modelPath,self.sizeSelectedElmt)
						elif in_mari==True:
								project = sg_mariLibraryCommands.currentProject()
								if project != None:
									## Import model in the current project
									model = sg_mariLibraryCommands.importModel(modelPath)
								else:
									## Create a new project
									channels = []
									project = sg_mariLibraryCommands.createNewProject(nameAsset,modelPath,channels)
						elif in_blen  == True:
								model= sg_blenderLibraryCommands.importModel(modelPath)
						elif in_unreal==True:
								model = sg_unrealLibraryCommands.importModel(modelPath,otherLODs,nameAsset,nameAsset+"_Model","")

					elif action =="arnold":
						##create standin
						if in_maya==True:
								name= modelFiles[0].split(".")[0]
								standin = sg_mayaArnold.createStandin(name,modelPath)
					
					###### Message ######
					print("Import Successfull:" + modelPath + "!")
					try:
						logger.info("Import Successfull: %s ",modelPath)
					except:
						pass
					if in_maya:
						cmds.inViewMessage( amg="Import Successfull:" + modelPath + "!", pos='botCenter', fade=True, fadeOutTime=500)
				else:
					if in_maya== True:
						cmds.warning("File not found: " + self.fileExtension)
					else:
						print("File not found: " + self.fileExtension )
					try:
						logger.warning("File not found: %s", self.fileExtension)
					except:
						pass

				## Extra Processes - Backdrop
				if in_nuke:
					sg_nukeLibraryCommands.createBackDrop(nameAsset)
				elif in_hou:
					## Backdrop Creation
					if houdiniContext == "Object" or houdiniContext == "Sop" and not "/stage" in houdiniNodePath:
						frame = model[0]
					else:
						frame = self.assetLop[0]
					sg_houdiniLibraryCommands.createNetworkBox([frame],nameAsset,houdiniNodeInfos)

	def importTexture(self,action):
			print(" -- Texture Import -- ")
			###
			try:
				logger.info(" ---- Texture Import ---- ")
			except:
				pass
			
			### Init Variables
			self.sharedUV = self.main_widget.checkBox_sgTextureSharedUV.isChecked()
			self.triplanar = self.main_widget.checkBox_sgTextureTriplanar.isChecked()
			colorspaceMari = self.main_widget.sgMariSettings_ColorSpace.itemText(self.main_widget.sgMariSettings_ColorSpace.currentIndex())
			
			textureFiles = []
			texturesListDrop = []
			self.listFullpathImages = []
			self.manifold =""
			self.textureNodeList=[]
			
			depth= 3
			xPos = -500
			yPos = 0
			idName = "_"+str(random.randint(0,9999999))

			#  Find Selection in UI
			listToParse = self.findListSelectedItems()

			## Parse dictionnary to find info
			for item in listToParse:
				# Get Infos
				pathImage,nameAsset,pathToLookIn = self.getDataFromDicImport(item)
				nameIcon = os.path.basename(pathImage)
				# Textures are stored in a folder named sourcemages now
				pathToLookIn = pathToLookIn + "sourceimages/"
				## Create Container or Group Per Asset selected
				if in_hou:
					houdiniNodeInfos = sg_houdiniLibraryCommands.getCurrentContextNode()
					houdiniContext = houdiniNodeInfos[1]
					houdiniNodePath = houdiniNodeInfos[2]
					houdiniContextPos = houdiniNodeInfos[3]
					if houdiniContext == "Object" or houdiniContext == "Sop" and not "/stage" in houdiniNodePath :
						self.containerTexture = hou.node('/obj').createNode('matnet',nameAsset+"_Textures")
					elif houdiniContext == "Vop":
						self.containerTexture = hou.node(houdiniNodePath)
					elif houdiniContext == "Lop":
						self.containerTexture = hou.node('/stage').createNode('materiallibrary',nameAsset+"_Textures")
						self.containerTexture.moveToGoodPosition()
				if in_katana:
					self.contextKatana = sg_katanaLibraryCommands.getContext()
					if self.contextKatana == "rootNode":
						self.containerTexture = sg_katanaLibraryCommands.createNetworkMaterial(nameAsset+"_Textures")
					else:
						self.containerTexture = self.contextKatana

				## Create Manifold
				if action == "rman":
					if in_maya == True:
						self.manifold = sg_mayaRenderman.createSharedRmanTexture(self.sharedUV,self.triplanar)
					if in_hou == True:
						self.manifold = sg_houdiniRenderman.createSharedRmanTexture(self.sharedUV,self.triplanar,self.containerTexture,nameAsset+"_manifold")
					if in_katana == True:
						self.manifold = sg_katanaRenderman.createSharedRmanManifold(self.sharedUV,self.triplanar,self.containerTexture,nameAsset,xPos)
				elif action == "arnold":
					self.manifold = sg_mayaArnold.createSharedArnoldTexture(self.sharedUV,self.triplanar)
				elif action == "mayaDefault":
					self.manifold = sg_mayaLibraryCommands.createSharedMayaTexture(self.sharedUV,self.triplanar)
				elif action == "mantra":
					self.manifold = sg_houdiniMantra.createSharedMantraTexture(self.sharedUV,self.triplanar,self.containerTexture,nameAsset)
				elif action=="nuke":
					sg_nukeLibraryCommands.clearSelection()
					self.manifold =""
				elif action=="nukeDrop":
					sg_nukeLibraryCommands.clearSelection()
					self.manifold =""
				elif action == "mari":
						sg_mariLibraryCommands.createTextureCategory(nameAsset)

				## Add manifolds in list node created
				self.textureNodeList.append(self.manifold)

				## Parsing all the files in the asset folder except in Nuke
				if action == "nuke":
					if nuke.getFileNameList(pathToLookIn) != False:
						for seq in nuke.getFileNameList(pathToLookIn):
							if seq.split(" ")[0][-depth:] in tuple(self.listImagefileExtension) and seq != nameIcon:
								texture = sg_nukeLibraryCommands.createSequenceTextureFileNuke(pathToLookIn,seq)
								self.textureNodeList.append(texture)
						else:
							print("ERROR: No matching files, check the name of the preview icon")
				else:
					sequences = self.findImageSequences(pathToLookIn)
					if sequences:
						# May not work in python 2 : listPaths = [*sequences]
						#listPaths = [*sequences]
						listPaths = list(sequences.keys())
					else:
						listPaths = os.listdir(pathToLookIn)

					for file in listPaths:
						# Get Data Textures
						dataTexture = self.dataAssetSelected["releaseInfos"][0]
						if file[-depth:].lower() in tuple(self.listImagefileExtension) and file != nameIcon:
							textureFiles.append(file)
							self.filename = pathToLookIn+file
							#nameTexture = file.split(".")[0] # to replace with basename ?
							nameTexture = os.path.basename(file).split(".")[0]
							texture = None
							## Create Texture File
							if action == "rman":
								# need to check if #### and replace with <frame> or with <f4> 
								if in_maya == True:
									texture = sg_mayaRenderman.createTextureFileRman(self.sharedUV, self.triplanar,self.manifold,self.filename,nameTexture)
								if in_hou == True:
									texture = sg_houdiniRenderman.createTextureFileRman(self.sharedUV, self.triplanar,self.manifold,nameTexture,self.filename,self.containerTexture)
								if in_katana == True:
									texture = sg_katanaRenderman.createTextureFileRman(self.sharedUV, self.triplanar,self.manifold,self.filename,self.containerTexture,nameTexture,xPos,yPos)
									self.listFullpathImages.append(self.filename)
									xPos -= 0
									yPos += 450
							elif action == "arnold":
								if in_maya == True:
									texture = sg_mayaArnold.createTextureFileArnold(self.sharedUV, self.triplanar,self.manifold,self.filename,nameTexture,dataTexture)
							elif action == "mayaDefault":
								texture = sg_mayaLibraryCommands.createTextureFileMaya(self.sharedUV, self.triplanar,self.manifold,self.filename)
							elif action == "mantra":
								texture = sg_houdiniMantra.createTextureFileMantra(self.sharedUV, self.triplanar,self.manifold,file.split(".")[0],self.filename,self.containerTexture)
							# elif action == "nuke":
								# texture = sg_nukeLibraryCommands.createTextureFileNuke(self.filename)
							elif action == "nukeDrop":
								texturesListDrop.append(self.filename)
							elif action == "mari":
								texture = sg_mariLibraryCommands.importTexture(self.filename,colorspaceMari)
							elif action == "mariLight":
								texture = sg_mariLibraryCommands.createLighting(None,self.filename)
							elif action == "blender":
								texture = sg_blenderLibraryCommands.importTexture(self.filename,file)
							
							if texture != None:
								self.textureNodeList.append(texture)
				##### Extra Processes #####
				### Backdrop Creation
				if in_nuke and action == "nuke":
					sg_nukeLibraryCommands.createBackDrop(nameAsset)
				elif action == "nukeDrop":
					return texturesListDrop
				if in_hou:
					sg_houdiniLibraryCommands.createNetworkBox([self.containerTexture],nameAsset,houdiniNodeInfos)
				if in_katana:
					## Create Backdrop
					# scaleBackdrop = sg_katanaLibraryCommands.calculateBackdropBBox(self.textureNodeList)
					# sg_katanaLibraryCommands.createBackDrop(nameAsset,scaleBackdrop,"texture")
					## Automatically Launch tex convertion in Houdini
					print ("\n" + " ---- Converting Textures as TEX in Background ---- ")
					dataAutomaticTex = sg_katanaLibraryCommands.convertTexAutomatic(self.listFullpathImages)
					sg_batchTextureConvert.makeTex(ui_obj=self,listTextures = self.listFullpathImages,commands = dataAutomaticTex[1],settings = dataAutomaticTex[2],bypass_UI = True)

				## Messages For Maya
				if in_maya:
					cmds.inViewMessage( amg="Texture(s) Imported: " + nameAsset , pos='botCenter', fade=True, fadeOutTime=500)
				print("Texture(s) Imported: " + nameAsset)
				try:
					logger.info("Path Textures: %s",pathToLookIn)
					logger.info("Texture(s) Imported: %s",nameAsset)
				except:
					pass

	def importShader(self,action):
			print(" -- Shader Import -- ")

			try:
				logger.info(" ---- Shader Import ---- ")
			except:
				pass

			### Init Variables
			fileExtensionJson = "json"
			fileExtensionKatana = "katana"
			fileExtensionUnreal = "uasset"
			katanaLoad = False
			shaderFiles = []
			listNodeCreated = []

			## Settings Check
			self.houdiniSettings = self.main_widget.sgHoudiniSettings_Settings.itemText(self.main_widget.sgHoudiniSettings_Settings.currentIndex())
			if self.houdiniSettings == "MPC":
				self.houdiniMPC = True
			else:
				self.houdiniMPC = False

			if action == "importRman":
				depth= 4
			elif action == "importAssign":
				depth= 4

			idName = "_"+ str(random.randint(0,9999999))

			#  Find Selection in UI
			listToParse = self.findListSelectedItems()
			
			## Collect Infos
			if in_hou:
				houdiniNodeInfos = sg_houdiniLibraryCommands.getCurrentContextNode()

			for item in listToParse:
				# Get Infos
				pathImage,nameAsset,pathToLookIn = self.getDataFromDicImport(item)

				for file in sorted(os.listdir(pathToLookIn),reverse = True):
					#print(file)
					if file ==  nameAsset+"."+fileExtensionKatana:
						if in_katana:
							katanaLoad = True
							shadingNode = sg_katanaLibraryCommands.importKatanaShader(pathToLookIn+file,nameAsset)
					elif file ==  nameAsset+"."+fileExtensionUnreal:
						if in_unreal:
							folderMaterial = "Materials"
							shadingNode = sg_unrealLibraryCommands.importShaderUnreal(pathToLookIn+file,file,folderMaterial,nameAsset)
					elif file ==  nameAsset+"."+fileExtensionJson:
						if in_maya == True:
							if self.subContext == 'renderman':
								shadingNode = sg_mayaRenderman.readShaderJson(pathToLookIn+file)
							elif self.subContext == 'arnold':
								shadingNode = sg_mayaArnold.readShaderJson(pathToLookIn+file)
						elif in_hou == True:
							containerShader = sg_houdiniLibraryCommands.createContainerShader(nameAsset,houdiniNodeInfos,None)
							shadingNode = sg_houdiniRenderman.readShaderJson(pathToLookIn+file,nameAsset,containerShader)
							shadingNode[0].moveToGoodPosition()
						elif in_katana and katanaLoad == False:
							containerShader = sg_katanaLibraryCommands.getContainer(nameAsset)
							shadingNode = sg_katanaRenderman.readShaderJson(pathToLookIn+file,nameAsset,containerShader)

			if in_maya:
				cmds.inViewMessage( amg="Shader Imported: " + str(nameAsset), pos='botCenter', fade=True, fadeOutTime=500)
			elif in_hou:
				## Add Container
				sg_houdiniLibraryCommands.createNetworkBox([containerShader],nameAsset,houdiniNodeInfos)
			print("\n")
			print("Shader Imported: " + str(nameAsset))
			try:
				logger.info("Shader Imported: %s",str(nameAsset))
			except:
				pass

			return shadingNode
	
	def importTextureToLight(self,action):
			if in_unreal:
				setLevelPath = sg_unrealLibraryCommands.getLevelPath()
				## Find Sky Folder as they could be named differently
				if sg_unrealLibraryCommands.directoryExist(setLevelPath + "Skies"):
					skyMPCLevelPath = setLevelPath + "Skies"
				elif sg_unrealLibraryCommands.directoryExist(setLevelPath + "Sky"):
					skyMPCLevelPath = setLevelPath + "Sky"
				else:
					sg_unrealLibraryCommands.createDirectory(setLevelPath+"Skies/MPC")
					skyMPCLevelPath = setLevelPath +"Skies/MPC/"

				## Create an MPC folder if it doesn't exist
				if not sg_unrealLibraryCommands.directoryExist(skyMPCLevelPath+"/MPC"):
					sg_unrealLibraryCommands.createDirectory(skyMPCLevelPath+"/MPC")
					skyMPCLevelPath = setLevelPath + "Skies/MPC/"
				else:
					skyMPCLevelPath = setLevelPath + "Skies/MPC/"
					print("Folder already exists")

				if self.searchMode == False:
					listToParse = self.main_widget.tableWidget_sgElementBrowser.selectedItems()
				else:
					listToParse = self.main_widget.tableWidget_sgSearchBrowser.selectedItems()

				for item in listToParse:
					## Get Infos
					pathImage,nameAsset,pathToLookIn = self.getDataFromDicImport(item)
					pathToLookIn = pathToLookIn + "sourceimages/"
					############# Problem ? #####
					nameIcon= os.path.basename(pathImage)
					depth = 3
					listFilenames = []
					for file in os.listdir(pathToLookIn):
						if file[-depth:].lower() in tuple(self.listImagefileExtension) and file != nameIcon:
							self.filename = pathToLookIn+file
							listFilenames.append(self.filename)
					assets = sg_unrealLibraryCommands.importTexturesForMPC(listFilenames,nameAsset,skyMPCLevelPath)

					## Show Asset In Browser
					sg_unrealLibraryCommands.showAssetsInContentBrowser(assets)

					####### Copy Material Instance
					materialReference = "/MPC_SUITE/MPC_Lighting/Materials/MMPC_MasterSky_Default.MMPC_MasterSky_Default"
					meshReference = "/MPC_SUITE/MPC_Lighting/Meshes/MPC_SkySphereMesh2.MPC_SkySphereMesh2"
					## Name Instance
					for i in range(0,100):
							materialInstance = skyMPCLevelPath+nameAsset+"_v" + str(i)
							meshDuplicate = skyMPCLevelPath+nameAsset_Mesh+"_v" + str(i)
							if not sg_unrealLibraryCommands.doesAssetExist(assetNewName):
								break
					
					materialDuplicated = sg_unrealLibraryCommands.duplicateAsset02(materialReference,materialInstance)

					## Duplicate Mesh
					meshDuplicated = sg_unrealLibraryCommands.duplicateAsset02(meshReference,meshDuplicate)
					
					## SetTexture on material
					sg_unrealLibraryCommands.connectTexturesToLight(assets[0],materialDuplicated)

					## Set Material on
					materialInstance.set_editor_property('SkyMaterial',assets[0])

	def importLightrig(self,action):
		print(" -- Lightrig Import -- ")

		try:
			logger.info(" ---- Lightrig Import ---- ")
		except:
			pass

		### Variables
		fileExtensionJson = "json"
		fileExtensionKatana = "katana"
		fileExtensionUnreal = "uasset"
		katanaLoad = False
		shaderFiles = []
		listNodeCreated = []

		## Settings Check
		self.houdiniSettings = self.main_widget.sgHoudiniSettings_Settings.itemText(self.main_widget.sgHoudiniSettings_Settings.currentIndex())
		if self.houdiniSettings == "MPC":
			self.houdiniMPC = True
		else:
			self.houdiniMPC = False

		if action == "importRman":
			depth= 4
		elif action == "importAssign":
			depth= 4

		idName = "_"+str(random.randint(0,9999999))

		#  Find Selection in UI
		listToParse = self.findListSelectedItems()
		
		## Collect Infos
		if in_hou:
			houdiniNodeInfos = sg_houdiniLibraryCommands.getCurrentContextNode()

		for item in listToParse:
			# Get Infos
			pathImage,nameAsset,pathToLookIn = self.getDataFromDicImport(item)

			for file in sorted(os.listdir(pathToLookIn),reverse = True):
				dicLightRig = self.readJsonInfos(pathToLookIn + nameAsset + "." + fileExtensionJson)
				dicLights = dicLightRig["lightHierarchy"]
				dicConnections = dicLightRig['connectionsHierarchy']
				dicLightInfos =  dicLightRig["infos"]
				if in_maya == True:
					if self.subContext == 'renderman':
						if self.RfM == True:
							lightRig = sg_mayaLibraryCommands.importLgtRig(nameAsset,dicLights,dicConnections,dicLightInfos)
						else:
							self.message("Renderman for Maya is not loaded, it may causes some issue when loading Renderman lightrig - ABORTED -")
					elif self.subContext == 'arnold' :
						if self.MtoA == True:
							lightRig = sg_mayaLibraryCommands.importLgtRig(nameAsset,dicLights,dicConnections,dicLightInfos)
						else:
							self.message("Arnold is not loaded, it may causes some issue when loading lightrig - ABORTED -")
					elif self.subContext == 'maya':
						lightRig = sg_mayaLibraryCommands.importLgtRig(nameAsset,dicLights,dicConnections,dicLightInfos)
				elif in_hou == True:
					if self.subContext == 'renderman':
						lightRig = sg_houdiniLibraryCommands.importLgtRig(nameAsset,dicLights,dicConnections,dicLightInfos,houdiniNodeInfos)
						if lightRig:
							## Organize the nodes
							sg_houdiniLibraryCommands.layoutChildren(lightRig[0])
							## Create a visual container
							sg_houdiniLibraryCommands.createNetworkBox(lightRig,nameAsset,houdiniNodeInfos)
				elif in_katana:
					listTexturesToConvert = sg_katanaLibraryCommands.importLgtRig(nameAsset,dicLights,dicConnections,dicLightInfos)
					lightRig = []
					# Convert to Tex ?
					#if listTexturesToConvert:
					#	dataAutomaticTex = sg_katanaLibraryCommands.convertTexAutomatic(listTexturesToConvert)
					#	sg_batchTextureConvert.makeTex(ui_obj=self,listTextures = listTexturesToConvert,commands = dataAutomaticTex[1],settings = dataAutomaticTex[2],bypass_UI = True)
				# only import one 
				break

		if in_maya:
			cmds.inViewMessage( amg="Lightrig Imported: " + str(nameAsset), pos='botCenter', fade=True, fadeOutTime=500)
		print("\n")
		print("Lightrig Imported: " + str(nameAsset))
		try:
			logger.info("Lightrig Imported: %s",str(nameAsset))
		except:
			pass

		return lightRig

	def assignTextureToLight(self,action,duplication):
		print(" -- Assign Texture to Light -- ")
		if action == "unreal":
			## Get the path of the asset linked to ( it should be in the metadata section)
			pathToSkyData = self.metaData.split(",")
			for path in pathToSkyData:
				if "StaticMesh" in path:
					pathToUMesh = path.split("'")[1]
				if "MaterialInstanceConstant" in path:
					pathToUMaterial = path.split("'")[1]

			## Find the asset Data
			textureData = unreal.EditorAssetLibrary.find_asset_data(pathToUMaterial)
			meshData = unreal.EditorAssetLibrary.find_asset_data(pathToUMesh)

			textureAsset = textureData.get_asset()
			meshAsset = meshData.get_asset()

			materialLibraryAsset = textureData.get_asset()
			materialToCopy = unreal.AssetRegistryHelpers.get_asset(textureData)

			## Get the selected Actor if it's a light will look for the material
			selectedActors = sg_unrealLibraryCommands.getSelectedActors()

			if selectedActors:
				## Find Current Static Mesh
				components = selectedActors[0].get_components_by_class(unreal.StaticMeshComponent)
				meshSlot = ""
				for item in components:
					if "SkyDome" in str(item):
							meshSlot = item
							break

				if meshSlot != "":
					mesh = meshSlot.get_editor_property('StaticMesh')
				else:
					self.main_widget.lineEdit_sgDisplayMessage.setText("Unvalid Selection, please select a skyDome")
					# time.sleep(2)
					# self.main_widget.lineEdit_sgDisplayMessage.setText("")

				## Get Level Path
				setLevelPath = sg_unrealLibraryCommands.getLevelPath()

				## Asset Name
				assetName = pathToUMaterial.split(".")[-1]
				meshName = pathToUMesh.split(".")[-1]

				if duplication == True:
					## Find Sky Folder as they could be named differently
					if sg_unrealLibraryCommands.directoryExist(setLevelPath + "Skies"):
							skyMPCLevelPath = setLevelPath + "Skies"
					elif sg_unrealLibraryCommands.directoryExist(setLevelPath + "Sky"):
							skyMPCLevelPath = setLevelPath + "Sky"
					else:
							sg_unrealLibraryCommands.createDirectory(setLevelPath+"Skies/MPC")
							skyMPCLevelPath = setLevelPath +"Skies/MPC/"

					## Create an MPC folder if it doesn't exist
					if not sg_unrealLibraryCommands.directoryExist(skyMPCLevelPath+"/MPC"):
							sg_unrealLibraryCommands.createDirectory(skyMPCLevelPath+"/MPC")
							skyMPCLevelPath = setLevelPath + "Skies/MPC/"
					else:
							skyMPCLevelPath = setLevelPath + "Skies/MPC/"
							print("Folder already exists")

					## Test if Shader already Exists - Find a good name
					for i in range(0,100):
							assetNewName = skyMPCLevelPath+assetName+"_v" + str(i)
							meshNewName = skyMPCLevelPath+meshName+"_v" + str(i)
							if not sg_unrealLibraryCommands.doesAssetExist(assetNewName):
								break
					
					## Duplicate Material
					materialDuplicated = sg_unrealLibraryCommands.duplicateAsset02(pathToUMaterial,assetNewName)
					materialToAssign = materialDuplicated
					pathToNewMaterial = skyMPCLevelPath

					## Duplicate Mesh
					meshDuplicated = sg_unrealLibraryCommands.duplicateAsset02(pathToUMesh,meshNewName)
					meshToAssign = meshDuplicated
					
				else:
					## Assign Material From Library
					materialToAssign = materialLibraryAsset
					pathToNewMaterial = pathToUMaterial
					## Assign Mesh From Library
					meshToAssign = meshAsset

				## Set Mesh
				meshSlot.set_editor_property('StaticMesh',meshToAssign)

				## Set New Material
				selectedActors[0].set_editor_property('SkyMaterial',materialToAssign)

				## Show Material In Browser
				listPathNewMaterial = [pathToNewMaterial]
				sg_unrealLibraryCommands.showAssetsInContentBrowser(listPathNewMaterial)

				## SetTexture on material
				##sg_unrealLibraryCommands.connectTexturesToLight(textureAsset,material)
			else:
				self.main_widget.lineEdit_sgDisplayMessage.setText("Nothing Selected, please select a skyDome")
				# time.sleep(2)
				# self.main_widget.lineEdit_sgDisplayMessage.setText("")
		else:
			print("Software : "+ action)

	def assignShader(self,action):
		print(" -- Shader/Assign Import -- ")
		try:
			logger.info(" ---- Shader/Assign Import ---- ")
		except:
			pass

		if action == "assign":
			shadingGroup=""
			#  Find Selection in UI
			listToParse = self.findListSelectedItems()

			if in_maya == True:
				listSelectionObject= sg_mayaLibraryCommands.getSelection(False)
				if len(listToParse)>1:
					cmds.warning( "Assignment will not work properly" )
				else:
					for item in listToParse:
						namespaceShader = self.importShader(action="importAssign")
						for content in namespaceShader:
							##Remove Namespace as it was created with a namespace
							fixedName = content.split(":")[-1]
							if cmds.nodeType(fixedName) == 'shadingEngine':
								shadingGroup = fixedName
						for selection in listSelectionObject:
							##Assign Shading Group
							try:
								cmds.sets(selection, e=True, forceElement=shadingGroup)
							except:
								shapes = cmds.listRelatives(selection, shapes=True)
								cmds.connectAttr(shapes[0]+".instObjGroups[0]", shadingGroup+".dagSetMembers[0]", f= True)
							cmds.select(selection,add = True)
			elif in_hou == True:
				shadingNode= self.importShader(action="importAssign")
				shadingNode[0].moveToGoodPosition()
				if hou.selectedNodes():
					for node in hou.selectedNodes():
						node.parm('shop_materialpath').set("/obj/"+shadingNode[0].name()+"/"+shadingNode[1].name())

			if in_maya:
				cmds.inViewMessage( amg="Shader Imported and Assigned: " + str(shadingGroup) + " !", pos='botCenter', fade=True, fadeOutTime=500)

			print("Shader Imported and Assigned: " + str(shadingGroup) + " !")
			try:
				logger.info("Shader Imported and Assigned: %s !",str(shadingGroup))
			except:
				pass

	def importVDB(self,action):                       
			try:
				logger.info(" ---- Import VDB ---- ")
			except:
				pass
			pathVDB = ""
			#### Init per software
			if in_hou:
				houdiniNodeInfos = sg_houdiniLibraryCommands.getCurrentContextNode()
				houdiniContext = houdiniNodeInfos[1]
				houdiniNodePath = houdiniNodeInfos[2]
				houdiniContextPos = houdiniNodeInfos[3]

			#  Find Selection in UI
			listToParse = self.findListSelectedItems()
			
			for item in listToParse:
				# Get Infos
				pathImage,nameAsset,pathToLookIn = self.getDataFromDicImport(item)
				
				files = glob.glob(pathToLookIn + "*.vdb")
				if action == "rman":
					if in_maya:
						if len(files)>1:
							pathVDB = pathToLookIn+nameAsset+"_<f4>" + ".vdb"
						else:
							pathVDB = pathToLookIn+nameAsset + ".vdb"
						vdb = sg_mayaRenderman.createVDB(nameAsset,pathVDB)
					elif in_hou==True:
						if len(files)>1:
							pathVDB = pathToLookIn+nameAsset+"_$F" + ".vdb"
						else:
							pathVDB = pathToLookIn+nameAsset + ".vdb"
						vdb= sg_houdiniLibraryCommands.importVDB(pathVDB,nameAsset,nameAsset+"_VDB",houdiniNodeInfos)

				elif action == "arnold":
					if in_maya:
						if len(files)>1:
							pathVDB = pathToLookIn+nameAsset+"_####" + ".vdb"
							sequence = True
						else:
							pathVDB = pathToLookIn+nameAsset + ".vdb"
							sequence = False
						vdb = sg_mayaArnold.createVDB(nameAsset,pathVDB,sequence)
						sg_mayaArnold.buildVdbShader(vdb)

				elif action == "vdb":
					if in_nuke:
						sg_nukeLibraryCommands.cleanSelection()
						if len(files)>1:
							pathVDB = pathToLookIn+nameAsset+"_####" + ".vdb"
						else:
							pathVDB = pathToLookIn+nameAsset + ".vdb"
						vdb = sg_nukeLibraryCommands.importVDB(pathVDB,nameAsset)

						## Extra Processes
						sg_nukeLibraryCommands.createBackDrop(nameAsset)

				self.main_widget.lineEdit_sgDisplayMessage.setText(pathVDB)
				print("VDB Imported Successfuly: " + pathVDB)
				try:
					logger.info("VDB Imported Successfuly: %s",pathVDB)
				except:
					pass
	
	def importMetaHumans(self):
			#### Idea is unzip and copy - temp for now - Ideal: directly unzip in Unreal content folder
			## Get Content Folder
			contentFolder = sg_unrealLibraryCommands.getAbsoluteProjectContentFolder()
			## Unzip
			self.extractingZip('unzip')
			## Copy Assent to Content Folder
			sg_unrealLibraryCommands.copyToContentFolder(self.pathUnzipFolder+"Metahumans/Common",contentFolder)
			sg_unrealLibraryCommands.copyToContentFolder(self.pathUnzipFolder+"Metahumans/"+self.nameAsset,contentFolder)

	def viewFile(self):
		if self.searchMode == False:
			listToParse = self.main_widget.tableWidget_sgElementBrowser.selectedItems()
		else:
			listToParse = self.main_widget.tableWidget_sgSearchBrowser.selectedItems()
		for item in listToParse:
			if self.context != "Megascans":
					if self.searchMode == False:
						name =self.dicPaths[str(item.row())+str(item.column())][0]["name"]+".json"
						pathRaw = self.dicPaths[str(item.row())+str(item.column())][0]["path"]+name
					else:
						name =self.dicPathsSearch[str(str(item.row()))+str(item.column())][0]["name"]+".json"
						pathRaw = self.dicPathsSearch[str(item.row())+str(item.column())][0]["path"]+name

		if self.platform == "win32" or self.platform == "win64":
			os.system(os.path.abspath(pathRaw))
			##os.popen('start sublime_Text_3 "%s" ' % os.path.abspath(pathRaw))
		elif self.platform == "linux2" or self.platform == "linux":
			subprocess.Popen(["gedit" , os.path.abspath(pathRaw)])
			# os.system("gedit %s" % os.path.abspath(pathRaw))

	def viewLog(self):
		if self.platform == "win32" or self.platform == "win64":
			os.startfile(os.path.abspath(self.pathLogFile))
		elif self.platform == "linux2" or self.platform == "linux":
			subprocess.Popen(["gedit" , os.path.abspath(self.pathLogFile)])

	def openExplorer(self):
		textActionExplorer = "Opening:"
		pathRaw = ""
		if self.currentUITab == 0:
			if self.searchMode == False:
				listToParse = self.main_widget.tableWidget_sgElementBrowser.selectedItems()
			else:
				listToParse = self.main_widget.tableWidget_sgSearchBrowser.selectedItems()
		elif self.currentUITab ==1:
			listToParse = self.main_widget.tableWidget_sgCollectionBrowser.selectedItems()
			
		for item in listToParse:
			if self.context == "Models" or self.context == "Textures" or self.context == "Lightrigs" or self.context == "IES" or self.context == "VDB" or self.context == "DMP" or self.context == "Shaders" or self.context == "Collections" or self.context == "ArtBooks" or self.context == "Tutorials":
				if self.searchMode == False:
					pathRaw = self.dicPaths[str(item.row())+str(item.column())][0]["path"]
				else:
					pathRaw = self.dicPathsSearch[str(self.searchRow)+str(self.searchColumn)][0]["path"]

			elif self.context == "Megascans" or self.context == "MetaHumans":
				pathTemp = self.pathUnzipFolder
				if self.searchMode == False:
					pathTemp02 = self.dicPaths[str(item.row())+str(item.column())][0]["path"]
					nameTemp = self.dicPaths[str(item.row())+str(item.column())][0]["name"]
					# zipFile = self.dicPaths[str(item.row())+str(item.column())][0]["zipFile"]
				else:
					pathTemp02 = self.dicPathsSearch[str(self.searchRow)+str(self.searchColumn)][0]["path"]
					nameTemp = self.dicPathsSearch[str(self.searchRow)+str(self.searchColumn)][0]["name"]
				
				if self.context == "Megascans":
					pathRaw = pathTemp + nameTemp
				else:
					pathRaw = pathTemp + "MetaHumans/"+ nameTemp

				if not os.path.exists(pathRaw):
					pathRaw = pathTemp02.split(nameTemp+"/")[0]
					textActionExplorer = "Asset not unzipped yet, opening library folder instead:"

			elif self.context == "Collections":
				if self.currentUITab ==0:
					if self.searchMode == False:
						pathRaw = self.dicPaths[str(item.row())+str(item.column())][0]["path"]
					else:
						pathRaw = self.dicPathsSearch[str(self.searchRow)+str(self.searchColumn)][0]["path"]
				elif self.currentUITab == 1:
					pathTemp = self.pathUnzipFolder
					if self.searchMode == False:
						pathTemp02 = self.dicPaths[str(item.row())+str(item.column())][0]["path"]
						nameTemp = self.dicPaths[str(item.row())+str(item.column())][0]["name"]
					else:
						pathTemp02 = self.dicPathsSearch[str(self.searchRow)+str(self.searchColumn)][0]["path"]
						nameTemp = self.dicPathsSearch[str(self.searchRow)+str(self.searchColumn)][0]["name"]
					
					if not os.path.exists(pathRaw):
						pathRaw = pathTemp02.split(nameTemp+"/")[0]
						textActionExplorer = "Asset not unzipped yet, opening library folder instead:"
		
			print("\n" + textActionExplorer + " " + pathRaw)

			if self.platform == "win32" or self.platform == "win64" :
				os.popen('start explorer "%s" ' % os.path.abspath(pathRaw))
			elif self.platform == "linux2" or self.platform == "linux":
				if in_nuke:
					os.system('xdg-open "%s" ' % os.path.abspath(pathRaw))
				else:
					os.system('caja "%s" ' % os.path.abspath(pathRaw))
	
	def copyPath(self):
		app = QtWidgets.QApplication.instance()
		clipboard = app.clipboard()
		pathRaw = ""
		if self.searchMode == False:
			listToParse = self.main_widget.tableWidget_sgElementBrowser.selectedItems()
			dictToParse = self.dicPaths
		else:
			listToParse = self.main_widget.tableWidget_sgSearchBrowser.selectedItems()
			dictToParse = self.dicPathsSearch

		pathTemp = self.pathUnzipFolder

		for item in listToParse:
			if self.context == "IES" or self.context == "VDB":
				for file in os.listdir(dictToParse[str(item.row())+str(item.column())][0]["path"]):
					if file.endswith("ies") or file.endswith("IES")or file.endswith("vdb") :
						pathRaw = dictToParse[str(item.row())+str(item.column())][0]["path"]+file
						clipboard.setText(pathRaw)
			elif self.context == "Megascans":
				nameTemp = dictToParse[str(item.row())+str(item.column())][0]["name"]
				pathRaw = pathTemp + nameTemp
				clipboard.setText(pathRaw)
			elif self.context == "Textures" or self.context == "DMP":
				if self.context == "Textures":
					dataFolder = "sourceimages/"
				elif self.context == "DMP":
					dataFolder = "dmpSources/"
				# Try to find sequences in directory, output a dictionary 
				sequences = self.findImageSequences(dictToParse[str(item.row())+str(item.column())][0]["path"]+dataFolder)
				if sequences:
					pathRaw = ",".join(sequences)
					clipboard.setText(pathRaw)
				else:
					for file in os.listdir(dictToParse[str(item.row())+str(item.column())][0]["path"]+dataFolder):
						# TODO sloppy, needs to improve that 
						if file.endswith(".tex"):
							pathRaw = dictToParse[str(item.row())+str(item.column())][0]["path"]+dataFolder+file
							clipboard.setText(pathRaw)
							break
						else:
							pathRaw = dictToParse[str(item.row())+str(item.column())][0]["path"]+dataFolder+file
							clipboard.setText(pathRaw)
							break
			else:
				pathRaw = dictToParse[str(item.row())+str(item.column())][0]["path"]
				clipboard.setText(pathRaw)

		self.main_widget.lineEdit_sgDisplayMessage.setText(pathRaw)

	def loadShader(self,shaderPath,model,houdiniNodeInfos):
		# Shader path
		#
		#
		#
		listShaders=[]
		shaderAlreadyDone=[]
		listShadersFile = glob.glob(shaderPath+"/*.json")
		houMaterialAssign = False
		
		if listShadersFile:
			for shaderFile in listShadersFile:
					## Find the assignment jsonFile
					if self.jsonAttachmentShader in shaderFile:
						with open(shaderFile) as shader_attachment:
								shaderAttachment = json.load(shader_attachment)
								for geo in shaderAttachment:
									index = 1
									shadingGroup = shaderAttachment[geo]['shaders']
									shape = shaderAttachment[geo]['shape']
									typeShader = shaderAttachment[geo]['type']
									print("Type Shader: " + typeShader)
									
									## Load Shader
									shaderToBuild = shaderPath+"/"+shadingGroup+".json"
						
									if shadingGroup not in shaderAlreadyDone:
											if typeShader == 'arnold' :
												if in_maya:
													shader = sg_mayaArnold.readShaderJson(shaderToBuild)
													nameAsset = model
												if in_hou:
													## Data
													nameAsset = shadingGroup
													containerGeo = model
													houdiniContext = houdiniNodeInfos[1]
													houdiniNodePath = houdiniNodeInfos[2]
													houdiniContextPos =houdiniNodeInfos[3]
													
													## Context Update
													if houdiniContext == "Object" or houdiniContext == "Sop" and not "/stage" in houdiniNodeInfos[2]:
														## Create a material assignment
														if houMaterialAssign == False:
															materialAssignNode = sg_houdiniLibraryCommands.createMaterialAssignSOP("materialAssign",containerGeo)
															houMaterialAssign = True
														## Update connector on container geo
														containerGeo[2] = materialAssignNode
														## Create a container for the shader
														containerShader = sg_houdiniLibraryCommands.createContainerShader(shadingGroup,houdiniNodeInfos,containerGeo)
														# materialBuilder = sg_houdiniRenderman.createMaterialBuilder(shadingGroup,containerShader)
													elif houdiniContext == "Lop":
														if self.houdiniMPC == True:
															## Find the Material Library in the lop node
															containerShader = hou.node(self.assetLop[2].path()+"/EDIT/materiallibrary")
															## Update connector on container geo
															materialAssignNode = hou.node(self.assetLop[2].path()+"/EDIT/assignmaterial")
															## Create a material assignment
															# materialAssignNode= sg_houdiniLibraryCommands.createMaterialAssignLOP(shadingGroup,containerShader)
													else:
														self.assignHoudini = None
														containerShader = hou.node('/stage').createNode('materiallibrary',nameAsset+"_Shader")

													## Build Shader
													shaderBuild = sg_houdiniRenderman.readShaderJson(shaderToBuild,shadingGroup,containerShader)
												shaderAlreadyDone.append(shadingGroup)
											elif typeShader == 'renderman':
												if in_maya:
													shader = sg_mayaRenderman.readShaderJson(shaderToBuild)
													nameAsset = model
												if in_hou:
													## Data
													nameAsset = shadingGroup
													containerGeo = model
													houdiniContext = houdiniNodeInfos[1]
													houdiniNodePath = houdiniNodeInfos[2]
													houdiniContextPos =houdiniNodeInfos[3]
													
													print("Houdini Context: ", houdiniContext)
													## Context Update
													if houdiniContext == "Object" or houdiniContext == "Sop" and not "/stage" in houdiniNodeInfos[2]:
														## Create a material assignment
														if houMaterialAssign == False:
															materialAssignNode = sg_houdiniLibraryCommands.createMaterialAssignSOP("materialAssign",containerGeo)
																
															houMaterialAssign = True
														## Update material connector on container geo
														containerGeo[2] = materialAssignNode
														## Create a container for the shader
														containerShader = sg_houdiniLibraryCommands.createContainerShader(shadingGroup,houdiniNodeInfos,containerGeo)
														# materialBuilder = sg_houdiniRenderman.createMaterialBuilder(shadingGroup,containerShader)
													elif houdiniContext == "Lop":
														if self.houdiniMPC == True:
															## Find the Material Library in the lop node
															containerShader = hou.node(self.assetLop[2].path()+"/EDIT/materiallibrary")
															## Update connector on container geo
															materialAssignNode = hou.node(self.assetLop[2].path()+"/EDIT/assignmaterial")
															## Create a material assignment
															# materialAssignNode= sg_houdiniLibraryCommands.createMaterialAssignLOP(shadingGroup,containerShader)
														else:
															containerShader = hou.node('/stage').createNode('materiallibrary',nameAsset+"_Shader")
													else:
														self.assignHoudini = None
														containerShader = hou.node('/stage').createNode('materiallibrary',nameAsset+"_Shader")

													### Build Shader
													shaderBuild = sg_houdiniRenderman.readShaderJson(shaderToBuild,shadingGroup,containerShader)
														
												shaderAlreadyDone.append(shadingGroup)
									else:
											shader = shadingGroup
											if in_hou:
												if houdiniContext == "Object" or houdiniContext == "Sop" and not "/stage" in houdiniNodeInfos[2]:
													# print(shadingGroup,containerGeo[0].path()+ "/" + shadingGroup+"_Shader")
													containerShader = hou.node(containerGeo[0].path()+ "/" + shadingGroup +"_Shader")

									## Create Assign Node
									if in_hou:
										if houdiniContext == "Lop" and self.houdiniMPC == False:
											materialAssignNode = sg_houdiniLibraryCommands.createMaterialAssignLOP(containerGeo)

									######### Assign Shader to geo ########
									if in_maya:
										## Find Geo in the scene
										geometry = nameAsset +":"+ geo
										sg_mayaLibraryCommands.assignShaderOnModel(shader,geometry)
									if in_hou:
										nameModel = shadingGroup
										#print(nameModel)
										sg_houdiniLibraryCommands.assignShaderOnModel(shadingGroup,index,containerShader,containerGeo,shape,materialAssignNode,houdiniNodeInfos,self.houdiniMPC)
										index += 1
		
		############################### Extra Behaviours ######################################
		if in_hou:
			if houdiniContext == "Lop":
				## Render Geometry Settings
				# Check Renderman Version
				self.renderman
				sg_houdiniRenderman.createRenderGeometrySettings(materialAssignNode)
	
	def browseImages(self,action):
		#  Find Selection in UI
		listToParse = self.findListSelectedItems()
		for item in listToParse:
			# Get Infos
			pathImage,nameAsset,pathToLookIn = self.getDataFromDicImport(item)
			# If Selection is not empty
			if nameAsset:
				# Find Folder to look for Images/PDF
				if action == "pdf":
					sourcesFolderPath = os.path.join(pathToLookIn,self.nameATBSource)
				if  action == "dmp":
					sourcesFolderPath = os.path.join(pathToLookIn,self.nameDMPSource)
				# Check if there is a link file. If yes, will use that as source
				linkFile = os.path.join(pathToLookIn, nameAsset+self.jsonDMPLinkExtension)
				if os.path.exists(linkFile):
					dataLink = self.readJsonInfos(linkFile)
					try:
						sourcesFolderPath = dataLink["linkInfos"]["linkToImgs"]
					except:
						print("DMP Link File has changed of structure, ignored for now")
						pass

				# Open Browser
				if self.platform == "win32" or self.platform == "win64" :
					if action == "pdf":
						browser = self.pdfBrowserPathWindows
					elif action == "dmp":
						browser = self.imageBrowserPathWindows
					if browser:
						if action == "pdf":
							pdfs = glob.glob(sourcesFolderPath+"*")
							pdfs = self.naturalSorting(pdfs)
							for file in pdfs:
								subprocess.Popen([browser,os.path.abspath(file)])
						elif action == "dmp":
							subprocess.Popen([browser,os.path.abspath(sourcesFolderPath)])
					else:
						os.popen('start explorer "%s" ' % os.path.abspath(sourcesFolderPath))

				elif self.platform == "linux2" or self.platform == "linux":
					# TODO plug the app 
					if action == "pdf":
						browser = self.pdfBrowserPathLinux 
					elif action == "dmp":
						browser = self.imageBrowserPathLinux
					if browser:
						if action == "pdf":
							pdfs = glob.glob(sourcesFolderPath+"*")
							pdfs = self.naturalSorting(pdfs)
							for file in pdfs:
								os.system('browser "%s" ' % os.path.abspath(file))
						elif action == "dmp":
							os.system('browser "%s" ' % os.path.abspath(sourcesFolderPath))

	def addToCollection(self):
		listIcons = self.getSelectedIcons()
		## Collect Data Collection
		listCollection = self.listFolders(self.collectionLibraryPath)
		## Launch UI
		self.addToCollectionUI = sgAddCollection()

		## Add collection to UI
		self.addToCollectionUI.appendUI(sorted(listCollection))
		self.addToCollectionUI.getListCollections(sorted(listCollection))
		self.addToCollectionUI.setPathCollection(self.collectionLibraryPath)

		response = self.addToCollectionUI.exec_()
		
		if response == 1:
			# if new collection created add that to database
			dicNewCollection = self.addToCollectionUI.saveAddToCollection()
			if dicNewCollection:
				# Can merge the 2 dictionaries
				self.dicAssetDatabase = fcn.mergeDictionaries(self.dicAssetDatabase,dicNewCollection)
				self.dicAllDatabase = fcn.mergeDictionaries(self.dicAssetDatabase,self.dicMegascansZip)

				# Save the dictionary to json
				self.writeJsonFile(self.databaseAssetsJson,self.dicAssetDatabase)
				self.writeJsonFile(self.databaseJson ,self.dicAllDatabase)
			## Get name selected
			try:
				collection = self.addToCollectionUI.listCollectionWidget.currentItem().text()
			except:
				self.sendMessage("No Collection Selected")
				return

			if collection != "":
				print("Collection Selected: " + collection)
				# Write the collection list icon, dictionnary , collection to be added
				data = sg_collectionsCreation.writeCollection(self.collectionLibraryPath,listIcons,self.dicAllDatabase,collection)
				#print(json.dumps(data,indent=4))

		else:
			"Cancel by User"

	def removeFromCollection(self):
			collection = os.path.basename(os.path.dirname(self.collectionPicture))
			listIcons = self.getSelectedIcons()

			removal = sg_collectionsCreation.removeFromCollection(self.collectionLibraryPath,listIcons,collection)
			print("Removed" + str(listIcons)+ "from Collection: " + collection + " " + str(removal))
			## Refresh UI
			self.libraryCollectionBrowser()

	def createContactSheet(self):
		# These are all in pixels space:
		outResW,outResH = 1024,1024
		outRes = (outResW,outResH)
		# Init Variable
		margins = [5,5,5,5]
		padding = 1
		listFilesContactSheet=[]
		rows = 2
		columns = 2
		depth= 3

		## Find Selected Cell
		if self.searchMode == False:
			listToParse = self.main_widget.tableWidget_sgElementBrowser.selectedItems()
		else:
			listToParse = self.main_widget.tableWidget_sgSearchBrowser.selectedItems()

		## UI
		progressBarValue = 0
		self.resetProgressBar(self.pbCreatingContactsheet)

		for item in listToParse:
			if self.context != "Megascans":
				# Get Infos
				pathImage,nameAsset,pathToLookIn = self.getDataFromDicImport(item)
					
			elif self.context == "Megascans":
				# Get Infos
				pathImage,nameTemp,pathTemp02 = self.getDataFromDicImport(item)
				pathToLookIn = self.pathUnzipFolder + nameTemp +"/"
			
			nameIcon= os.path.basename(pathImage)
			if os.path.exists(pathToLookIn) :
				for file in os.listdir(pathToLookIn):
					if file[-depth:].lower() in tuple(self.listImagefileExtension) and file != nameIcon:
						listFilesContactSheet.append(pathToLookIn+file)
			else:
				print(" Path doesn't exist, can't create CS ")
				self.main_widget.lineEdit_sgDisplayMessage.setText(" Path doesn't exist, can't create CS ")
				
		if len(listFilesContactSheet) < 10:
			print("**** Creating CS ... ****")
			## UI
			# Update UI
			progressBarValue = 30.0
			self.main_widget.progressBar_sgLoading.setValue(progressBarValue)

			## Create Contact Sheet
			columns = int(len(listFilesContactSheet)/2.0)
			if columns == 0:
				columns = 1
			rows = int(round(len(listFilesContactSheet)/float(columns) + 0.2 ))
			contactSheet = sg_contactSheet.makeContactSheet(listFilesContactSheet,padding,columns,rows,outResW,outResH,margins,self.pathTempFolder)
			## Show Image
			if self.platform == "win32" or self.platform == "win64" :
				subprocess.Popen([self.imageBrowserPathWindows,os.path.abspath(contactSheet)])
			elif self.platform == "linux2" or self.platform == "linux":
				os.system('caja "%s"'% contactSheet)
			self.main_widget.lineEdit_sgDisplayMessage.setText(contactSheet)
			print("**** CS Done ****")

			# Update UI
			progressBarValue = 100.0
			self.main_widget.progressBar_sgLoading.setValue(progressBarValue)
			self.main_widget.progressBar_sgLoading.setFormat("Done... "+'%p%')

			self.progressBarFinish(timeSleep = 0.5)
		else:
			print( "Too many images,it will take too long to create a Contact Sheet, aborting. Keep it small")
			self.main_widget.lineEdit_sgDisplayMessage.setText("Too many files, too long to create a Contact Sheet, aborting")

	def deleteItemLibrary(self):
		#  Find Selection in UI
		listToParse = self.findListSelectedItems()
		
		for item in listToParse:
			# Get Infos
			pathImage,nameAsset,pathToLookIn = self.getDataFromDicImport(item)
			imageName = os.path.basename(pathImage)
			label = "Remove " + nameAsset + " at path " + pathToLookIn
			
			## Needs to check if the aset is locked or not Loophole right now

			## Launch UI
			self.removeItemDialog = sgRemoveItemConfirmDialog()
			self.removeItemDialog.setTextRemoval(label)
			
			## Get Confirmation Dialog
			approval = self.removeItemDialog.exec_()

			## Get Result
			if approval == QtWidgets.QMessageBox.Ok:
				# Remove Dictionary Entry
				deletedEntryAssetDic = self.removeItemFromAssetDatabase(imageName)
				deleteEntryGlobDic = self.removeItemFromGlobalDatabase(imageName)
				fcn.saveAssetDatabase(self.databaseAssetsJson,self.dicAssetDatabase)
				self.dicAllDatabase = fcn.saveGlobalDatabase(self.dicAllDatabase,self.databaseJson,self.dicAssetDatabase,self.dicMegascansZip)
				if deletedEntryAssetDic:
					print("Removed element: " + nameAsset + " - Successful")
				# Remove Folder / For now no check
				deletedFolder = self.deleteFolderLibrary(pathToLookIn)
				print("Removed folder: " + pathToLookIn + " - Successful")
				print("\n")

		# Refresh Library
		self.refreshLibrary()
		self.launchBrowsing()

#######################################################################################################################
################################################ MEGASCANS LOADING ####################################################
#######################################################################################################################
	
	def refreshTreeView(self):
		## Get selection
		self.selectedPath[2]
		self.main_widget.treeWidget_sgLibrary.clear()
		self.libraryFolderStructure(self.libraryPath,self.main_widget.treeWidget_sgLibrary)

	def queryInput(self,test):
		self.listReturnLODs = cmds.textScrollList(objectScroll,query = True,selectItem = True)
		##print("LOD(s) choosen: " + str(self.listReturnLODs))
		cmds.layoutDialog(dismiss="OK")
		cmds.waitCursor( state=True )
		return self.listReturnLODs

	def findShaderTemplate(self,nameAsset,renderer):
		listPlants= ["aquatic","plant","grass","herb","mushroom","ocean","shrub","succulent","tree","weed","wood","moss"]
		listRocks= ["rock","stone","ground","structure","brick","antique","building","cardboard","castle","manmade","modular","sandy","street","terrain","tiles","wall"]
		listMetals = ["metal","hardware","grass","herb","mushroom","ocean","shrub","succulent","tree","weed","wood","moss"]

		if in_maya or in_hou:
			extention = ".json"
		elif in_katana:
			extention = ".katana"
		elif in_unreal:
			extention = ".uasset"
		else:
			extention = ".json"

		if renderer == "rman":
			rendererPath = "renderman/"
		elif renderer == "arnold":
			rendererPath = "arnold/"
		elif renderer == "unreal":
			rendererPath = "unreal/"
		else:
			rendererPath = ""
		if not in_unreal:
			if any(plant in nameAsset.lower() for plant in listPlants):
				shaderPath = self.shaderLibraryPath+ rendererPath + "megascans/plantShaderDefault/plantShaderDefault"+extention
			elif any(metal in nameAsset.lower() for metal in listMetals):
				shaderPath = self.shaderLibraryPath+ rendererPath + "megascans/metalShaderDefault/metalShaderDefault"+extention
			elif any(rock in nameAsset.lower() for rock in listRocks):
				shaderPath = self.shaderLibraryPath+ rendererPath + "megascans/rockShaderDefault/rockShaderDefault"+extention
			else:
				shaderPath = self.shaderLibraryPath+ rendererPath + "megascans/shaderDefault/shaderDefault"+extention
		else:
			## Unreal Split for the type of Material
			if self.subContext == "3d" or self.subContext == "surface":
				if any(plant in nameAsset.lower() for plant in listPlants):
					shaderPath = self.shaderLibraryPath+ rendererPath + "megascans/MS_DefaultMaterial_Foliage/MS_DefaultMaterial_Foliage"+extention
				elif any(metal in nameAsset.lower() for metal in listMetals):
					if self.unrealDisplacement == True:
							shaderPath = self.shaderLibraryPath+ rendererPath + "megascans/MS_DefaultMaterial_Displacement/MS_DefaultMaterial_Displacement"+extention
					else:
							shaderPath = self.shaderLibraryPath+ rendererPath + "megascans/MS_DefaultMaterial/MS_DefaultMaterial"+extention
				elif any(rock in nameAsset.lower() for rock in listRocks):
					if self.unrealDisplacement == True:
						shaderPath = self.shaderLibraryPath+ rendererPath + "megascans/MS_DefaultMaterial_Displacement/MS_DefaultMaterial_Displacement"+extention
					else:
						shaderPath = self.shaderLibraryPath+ rendererPath + "megascans/MS_DefaultMaterial/MS_DefaultMaterial"+extention
				else:
					if self.unrealDisplacement == True:
						shaderPath = self.shaderLibraryPath+ rendererPath + "megascans/MS_DefaultMaterial_Displacement/MS_DefaultMaterial_Displacement"+extention
					else:
						shaderPath = self.shaderLibraryPath+ rendererPath + "megascans/MS_DefaultMaterial/MS_DefaultMaterial"+extention
			elif self.subContext == "atlas":
				shaderPath = self.shaderLibraryPath+ rendererPath + "megascans/Atlas_Material/Atlas_Material"+extention
			elif self.subContext == "brush":
				shaderPath = self.shaderLibraryPath+ rendererPath + "megascans/BrushDecal_Material/BrushDecal_Material"+extention

		print("Apply Shader Preset: "+ shaderPath)

		return shaderPath

	def unzipMegascan(self):
		timeStart = time.time()
		megascanFiles = []

		self.lodGeometryList= []
		self.LODList= []
		self.lodImageList=[]
		self.listFileToUnzip=[]
		self.lodImagesToLoad =[]
		self.variantAsset = False
		self.lodGeometryToLoad =[]
		self.nameNamespace=[]
		self.importedMObject=[]
		self.extraList= []
		self.lod = ""

		try:
			logger.info(" ---- Megascans Extraction Process Started ---- ")
		except:
			pass
		
		####################################################### UI ###################################################
		self.main_widget.lineEdit_sgDisplayMessage.setText("")
		progressBarValue = 0
		self.main_widget.progressBar_sgLoading.setValue(progressBarValue)
		self.main_widget.progressBar_sgLoading.setTextVisible(True)
		self.main_widget.progressBar_sgLoading.setFormat("Unzipping... "+'%p%')
		self.main_widget.progressBar_sgLoading.setAlignment(QtCore.Qt.AlignCenter)

		########################## Find the zip from the selection and list its content
		if self.currentUITab == 0:
			item = self.main_widget.tableWidget_sgElementBrowser.selectedItems()
			if self.searchMode == False:
				try:
					pathImage = self.dicPaths[str(item[0].row())+str(item[0].column())][0]["preview"]
					self.nameAsset = self.dicPaths[str(item[0].row())+str(item[0].column())][0]["name"]
				except:
					print(sys.exc_info())
					print(traceback.format.exc())
					return
					pass
			else:
				try:
					pathImage = self.dicPathsSearch[str(self.searchRow)+str(self.searchColumn)][0]["preview"]
					self.nameAsset = self.dicPathsSearch[str(self.searchRow)+str(self.searchColumn)][0]["name"]
				except:
					print(sys.exc_info())
					print(traceback.format.exc())
					return
					pass
		if self.currentUITab == 1:
			item = self.main_widget.tableWidget_sgCollectionBrowser.selectedItems()
			try:
				pathImage = self.dicPaths[str(item[0].row())+str(item[0].column())][0]["preview"]
				self.nameAsset = self.dicPaths[str(item[0].row())+str(item[0].column())][0]["name"]
			except:
				print(sys.exc_info())
				print(traceback.format.exc())
				return
				pass

		nameIcon= os.path.basename(pathImage)
		## Find zip in dictionary - now the all database
		pathZip = str(self.dicAllDatabase[nameIcon][0]["zipFile"] )
		# pathZip = str(self.dicMegascansZip[nameIcon][0]["zipFile"] )
		
		## window/linux issue with hardcoded path in dictionary between Linux and Windows
		if self.platform == "win32" or self.platform == "win64":
			#pathZip = pathZip.replace("/jobs","J:")
			pathZip = pathZip.replace(self.megascanZIPLibraryLinPath,self.megascanZIPLibraryWinPath)
		elif self.platform == "linux" or self.platform == "linux2":
			#pathZip = pathZip.replace("J:","/jobs")
			pathZip = pathZip.replace(self.megascanZIPLibraryWinPath,self.megascanZIPLibraryLinPath)

		if os.path.exists(pathZip):
			self.compressedFile = zipfile.ZipFile(pathZip, "r")
		else:
			print("\n")
			print("Zip file don't exist check if database is correct")
		listZipFiles = self.compressedFile.namelist()

		###################################### Organise every zip per file or asset to load ############################
		for filename in listZipFiles:
			if "var" in filename.lower() or "/" in filename :
				self.variantAsset = True
				if any ( extension in filename.lower() for extension in self.listImagesFormat):
					self.lodImageList.append(filename)
				if any ( extension in filename.lower() for extension in self.list3dFormat):
					self.lodGeometryList.append(filename)
					LOD = filename.split("_")[-1].split(".")[0]
					if LOD not in self.LODList:
						self.LODList.append(filename.split("_")[-1].split(".")[0])
			else:
				if any ( extension in filename.lower() for extension in self.listImagesFormat):
					self.lodImageList.append(filename)
				if any ( extension in filename.lower() for extension in self.list3dFormat):
					self.lodGeometryList.append(filename)
					LOD = filename.split("_")[-1].split(".")[0]
					if LOD not in self.LODList:
						self.LODList.append(filename.split("_")[-1].split(".")[0])
				if any ( extension in filename.lower() for extension in self.listExtraFormat):
					self.extraList.append(filename)

		if self.variantAsset == True:
			print("\n")
			print("Several Variant of the asset are in the zip")
		else:
			print("\n")
			print("No Model Variant found")

		self.LODList.sort()

		## Folder Creation if needed - Metahumans ar eunzipped automatically in the metahumans folder so can skip that
		if self.context != "MetaHumans":
			self.folderUnzip = self.pathUnzipFolder+self.nameAsset
			if not os.path.exists(self.pathUnzipFolder+self.nameAsset):
				self.createNewFolder(self.pathUnzipFolder+self.nameAsset)
		
		print("Used action: " + self.usedRenderer)
		############################# Confirm the LOD or automatically pick it from the UI #############################
		if len(self.lodGeometryList) != 0 :
			self.returnLODValue = []
			if self.usedRenderer != "unzip" :
				## Launch Pick LOD UI
				self.pickLODUI = sgPickLOD()
				## Add LODs to listWidget
				self.pickLODUI.appendUI(self.LODList)

				## Find the default choice
				if in_maya == True:
					cmds.scriptEditorInfo(suppressWarning=True,suppressErrors=True,suppressResults=True)
					cmds.waitCursor( state= False )
					widgItem = self.pickLODUI.listLODWidget.findItems(self.mayaLOD,QtCore.Qt.MatchExactly)
				elif in_hou == True:
					widgItem =self.pickLODUI.listLODWidget.findItems(self.houdiniLOD,QtCore.Qt.MatchExactly)
				elif in_nuke == True:
					widgItem =self.pickLODUI.listLODWidget.findItems(self.nukeLOD,QtCore.Qt.MatchExactly)
				elif in_katana == True:
					widgItem =self.pickLODUI.listLODWidget.findItems(self.katanaLOD,QtCore.Qt.MatchExactly)
				elif in_mari == True:
					widgItem =self.pickLODUI.listLODWidget.findItems(self.mariLOD,QtCore.Qt.MatchExactly)
				elif in_blen == True:
					widgItem =self.pickLODUI.listLODWidget.findItems(self.blenderLOD,QtCore.Qt.MatchExactly)
				elif in_unreal == True:
					widgItem =self.pickLODUI.listLODWidget.findItems(self.unrealLOD,QtCore.Qt.MatchExactly)
				
				## Preselect the proposed LOD
				if widgItem:
					self.pickLODUI.listLODWidget.setCurrentItem(widgItem[0])
				else:
					self.pickLODUI.listLODWidget.setCurrentRow(0)

				## Wait for User
				valueLODWindow = self.pickLODUI.exec_()

				returnSelection = self.pickLODUI.listLODWidget.selectedItems()
				if valueLODWindow == "Cancel" or valueLODWindow == 0:
					return "Cancel"
				else:
					if returnSelection:
						for item in returnSelection:
							self.returnLODValue.append(item.text())

				## Unreal stays appart for now
				if in_unreal == True:
					if self.usedRenderer != "unzip" :
						self.returnLODValue =[]
						if self.unrealLOD in self.LODList:
							self.returnLODValue.append(self.unrealLOD)
						else:
							self.returnLODValue.append("LOD0")

						## For Lod switch
						self.returnLODValue.append(self.LODList[-2])
						self.returnLODValue.append(self.LODList[-1])
			else:
				## If action is unzip, take all the lods
				self.returnLODValue=self.LODList
		else:
			self.returnLODValue = ""

		######################### Log Megascans ####
		try:
			logger.info("Megascans chosen: %s",self.nameAsset)
			logger.info("LOD chosen: %s",self.returnLODValue)
			logger.info("Renderer chosen: %s",self.usedRenderer)
		except:
			pass
		##### LOD Count
		self.LODAmount = len(self.returnLODValue)
		################################ Select the geometry to unzip ######################################
		print(" ---- Megascans Unzipping Process Starting ---- ")
		if self.lodGeometryList :
			for geo in sorted(self.lodGeometryList):
				for lod in self.returnLODValue:
					if lod in geo:
						self.lodGeometryToLoad.append(geo)
						self.lod = lod
						self.modelType = geo.split(".")[-1]
						# print("Namespace for Geo = " + geo.replace("/", "_").split(".")[0])
						self.nameNamespace.append(geo.replace("/", "_").split(".")[0])
		else:
			print("No geometry to unzip, must be a shader or a texture ")
			self.lodGeometryToLoad = ""

		## Select Brushes and ZTL == ALL
					
		#################################### Select the pictures to unzip ###################################
		for pic in self.lodImageList:
			if "LOD" in pic.split("_")[-1] :
				for lod in self.returnLODValue:
					if lod in pic:
						self.lodImagesToLoad.append(pic)
			else:
					self.lodImagesToLoad.append(pic)

		############################################ UI Progress Bar ########################################
		progressBarValue = 0
		percentage = int(100/(len(self.lodImagesToLoad)+ len(self.lodGeometryToLoad) + 1))

		self.main_widget.progressBar_sgLoading.setValue(progressBarValue)
		self.main_widget.progressBar_sgLoading.setTextVisible(True)
		self.main_widget.progressBar_sgLoading.setFormat("Unzipping... "+'%p%')
		self.main_widget.progressBar_sgLoading.setAlignment(QtCore.Qt.AlignCenter)

		########################################### Extract Geometry #######################################
		if self.lodGeometryToLoad:
			for geometryToLoad in self.lodGeometryToLoad:
				if not os.path.exists(self.folderUnzip+ "/" + geometryToLoad ):
					self.compressedFile.extract(geometryToLoad,self.folderUnzip+"/")
					## UI Progress Bar
					progressBarValue += percentage
					self.main_widget.progressBar_sgLoading.setValue(progressBarValue)
				else:
					print(" ---- Geometry already there, skip extraction ---- ")
		else:
			print("Only Shader or Texture(s) to load")

		######################################### Extract Extras ###########################################
		if self.extraList:
			for extra in self.extraList:
				if not os.path.exists(self.folderUnzip+"/" +extra):
					self.compressedFile.extract(extra,self.folderUnzip+"/")
					## UI Progress Bar
					progressBarValue += percentage
					self.main_widget.progressBar_sgLoading.setValue(progressBarValue)
				# else:
					# print("Extras already there, skip extraction")
		else:
			print("No ZTL or Brushes to load")

		########################################## Extract Images ##########################################
		for image in self.lodImagesToLoad:
			if not os.path.exists(self.folderUnzip+"/" +image):
				self.compressedFile.extract(image,self.folderUnzip+"/")
				## UI Progress Bar
				progressBarValue += percentage
				self.main_widget.progressBar_sgLoading.setValue(progressBarValue)
		##########################################  MetaHumans ###########################################
		if self.context == "MetaHumans":
			self.compressedFile.extractall(self.pathUnzipFolder)

		self.compressedFile.close()

		## Drag and Drop
		# self.objectsToDrop = self.lodImagesToLoad + self.lodGeometryList

		##########################################  Brushes  ###############################################
		if self.context == "Megascans" and self.subContext == "brush":
			# UI will probably not be relevant
			progressBarValue = 0
			self.main_widget.progressBar_sgLoading.setValue(0)
			self.main_widget.progressBar_sgLoading.setFormat("Converting Brush... "+'%p%')
			for image in self.lodImagesToLoad:
				if not os.path.exists(self.folderUnzip+"/"+ image.split(".")[0] + ".png"):
					try:
						self.convertToPNG(self.folderUnzip+"/"+image)
					except:
						print("Could not convert to PNG: " + self.folderUnzip+"/"+image,sys.exc_info())
						pass
				# Update UI
				progressBarValue += percentage
				self.main_widget.progressBar_sgLoading.setValue(progressBarValue)

		################################################## Messages ####################################################
		timeEnd = time.time()
		timeElapsed = timeEnd - timeStart
		
		print("Unzipped Geometry: "+"\n" + '\n'.join("- " + str(p) for p in sorted(self.lodGeometryToLoad)))
		print("Unzipped Extras: "+"\n" + '\n'.join("- " + str(p) for p in sorted(self.extraList)))
		print("Unzipped Textures: "+"\n" + '\n'.join("- " + str(p) for p in sorted(self.lodImagesToLoad)))
		print("\n")
		print(" ---- Unzip Finished in: "+  str(timedelta(seconds=timeElapsed)) + " ---- ")
		try:
			logger.info(" ---- Unzip Finished ---- ")
		except:
			pass

		self.main_widget.progressBar_sgLoading.setValue(100)

		############################################## Unzip Action or Load Geometry ###################################
		if self.usedRenderer== "unzip":
			self.main_widget.lineEdit_sgDisplayMessage.setText("Unzip Done, opening Explorer .... ")
			self.progressBarFinish(timeSleep = 0.15)
			self.openExplorer()
		else:
			print ("\n" + " ---- Loading Geometry and/or Textures ---- ")
			try:
				logger.info(" ---- Loading Geometry and/or Textures ---- ")
			except:
				pass

		self.main_widget.lineEdit_sgDisplayMessage.setText("")
		return "Ok"

	def loadMegascans(self):
			# Set Variables
			self.listTextureFilesMegascans = []
			self.textureNodes = []
			self.manifold = ""
			self.sharedUV =  self.main_widget.checkBox_sgTextureSharedUV.isChecked()
			self.triplanar =  self.main_widget.checkBox_sgTextureTriplanar.isChecked()

			self.houdiniSettings = self.main_widget.sgHoudiniSettings_Settings.itemText(self.main_widget.sgHoudiniSettings_Settings.currentIndex())
			
			if self.houdiniSettings == "MPC":
				self.houdiniMPC= True
			else:
				self.houdiniMPC = False

			p = 0
			self.dictModelConnection = {}
			self.listFullpathImages = []
			self.listBillboardImages = []
			listTextureNodeCreated = []
			texturesBillboard = []
			readNode = None

			## Fix Name
			self.nameAsset = self.nameAsset.replace(" ", "_")
			self.idMegascans = self.nameAsset.split("_")[-2]
			self.categoryMegascans = self.nameAsset
			self.nameMegascans = self.nameSelection + "_" + self.idMegascans
			self.nameMegascans = self.nameMegascans.replace(" ", "_")

			########################################## Initiliase For Software ##########@##################################
			## Katana node Pos
			xPos = -500
			yPos = -750
			xOffset = 500
			yOffset = 500

			## Unreal
			index = 0

			## Maya
			if in_maya:
				# cmds.scriptEditorInfo(suppressWarning=False,suppressErrors=False,suppressResults=False)
				cmds.scriptEditorInfo(suppressWarning=True,suppressErrors=True,suppressResults=True)
				
			## Houdini 
			if in_hou:
				## Get the context from the node editor
				houdiniNodeInfos = sg_houdiniLibraryCommands.getCurrentContextNode()
				houdiniContext = houdiniNodeInfos[1]
				houdiniNodePath = houdiniNodeInfos[2]
				houdiniContextPos =houdiniNodeInfos[3]
				sg_houdiniLibraryCommands.cleanSelection()
				if self.houdiniMPC == True and houdiniContext == "Lop" and self.usedRenderer != "atlas":
					assetLop = sg_houdiniLibraryCommands.importMPCMegascansLop(self.nameAsset)
			## Nuke
			if in_nuke :
				## Let's deselect all Nodes
				sg_nukeLibraryCommands.clearSelection()
			############################################# Load Geometry ###################################################
			
			if self.lodGeometryToLoad :
				for geometryToLoad in self.lodGeometryToLoad:
					modelPath = self.folderUnzip+ "/" +geometryToLoad
					otherLODs=[]
					geometryFilename = os.path.basename(geometryToLoad)
					if "LOD" in geometryToLoad:
						number = int(geometryFilename.split(".")[0].split("LOD")[-1])
						self.mpcLOD = chr(ord('A')+number)
						self.nameAsset = geometryFilename.split("LOD")[0]+ "LOD" + self.mpcLOD
					else:
						self.nameAsset = geometryFilename.split(".")[0]
					## Fix name
					self.nameAsset = self.nameAsset.replace(" ", "_")

					if in_maya:
						##if self.usedRenderer != "mayaDrop":
						cmds.file(self.folderUnzip+"/"+geometryToLoad, i=True, f=True, op= "materials=0", namespace= self.nameNamespace[p] )
						self.renameDuplicates()
						self.importedMObject.append(cmds.ls( self.nameNamespace[p]+":*", type ="transform" ))
						# Cleanup uv set
						sg_mayaLibraryCommands.renameMegascanUVSet(cmds.ls( self.nameNamespace[p]+":*", type ="transform" ))
						# Set Max Scale
						sg_mayaLibraryCommands.setTransform(cmds.ls( self.nameNamespace[p]+":*", type ="transform" ),self.sizeSelectedElmt)
						p += 1
					if in_hou:
						if self.usedRenderer != "houdiniDrop":
							if self.houdiniMPC:
								if houdiniContext == "Object" or houdiniContext == "Sop" and not "/stage" in houdiniNodePath:
									model = sg_houdiniLibraryCommands.importMegascansModel(modelPath,self.nameMegascans, self.nameAsset,houdiniNodeInfos)
								elif  houdiniContext == "Lop":
									model = sg_houdiniLibraryCommands.importMPCMegascansModel(assetLop,modelPath,self.mpcLOD)
									sg_houdiniLibraryCommands.setLOPVariant(assetLop[1])
							else:
								model = sg_houdiniLibraryCommands.importMegascansModel(modelPath,self.nameMegascans, self.nameAsset,houdiniNodeInfos)
							if model[0] not in self.importedMObject:
								self.importedMObject.append(model[0])
							
							print("Model created: "+   model[0].name())
					if in_nuke:
						if self.usedRenderer != "nukeDrop":
							sg_nukeLibraryCommands.importModel(self.folderUnzip+"/"+geometryToLoad,self.sizeSelectedElmt)
						else:
							self.objectsToDrop.append(self.folderUnzip+"/"+geometryToLoad)
					if in_mari:
						project = sg_mariLibraryCommands.currentProject()
						if project != None:
							## Import Megascans in the current project
							new = False
							channels = sg_mariLibraryCommands.createImportChannels(self.folderUnzip+"/", self.folderUnzip+"/"+geometryToLoad,self.lodImagesToLoad,self.returnLODValue,self.listMariChannels,new,self.mariColorspace)
							sg_mariLibraryCommands.importMegascansModel( self.folderUnzip+"/"+geometryToLoad,channels[0])
						else:
							## Create a new Mari project then import
							new = True
							channels = sg_mariLibraryCommands.createImportChannels(self.folderUnzip+"/", self.folderUnzip+"/"+geometryToLoad,self.lodImagesToLoad,self.returnLODValue,self.listMariChannels,new,self.mariColorspace)
							project = sg_mariLibraryCommands.createNewProject(self.nameMegascans,self.folderUnzip+"/"+geometryToLoad,channels[0])
							##sg_mariLibraryCommands.importMegascansModel(self.folderUnzip+"/", self.folderUnzip+"/"+geometryToLoad,self.lodImagesToLoad,self.returnLODValue)
					if in_blen:
						model = sg_blenderLibraryCommands.importMegascansModel(modelPath,self.nameAsset,self.overrideBlenderContext)
						self.importedMObject.append(model)
					if in_unreal:
						## Fix if unreal tool loaded in nuke
						if in_nuke == False:
							mainLOD= self.folderUnzip+"/"+self.lodGeometryToLoad[index]
							for i in range(1,self.LODAmount):
								otherLODs.append(self.folderUnzip+"/"+self.lodGeometryToLoad[index+i])
							nameVariant = os.path.splitext(os.path.basename(mainLOD))[0]
							#self.nameAssetMegascans = self.nameSelectedElmt + "_" + nameVariant + "_" + self.idMegascans
							self.nameAssetMegascans = self.nameSelection + "_" + nameVariant + "_" + self.idMegascans
							
							self.importedMObject.append(sg_unrealLibraryCommands.importModel(mainLOD,otherLODs,self.nameMegascans,self.nameAssetMegascans,self.categoryMegascans))
							if index + self.LODAmount < len(self.lodGeometryToLoad)-1:
								index += self.LODAmount
							else:
								break
				##  Fix list Objects
				if in_maya:
						tmpList = [j for i in self.importedMObject for j in i]
						self.importedMObject = tmpList
							
			else:
				self.importedMObject = None
				model=["","","",""]
				print("No Geometry to Load")

			################################################ Load Textures ################################################
			## Create or Find Container for Textures/Shader
			if in_hou == True and self.usedRenderer != "atlas":
				self.assignHoudiniNode = None
				if houdiniContext == "Object" or houdiniContext == "Sop" and not "/stage" in houdiniNodePath:
						# self.containerTexture = hou.node('/obj').createNode('matnet',self.nameMegascans+"_Shader")
						self.containerTexture = sg_houdiniLibraryCommands.createContainerShader(self.nameMegascans,houdiniNodeInfos,model)
						self.assignHoudiniNode = model[3]
				elif houdiniContext == "Lop":
					if self.houdiniMPC == True:
						self.containerShader = sg_houdiniLibraryCommands.importMegascansShaderLop(assetLop,self.nameAsset)
						self.containerTexture = self.containerShader[1]
						self.assignHoudiniNode = self.containerShader[2]
					else:
						self.assignHoudini = None
						self.containerTexture = hou.node('/stage').createNode('materiallibrary',self.nameMegascans+"_Shader")
				elif houdiniContext == "Vop":
						self.containerTexture = hou.node(houdiniNodePath)
				self.containerTexture.moveToGoodPosition()
			elif in_katana:
				self.contextKatana = sg_katanaLibraryCommands.getContext()
				if self.contextKatana != "rootNode":
					self.childrenInGroup = sg_katanaLibraryCommands.getChildren(self.contextKatana)
				else:
					self.childrenInGroup = []
				## Find Shader Template to use
				katanaShader = self.findShaderTemplate(self.categoryMegascans,self.usedRenderer )
				## Load container and shader type
				self.containerTexture = sg_katanaLibraryCommands.loadContainer(self.shaderLibraryPath,self.nameMegascans, self.context,katanaShader)
				if self.containerTexture == None:
						self.containerTexture = sg_katanaLibraryCommands.createNetworkMaterial(self.nameMegascans+"_Shader")
			## Manifold
			if self.usedRenderer == "rman":
				if in_maya:
					if self.sharedUV == True:
						self.manifold = sg_mayaRenderman.createSharedRmanTexture(self.sharedUV, self.triplanar)
				if in_hou:
					self.manifold = sg_houdiniRenderman.createSharedRmanTexture(self.sharedUV,self.triplanar,self.containerTexture,self.nameAsset+"_manifold")
				if in_katana:
					self.manifold = sg_katanaRenderman.createSharedRmanManifold(self.sharedUV, self.triplanar,self.containerTexture,self.nameAsset,xPos)

			elif self.usedRenderer == "arnold":
				if in_maya:
					if self.triplanar == False and self.sharedUV == True:
						self.manifold = sg_mayaArnold.createSharedArnoldTexture(self.sharedUV, self.triplanar)
					elif self.triplanar == True and self.sharedUV == True:
						self.manifold = sg_mayaArnold.createSharedArnoldTexture(self.sharedUV, self.triplanar)

			elif self.usedRenderer == "mayaDefault":
				if in_maya:
					if self.triplanar == False and self.sharedUV == True:
						self.manifold = sg_mayaLibraryCommands.createSharedMayaTexture(self.sharedUV, self.triplanar)
					elif self.triplanar == True and self.sharedUV == True:
						self.manifold = sg_mayaLibraryCommands.createSharedMayaTexture(self.sharedUV, self.triplanar)
					else:
						print("Don't know what to do!")

			elif self.usedRenderer == "mantra":
				self.manifold = sg_houdiniMantra.createSharedMantraTexture(self.sharedUV,self.triplanar,self.containerTexture,self.nameAsset+"_manifold")
			## Create Textures
			idName = "_" + str(random.randint(0,9999999))
			# Get Megascans Dictionary

			for image in sorted(self.lodImagesToLoad):
				# print(image)
				self.filename = self.folderUnzip+"/"+image
				self.listFullpathImages.append(self.filename)

				if image in self.dataAssetSelected[self.picturePath][0]["maps"]:
					dataTexture = self.dataAssetSelected[self.picturePath][0]["maps"][image]
					#print(json.dumps(self.dataAssetSelected[self.picturePath][0]["maps"][image],indent = 4))
				else:
					dataTexture = {}
					#print(" ------- Can't find data on Texture: " + image)

				## Set name of Texture Node
				nameTextureNode = "T_"+ os.path.basename(self.filename).split(".")[0]

				## Create Name Image
				if "/" in image:
					nameImage =os.path.basename(image).split(".")[0]
				else:
					nameImage = image.split(".")[0]

				## Separate per Software/Renderer
				if self.usedRenderer == "rman":
					if in_maya:
						if cmds.objExists(nameTextureNode):
							nameTextureNode += idName
						texture = sg_mayaRenderman.createTextureFileRman(self.sharedUV, self.triplanar,self.manifold,self.filename,nameTextureNode)
					if in_hou:
						texture = sg_houdiniRenderman.createTextureFileRman(self.sharedUV, self.triplanar,self.manifold,nameTextureNode,self.filename,self.containerTexture)
					if in_katana:
						if NodegraphAPI.GetNode(nameTextureNode):
							nameTextureNode += idName
						texture = sg_katanaRenderman.createTextureFileRman(self.sharedUV, self.triplanar,self.manifold,self.filename,self.containerTexture,nameTextureNode,xPos,yPos)
						yPos += yOffset
					if in_nuke:
						texture = sg_nukeLibraryCommands.createTextureFileNuke(self.filename)
						# Get color map
						if "albedo" in self.filename.lower():
							readNode = texture
						##ocio = sg_nukeLibraryCommands.createOCIONuke(texture,True)
					if in_mari:
						if len(self.lodGeometryToLoad) == 0:
							sg_mariLibraryCommands.createTextureCategory(self.nameMegascans)
							texture = sg_mariLibraryCommands.importTextureMegascans(self.filename,self.mariColorspace)
				if self.usedRenderer == "brush":
					if in_mari:
						if len(self.lodGeometryToLoad) == 0:
							#self.openFileInExplorer(self.filename)
							self.openExplorer()
							#sg_mariLibraryCommands.createBrush(self.nameMegascans)
				elif self.usedRenderer == "arnold":
					if in_maya:
						if cmds.objExists(nameTextureNode):
							nameTextureNode += idName
						texture = sg_mayaArnold.createTextureFileArnold(self.sharedUV, self.triplanar,self.manifold,self.filename,nameTextureNode,dataTexture)
				elif self.usedRenderer == "mayaDefault":
					if in_maya:
						texture = sg_mayaLibraryCommands.createTextureFileMaya(self.sharedUV, self.triplanar,self.manifold,self.filename)
				elif self.usedRenderer == "mantra":
					texture = sg_houdiniMantra.createTextureFileMantra(self.sharedUV, self.triplanar,self.manifold,nameTextureNode,self.folderUnzip+"/"+image,self.containerTexture)
				elif self.usedRenderer == "blender":
					texture = sg_blenderLibraryCommands.createTextureFileBlender(nameImage,self.folderUnzip+"/"+image)
				elif self.usedRenderer == "nukeDrop":
					self.objectsToDrop.append(self.filename)

				## Variant Textures ( Switch which texture to list for Arnold and Triplanar)
				if self.variantAsset == False:
					if self.triplanar and self.usedRenderer == "arnold":
						self.listTextureFilesMegascans.append(texture)
					else:
						self.listTextureFilesMegascans.append(nameTextureNode)
				else:
					if "billboard" not in image.lower():
						if self.triplanar and self.usedRenderer == "arnold":
							self.listTextureFilesMegascans.append(texture)
						else:
							self.listTextureFilesMegascans.append(nameTextureNode)
					else:
						self.listBillboardImages.append(self.filename)

			## Unreal can take a list to load textures
			if in_unreal :
				if in_nuke == False:
					textures = sg_unrealLibraryCommands.importTextures(self.listFullpathImages,self.nameMegascans)
					if self.listBillboardImages:
						texturesBillboard = sg_unrealLibraryCommands.importTextures(self.listBillboardImages,self.nameMegascans+"/Billboard")

			############################################### Build Shader ##################################################
			jsonShader = self.findShaderTemplate(self.categoryMegascans,self.usedRenderer)
			if self.usedRenderer == "rman":
				if in_maya:
						sg_mayaRenderman.loadMegascansShaderR(jsonShader,self.listTextureFilesMegascans,self.nameMegascans,self.importedMObject,self.manifold,idName)
						##sg_mayaRenderman.buildMegascanShaderR(self.listTextureFilesMegascans,self.usedRenderer,self.nameAsset,self.importedMObject,self.manifold,idName )
				elif in_hou:
						##Layout the textures first
						sg_houdiniLibraryCommands.layoutSelection(self.containerTexture)
						## Create Shader only if not in VOP else skip
						if houdiniContext != "Vop":
							shadingGroup = sg_houdiniRenderman.loadMegascanShaderR(jsonShader,self.listTextureFilesMegascans,self.nameMegascans,self.importedMObject,self.manifold,idName,self.containerTexture,houdiniNodeInfos)
							sg_houdiniRenderman.assignShader(self.containerTexture,shadingGroup[0],self.nameAsset,self.nameMegascans,self.importedMObject,self.assignHoudiniNode,houdiniNodeInfos,self.houdiniMPC)
							if houdiniContext == "Lop" :
								openGLShader = sg_houdiniRenderman.buildOGLShader(self.listTextureFilesMegascans,self.containerTexture,shadingGroup[0],shadingGroup[1],self.nameAsset,houdiniNodeInfos)
								# Need to swap openGl shader and renderman shader for proper visualisation in solaris
								sg_houdiniRenderman.swapOpenGLShader(shadingGroup[0])
							# Add Renderman Parameters
							if houdiniContext == "Object" and not "/stage" in houdiniNodePath:
								openGLShader = sg_houdiniRenderman.buildOGLShader(self.listTextureFilesMegascans,self.containerTexture,shadingGroup[0],shadingGroup[1],self.nameAsset,houdiniNodeInfos)
								# sg_houdiniRenderman.swapOpenGLShader(shadingGroup[0])
								if self.importedMObject:
									sg_houdiniRenderman.addRendermanParameters(self.importedMObject)
									
							elif houdiniContext == "Sop" and not "/stage" in houdiniNodePath:
								openGLShader = sg_houdiniRenderman.buildOGLShader(self.listTextureFilesMegascans,self.containerTexture,shadingGroup[0],shadingGroup[1],self.nameAsset,houdiniNodeInfos)
								print("To Add Renderman Parameters on the geo")
				elif in_katana:
					sg_katanaRenderman.connectMegascansShaderR(self.listTextureFilesMegascans,self.containerTexture,self.nameMegascans,self.importedMObject,self.manifold,idName,self.childrenInGroup)
				elif in_mari:
					if len(self.lodGeometryToLoad) != 0:
						shaderMari = sg_mariLibraryCommands.createMegascansShader(self.nameMegascans,channels[1],self.mariShader,self.mariColorspace)
			elif self.usedRenderer == "arnold":
				if in_maya:
					sg_mayaArnold.loadMegascansShaderA(jsonShader,self.listTextureFilesMegascans,self.nameMegascans,self.importedMObject,self.manifold,idName)
			elif self.usedRenderer == "mayaDefault":
				if in_maya:
					sg_mayaLibraryCommands.buildMegascanShaderMaya(self.listTextureFilesMegascans,self.usedRenderer,self.nameAsset,self.importedMObject )
			elif self.usedRenderer == "mantra":
				sg_houdiniMantra.buildMegascanShaderM(self.listTextureFilesMegascans,self.usedRenderer,self.nameAsset,self.importedMObject )
			elif self.usedRenderer == "atlas":
				if in_hou:
					sg_houdiniLibraryCommands.createMegascansAtlas(self.folderUnzip+"/",self.nameAsset,houdiniNodeInfos )
			elif self.usedRenderer == "blender":
				sg_blenderLibraryCommands.buildMegascanShaderBlender(self.listTextureFilesMegascans,self.usedRenderer,self.nameAsset,self.importedMObject )
			elif self.usedRenderer == "unreal":
				unrealShader = self.findShaderTemplate(self.categoryMegascans,self.usedRenderer)
				sg_unrealLibraryCommands.createMegascansMaterial(self.nameMegascans,self.importedMObject,textures,unrealShader,0)
				if texturesBillboard:
					unrealBillboardShader = self.shaderLibraryPath+ self.usedRenderer + "/megascans/Billboard_Material/Billboard_Material.uasset"
					sg_unrealLibraryCommands.createMegascansMaterial(self.nameMegascans,self.importedMObject,texturesBillboard,unrealBillboardShader,self.LODAmount-1)

			################################################# Extra Processes ##############################################
			if in_maya:
				## Group Geo/Delete Namespace and Add message
				group = None
				if self.importedMObject != None:
						group = sg_mayaLibraryCommands.groupGeo(self.importedMObject,self.nameMegascans,self.lod)
				sg_mayaLibraryCommands.deleteNamespace(self.nameNamespace)
				if group != None:
					try:
						sg_mayaLibraryCommands.renameGeo(group,self.nameMegascans)
					except:
						e = sys.exc_info()
						print(e)
						print("Couldn't rename Geo " + group)
				cmds.scriptEditorInfo(suppressWarning=False,suppressErrors=False,suppressResults=False)
				cmds.inViewMessage( amg='Megascan(s) Imported Successfully !', pos='botCenter', fade=True, fadeOutTime=1000)
			elif in_hou:
				## Backdrop Creation
				if houdiniContext == "Object" or houdiniContext == "Sop" and not "/stage" in houdiniNodePath:
					frame = [model[0],self.containerTexture]
				elif houdiniContext == "Lop" and self.houdiniMPC == True:
					frame = [assetLop[0]]
				try:
					sg_houdiniLibraryCommands.createNetworkBox(frame,self.nameMegascans,houdiniNodeInfos)
				except:
					pass
				## Automatically Launch tex convertion in Houdini
				print ("\n" + " ---- Converting Textures as TEX in Background ---- ")
				dataAutomaticTex = sg_houdiniLibraryCommands.convertTexAutomatic(self.listFullpathImages)
				sg_batchTextureConvert.makeTex(ui_obj=self,listTextures = self.listFullpathImages,commands = dataAutomaticTex[1],settings = dataAutomaticTex[2],bypass_UI = True)
			elif in_katana:
				## Automatically Launch tex convertion in Houdini
				print ("\n" + " ---- Converting Textures as TEX in Background ---- ")
				dataAutomaticTex = sg_katanaLibraryCommands.convertTexAutomatic(self.listFullpathImages)
				sg_batchTextureConvert.makeTex(ui_obj=self,listTextures = self.listFullpathImages,commands = dataAutomaticTex[1],settings = dataAutomaticTex[2],bypass_UI = True)
				
				# nodes = self.listTextureFilesMegascans + self.containerTexture
				# sg_katanaLibraryCommands.nodeFloating(nodes)
				## Backdrop Creation
				# sg_katanaLibraryCommands.createBackDrop(self.nameAsset)
			elif in_nuke:
				if self.usedRenderer != "nukeDrop":
					## Backdrop Creation
					sg_nukeLibraryCommands.createBackDrop(self.nameAsset)
					#sg_nukeLibraryCommands.autoPlaceSelectedNodes()

					## Create projection if UI is set on it
					if self.triplanar:
						nodeProjection = sg_nukeLibraryCommands.create3DProj(readNode)
						# Save Selection
						savedSelection = sg_nukeLibraryCommands.saveSelection()
						sg_nukeLibraryCommands.clearSelection()
						# Get new projection node selected to get new backDrop
						sg_nukeLibraryCommands.restoreSelection(nodeProjection,True)
						bg = sg_nukeLibraryCommands.createBackDrop(self.nameAsset + "_projection")
						# Restore selection with Read Nodes
						sg_nukeLibraryCommands.restoreSelection(savedSelection,True)
							
			elif in_mari:
				if len(self.lodGeometryToLoad) != 0:
					## Manage Lights
					pathMariHDR = sg_mariLibraryCommands.findEnvMap(self.mariHDR,self.textureLibraryPath)
					sg_mariLibraryCommands.createLighting(shaderMari,pathMariHDR)

			print(" ---- Megascans Process Finished Sucessfully ---- ")
			try:
				logger.info(" ---- Megascans Process Finished Sucessfully ---- ")
			except:
				pass

			self.progressBarFinish(timeSleep = 0.5)
			
#######################################################################################################################
################################################## Progress Window UI #################################################
#######################################################################################################################

	def progressWindow(self,text):
		self.pWindow = cmds.window(t=text,s= False, w=360,h=20)
		cmds.columnLayout()
		self.progressControl = cmds.progressBar(maxValue=100, width=360)
		cmds.showWindow( self.pWindow )
		return self.pWindow

	def resetProgressBar(self,text):
		self.main_widget.lineEdit_sgDisplayMessage.setText("")
		progressBarValue = 0
		self.main_widget.progressBar_sgLoading.setValue(progressBarValue)
		self.main_widget.progressBar_sgLoading.setTextVisible(True)
		self.main_widget.progressBar_sgLoading.setFormat(text+'%p%')
		self.main_widget.progressBar_sgLoading.setAlignment(QtCore.Qt.AlignCenter)

	def progressBarFinish(self,timeSleep):
		time.sleep(timeSleep)
		self.main_widget.progressBar_sgLoading.setTextVisible(False)
		self.main_widget.progressBar_sgLoading.setValue(0)

#######################################################################################################################
#################################################### Utils New Entry ##################################################
#######################################################################################################################

	def compareTimeModification(self,path):
		## Compare Modification time of folder to an arbitrary time
		## chek if path exists
		##
		if os.path.exists(path):
			limitDate = datetime.now() - timedelta(days = self.freshTimeLimit)
			currentDate = datetime.now()
			modifDate = datetime.fromtimestamp(os.path.getmtime(path))
			if modifDate > limitDate :
					freshPath = True
			else:
					freshPath = False
		else:
			freshPath = False
		return freshPath

	def screenGrabWindow(self,imageSnapshot):
		# Take a snapshot of the entire screen 
		if not QtWidgets.QApplication.instance():
			app = QtWidgets.QApplication(sys.argv)
		else:
			app = QtWidgets.QApplication.instance()
		QtGui.QPixmap.grabWindow(QtWidgets.QApplication.desktop().winId()).save(imageSnapshot, 'png')

		return imageSnapshot

	def naturalSorting(self,l):
		convert = lambda text: int(text) if text.isdigit() else text.lower()
		alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
		return sorted(l, key=alphanum_key)

	def createPDF(self,path,outputPath):
		# Take some a folder with images (jpg) and create a pdf
		#
		if self.pilLoaded == True:
			images = glob.glob(path + "*.jp*")
			images = self.naturalSorting(images)

			pdfOutput = outputPath
			if images:
				try:
					imagesForPDF = [pilimage.open(f) for f in images]
				except:
					print("Can't load images for pdf")
					print(sys.exc_info())
					return ""

				try:
					imagesForPDF[0].save(pdfOutput,"PDF",resolution = 100.0,save_all =True,append_images = imagesForPDF[1:])
				except:
					print("Can't combine images for pdf")
					print(sys.exc_info())
					return ""
			else:
				self.sendMessage("No images in folder to create pdf")
				pdfOutput = ""
		else:
			print("PIL python library is not loaded, cannot create a pdf")
			pdfOutput = ""

		return pdfOutput

	def createCBZ(self,path,outputPath):
		 # Only read jpg and jpeg
		images=[]
		listExt = ["*.jpg","*.jpeg"]

		# Will convert jp2 format if it is there
		# Otherwise use jpeg
		jp2 = glob.glob(path + "*.jp2")
		if jp2:
			tmpFolder = os.path.join(path,"tmpJPG")
			self.createNewFolder(tmpFolder)
			for img in jp2:
				outImage= os.path.join(tmpFolder,os.path.basename(img).split(".")[0]+".jpg")
				images.append(self.convertToJPG(img,outImage))
		else:
			for ext in listExt:
				images.extend(glob.glob(path + ext))

		images = self.naturalSorting(images)
		cbzOutput = outputPath
		if images:
			z = zipfile.ZipFile(cbzOutput,'w')
			for img in images:
				z.write(img)
			z.close()
		else:
			cbzOutput = ""
		return cbzOutput

	def shaderSaveThumbnail(self,path,name):
		# Prepare unique image name for snapshot and return a path
		imageSnapshot = path+name+".jpg"
		if self.platform == "win32" or self.platform == "win64":
			imageSnapshot = imageSnapshot.replace(os.sep, "/")

		if in_maya:
			# Take a snapshot of the viewport and save to file
			cmds.refresh(cv=True, fe = "jpg", fn = imageSnapshot)
		if in_nuke:
			if nuke.selectedNodes():
				sg_nukeLibraryCommands.createThumbnail(imageSnapshot,nuke.selectedNodes()[0])
			else:
				sg_nukeLibraryCommands.createThumbnail(imageSnapshot,self.nukeObjectToSave[0])
		if in_katana:
			#Take a snapshot of the all screen in linux ?
			if self.platform == "linux2" or self.platform == "linux":
				os.system("import -window root " + imageSnapshot)
			elif self.platform == "win32" or self.platform == "win64":
				self.getScreenshot(imageSnapshot)
		if in_blen:
			# Do an openGl render in Windows ?
			if self.platform == "win32" or self.platform == "win64":
				sg_blenderLibraryCommands.createThumbnail(imageSnapshot,256,256,self.overrideBlenderContext)
				#self.screenGrabWindow(imageSnapshot)
			# Do an openGl render in Windows ?
			if self.platform == "linux2" or self.platform == "linux":
				sg_blenderLibraryCommands.createThumbnail(imageSnapshot,256,256,self.overrideBlenderContext)
				#os.system("import -window root " + imageSnapshot)
		if in_hou:
			sg_houdiniLibraryCommands.getSnapshot(imageSnapshot)
		return imageSnapshot

	def resizeThumbnail(self, picture):
		self.pilLoaded = False
		# Force to use QPixmap to remove the incorrect sRGB profile error from png - Fix multiple Error
		if self.pilLoaded == True:
			img = pilimage.open(picture)
			width,height = img.size
			
			if width >self.resolutionThumbnail:
				divisor = float(width/self.resolutionThumbnail)
				# Preserve ratio
				# img = img.resize((int(width/divisor),int(height/divisor)), pilimage.ANTIALIAS)
				left = (width/2 - height/2)
				right = (width/2 + height/2)
				bottom = height
				top = 0
				img = img.crop((left,top,right,bottom))

				imgResized = img.resize((self.resolutionThumbnail,self.resolutionThumbnail), pilimage.Resampling.LANCZOS)
				imgResized.save( picture )
				#print("Reformated with PIL")
		else:
			img = QtGui.QPixmap(picture)
			width = img.width()
			height = img.height()
			if width >self.resolutionThumbnail:
				divisor = int(round(width/self.resolutionThumbnail))
				#rect = QtCore.QRect(0,0,width/divisor,height/divisor)
				#imgCropped = QtGui.QPixmap.copy(img)
				imgCropped= img.scaled(width/divisor,height/divisor,QtCore.Qt.KeepAspectRatio)
				result = imgCropped.save(picture)
				#print("Reformated with pixmap",width/divisor,height/divisor,result)
		self.pilLoaded = True	
		return picture

	def resizeThumbnailMegascans(self, image):
		# Hardcoded resolution at 256
		# Force to use QPixmap to rmove the incorrect sRGB profile error from png - Fix multiple Error
		
		self.pilLoaded = False

		if self.pilLoaded == True:
			img = pilimage.open(image)
			width,height = img.size
			if width >self.megascansThumbnailResolution:
				divisor = int(round(width/self.megascansThumbnailResolution))
				imgResized = img.resize((int(width/divisor),int(height/divisor)),pilimage.Resampling.LANCZOS)
				imgResized.save( image )
				#print("Reformated with PIL")
		else:
			img = QtGui.QPixmap(image)
			width = img.width()
			height = img.height()
			if width >self.megascansThumbnailResolution:
				divisor = int(round(width/self.megascansThumbnailResolution))
				#rect = QtCore.QRect(0,0,width/divisor,height/divisor)
				#imgCropped = QtGui.QPixmap.copy(img)
				imgCropped = img.scaled(width/divisor,height/divisor,QtCore.Qt.KeepAspectRatio,QtCore.Qt.SmoothTransformation)
				imgCropped.save(image)
				#print("Reformated with pixmap")
		self.pilLoaded = True	
		return image

	def findFilesInFolder(self,recursive,folder,listFileExtension):
		files = [os.path.join(folder,f) for f in os.listdir(folder) if f.split(".")[-1].lower() in listFileExtension]
		#amountFiles = len(files)
		return files

	def findSizeList(self,listItems):
		amountFiles = len(listItems)
		return amountFiles

	def setTextUI(self,widget,text):
		widget.setText(text)

	def findFMLFromList(self,listItems):
		if len(listItems)%2 != 0:
			# Odd number
			return [0,int((len(listItems)-1)/4),int(((len(listItems)-1)/4)*2), len(listItems)-1]
		else:
			# Even
			return [0,int(len(listItems)/4), int(len(listItems)/4)*2,len(listItems)-1]

	def findDMPinFolder(self,folder):
		imageFiles = []
		
		## UI
		progressBar = 0.0
		self.resetProgressBar(self.pbConvertingToPNG)

		for fileType in self.listdmpImagefileExtension:
			imageFiles += self.findFilesInFolder(False,folder,fileType)
		quantity= self.findSizeList(imageFiles)

		# UI
		self.setTextUI(self.main_widget.label_sgFoundDMPFolder,"Found: " + str(quantity) + " images in the folder")

		## Find First/ Quarter / Quarter*2 / Last
		posImag = self.findFMLFromList(imageFiles)
		img01Path = imageFiles[posImag[0]]
		img01Path = img01Path.replace(os.sep,"/")
		img01Extension = img01Path.split(".")[-1]
		img02Path = imageFiles[posImag[1]]
		img02Path = img02Path.replace(os.sep,"/")
		img02Extension = img02Path.split(".")[-1]
		img03Path = imageFiles[posImag[2]]
		img03Path = img03Path.replace(os.sep,"/")
		img03Extension = img03Path.split(".")[-1]
		img04Path = imageFiles[posImag[3]]
		img04Path = img04Path.replace(os.sep,"/")
		img04Extension = img04Path.split(".")[-1]

		# From Raw/Cr2 to Png or Exr/Hdr to Png
		# TODO to save those images in a tmp folder
		
		thumbnailOutputNameTmp01 = os.path.join(self.pathTempFolder, os.path.splitext(os.path.basename(img01Path))[0] + ".png")
		if img01Extension.lower() in self.listRawImagesFormat:
			img01Path = self.convertToPNG02(img01Path,thumbnailOutputNameTmp01)
		elif img01Extension.lower() in self.listHdrImagesFormat:
			img01Path = fcn.ffmpegThumbnail(img01Path,thumbnailOutputNameTmp01,512,512)
		
		thumbnailOutputNameTmp02 = os.path.join(self.pathTempFolder, os.path.splitext(os.path.basename(img02Path))[0] + ".png")
		if img02Extension.lower() in self.listRawImagesFormat:
			img02Path = self.convertToPNG02(img02Path,thumbnailOutputNameTmp02)
		elif img02Extension.lower() in self.listHdrImagesFormat:
			img02Path = fcn.ffmpegThumbnail(img02Path,thumbnailOutputNameTmp02,512,512)
		
		thumbnailOutputNameTmp03 = os.path.join(self.pathTempFolder, os.path.splitext(os.path.basename(img03Path))[0] + ".png")
		if img03Extension.lower() in self.listRawImagesFormat:
			img03Path = self.convertToPNG02(img03Path,thumbnailOutputNameTmp03)
		elif img03Extension.lower() in self.listHdrImagesFormat:
			img03Path = fcn.ffmpegThumbnail(img03Path,thumbnailOutputNameTmp03,512,512)
		
		thumbnailOutputNameTmp04 = os.path.join(self.pathTempFolder, os.path.splitext(os.path.basename(img04Path))[0] + ".png")
		if img04Extension.lower() in self.listRawImagesFormat:
			img04Path = self.convertToPNG02(img04Path,thumbnailOutputNameTmp04)
		elif img01Extension.lower() in self.listHdrImagesFormat:
			img04Path = fcn.ffmpegThumbnail(img04Path,thumbnailOutputNameTmp04,512,512)

		# Update UI
		progressBarValue = 50.0
		self.main_widget.progressBar_sgLoading.setValue(progressBarValue)

		######## Show in UI
		# Buttons Icon
		self.iconDMPContactsheet01 = self.createNewIcon()
		self.iconDMPContactsheet01.addPixmap(QtGui.QPixmap(img01Path), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.main_widget.pushButton_sgDMPContactsheet01.setIcon(self.iconDMPContactsheet01)
		self.main_widget.pushButton_sgDMPContactsheet01.setIconSize(QtCore.QSize(92, 92))

		self.iconDMPContactsheet02 = self.createNewIcon()
		self.iconDMPContactsheet02.addPixmap(QtGui.QPixmap(img02Path), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.main_widget.pushButton_sgDMPContactsheet02.setIcon(self.iconDMPContactsheet02)
		self.main_widget.pushButton_sgDMPContactsheet02.setIconSize(QtCore.QSize(92, 92))

		self.iconDMPContactsheet03 = self.createNewIcon()
		self.iconDMPContactsheet03.addPixmap(QtGui.QPixmap(img03Path), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.main_widget.pushButton_sgDMPContactsheet03.setIcon(self.iconDMPContactsheet03)
		self.main_widget.pushButton_sgDMPContactsheet03.setIconSize(QtCore.QSize(92, 92))

		self.iconDMPContactsheet04 = self.createNewIcon()
		self.iconDMPContactsheet04.addPixmap(QtGui.QPixmap(img04Path), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.main_widget.pushButton_sgDMPContactsheet04.setIcon(self.iconDMPContactsheet04)
		self.main_widget.pushButton_sgDMPContactsheet04.setIconSize(QtCore.QSize(92, 92))

		# Text
		self.setTextUI(self.main_widget.label_sgDMPContactsheet01,os.path.basename(imageFiles[posImag[0]]))
		self.setTextUI(self.main_widget.label_sgDMPContactsheet02,os.path.basename(imageFiles[posImag[1]]))
		self.setTextUI(self.main_widget.label_sgDMPContactsheet03,os.path.basename(imageFiles[posImag[2]]))
		self.setTextUI(self.main_widget.label_sgDMPContactsheet04,os.path.basename(imageFiles[posImag[3]]))

		# Store value for reuse later
		self.listDMPContactsheetImg = [img01Path,img02Path,img03Path,img04Path]

		# Update UI
		progressBarValue = 100.0
		self.main_widget.progressBar_sgLoading.setValue(progressBarValue)
		self.main_widget.progressBar_sgLoading.setFormat("Done... "+'%p%')

		self.progressBarFinish(timeSleep = 0.5)

	def findIESinFolder(self,folder):
		tmpString = ""
		
		iesFilesRaw = glob.glob(folder+"/*.ies")
		txtFilesRaw = glob.glob(folder+"/*.txt")
		jsonFilesRaw = glob.glob(folder+"/*.json")
		iconsFilesRaw = []
		for img in self.thumbnailsfileExtension:
			iconsFilesRaw += glob.glob(folder+"/*." + img)

		iesFiles = [x.replace(os.sep, '/') for x in iesFilesRaw ]
		txtFiles = [x.replace(os.sep, '/') for x in txtFilesRaw ]
		jsonFiles = [x.replace(os.sep, '/') for x in jsonFilesRaw ]
		iconsFiles = [x.replace(os.sep, '/') for x in iconsFilesRaw ]

		## Update UI. If no IES was found no need to proceed
		if iesFiles:
			nameIESFileExtension = os.path.basename(iesFiles[0])
			nameIESFile = nameIESFileExtension.split(".")
			self.main_widget.pushButton_sgIESFoundFile.setText(nameIESFileExtension)
			if iconsFiles:
				self.buttonNewIESFound(iconsFiles[0])
			if txtFiles:
				tmpString += os.path.basename(txtFiles[0])
			if jsonFiles:
				tmpString += os.path.basename(jsonFiles[0])
		else:
			self.buttonNewIESFound("")
			self.main_widget.pushButton_sgIESFoundFile.setText("")
			print("Could not find an IES file")
		
		self.main_widget.pushButton_sgIESFoundJson.setText(tmpString)

		if len(iesFiles) > 1:
			message = "More than 1 ies profile found."
		elif len(iesFiles) == 0:
			message = "No ies profile found."
		else:
			message = "1 ies profile found."
		self.main_widget.label_sgIESNewMessageTxt.setText(message)

		#Add that as global variable for now
		if iesFiles:
			self.iesFileNewEntry =  iesFiles[0]
		else:
			self.iesFileNewEntry = ""
		if iconsFiles:
			self.iconIESNewEntry =  iconsFiles[0]
		else:
			self.iconIESNewEntry = ""
		
		#self.main_widget.lineEdit_sgAddIESRename.setText()

	def findABTinFolder(self,folder):
		preview = glob.glob(folder+"/*_Preview.*")
		textUI = ""
		tutorialFolder = ""
		self.dataNewATB={}
		if self.context == "ArtBooks":
			artBookImages = [img for img in glob.glob(folder+"/*.jp*") if self.thumbnailSuffix not in os.path.basename(img)]
			artBookPDFs = glob.glob(folder+"/*.pdf")
			artBookCBRs = glob.glob(folder+"/*.cb*")
			
			# Check if needed to create a pdf
			if artBookImages:
				textUI += "Found: "+ str(len(artBookImages)) + " Image(s) to convert as PDF or as CBZ, "
				# Show UI
				self.main_widget.groupBox_ABTConvert.setEnabled(True)
			else:
				# Hide UI
				self.main_widget.groupBox_ABTConvert.setEnabled(False)
			if artBookPDFs:
				textUI += "Found "+ str(len(artBookPDFs))+ " PDF(s), " 
			if artBookCBRs:
				textUI += "Found "+ str(len(artBookCBRs))+ " CBR(s) or CBZ(s), " 

		elif self.context == "Tutorials":
			tutorialFolder = folder
			textUI += "Found Tutorial: " + tutorialFolder

		else:
			artBookImages = []
			artBookPDFs = []
			artBookCBRs = []

		self.main_widget.label_sgFoundABTFolder.setText(textUI)

		# Set icon
		if preview:
			iconDefault = preview[0]
			self.buttonNewATBFound(iconDefault)
		else:
			if self.context == "ArtBooks":
				iconDefault = self.iconPathDefaultArtBooks
			elif self.context == "Tutorials":
				iconDefault = self.iconPathDefaultTutorials
			else:
				iconDefault = self.iconPathDefaultArtBooks
			self.buttonNewATBFound(iconDefault)

		# Fill Dictionary with Info
		self.dataNewATB={
			'previewImage':iconDefault,
			'artBookImages':artBookImages,
			'artBookPDFs': artBookPDFs,
			'artBookCBRs': artBookCBRs,
			'tutorialFolder':tutorialFolder,
		}
		#print(json.dumps(self.dataNewATB,indent = 4))

	def buttonNewIESFound(self,iconPathNewIES):
		if iconPathNewIES:
			# Will create an icon every time we click, workaround compared to previous method
			newIcon = self.createNewIcon()
			newPixmap = QtGui.QPixmap(iconPathNewIES)
			newIcon.addPixmap(newPixmap, QtGui.QIcon.Normal, QtGui.QIcon.Off)
			#self.iconNewIES
			self.main_widget.pushButton_sgIESPreview.setIcon(newIcon)
			self.main_widget.pushButton_sgIESPreview.setIconSize(QtCore.QSize(96, 96))
			self.main_widget.pushButton_sgIESPreview.setToolTip( "By pressing you can pick your own icon for the IES: 256 pixels x 256 pixels" )
		elif not iconPathNewIES:
			self.main_widget.pushButton_sgIESPreview.setIcon(self.iconNewEmtpyIES)

	def buttonNewATBFound(self,iconPathNewATB):
		if iconPathNewATB:
			# Will create an icon every time we click, workaround compared to previous method
			newIcon = self.createNewIcon()
			newPixmap = QtGui.QPixmap(iconPathNewATB)
			newIcon.addPixmap(newPixmap, QtGui.QIcon.Normal, QtGui.QIcon.Off)

			self.main_widget.pushButton_sgABTContactsheet01.setIcon(newIcon)
			self.main_widget.pushButton_sgABTContactsheet01.setIconSize(QtCore.QSize(96, 96))
			self.main_widget.pushButton_sgABTContactsheet01.setToolTip( "By pressing you can pick your own icon for the ArtBook or Tutorial: 256 pixels x 256 pixels" )
		elif not iconPathNewATB:
			self.main_widget.pushButton_sgABTContactsheet01.setIcon(self.iconNewEmtpyIES)

	def updateNewEntryIcons(self,button):
		newDMPIcon = QtWidgets.QFileDialog.getOpenFileName(self,"Choose a new icon file: ","","*.cr2 *.exr *.gif *.jpg *.hdr *.png")
		newDMPIcon.setFixedSize(1000,600)
		
		if newDMPIcon[0]!= "":
			# Check if need conversion/ TODO add size support
			iconImage = newDMPIcon[0]
			thumbnailOutputNameTmp01 = os.path.join(self.pathTempFolder, os.path.splitext(os.path.basename(iconImage))[0] + ".png")
			if newDMPIcon[0].endswith(".exr") or newDMPIcon[0].endswith(".hdr"):	
				iconImage = fcn.ffmpegThumbnail( newDMPIcon[0],thumbnailOutputNameTmp01,512,512)
			elif newDMPIcon[0].endswith(".cr2"):
				iconImage = self.convertToPNG02( newDMPIcon[0],thumbnailOutputNameTmp01)

			if button.objectName() == "pushButton_sgDMPContactsheet01":
				self.iconDMPContactsheet01 = self.createNewIcon()
				self.iconDMPContactsheet01.addPixmap(QtGui.QPixmap(iconImage), QtGui.QIcon.Normal, QtGui.QIcon.Off)
				self.main_widget.pushButton_sgDMPContactsheet01.setIcon(self.iconDMPContactsheet01)
				self.main_widget.pushButton_sgDMPContactsheet01.setIconSize(QtCore.QSize(92, 92))

				self.setTextUI(self.main_widget.label_sgDMPContactsheet01,os.path.basename(iconImage))

				self.listDMPContactsheetImg[0] = iconImage
			elif button.objectName() == "pushButton_sgDMPContactsheet02":
				self.iconDMPContactsheet02 = self.createNewIcon()
				self.iconDMPContactsheet02.addPixmap(QtGui.QPixmap(iconImage), QtGui.QIcon.Normal, QtGui.QIcon.Off)
				self.main_widget.pushButton_sgDMPContactsheet02.setIcon(self.iconDMPContactsheet02)
				self.main_widget.pushButton_sgDMPContactsheet02.setIconSize(QtCore.QSize(92, 92))

				self.setTextUI(self.main_widget.label_sgDMPContactsheet02,os.path.basename(iconImage))

				self.listDMPContactsheetImg[1] = iconImage
			elif button.objectName() == "pushButton_sgDMPContactsheet03":
				self.iconDMPContactsheet03 = self.createNewIcon()
				self.iconDMPContactsheet03.addPixmap(QtGui.QPixmap(iconImage), QtGui.QIcon.Normal, QtGui.QIcon.Off)
				self.main_widget.pushButton_sgDMPContactsheet03.setIcon(self.iconDMPContactsheet03)
				self.main_widget.pushButton_sgDMPContactsheet03.setIconSize(QtCore.QSize(92, 92))

				self.setTextUI(self.main_widget.label_sgDMPContactsheet03,os.path.basename(iconImage))

				self.listDMPContactsheetImg[2] = iconImage
			elif button.objectName() == "pushButton_sgDMPContactsheet04":
				self.iconDMPContactsheet04 = self.createNewIcon()
				self.iconDMPContactsheet04.addPixmap(QtGui.QPixmap(iconImage), QtGui.QIcon.Normal, QtGui.QIcon.Off)
				self.main_widget.pushButton_sgDMPContactsheet04.setIcon(self.iconDMPContactsheet04)
				self.main_widget.pushButton_sgDMPContactsheet04.setIconSize(QtCore.QSize(92, 92))

				self.setTextUI(self.main_widget.label_sgDMPContactsheet04,os.path.basename(iconImage))
				self.listDMPContactsheetImg[3] = iconImage

			elif button.objectName() == "pushButton_sgABTContactsheet01":
				newABTIcon = self.createNewIcon()
				newABTIcon.addPixmap(QtGui.QPixmap(iconImage), QtGui.QIcon.Normal, QtGui.QIcon.Off)
				self.main_widget.pushButton_sgABTContactsheet01.setIcon(newABTIcon)
				self.main_widget.pushButton_sgABTContactsheet01.setIconSize(QtCore.QSize(92, 92))

				self.setTextUI(self.main_widget.label_sgABTContactsheet01,os.path.basename(iconImage))
				if self.dataNewATB['previewImage']:
					self.dataNewATB['previewImage'] = iconImage
		else:
			print("No new icon selected")

	def convertToPNG(self,image):
		# Get a jpg,cr2 or an exr and convert to png with alpha equal
		# to r channel
		#
		#
		if self.pilLoaded == True:
			im = pilimage.open(image)
			alpha = pilimage.open(image).convert('L')
			output = image.split(".")[0] + ".png"
			listOutput = self.findResInMegascanName(output)
			# Compensate the use of 1 channel
			# brighten = pilimageEnhance.Brightness(alpha)
			# alphaB = alpha.brighten(1.3)
			# To Try:
			# pilimage.ANTIALIAS has ben deprecated for pilimage.Resampling.LANCZOS
			im.putalpha(alpha)

			width,height = im.size
			i = 1
			for output in listOutput:
				resizedImg = im.resize((width/(i),height/(i)), pilimage.Resampling.LANCZOS)
				resizedImg.save(output)
				print("Converted to PNG: " + output )
				if i == 1:
					i += 1
				else:
					i *= 2
		else:
			print("No PIL, can't convert to PNG")

		return output

	def convertToPNG02(self,image,output):
		# Get a jpg,cr2 or an exr and convert to png with alpha equal
		# to r channel
		#
		#
		if self.pilLoaded == True:
			im = pilimage.open(image)
			alpha = pilimage.open(image).convert('L')
			listOutput = self.findResInMegascanName(output)
			# Compensate the use of 1 channel
			# brighten = pilimageEnhance.Brightness(alpha)
			# alphaB = alpha.brighten(1.3)
			# To Try:
			# pilimage.ANTIALIAS has ben deprecated for pilimage.Resampling.LANCZOS
			im.putalpha(alpha)
			width,height = im.size
			i = 1
			for output in listOutput:
				resizedImg = im.resize((width/(i),height/(i)), pilimage.Resampling.LANCZOS)
				resizedImg.save(output)
				print("Converted to PNG: " + output )
				if i == 1:
					i += 1
				else:
					i *= 2
		else:
			print("No PIL, can't convert to PNG")

		return output

	def convertToJPG(self,image,output):
		if self.pilLoaded == True:
			img = pilimage.open(image)
			rgbIm = img.convert('RGB')
			rgbIm.save(output)
			return output
		else:
			return ""

	def findResInMegascanName(self,filepath):
		newRes = ""
		listFilenames = [filepath]
		words = filepath.split("_")
		resolution = words[-2]
		digits = [int(s) for s in [x for x in resolution] if s.isdigit()]
		for digit in digits:
			while digit > 1:
					newFilename = ""
					digit = digit/2
					newRes = str(digit)+ "K"
					newFilename = filepath.replace(resolution,newRes)
					listFilenames.append(newFilename)

		return listFilenames

	def setResThumbnailNewEntry(self,s):
		print("New entry Thumbnail resolution: " + s.split("x")[0])
		self.resolutionThumbnail = int(s.split("x")[0])

	def findCommonWord(self,string01,string02):
		str1_words = set(string01.split())
		str2_words = set(string02.split())

		common = str1_words & str2_words

		return common

#######################################################################################################################
##################################################### General UI TREE #################################################
#######################################################################################################################

################################################## Json File Read/Write ###############################################

	def readJsonInfos(self,jsonFile):
		if os.path.exists(jsonFile):
			with open(jsonFile) as jfile:
				data = json.load(jfile)
		else:
			data = {}
		return data

	def writeJsonFile(self,outFile,data):
		if type(data) != list:
			with open(outFile,'w') as outJson:
				json.dump(OrderedDict(data),outJson,indent = 4)
		elif type(data) == list:
			with open(outFile,'w') as outJson:
				json.dump(data,outJson,indent = 4)

	def writeJsonEntryInfos(self,path,name,listExtensionAvailable,listTextures,notes,version,tags,ocio,time,meta):
		data = {}
		data["releaseInfos"]= []
		data["releaseInfos"].append({
		'author': os.getenv("USER"),
		'timeEntry':time,
		'lock': False,
		'version':version,
		'ocio':ocio,
		'name':name,
		'extension': listExtensionAvailable,
		'textures' :listTextures,
		'tags':tags,
		'meta': meta,
		'note':notes
		})

		self.writeJsonFile(path,OrderedDict(data))

	def writeDmpLinkJson(self,path,nameEntry,folderImages):
		data = {}
		data["linkInfos"]= {
		'name' : nameEntry,
		'author': os.getenv("USER"),
		'linkToImgs': folderImages
		}

		self.writeJsonFile(path,data)

####################################################### Tree Item #####################################################

	def libraryFolderStructure(self,startpath,branch):
		listFolders = os.listdir(startpath)
		listFolders.sort()
		for element in listFolders:
			# Define Depth of search
			if  "Textures" in startpath+element or "IES" in startpath+element or "VDB" in startpath+element or "DMP" in startpath+element or "ArtBooks" in startpath+element or "Tutorials" in startpath+element:
				self.pathDepthReference= self.pathDepthReferenceModel
			elif "Shaders" in startpath+element or "Megascans" in startpath+element or "Models" in startpath+element or "Lightrigs" in startpath+element:
				self.pathDepthReference= self.pathDepthReferenceShader
			elif "Collections" in startpath+element:
				self.pathDepthReference = 0

			if not "." in element:
				if not element == "icons" :
					path_info = startpath + element + "/"
					parent_itm = QtWidgets.QTreeWidgetItem(branch, [os.path.basename(element)])
					# Check if it is fresh//modified
					freshModifiedFolder = self.compareTimeModification(path_info)
					if freshModifiedFolder == True:
						font = parent_itm.font(0)
						font.setItalic(True)
						colorFont = self.fontFreshDirectoryColor
						# Check parent and change color too
						if parent_itm.parent():
							parent_itm.parent().setFont(0,font)
							parent_itm.parent().setForeground(0,QtGui.QColor(colorFont))
							# parent_itm.parent().setTextColor(0,colorFont)
					else:
						font = parent_itm.font(0)
						font.setItalic(False)
						colorFont = self.fontNormalDirectoryColor
					#Set Font
					parent_itm.setFont(0,font)
					parent_itm.setForeground(0,QtGui.QColor(colorFont))

					pathLength = len(path_info.split("/"))
					if os.path.isdir(path_info) and pathLength < self.pathDepthReference:
						# Loop to iterate new embranchment
						self.libraryFolderStructure(path_info,parent_itm)

	def selectTreeItem(self):
		parents =[]
		tree= []
		pathAddEntry = ""
		treePathandIndex = []
		selectedItem = self.main_widget.treeWidget_sgLibrary.currentItem()
		selectedIndex = self.main_widget.treeWidget_sgLibrary.indexFromItem(selectedItem)
		
		currentItem = self.main_widget.treeWidget_sgLibrary.currentItem().parent()
		currentIndex = self.main_widget.treeWidget_sgLibrary.indexFromItem(currentItem)

		if currentIndex.isValid():
			parents.append(currentIndex)
			for parentIndex in parents:
				currentItem =  self.main_widget.treeWidget_sgLibrary.itemFromIndex(parentIndex.parent())
				currentIndex = self.main_widget.treeWidget_sgLibrary.indexFromItem(currentItem)
				if  currentIndex.isValid():
					if currentIndex not in parents :
						parents.append(currentIndex)
		for parent in parents[::-1]:
			folderName = self.main_widget.treeWidget_sgLibrary.itemFromIndex(parent).text(0)
			pathAddEntry += folderName+"/"
		pathAddEntry += selectedItem.text(0) + "/"
		pathComplete = self.libraryPath+pathAddEntry
		context = pathAddEntry.split("/")[0]

		##Add Selected Index for later testing
		tree = parents
		tree.reverse()
		tree.append(selectedIndex)

		treePathandIndex =[pathComplete, context, tree]

		return treePathandIndex

	def refreshLibrary(self):
		###### Refresh Library and keep selection 
		######
		# Get Selected Path - and Make it relative
		listPath = self.selectedPath[0].split(self.libraryPath)
		# Filter empty string
		listPath =  [x for x in listPath if x]
		relativePath = "/".join(listPath)
		listPathRelative = relativePath.split("/")
		listPathRelative =  [x for x in listPathRelative if x]
		
		# Refresh TreeView
		#self.main_widget.treeWidget_sgLibrary.clearSelection()
		self.refreshTreeView()

		# Offset one for base 0 list
		column = len(listPathRelative)-1
		textItemToFind = listPathRelative[column]

		# Get list of result
		listTreeItems= self.main_widget.treeWidget_sgLibrary.findItems(textItemToFind, QtCore.Qt.MatchContains|QtCore.Qt.MatchRecursive, 0)

		# Get selection back / not ideal with duplicated name
		if listTreeItems:
			for item in listTreeItems:
				self.main_widget.treeWidget_sgLibrary.setCurrentItem(item)
		else:
			print("Library Refreshed but can't find the previous selection")

	def getDepthSelectedTreePath(self):
		# Get Selected Path - and Make it relative
		listPath = self.selectedPath[0].split(self.libraryPath)
		# Filter empty string
		listPath =  [x for x in listPath if x]
		relativePath = "/".join(listPath)
		listPathRelative = relativePath.split("/")
		listPathRelative =  [x for x in listPathRelative if x]

		depth = len(listPathRelative)-1

		return depth

#######################################################################################################################
############################################## ADD New Entry Functions ################################################
#######################################################################################################################

	def createNewLibrary(self,firstTime,rootPath,nameNewLibrary):
		if firstTime == False:
			nameNewLibrary = self.main_widget.lineEdit_NameNewLibrary.text()
			rootPath = self.main_widget.lineEdit_PathNewLibrary.text()

		if nameNewLibrary != "" and os.path.exists(rootPath):
			dicNewFolderLibrary = fcn.dictionaryNewLibrary()
			# create folder hierarchy
			self.createNewFolderLibrary(rootPath,nameNewLibrary,dicNewFolderLibrary)
			#### Duplicate/create some of the json file for the library
			# Tags and super user json
			basedRootNewPath = os.path.join(rootPath,nameNewLibrary)
			if firstTime == True:
				# Create super user file and Add Default User
				fcn.createSuperUserFile(basedRootNewPath,"resurepus.json",self.username)
				fcn.createTagsFile(basedRootNewPath,"tags.json")
			elif firstTime == False:
				self.simpleCopyFile(os.path.join(self.libraryPath,self.superUserFilename),os.path.join(basedRootNewPath,self.superUserFilename))
				self.simpleCopyFile(os.path.join(self.libraryPath,self.tagsJsonFilename),os.path.join(basedRootNewPath,self.tagsJsonFilename))
			# Database Json
			databaseAsset = self.writeJsonFile(os.path.join(basedRootNewPath,self.databaseAssetFilename),{})
			databaseMegascans = self.writeJsonFile(os.path.join(basedRootNewPath+"/Megascans",self.databaseMegascansFilename ),{})
			databaseGlobal =  self.writeJsonFile(os.path.join(basedRootNewPath,self.databaseFilename),{})
			# Log Files
			logPath = fcn.createLogFiles(basedRootNewPath,os.path.basename(self.pathLogFile))
			logPath = logPath.replace(os.sep,"/")
			
			fcn.createLoggingFile(basedRootNewPath,"logging_linux.ini",logPath)
			fcn.createLoggingFile(basedRootNewPath,"logging_win.ini",logPath)
			# Add to List Library
			if firstTime == False:
				self.dataPathDefaultLibraries = fcn.addNewPathLibrary(self.defaulPathJson,self.dataPathDefaultLibraries,nameNewLibrary,rootPath+nameNewLibrary+"/",self.megascanZIPLibraryPath)
				self.initPathsLibrary()
			# Copy Shaders
			newShaders = copytree(self.initialLibraryShaders,os.path.join(rootPath,nameNewLibrary,"Shaders"),dirs_exist_ok = True)
		else:
			message = "Please add a valid name and pick a valid root directory"
			self.sendMessage(message)
			return False

		if firstTime == True:
			message = "Alexandria Library Created in: " + "\n" + os.path.join(rootPath,nameNewLibrary) + "\n" + " Now let's do Step 02 "
		elif firstTime == False:
			message = "New Library Created: " + nameNewLibrary + "\n" + "You will have to restart the library to update all the megascans "

		self.sendMessage(message)
		return True

	def launchBatchTextureTool(self):
		try:
			logger.info("-- Start Add Batch Texture Pre Process --")
		except:
			print(' -------- Start Add Texture Process -------- ')
			print("Launch Log Recorder")
			self.logInfos()
			pass
		# Get UI
		errorInBatchTextureCheck = False
		#category = self.main_widget.lineEdit_sgNewCategory.text()
		category = ""
		thumbResString = self.main_widget.comboBox_sgPreviewTextRes.currentText()
		thumbResString = thumbResString.split("x")
		thumbRes = list(map(int, thumbResString))
		notes = self.main_widget.lineEdit_sgTexturesAddNotes.text()
		tags = self.main_widget.lineEdit_sgTexturesAddTag.text()
		pathTexture = self.main_widget.lineEdit_sgFolderTexturesEntry.text()
		ocio = self.main_widget.comboBox_sgLTOCIO.currentText() 

		# Verify Context
		try:
			context = self.selectTreeItem()
			self.context = context[1]
		except:
			message = "ERROR: No context selected : should be in Textures or DMP context"
			self.sendMessage(message)
			return False
		## Check the context and the data entered by User
		if self.context != "Textures" and self.context != "DMP":
			errorInBatchTextureCheck = True
			message = "ERROR: Incorrect context selected : should be in Textures or DMP context"
			try:
				logger.error(message)
			except:
				print(message)
				pass
			self.sendMessage(message)
			print(message)

		if category == "":
			if self.subContext != "":
				category = self.subContext
			else:
				errorInBatchTextureCheck = True
				message = "ERROR: No Category selected"
				try:
					logger.error("ERROR: No Category selected")
				except:
					print("ERROR: No Category selected")
					pass
				self.sendMessage(message)
				print("ERROR: No Category selected")

		if pathTexture == "":
			errorInBatchTextureCheck = True
			message = "ERROR: No Texture Folder selected"
			try:
				logger.error(message)
			except:
				print(message)
				pass
			self.sendMessage(message)
			print(message)
			
		else:
			if pathTexture[-1] != "/":
					pathTexture += "/"
					
		if not os.path.exists(pathTexture):
			errorInBatchTextureCheck= True
			message = "ERROR: Selected Texture Folder doesn't exists"
			try:
				logger.error("ERROR: Selected Texture Folder doesn't exists")
			except:
				print("ERROR: Selected Texture Folder doesn't exists")
				pass
			self.sendMessage(message)

		if errorInBatchTextureCheck != True:
			try:
				logger.info("-- Checks done, Ready to add new texture entries --")
			except:
				print("-- Checks done, Ready to add new texture entries --")
				pass

			# Reload Database First
			self.reloadAllDatabase()

			# UI Update
			# TODO use the progress bar for the user
			self.main_widget.lineEdit_sgDisplayMessage.setText("Adding New Entry in the library in Textures/"+ category)
			displayMessage = self.main_widget.lineEdit_sgDisplayMessage
			try:
				sg_addBatchTextureToAlexandria.logger(self.pathLogIni)
			except:
				pass

			progressBarValue = 0.0
			self.resetProgressBar(self.pbCopyingFile)
			if self.newTexturesEntryQuantity != 0:
				progressIncrease = 100.0/self.newTexturesEntryQuantity
			else:
				progressIncrease = 1.0
			if self.context == "Textures":
				contextToSave = self.textureLibraryPath
			elif self.context == "DMP":
				contextToSave = self.dmpLibraryPath

			## Depending of user choice, launch the module
			if self.rbNewTextureEntryType == "radioButton_sgUniqueEntryText":
				databaseData = sg_addBatchTextureToAlexandria.mainUniqueAddBatchTexture(pathTexture,contextToSave,category,self.username,thumbRes,ocio,notes,tags,displayMessage)
			else:
				databaseData = sg_addBatchTextureToAlexandria.mainAddBatchTexture(pathTexture,contextToSave,category,self.username,thumbRes,ocio,notes,tags,displayMessage)

			# UI
			i = 0
			while i < self.newTexturesEntryQuantity:
				progressBarValue += progressIncrease
				self.main_widget.progressBar_sgLoading.setValue(progressBarValue)
				i += 1
			
			# Update UI
			progressBarValue = 100.0
			self.main_widget.progressBar_sgLoading.setValue(progressBarValue)
			self.main_widget.progressBar_sgLoading.setFormat("Done... "+'%p%')

			self.addBatchTextureToDatabase(databaseData,contextToSave,category,tags,notes,ocio)

			# Refresh Library
			time.sleep(0.5)
			self.setBrowserTab()
			self.refreshLibrary()

		else:
			try:
				logger.info("-- Error in Add Batch Texture Pre-Process: Aborted --")
			except:
				print("-- Error in Add Batch Texture Pre-Process: Aborted --")
				pass 
			print("-- Error in Add Batch Texture Pre-Process: Aborted --")

	def launchDMPThumbnail(self,outFolder):
		" Output path of contact sheet"
		""
		""
		# Progressbar UI
		progressBarValue = 0
		self.resetProgressBar(self.pbCreatingContactsheet)

		if self.listDMPContactsheetImg:
			sizeList = len(self.listDMPContactsheetImg)
			# Right now assume it will always be 4 images
			columns = int(sizeList/2)
			rows = int(sizeList/2)
			resolutionTxt = self.main_widget.comboBox_sgPreviewDMPRes.currentText()
			outResW = int(resolutionTxt.split("x")[0])
			outResH =  int(resolutionTxt.split("x")[1])
			# Update UI
			progressBarValue = 50.0
			self.main_widget.progressBar_sgLoading.setValue(progressBarValue)
			# Create Thumbnail
			thumbnail = self.createThumbnailContactSheet(self.listDMPContactsheetImg,columns,rows,outResW,outResH,outFolder)

			# Update UI
			progressBarValue = 100.0
			self.main_widget.progressBar_sgLoading.setValue(progressBarValue)
			self.main_widget.progressBar_sgLoading.setFormat("Done... "+'%p%')
		else:
			print("No folder/valid image to create the thumbnail")

		self.progressBarFinish(timeSleep = 0.5)

		return thumbnail

	def thumbnailsCreator(self,name,temp):
		# If it is a preview that test is not needed, if it is for new entry, the error will be detected before
		try:
			folderIcons = self.selectTreeItem()[0]+self.nameNewEntry+"/"
		except:
			print(sys.exc_info())
			print( " Error ignored but user need to select a category " )
			pass

		## Init Maya		
		if in_maya:
			cmds.select( clear=True )
			##hide ui
			sg_mayaLibraryCommands.set_actifViewVis(0, self.hideUI)

		## ScreenGrab work in maya,houdini,blender and katana
		if temp == True:
			nameThumbnail = "tmp"
			self.thumbnailPreviewImage = self.shaderSaveThumbnail(self.pathTempFolder+"/",nameThumbnail)
			try:
				self.thumbnailPreviewImage = self.resizeThumbnail(self.thumbnailPreviewImage)
			except:
				print ("Error Resizing the thumbnail, see log")
			self.thumbnailAddPreview(self.thumbnailPreviewImage)
			self.thumbnailAddVDBPreview(self.thumbnailPreviewImage)
		else:
			self.thumbnailPreviewImage = self.shaderSaveThumbnail(folderIcons,name)
			try:
				self.thumbnailPreviewImage = self.resizeThumbnail(self.thumbnailPreviewImage)
			except:
				print ("Error Resizing the thumbnail, see log")
		
		## Restaure UI in maya
		if in_maya:
			sg_mayaLibraryCommands.set_actifViewVis(1, self.hideUI)
			
		return self.thumbnailPreviewImage

	def createThumbnailContactSheet(self,listImages,columns,rows,outResW,outResH,outFolder):
		" Output path of contact Sheet"
		"							  "
		padding = 1
		margins = [5,5,5,5]
		contactSheet = sg_contactSheet.makeContactSheet(listImages,padding,columns,rows,outResW,outResH,margins,outFolder)
		return contactSheet

	def findExtensionFiles(self,listFiles):
		listResult = []
		for x in listFiles:
			if x.split(".")[-1] not in listResult:
				listResult.append(x.split(".")[-1])
		return listResult

	def findVDBSequences(self,vdbFile):
		filename = os.path.basename(vdbFile)
		sep = filename.split("#")
		baseFile = sep[0]
		extension = os.path.splitext(vdbFile)[-1]
		folder = os.path.dirname(vdbFile)

		files = glob.glob1(folder,baseFile+"*")
		num = [file[len(baseFile):len(baseFile)+len(sep)-1] for file in files]
		#files = sorted(files,key=lambda x:float(re.findall("\\d+",x)[0]))
		#seq = re.findall('\\d+',filename)
		return folder,files,num[0],num[-1]

	def findVDBSequencesOLD(self,vdbFiles):
		if type(vdbFiles) == list:
			# Sequence
			filename = os.path.basename(vdbFiles[0])
			typeVDB = "list"
		else:
			filename = vdbFiles
			typeVDB = "string"
		seq = re.findall('\\d+',filename)
		#seq = re.findall('^(.*)([^_v])(\d+)([^\d]*)',filename)

		return vdbFiles,typeVDB

	def saveTexturesFromModel(self,setExport,sourceImagesPath):
		filepathList=[]
		shadingGroups = []
		texturefiles= []
		listNewTextures = []

		if in_maya:
			if cmds.nodeType(setExport) == 'objectSet':
				cmds.select( setExport,replace = True )
				## Find all the shapes at the base of the hierarchy
				listShapesInSet = sg_mayaLibraryCommands.findMeshInSelection()
				listTexturesInSet = sg_mayaLibraryCommands.findTexturesInSelection()
				if listShapesInSet:
					# Bring back a list with a dictionary
					shadingGroups = sg_mayaLibraryCommands.findShadersOnGeo(listShapesInSet)
					shadingGroups= list(shadingGroups[0])
					#print(type(shadingGroups),shadingGroups)
				else:
					print("No Geometry in the set, try if there are Texture Nodes")
					if listTexturesInSet:
						shadingGroups = listTexturesInSet

			elif cmds.nodeType(setExport) == 'shadingEngine':
				shadingGroups.append(setExport)

			if shadingGroups:
				for sGrp in shadingGroups:
					if sGrp != "initialShadingGroup":
						print("Shader to inspect: ", sGrp)
						texturefiles = sg_mayaLibraryCommands.texturesIntoGraph(sGrp)
						print("Texture files associated to shader: ", texturefiles)
						if texturefiles:
							## UI
							window = self.progressWindow(self.textProgressCopyTextures)
							percentage = int(100/(len(texturefiles)))
							progressBarValue = 0
							cmds.progressBar(self.progressControl, edit=True, progress= progressBarValue)

							## Parse the dictionary
							print("Starting texture file process: ")
							for key in texturefiles:
								node = key
								print("For filenode: " + node)
								for attribute in texturefiles[node]:
									originalTexturePath = texturefiles[node][attribute]["filepath"]
									newTextureName = ""
									# Test if it is a UDIM collection
									if "_MAPID_" in originalTexturePath or "<UDIM>" in originalTexturePath:
										print("MAPID/UDIM found on: " + node)
										# Find all the texture matching pattern
										pattern = originalTexturePath.split("_MAPID_")[0]
										listMatchingTextures = glob.glob(pattern+"*")
										pattern = originalTexturePath.split("<UDIM>")[0]
										listMatchingTextures += glob.glob(pattern+"*")
										for patternTexture in listMatchingTextures:
											## Copying file
											print("Copying UDIM: " + patternTexture)
											newTextureName = self.copyFile(patternTexture,sourceImagesPath)
									else:
										## Copying file
										newTextureName = self.copyFile(originalTexturePath,sourceImagesPath)
										print("Copying texture: " + originalTexturePath)
									## Resetting the file node with the new path
									if "_MAPID_" in originalTexturePath:
										# Update with newpath but keep _MAPID_
										nameMAPIDFile = newTextureName.split(sourceImagesPath)[-1]
										# find UDIM
										num = re.findall(r'\d+',nameMAPIDFile)
										if num:
											newTextureName = sourceImagesPath+nameMAPIDFile.split(num[-1])[0] + "_MAPID_" + nameMAPIDFile.split(num[-1])[-1]
										else:
											newTextureName = sourceImagesPath+nameMAPIDFile
										print("MAPID Update: " + sourceImagesPath+nameMAPIDFile)
									cmds.setAttr(attribute, newTextureName, type="string")
									print("Set filenode: " + node + " with new copied path: " + newTextureName)
								## Store new name
								listNewTextures.append(newTextureName)
								## UI
								progressBarValue += percentage
								cmds.progressBar(self.progressControl, edit=True, progress= progressBarValue)
					
							## Close UI
							cmds.progressBar(self.progressControl, edit=True, endProgress=True)
							cmds.deleteUI( window, window=True )

		if in_hou:
			if hou.node(setExport).type().name()== "collect":
				shadingGroups.append(hou.node(setExport))
			if shadingGroups:
				for sGrp in shadingGroups:
					print("Shader Found = " + str(sGrp.name()))
					texturefiles = sg_houdiniLibraryCommands.texturesIntoGraph(sGrp)
				if texturefiles:
					## Parse the dictionary
					for key in texturefiles:
						node = key
						print("Texture file: " + node.name())
						for attribute in texturefiles[node]:
							originalTexturePath = texturefiles[node][attribute]["filepath"]
							if "_MAPID_" in originalTexturePath or "<UDIM>" in originalTexturePath:
								print("MAPID/UDIM found on: " + node)
								# Find all the texture matching pattern
								pattern = originalTexturePath.split("_MAPID_")[0]
								listMatchingTextures = glob.glob(pattern+"*")
								pattern = originalTexturePath.split("<UDIM>")[0]
								listMatchingTextures += glob.glob(pattern+"*")
								for patternTexture in listMatchingTextures:
									## Copying file
									print("Copying UDIM: " + patternTexture)
									newTextureName = self.copyFile(patternTexture,sourceImagesPath)
							else:
								## Copying file
								attribute = attribute.split(".")[-1]
								newTextureName = self.copyFile(originalTexturePath,sourceImagesPath)
							## Resetting the old node withthe new path
							node.parm(attribute).set(newTextureName)
							print("Copied file: " + newTextureName)
							listNewTextures.append(newTextureName)

		return listNewTextures

	def saveShadersFromModel(self,setExport,shaderPath):
		listShaderAdded = []
		dicShader= []
		if in_maya:
			cmds.select( setExport,replace = True )
			listMeshes = sg_mayaLibraryCommands.findMeshInSelection()
			listShaders = sg_mayaLibraryCommands.findShadersOnGeo(listMeshes)
			for shadingGrp in listShaders[0]:
					## Found Material Type
					try:
						materialRman = cmds.listConnections(shadingGrp+".rman__surface",source= True, destination = False)
					except:
						materialRman = None
					try:
						materialArnold = cmds.listConnections(shadingGrp+".aiSurfaceShader",source= True, destination = False)
					except:
						materialArnold = None

					if materialRman != None:
						self.rendererShader =  'renderman'
					elif materialArnold != None:
						self.rendererShader =  'arnold'
					else:
						self.rendererShader =  'arnold'

					## Export Json Shaders
					if self.rendererShader == 'renderman' :
						dicShader = sg_mayaRenderman.buildDictionary(shadingGrp)
					elif self.rendererShader == 'arnold':
						dicShader = sg_mayaArnold.buildDictionary(shadingGrp)
					else:
						dicShader = sg_mayaArnold.buildDictionary(shadingGrp)
					if dicShader:
						jsonShader = shaderPath+shadingGrp +".json"
						with open(jsonShader,'w') as outJson:
								json.dump(dicShader,outJson,indent = 4)

						attachmentShader  = shaderPath+ self.jsonAttachmentShader
						with open(attachmentShader,'w') as outAttachJson:
								json.dump(listShaders[1],outAttachJson,indent = 4)
					listShaderAdded.append(shadingGrp)
			print("Shader Exporting Process Done")

	def saveTexturesFromLight(self,setExport,sourceImagesPath):
		print(" - Looking for texture to copy, on lights - ")
		dicMapsLight = {}
		lightShapes = []
		if in_maya:
			# Get object in set with long name
			sg_mayaLibraryCommands.selectObjects(setExport,"replace")
			# Find Light in Hierarchy
			for top in sg_mayaLibraryCommands.getSelection(True):
				lightShapes += sg_mayaLibraryCommands.findLightsInHierarchy(top)
			## Look For the texture in all the hierarchy lights
			dicMapsLight = sg_mayaLibraryCommands.findTextureFilesOnNodes(lightShapes)
			for key in dicMapsLight:
				textureMapI = dicMapsLight[key]['textureMap']
				attribute = key + "." + dicMapsLight[key]['attribute']
				if textureMapI != "":
					basenameI = os.path.basename(textureMapI)
					textureMapO = os.path.join(sourceImagesPath,basenameI)
					# Copy the map to the new path
					if textureMapI != textureMapO:
						self.simpleCopyFile(textureMapI,textureMapO)
						# Set New path on the Light
						sg_mayaLibraryCommands.setAttrString(attribute,textureMapO)
					else:
						print("No need to copy textures, path are identical")
		if in_katana:
			print("Keep Textures on Lights, no saving")
		if in_hou:
			# Get object in set with long name
			topNode = hou.node(self.exportSet)
			# Find Light in Hierarchy
			if topNode:
				mergeAllLightType = self.listRendermanLights + self.listArnoldLights
				lightShapes = sg_houdiniLibraryCommands.findLightsInHierarchy(topNode,lightShapes,mergeAllLightType)
				## Look For the texture in all the hierarchy lights
				dicMapsLight = sg_houdiniLibraryCommands.findTextureFilesOnNodes(lightShapes)
				for key in dicMapsLight:
					textureMapI = dicMapsLight[key]['textureMap']
					attribute = dicMapsLight[key]['attribute']
					if textureMapI != "":
						basenameI = os.path.basename(textureMapI)
						textureMapO = os.path.join(sourceImagesPath,basenameI)
						# Copy the map to the new path
						if textureMapI != textureMapO:
							self.simpleCopyFile(textureMapI,textureMapO)
							# Set New path on the Light
							hou.node(key).parm(attribute).set(textureMapO)
						print("No need to copy textures, path are identical")
			else:
				print("No Node to parse to find Textures")

	def copyFile(self, inFile, outPath):
		nameFile = os.path.basename(inFile)
		outFile = os.path.join(outPath,nameFile)
		try:
			if not os.path.exists(outFile):
				copyfile(inFile, outFile)
			else:
				print("Copy Failed: "+ outFile + " ... SKIPPED")
		except:
			print(sys.exc_info())
			print("Copy Failed - ")
			pass
		return outFile
		
	def simpleCopyFile(self, inFile, outFile):
		try:
			copyfile(inFile, outFile)
		except:
			print(sys.exc_info())
			print("Copy Failed - " + inFile + " - " + outFile + " ")
			pass
		return outFile

	def copyExternalFile(self, inFile, outFile):
		try:
			copyfile(inFile, outFile)
		except:
			e = sys.exc_info()
			print(e)
			print("Copy Failed, please manually add the file to your new entry")
			pass
		return outFile

	def setBrowserTab(self):
		self.main_widget.libraryTab.setCurrentIndex(0)

	######################################## UI  ########################################

	def toggleUseDiscThumbnail(self,enabled):
		self.main_widget.sg_thumbnailFile_lineEdit.setEnabled(enabled)
		self.main_widget.sg_thumbnailFile_toolButton.setEnabled(enabled)

	def toggleVDBUseDiscThumbnail(self,enabled):
		self.main_widget.sg_VDBthumbnailFile_lineEdit.setEnabled(enabled)
		self.main_widget.sg_VDBthumbnailFile_toolButton.setEnabled(enabled)

	#########################################################################################

	def selectThumbnailFile(self):
		selected_thumbnailFile = QtWidgets.QFileDialog.getOpenFileName(self,"Choose an image file","","*.jpg *.png *.gif")
		selected_thumbnailFile.setFixedSize(1000,600)
		self.main_widget.sg_thumbnailFile_lineEdit.setText(str(selected_thumbnailFile[0]))

	def selectThumbnailIES(self):
		newIESIcon = QtWidgets.QFileDialog.getOpenFileName(self,"Choose an image file","","*.jpg *.png *.gif")
		newIESIcon.setFixedSize(1000,600)
		# Update Icon
		if newIESIcon[0] != "":
			self.iconIESNewEntry = newIESIcon[0]
			self.buttonNewIESFound(self.iconIESNewEntry)
		else:
			self.iconIESNewEntry = ""
			print("No IES Icon Selected")

	def selectVDBThumbnailFile(self):
		selected_thumbnailFile = QtWidgets.QFileDialog.getOpenFileName(self,"Choose an image file","","*.jpg *.png *.gif")
		selected_thumbnailFile.setFixedSize(1000,600)
		self.main_widget.sg_VDBthumbnailFile_lineEdit.setText(str(selected_thumbnailFile[0]))

	def selectFolderDialog(self):
		dialogFolder = sgFolderDialog()
		dialogFolder = QtWidgets.QFileDialog(self,"Pick Folder")
		dialogFolder.setFixedSize(1000,600)
		dialogFolder.setFileMode(QtWidgets.QFileDialog.Directory)
		dialogFolder.setOption(QtWidgets.QFileDialog.DontUseNativeDialog,True)
		dialogFolder.setOption(QtWidgets.QFileDialog.ShowDirsOnly,False)

		dialogFolder.exec_()

		selected_Folder = dialogFolder.selectedFiles()[0]
		if dialogFolder.result() == True:
			return selected_Folder
		else:
			return None

	def selectFilesListDialog(self):
		dialogList = QtWidgets.QFileDialog(self,"Pick VDB")
		dialogList.setFixedSize(1000,600)
		dialogList.setFileMode(QtWidgets.QFileDialog.AnyFile)
		dialogList.setNameFilter("*.vdb")
		dialogList.setOption(QtWidgets.QFileDialog.DontUseNativeDialog,True)
		dialogList.setOption(QtWidgets.QFileDialog.ShowDirsOnly,False)
		dialogList.exec_()

		selectedFiles = dialogList.selectedFiles()[0]
		if dialogList.result() == True:
			return selectedFiles
		else:
			return None

	def selectFolderNewLibrary(self):
		selected_Folder = QtWidgets.QFileDialog.getExistingDirectory(self,"Choose folder to create a library","",QtWidgets.QFileDialog.ShowDirsOnly)
		#selected_Folder.setFixedSize(1000,600)
		self.main_widget.lineEdit_PathNewLibrary.setText(str(selected_Folder)+"/")

		self.main_widget.lineEdit_sgFolderTexturesEntry.setText(str(selected_Folder)+"/")

	def selectFolderUIUpdate(self,button):
		# Open Dialog box
		selectedFolder = self.selectFolderDialog()
		# Depending of the button, launch the adequate process
		# New Textures
		if button.objectName() == "pushButton_sg_PickFolderTexturesEntry":
			if selectedFolder != None:
				self.main_widget.lineEdit_sgFolderTexturesEntry.setText(str(selectedFolder)+"/")
				files = self.findFilesInFolder(False,selectedFolder,self.listImagefileExtension)
				# UI
				self.newTexturesEntryQuantity = self.findSizeList(files)
				self.main_widget.label_sgFoundTextureFolder.setText("Found: " + str(self.newTexturesEntryQuantity) + " images in the folder")

				suggestedName = self.suggestNameFromFile(files[0])
				self.setTextureNameUI(suggestedName)
			else:
				self.main_widget.lineEdit_sgFolderTexturesEntry.setText("")
				self.newTexturesEntryQuantity = 0
				self.main_widget.label_sgFoundTextureFolder.setText("Found: " + "0" + " image in the folder")
				self.setTextureNameUI("")
		# New DMP
		elif button.objectName() == "pushButton_sg_PickDMPFolderEntry":
			if selectedFolder:
				# UI
				self.main_widget.lineEdit_sgFolderDMPEntry.setText(str(selectedFolder)+"/")
				files = self.findDMPinFolder(selectedFolder)
				suggestedName = self.suggestNameFromFolder(selectedFolder)
				self.setDMPNameUI(suggestedName)
			else:
				#self.main_widget.lineEdit_sgFolderDMPEntry.setText("")
				self.setDMPNameUI("")
		# New IES
		elif button.objectName() == "pushButton_sg_PickFolderIESEntry":
			if selectedFolder != None:
				# UI
				self.main_widget.lineEdit_sgFolderIESEntry.setText(str(selectedFolder)+"/")
				files = self.findIESinFolder(selectedFolder)
				suggestedName = self.suggestNameFromFolder(selectedFolder)
				self.setIESNameUI(suggestedName)
			else:
				#self.main_widget.lineEdit_sgFolderIESEntry.setText("")
				self.setIESNameUI("")
		# New Artbook Or Tutorial
		elif button.objectName() == "pushButton_sg_PickABTFolderEntry":
			if selectedFolder != None:
				# UI
				self.main_widget.lineEdit_sgFolderABTEntry.setText(str(selectedFolder)+"/")
				files = self.findABTinFolder(selectedFolder)
				suggestedName = self.suggestNameFromFolder(selectedFolder)
				self.setATBNameUI(suggestedName)
			else:
				#self.main_widget.lineEdit_sgFolderABTEntry.setText("")
				self.setATBNameUI("")
		else:
			print(button.objectName())

	def selectVDBFile(self):
		selected_vdbFile = self.selectFilesListDialog()
		#selected_vdbFile = QtWidgets.QFileDialog.getOpenFileNames(self,"Choose one vdb","","*.vdb")
		if selected_vdbFile != None:
			self.main_widget.lineEdit_sgFolderVDBntry.setText(str(selected_vdbFile))
			if "#" in selected_vdbFile:
				folder,files,first,last = self.findVDBSequences(selected_vdbFile)
				# UI
				self.main_widget.frame_sgVDBFilesSequence.setEnabled(True)
				self.main_widget.lineEdit_sgVDBSequenceStart.setText(str(first))
				self.main_widget.lineEdit_sgVDBSequenceEnd.setText(str(last))
			else:
				self.main_widget.frame_sgVDBFilesSequence.setEnabled(False)
			#self.main_widget.lineEdit_sgFolderVDBntry.setText(str(selected_vdbFile[0][0]))
			#self.findVDBSequences(selected_vdbFile[0])
		else:
			self.main_widget.lineEdit_sgFolderVDBntry.setText("")

#######################################################################################################################
################################################## ADD New Entry UI ###################################################
#######################################################################################################################

	def createNewFolder(self,newpath):
		if not os.path.exists(newpath):
			os.umask(0)
			folderCreated = os.makedirs(newpath,0o777)
		else:
			folderCreated = "Already Exist"
		return folderCreated

	def createNewFolderLibrary(self,rootPath,nameLibrary,dicNewHierarchy):
		if not os.path.exists(rootPath+nameLibrary):
			os.umask(0)
			folderMain = os.makedirs(rootPath+nameLibrary,0o777)

			baseFolder = os.path.join(rootPath+nameLibrary)
			for key,value in dicNewHierarchy["new"].items():
				if type(value)== str:
					folderCreated = os.makedirs(os.path.join(baseFolder,key),0o777)
					#print("Created Folder: ", folderCreated)
				else:
					subData = value
					subBaseFolder = os.path.join(baseFolder,key)
					for subkey in subData:
						folderCreated = os.makedirs(os.path.join(subBaseFolder,subkey),0o777)
						#print("Created Folder: ", folderCreated)

		else:
			folderCreated = "Already Exist"
		return folderCreated

	def deleteFolderLibrary(self,path):
		delete = ""
		if os.path.exists(path):
			delete = shutil.rmtree(path)
		return delete

	def deleteFileLibrary(self,path):
		delete = ""
		if os.path.exists(path):
			delete = os.remove(path)
		return delete

	def renameAndCopyTextures(self,listTextures,folder,entryName):
		listNewTextures=[]
		for texture in listTextures:
			newName = folder + entryName + "_" + texture.split("_")[-1]
			try:
				copyfile(texture, newName)
				print (" File Copied: " + str(newName))
				listNewTextures.append(newName)
			except:
				pass
				print("Texture Copy Failed, Ignored: " + str(texture))
		return listNewTextures

	def thumbnailAddEntry(self,path,uuid):
		thumbnail=""
		## Thumbnail export
		# Use choosen image
		if self.context != "ArtBooks" and self.context != "Tutorials":
			if self.main_widget.checkBox_sgUseFileDisc.isChecked():
				try:
					thumbnail = path + uuid + self.nameNewEntry+ self.thumbnailSuffix + ".jpg"
					copyfile(self.main_widget.sg_thumbnailFile_lineEdit.text(), thumbnail)
				except:
					print(sys.exc_info())
					thumbnail = self.thumbnailsCreator(uuid + self.nameNewEntry+self.thumbnailSuffix,False)
			# Do a screen grab
			else:
				thumbnail = self.thumbnailsCreator(uuid+ self.nameNewEntry+self.thumbnailSuffix,False)
		elif self.context == "ArtBooks" or self.context == "Tutorials":
			# Copy the file picked
			extension =  self.dataNewATB['previewImage'].split(".")[-1]
			thumbnail = path + "/" + uuid + self.nameNewEntry + self.thumbnailSuffix + "." + extension
			self.simpleCopyFile(self.dataNewATB['previewImage'], thumbnail)

		return thumbnail

	def suggestNameFromFolder(self,folder):
		if os.path.isdir(folder):
			if folder[-1] != "/":
				folder += "/"
			nameFile = os.path.basename(os.path.dirname(folder))
		#nameFile = folder.split("/")[-1]
		return nameFile

	def suggestNameFromFile(self,file):
		nameFile = os.path.basename(file).split(".")[0]
		return nameFile

	def setATBNameUI(self,text):
		self.main_widget.lineEdit_sgABTNewName.setPlaceholderText(text)
		self.main_widget.lineEdit_sgABTNewName.setText(text)

	def setVDBNameUI(self,text):
		self.main_widget.lineEdit_sgVDBNameEntry.setPlaceholderText(text)
		self.main_widget.lineEdit_sgVDBNameEntry.setText(text)

	def setIESNameUI(self,text):
		self.main_widget.lineEdit_sgAddIESRename.setPlaceholderText(text)
		self.main_widget.lineEdit_sgAddIESRename.setText(text)

	def setDMPNameUI(self,text):
		self.main_widget.lineEdit_sgDMPNewName.setPlaceholderText(text)
		self.main_widget.lineEdit_sgDMPNewName.setText(text)

	def setTextureNameUI(self,text):
		self.main_widget.lineEdit_sgTexturesNewName.setPlaceholderText(text)
		self.main_widget.lineEdit_sgTexturesNewName.setText(text)

	def setModelNameUI(self,text):
		self.main_widget.lineEdit_sgNameEntry.setPlaceholderText(text)
		self.main_widget.lineEdit_sgNameEntry.setText(text)

#######################################################################################################################

	def saveModelEntry(self,folder,nameEntry,export,alembic):
		listFilesExported = []
		##Export Model
		if in_maya:
			## First Select
			cmds.select(export, replace= True)
			# sg_mayaLibraryCommands.generateData(cmds.ls(selection=True))
			
			cmds.file( rename= folder + nameEntry + ".ma")
			listFilesExported.append(folder + nameEntry + ".ma")

			cmds.select(export, replace= True,hi=True)
			cmds.file(es=True, type='mayaAscii' )

			if alembic == True:
				##Shader renderer set in saveShadersFromModel
				cmds.select(export, replace= True,hi=True)
				sg_mayaLibraryCommands.exportAlembic(folder+nameEntry+".abc",self.rendererShader)
				listFilesExported.append(folder+nameEntry+".abc")
				# pm.mel.FBXExport(f = folder + nameEntry+ ".fbx")

		return listFilesExported

	def saveShaderEntry(self,folder,nameEntry,export):
		# Expect one shading group
		#
		#
		#
		print("-- Saving Shader for: ", self.subContext )
		dicShader = {}
		if in_maya:
			selectionNodes = cmds.select(export, replace= True)
			## Export Shader
			if self.subContext == 'renderman':
				dicShader = sg_mayaRenderman.buildDictionary(node)
			elif self.subContext == 'arnold':
				dicShader = sg_mayaArnold.buildDictionary(self.exportSet)
			else:
					print("Unrecognized subcontext: " + self.subContext)
		elif in_hou:
			dicShader = sg_houdiniRenderman.buildDictionary(self.exportSet)
		if dicShader:
			jsonShader = folder+nameEntry +".json"
			with open(jsonShader,'w') as outJson:
						json.dump(dicShader,outJson,indent = 4)
		else:
			print("Error in building/exporting the shader: shader node list errored")

	def saveTextureEntry(self,folder,nameEntry,export):
		if in_maya:
			cmds.select(export, replace= True)
			listFileToParse = cmds.ls(type=('PxrTexture','PxrMultiTexture','file','aiImage'),sl= True)
		if in_nuke:
			if nuke.selectedNodes():
				listFileToParse = nuke.selectedNodes()
			else:
				listFileToParse = self.nukeObjectToSave

		if listFileToParse:
			for imageFile in listFileToParse:
				if in_maya:
					id = cmds.nodeType(imageFile)
					if id =="PxrTexture" or  id == 'aiImage':
						attributeFilename = ".filename"
					elif id =='PxrMultiTexture':
						attributes = [".filename0",".filename1",".filename2",".filename3",".filename4",".filename5",".filename6",".filename7",".filename8",".filename9"]
					elif id == 'file':
						attributeFilename = ".fileTextureName"
					if id !='PxrMultiTexture':
						if imageFile + attributeFilename not in self.textureFileToExport:
							self.textureFileToExport.append(cmds.getAttr(imageFile + attributeFilename))
					else:
						for attributeFilename in attributes:
							if imageFile + attributeFilename not in self.textureFileToExport and cmds.getAttr(imageFile + attributeFilename) != "":
									self.textureFileToExport.append(cmds.getAttr(imageFile + attributeFilename))
				if in_nuke:
					id = imageFile.Class()
					if id== "Read":
						if imageFile['file'].value() not in self.textureFileToExport:
							self.textureFileToExport.append(imageFile['file'].value())
					elif id == "ReadGeo2":
						print("Can't save a model in the texture folder")
					else:
						nameFile = nameEntry
						sg_nukeLibraryCommands.writeTextureToExport(imageFile,folder,nameFile)

		## Copy with New Name
		listNewTextureName = self.renameAndCopyTextures(self.textureFileToExport,folder,nameEntry)

		return listNewTextureName

	def saveDMPEntry(self,folder,nameEntry):
		imageFiles=[]
		folderImg = self.main_widget.lineEdit_sgFolderDMPEntry.text()
		folderDMPImages = os.path.join(folder,"dmpSources")

		# UI
		progressBarValue = 0.0
		self.resetProgressBar(self.pbCopyingFile)

		if folderImg:
			for fileType in self.listdmpImagefileExtension:
				imageFiles += self.findFilesInFolder(False,folderImg,fileType)
			if imageFiles:
				if self.rbNewDMPEntryType == "radioButton_sgDMPCopyImgs":
					progressIncrease = 100.0/len(imageFiles)
					for file in imageFiles:
						basename = os.path.basename(file)
						newTextureName = self.simpleCopyFile(file,os.path.join(folderDMPImages,basename))
						# UI
						progressBarValue += progressIncrease
						self.main_widget.progressBar_sgLoading.setValue(progressBarValue)
					# Update UI
					progressBarValue = 100.0
					self.main_widget.progressBar_sgLoading.setValue(progressBarValue)
					self.main_widget.progressBar_sgLoading.setFormat("Done... "+'%p%')

					self.progressBarFinish(timeSleep = 0.5)
				else:
					folderImg = os.path.dirname(imageFiles[0])
					pathJsonDMPLink = folder + "/" + nameEntry + self.jsonDMPLinkExtension 
					jsonDMPLink = self.writeDmpLinkJson(pathJsonDMPLink,nameEntry,folderImg)
			else:
				print("No Images in folder")

		return imageFiles

	def saveLightrigEntry(self,folder,nameEntry,export):
		### Expect a set then convert as selection
		###
		print("-- Saving Lightrig for: ", self.subContext )
		dicLights = {}
		dicLightRig = {}
		dicConnections = {}
		if in_maya:
			select = sg_mayaLibraryCommands.selectObjects(self.exportSet, "replace")
			selectedObjects = sg_mayaLibraryCommands.getSelection(False)
			## Export Light
			if selectedObjects:
				for obj in selectedObjects:
					dcc = cmds.about(application=True)
					version = str(cmds.about(version=True))
					idString = ""
					
					dicLights,dicConnections = sg_mayaLibraryCommands.hierarchyDict(obj,dicLights,dicConnections)
					dicLightRig = fcn.setDefaultLightrigDict(dicLights,dicConnections,dcc,version,idString)
			else:
				print("Set is empty")

		elif in_hou:
			topNode = hou.node(self.exportSet)
			houdiniNodeInfos = sg_houdiniLibraryCommands.getCurrentContextNode()
			if topNode:
				dcc = hou.applicationName()
				version = ".".join(str(h) for h in hou.applicationVersion())
				idString = ""
				
				dicLights,dicConnections = sg_houdiniLibraryCommands.hierarchyDict(topNode,dicLights,dicConnections,self.listRendermanLights,houdiniNodeInfos)
				dicLightRig = fcn.setDefaultLightrigDict(dicLights,dicConnections,dcc,version,idString)
			else:
				self.message("Node don't exist anymore, please retry with correct node")

		elif in_katana:
			objType = NodegraphAPI.GetNode(self.exportSet).getType()
			obj = NodegraphAPI.GetNode(self.exportSet)
			rootPackage = obj.getRootPackage()
			children = rootPackage.getChildPackages()
			
			dcc = "katana"
			version = "unknown"
			idString = ""
			for child in children:
				dicLights,dicConnections = sg_katanaLibraryCommands.hierarchyDict(child,dicLights,dicConnections)
			dicLightRig = fcn.setDefaultLightrigDict(dicLights,dicConnections,dcc,version,idString)
		
		# Save the dictionary as json
		if dicLightRig:
			jsonLights = folder+nameEntry +".json"
			with open(jsonLights,'w') as outJson:
				json.dump(dicLightRig,outJson,indent = 4)
		else:
			print("Error in exporting the lightrig: nodes list errored")

	def saveIESEntry(self,folder,nameEntry,uuid):
		listFileCopied = []

		## Copy Icon
		iconExtension = self.iconIESNewEntry.split(".")[-1]
		iconIESNewEntryNewPath = folder + uuid + nameEntry+"_Preview." + iconExtension
		
		copyIcon = self.simpleCopyFile(self.iconIESNewEntry,iconIESNewEntryNewPath)

		self.nameNewEntryThumbnail = uuid + nameEntry+"_Preview." + iconExtension

		## Copy IES file
		iesExtension = self.iesFileNewEntry.split(".")[-1]
		iesFileNewEntryNewPath = folder+nameEntry + "." + iesExtension

		copyIES = self.simpleCopyFile(self.iesFileNewEntry,iesFileNewEntryNewPath)

		if copyIES:
			listFileCopied.append(iesFileNewEntryNewPath)

		return listFileCopied

	def saveVDBEntry(self,folder,nameEntry,vdbFiles):
		listVDBCopied = []
		# Copy files to destination folder
		if type(vdbFiles) == list:
			for vdb in vdbFiles:
				print("Copy : " + vdb + " to: " + folder)
		elif type(vdbFiles) == tuple:
			# UI
			progressBarValue = 0.0
			self.resetProgressBar(self.pbCopyingFile)

			folderIn,files,first,last = self.findVDBSequences(vdbFiles[0])
			first = vdbFiles[1]
			last = vdbFiles[2]
			filename = os.path.basename(vdbFiles[0])
			num = filename.split("#")

			progressIncrease = 100.0/len(files)
			for file in files:
				if int(first) <= int(file[len(num[0]):len(num[0])+len(num[-1])-1]) <= int(last):
					destinationFile = os.path.join(folder,file)
					self.simpleCopyFile(os.path.join(folderIn,file),destinationFile)
					listVDBCopied.append(destinationFile)

					# UI
					progressBarValue += progressIncrease
					self.main_widget.progressBar_sgLoading.setValue(progressBarValue)
			
			# Update UI
			progressBarValue = 100.0
			self.main_widget.progressBar_sgLoading.setValue(progressBarValue)
			self.main_widget.progressBar_sgLoading.setFormat("Done... "+'%p%')
			print("Copied: "+"\n" + '\n'.join("- " + str(p) for p in listVDBCopied))
		
		else:
			# TODO
			# Right now it is a string
			
			filename = os.path.basename(vdbFiles)
			destinationFile = os.path.join(folder,filename)
			self.simpleCopyFile(vdbFiles,destinationFile)
			listVDBCopied.append(destinationFile)
			print("Copied : " , vdbFiles ," of type: " ,str(type(vdbFiles))," to: " + folder)

		return listVDBCopied

	def saveATBEntry(self,folder,nameEntry,dictNewATB):
		# Folder is the root folder -  Needs to add the atb source folder for copy of file 
		#
		listATBCopied = []

		## UI
		progressBarValue = 0.0
		self.resetProgressBar(self.pbCopyingFile)

		## Copy Images 
		if dictNewATB['artBookImages']:
			if len(dictNewATB['artBookImages']) > 1:
				if self.rbNewATBEntryType == "radioButton_sgABTCopyImgs":
					# Take in account the UI
					if self.main_widget.radioButton_sgABTConvertCBZ.isChecked() == True and self.main_widget.groupBox_ABTConvert.isEnabled() == True:
						nameNewCBZ = os.path.join(os.path.join(folder,self.nameATBSource),nameEntry+".cbz")
						# Create CBZ
						outCBZ = self.createCBZ(os.path.dirname(dictNewATB['artBookImages'][0])+"/",nameNewCBZ)
						# Copy
						if outCBZ:
							#self.simpleCopyFile(outPDF,nameNewPDF)
							listATBCopied.append(outCBZ)
						else:
							userMessage = self.sendMessage("CBZ Not Created, please check the error log")
					elif self.main_widget.radioButton_sgABTConvertPDF.isChecked() == True and self.main_widget.groupBox_ABTConvert.isEnabled() == True:
						nameNewPDF = os.path.join(os.path.join(folder,self.nameATBSource),nameEntry+".pdf")
						# Create PDF
						outPDF = self.createPDF(os.path.dirname(dictNewATB['artBookImages'][0])+"/",nameNewPDF)
						# Copy
						if outPDF:
							#self.simpleCopyFile(outPDF,nameNewPDF)
							listATBCopied.append(outPDF)
						else:
							userMessage = self.sendMessage("PDF Not Created, please check the error log")
				elif self.rbNewATBEntryType == "radioButton_sgABTLinkToOriginal":
					folderImgPDF = os.path.dirname(dictNewATB['artBookImages'][0])
					pathJsonDMPLink = os.path.join(folder,nameEntry+ self.jsonDMPLinkExtension)
					jsonDMPLink = self.writeDmpLinkJson(pathJsonDMPLink,nameEntry,folderImgPDF)

		if dictNewATB['artBookPDFs'] or dictNewATB['artBookCBRs']:
			if self.rbNewATBEntryType == "radioButton_sgABTCopyImgs":
				# Copy
				if dictNewATB['artBookPDFs']:
					for pdf in dictNewATB['artBookPDFs']:
						basename = os.path.basename(pdf)
						nameNewPDF = os.path.join(os.path.join(folder,self.nameATBSource),basename)
						self.simpleCopyFile(pdf,nameNewPDF)
						listATBCopied.append(nameNewPDF)
				if dictNewATB['artBookCBRs']:
					for cbr in dictNewATB['artBookCBRs']:
						basename = os.path.basename(cbr)
						nameNewCBR = os.path.join(os.path.join(folder,self.nameATBSource),basename)
						self.simpleCopyFile(cbr,nameNewCBR)
						listATBCopied.append(nameNewCBR)

			elif self.rbNewATBEntryType == "radioButton_sgABTLinkToOriginal":
				if dictNewATB['artBookPDFs']:
					folderPDF = os.path.dirname(dictNewATB['artBookPDFs'][0])
					pathJsonDMPLink = os.path.join(folder,nameEntry+ self.jsonDMPLinkExtension)
					jsonDMPLink = self.writeDmpLinkJson(pathJsonDMPLink,nameEntry,folderPDF)
				if dictNewATB['artBookCBRs']:
					folderCBR = os.path.dirname(dictNewATB['artBookCBRs'][0])
					pathJsonDMPLink = os.path.join(folder,nameEntry+ self.jsonDMPLinkExtension)
					jsonDMPLink = self.writeDmpLinkJson(pathJsonDMPLink,nameEntry,folderCBR)

		if dictNewATB['tutorialFolder']:
			if self.rbNewATBEntryType == "radioButton_sgABTCopyImgs":
				# Copy
				self.simpleCopyFile(dictNewATB['tutorialFolder'],os.path.join(folder,self.nameATBSource))
				listATBCopied.append(folder)
			elif self.rbNewATBEntryType == "radioButton_sgABTLinkToOriginal":
				print("Not yet there")

		return listATBCopied

	def addNewEntry(self,button):
		try:
			self.selectedPath = self.selectTreeItem()
			if button.objectName() == "pushButton_sgAddEntry":
				self.nameNewEntry = self.main_widget.lineEdit_sgNameEntry.text()
				self.exportSet = self.main_widget.lineEdit_sgExportSet.text()
				choosenThumbn = self.main_widget.sg_thumbnailFile_lineEdit.text()
			elif button.objectName() == "pushButton_sgVDBAddEntry":
				self.nameNewEntry = self.main_widget.lineEdit_sgVDBNameEntry.text()
				if self.main_widget.frame_sgVDBFilesSequence.isEnabled():
					sequenceFileStart = self.main_widget.lineEdit_sgVDBSequenceStart.text()
					sequenceFileEnd = self.main_widget.lineEdit_sgVDBSequenceEnd.text()
					self.exportSet = (self.main_widget.lineEdit_sgFolderVDBntry.text(),sequenceFileStart,sequenceFileEnd)
				else:
					self.exportSet = self.main_widget.lineEdit_sgFolderVDBntry.text()
				
				choosenThumbn = self.main_widget.sg_VDBthumbnailFile_lineEdit.text()
			## Need to improve that, it can be something else like a gif or a png
			if choosenThumbn != "" :
				extensionThumb = choosenThumbn.split(".")[-1]
			else:
				extensionThumb = "jpg"
			self.nameNewEntryThumbnail  = self.nameNewEntry + "_Preview." + extensionThumb

			self.indexFolderToSave =  self.main_widget.treeWidget_sgLibrary.indexFromItem(self.main_widget.treeWidget_sgLibrary.currentItem())
			self.category = self.main_widget.treeWidget_sgLibrary.itemFromIndex(self.indexFolderToSave).text(0)
			self.context = self.main_widget.treeWidget_sgLibrary.itemFromIndex(self.selectedPath[2][0]).text(0)

			folderNewEntry = self.selectedPath[0] + self.nameNewEntry + "/"
		except:
			self.selectedPath= [""]
			self.nameNewEntry= ""
			self.exportSet = ""
			print("Could not get UI infos")
			print(sys.exc_info())
			pass

		self.format =""
		self.nukeObjectToSave = []

		self.textureFileToExport=[]
		self.notes =  self.main_widget.lineEdit_sgWriteNotes.text()
		self.tags = self.main_widget.lineEdit_sgWriteTags.text()
		self.listFileAvailable = []
		self.extraFile01 = self.main_widget.lineEdit_sgWriteExtraFiles01.text()
		self.extraFile02 = self.main_widget.lineEdit_sgWriteExtraFiles02.text()
		
		# Reload Database to check if nobody did a new entry
		self.reloadAllDatabase()

		print("---- Add Element Process Started ----")
		print("New Entry Name: " + self.nameNewEntry + " to be saved in: " + self.selectedPath[0] + " with that set: ", self.exportSet)

		tmpname01 = self.nameNewEntry + "_Preview.jpg"
		tmpname02 = self.nameNewEntry + "_Preview.png"
		tmpname03 = self.nameNewEntry + "_Preview.gif"
		if tmpname01 in self.dicAllDatabase.keys() or tmpname02 in self.dicAllDatabase.keys() or tmpname03 in self.dicAllDatabase.keys():
			self.sendMessage("ERROR: Name is not unique. Pick a different name")
			return False

		if self.selectedPath[0] != "" and self.nameNewEntry != "" and self.exportSet != "" :
			## Verify content of data to export
			if button.objectName() == "pushButton_sgAddEntry":
				if in_maya:
					toExport = cmds.nodeType(self.exportSet)
					# SelectIt and get the 
					print("Node type to export: " + toExport )
				if in_nuke:
					toExport = ""
					self.listNukeObjects = list(self.exportSet.split(self.separator))
					for obj in self.listNukeObjects:
						if nuke.exists(obj):
							toExport = "objectSet"
							self.nukeObjectToSave.append(nuke.toNode(obj))
				if in_hou:
					typ = hou.node(self.exportSet).type().description()
					if typ == "collect":
						toExport = "shadingEngine"
						print("Node type to export: " + toExport )
					elif typ == "Null" or typ in self.listRendermanLights or typ in self.listArnoldLights:
						toExport = "objectSet"
						print("Node type to export: " + toExport )
					else:
						toExport = "None"
						self.sendMessage("Cannot export that node for a lightrig. Please export a null or a light instead")
				if in_katana:
					tmpExport = NodegraphAPI.GetNode(self.exportSet).getType()
					if tmpExport == "GafferThree":
						toExport = "objectSet"
					obj = NodegraphAPI.GetNode(self.exportSet)
					print("Node to export: " + obj.getName() +  " of type: " + tmpExport)

			elif button.objectName() == "pushButton_sgVDBAddEntry":
				if self.exportSet:
					toExport = "VDB"
			
			###################### Check if the context is legit compare to data exported
			print("Context Selected: " + self.context + " / Subcontext Selected: " + self.subContext)
			depthFolderSelection = self.getDepthSelectedTreePath()
			if self.context == "Models" or self.context =="Shaders" or self.context == "Lightrigs":
				if depthFolderSelection < 2:
					message = "Can't save in that category - Please select a subcategory to export your new element to, or create one"
					userMessage = self.sendMessage(message)
					if userMessage == True:
						print(message)
						print("Cancelled Operation")
						return False
			elif self.context == "Textures" or self.context == "DMP" or self.context == "VDB" or self.context == "IES":
				if depthFolderSelection < 1:
					message = "Can't save in that category - Please select a subcategory to export your new element to, or create one"
					userMessage = self.sendMessage(message)
					if userMessage == True:
						print(message)
						print("Cancelled Operation")
						return False
			else:
				message = "Can't save YET in that category - Please contact the developper"
				userMessage = self.sendMessage(message)
				if userMessage == True:
					print(message)
					print("Cancelled Operation")
					return False

			################## Triage depending of context
			if self.context == "Models" and self.subContext != "" and toExport == "objectSet" or self.context == "Shaders" and self.subContext != "" and toExport == "shadingEngine" or self.context == "Textures" and toExport == "objectSet" or self.context == "Lightrigs" and self.subContext != "" and toExport == "objectSet" or self.context == "VDB" and toExport == "VDB":
				## Check User input
				userAddConfirmation = self.getUserConfirmation("You are about to add one element to: "+ self.context +" in the category: "+ self.category + " named: "+self.nameNewEntry)
				## If user proceed
				if userAddConfirmation == "Yes" or userAddConfirmation == True:
					# Create New Folder
					newFolder = self.createNewFolder(folderNewEntry)
					################################################ Overwrite Entry ################################################
					if newFolder == "Already Exist":
						# Check user wants to overwrite	
						userOverwriteConfirmation = self.getUserConfirmation("You are about to overwrite a version in the library. Do you want to proceed? ")
						if userOverwriteConfirmation=="Yes" or userOverwriteConfirmation == True:
							## Delete old thumbnail
							listOldThumb = glob.glob(folderNewEntry + "*_Preview.*")
							if listOldThumb:
								self.deleteFileLibrary(listOldThumb[0])
								basenameOldThumb = os.path.basename(listOldThumb[0])
								## Delete old databaseEntry but don't save as json until new one is created
								if basenameOldThumb in self.dicAssetDatabase:
									self.removeItemFromAssetDatabase(basenameOldThumb)
									self.removeItemFromGlobalDatabase(basenameOldThumb)
							## Create new entry
							self.processNewEntry(True,folderNewEntry)
							messageCongratsEntry = "---- Entry Overwritten Successfully: " + self.nameNewEntry + " ----"
						else:
							messageCongratsEntry = "- Operation Cancelled - User Cancelled "
					else:
		#################################################### New Entry ##################################################
						self.processNewEntry(False,folderNewEntry)
						messageCongratsEntry = "---- New Entry Added Successfully: " + self.nameNewEntry + " ----"

					## Congrats
					userMessage = self.sendMessage(messageCongratsEntry)
					if userMessage == True:
						print(messageCongratsEntry)
					else:
						return False

					# Refresh Library
					self.setBrowserTab()
					self.refreshLibrary()
					self.launchBrowsing()

					## Log Success
					try:
						logger.info(' New Entry added: ' + self.nameNewEntry + ' successfully ! ')
					except:
						pass
					print("\n")
				else:
					# User Cancelled operation 
					print (self.uiMessageOperationCancelled)
			else:
				if self.subContext == "":
					message = "- Operation Cancelled - Need to pick a sub-category before adding your entry like: prod, previs,arnold or renderman "
				elif self.context not in self.libraryWritableContext:
					message = "- Operation Cancelled - Need to pik a context before adding your entry, please pick one before adding a new element - Operation Cancelled "
				elif toExport != "objectSet" or toExport != "shadingGroup":
					message = "- Operation Cancelled - Set content doesn't match the requirement for the category. It could be empty or wrong type - Operation Cancelled "
				
				userMessage = self.sendMessage(message)
				if userMessage == True:
					print(message)
					return False	
		else:
			# No New name or selection or data to export
			if self.selectedPath[0] == "":
				print("- Please select where to export in the Library")
				message = "- Please select where to export in the Library"
			elif self.nameNewEntry == "":
				print("- Please pick a name for the entry")
				message = "- Please pick a name for the entry"
			elif self.exportSet == "" :
				print("- Please pick a set, a container, a shading group, a gaffer to export")
				message = "- Please pick a set, a container, a shading group, a gaffer to export"
			userMessage = self.sendMessage(message)
			if userMessage == True:
				print(message)
				return False

	def addNewEntryIES(self):
		# UI
		self.selectedPath = self.selectTreeItem()
		self.nameNewEntry = self.main_widget.lineEdit_sgAddIESRename.text()
		self.notes =  self.main_widget.lineEdit_sgIESAddNotes.text()
		self.tags = self.main_widget.lineEdit_sgIESAddTag.text()
		folderNewEntry = self.selectedPath[0] + self.nameNewEntry + "/"

		self.extraFile01 = ""
		self.extraFile02 = ""

		# Reload Database to check if nobody did a new entry
		self.reloadAllDatabase()

		# Check if Entry already exist ( Potentially useless with uuid ) TODO
		for ext in self.thumbnailsfileExtension:
			tmpname = self.nameNewEntry + "_Preview." + ext
			if tmpname in self.dicAllDatabase.keys():
				self.sendMessage("ERROR: Name is not unique. Pick a different name")
				return False

		if self.context == "IES":
			depthFolderSelection = self.getDepthSelectedTreePath()
			if depthFolderSelection < 1:
				message = "- Operation Cancelled - Can't save in that category - Please select a subcategory to export your new element to, or create one"
				userMessage = self.sendMessage(message)
				if userMessage == True:
					print(message)
					print("Cancelled Operation")
					return False
			elif depthFolderSelection > 1:
				message = "- Operation Cancelled - Can't save inside an entry - Please select a parent category"
				userMessage = self.sendMessage(message)
				if userMessage == True:
					print(message)
					print("Cancelled Operation")
					return False
			else:
				# Check if the new entry are not empty/legit
				if self.iesFileNewEntry and self.iconIESNewEntry :
					# Create folder
					newFolder = self.createNewFolder(folderNewEntry)
					if newFolder == "Already Exist":
						# Check user wants to overwrite	
						userOverwriteConfirmation = self.getUserConfirmation("You are about to overwrite a version in the library. Do you want to proceed? ")
						if userOverwriteConfirmation=="Yes" or userOverwriteConfirmation == True:
							## Delete old thumbnail
							listOldThumb = glob.glob(folderNewEntry + "*_Preview.*")
							if listOldThumb:
								self.deleteFileLibrary(listOldThumb[0])
								basenameOldThumb = os.path.basename(listOldThumb[0])
								## Delete old databaseEntry but don't save as json until new one is created
								if basenameOldThumb in self.dicAssetDatabase:
									self.removeItemFromAssetDatabase(basenameOldThumb)
									self.removeItemFromGlobalDatabase(basenameOldThumb)
							#### Overwrite Entry
							self.processNewEntry(True,folderNewEntry)
							messageCongratsEntry = "---- Entry Overwritten Successfully: " + self.nameNewEntry + " ----"
						else:
							messageCongratsEntry = "- Operation Cancelled - User Cancelled "
					else:
						# Add Entry
						self.processNewEntry(False,folderNewEntry)
						messageCongratsEntry = "---- New Entry Added Successfully: " + self.nameNewEntry + " ----"
					## Congrats
					userMessage = self.sendMessage(messageCongratsEntry)
					if userMessage == True:
						print(messageCongratsEntry)
					else:
						return False

					# Refresh Library
					self.setBrowserTab()
					self.refreshLibrary()
					self.launchBrowsing()
				else:
					message = "- Operation Cancelled - Missing IES file and/or icon "
					userMessage = self.sendMessage(message)
					if userMessage == True:
						print(message)
						return False
		else:		
			message = "- Operation Cancelled - Not in the correct context "
			userMessage = self.sendMessage(message)
			if userMessage == True:
				print(message)
				return False

	def addNewEntryDMP(self):
		# UI
		self.selectedPath = self.selectTreeItem()
		self.nameNewEntry = self.main_widget.lineEdit_sgDMPNewName.text()
		self.notes =  self.main_widget.lineEdit_sgDMPAddNotes.text()
		self.tags = self.main_widget.lineEdit_sgDMPAddTag.text()
		folderNewEntry = self.selectedPath[0] + self.nameNewEntry + "/"

		self.extraFile01 = ""
		self.extraFile02 = ""

		# Reload Database to check if nobody did a new entry
		self.reloadAllDatabase()

		if self.context == "DMP":
			depthFolderSelection = self.getDepthSelectedTreePath()
			if depthFolderSelection < 1:
				message = "- Operation Cancelled - Can't save in that category - Please select a subcategory to export your new element to, or create one"
				userMessage = self.sendMessage(message)
				if userMessage == True:
					print(message)
					print("Cancelled Operation")
					return False
			elif depthFolderSelection > 1:
				message = "- Operation Cancelled - Can't save inside an entry - Please select a parent category"
				userMessage = self.sendMessage(message)
				if userMessage == True:
					print(message)
					print("Cancelled Operation")
					return False
			else:
				# Check if the new entry are not empty/legit
				if self.nameNewEntry:
					# Create folder
					newFolder = self.createNewFolder(folderNewEntry)
					dmpSources = self.createNewFolder(folderNewEntry+"/dmpSources")
					if newFolder == "Already Exist":
						# Check user wants to overwrite	
						userOverwriteConfirmation = self.getUserConfirmation("You are about to overwrite a version in the library. Do you want to proceed? ")
						if userOverwriteConfirmation=="Yes" or userOverwriteConfirmation == True:
							## Delete old thumbnail
							listOldThumb = glob.glob(folderNewEntry + "*_Preview.*")
							if listOldThumb:
								self.deleteFileLibrary(listOldThumb[0])
								basenameOldThumb = os.path.basename(listOldThumb[0])
								## Delete old databaseEntry but don't save as json until new one is created
								if basenameOldThumb in self.dicAssetDatabase:
									self.removeItemFromAssetDatabase(basenameOldThumb)
									self.removeItemFromGlobalDatabase(basenameOldThumb)
							###### Overwrite Entry
							self.processNewEntry(True,folderNewEntry)
							messageCongratsEntry = "---- Entry Overwritten Successfully: " + self.nameNewEntry + " ----"
						else:
							messageCongratsEntry = "- Operation Cancelled - User Cancelled "
					else:
						# Add Entry
						self.processNewEntry(False,folderNewEntry)
						messageCongratsEntry = "---- New Entry Added Successfully: " + self.nameNewEntry + " ----"
					## Congrats
					userMessage = self.sendMessage(messageCongratsEntry)
					if userMessage == True:
						print(messageCongratsEntry)
					else:
						return False
					# UI win
					self.progress = 100.00
					self.pb.setValue(self.progress,self.pbCopyingFile)
					self.pb.finishBar(timeFade = 0.1)

					# Refresh Library
					self.setBrowserTab()
					self.refreshLibrary()
					self.launchBrowsing()

				else:
					message = "- Operation Cancelled - Missing Entry Name "
					userMessage = self.sendMessage(message)
					if userMessage == True:
						print(message)
						return False
		else:		
			message = "- Operation Cancelled - Not in the correct context "
			userMessage = self.sendMessage(message)
			if userMessage == True:
				print(message)
				return False

	def addNewEntryATB(self):
		# UI
		self.selectedPath = self.selectTreeItem()
		self.nameNewEntry = self.main_widget.lineEdit_sgABTNewName.text()
		self.notes =  self.main_widget.lineEdit_sgABTAddNotes.text()
		self.tags = self.main_widget.lineEdit_sgABTAddTag.text()
		folderNewEntry = self.selectedPath[0] + self.nameNewEntry + "/"

		self.extraFile01 = ""
		self.extraFile02 = ""

		# Reload Database to check if nobody did a new entry
		self.reloadAllDatabase()

		if self.context == "ArtBooks" or self.context == "Tutorials":
			depthFolderSelection = self.getDepthSelectedTreePath()
			if depthFolderSelection < 1:
				message = "- Operation Cancelled - Can't save in that category - Please select a subcategory to export your new element to, or create one"
				userMessage = self.sendMessage(message)
				if userMessage == True:
					print(message)
					print("Cancelled Operation")
					return False
			elif depthFolderSelection > 1:
				message = "- Operation Cancelled - Can't save inside an entry - Please select a parent category"
				userMessage = self.sendMessage(message)
				if userMessage == True:
					print(message)
					print("Cancelled Operation")
					return False
			else:
				# Check if the new entry are not empty/legit
				if self.nameNewEntry:
					# Create folder
					newFolder = self.createNewFolder(folderNewEntry)
					storageSource = self.createNewFolder(folderNewEntry+"/sources")
					if newFolder == "Already Exist":
						# Check user wants to overwrite	
						userOverwriteConfirmation = self.getUserConfirmation("You are about to overwrite a version in the library. Do you want to proceed? ")
						if userOverwriteConfirmation=="Yes" or userOverwriteConfirmation == True:
							## Delete old thumbnail
							listOldThumb = glob.glob(folderNewEntry + "*_Preview.*")
							if listOldThumb:
								self.deleteFileLibrary(listOldThumb[0])
								basenameOldThumb = os.path.basename(listOldThumb[0])
								## Delete old databaseEntry but don't save as json until new one is created
								if basenameOldThumb in self.dicAssetDatabase:
									self.removeItemFromAssetDatabase(basenameOldThumb)
									self.removeItemFromGlobalDatabase(basenameOldThumb)
							###### Overwrite Entry
							self.processNewEntry(True,folderNewEntry)
							messageCongratsEntry = "---- Entry Overwritten Successfully: " + self.nameNewEntry + " ----"
						else:
							messageCongratsEntry = "- Operation Cancelled - User Cancelled "
					else:
						# Add Entry
						self.processNewEntry(False,folderNewEntry)
						messageCongratsEntry = "---- New Entry Added Successfully: " + self.nameNewEntry + " ----"
					## Congrats
					userMessage = self.sendMessage(messageCongratsEntry)
					if userMessage == True:
						print(messageCongratsEntry)
					else:
						return False
					# UI win
					self.progress = 100.00
					self.pb.setValue(self.progress,self.pbCopyingFile)
					self.pb.finishBar(timeFade = 0.1)

					# Refresh Library
					self.setBrowserTab()
					self.refreshLibrary()
					self.launchBrowsing()

				else:
					message = "- Operation Cancelled - Missing Entry Name "
					userMessage = self.sendMessage(message)
					if userMessage == True:
						print(message)
						return False
		else:		
			message = "- Operation Cancelled - Not in the correct context "
			userMessage = self.sendMessage(message)
			if userMessage == True:
				print(message)
				return False

	def processNewEntry(self,over,folderNewEntry):
		listModelFiles = []
		listTextureFiles = []
		listAllExportedFiles = []

		ocio = ""
		time = os.path.getmtime(folderNewEntry)
		meta = ""
		nakedIcon = ""
		uuid = self.generateUUID()
		jsonFile = folderNewEntry+str(self.nameNewEntry)+self.jsonInfoFileExtension
		data = self.readJsonInfos(jsonFile)
		if over == True:
			if data:
				self.newversion = str(int(data["releaseInfos"][0]["version"])+1)
			else:
				self.newversion = 1
		else:
			self.newversion = 1

		if self.context == "Models":
			## Export Thumbnail
			self.nameNewEntryThumbnail=os.path.basename(self.thumbnailAddEntry(folderNewEntry,uuid))
			nakedIcon = self.nameNewEntryThumbnail.split(self.databaseSeparator)[-1]
			## Export Textures and Reassign path
			sourceImagesFolder = self.createNewFolder(folderNewEntry+ "sourceimages")
			shadersFolder = self.createNewFolder(folderNewEntry+ "shaders")
			listTextureFiles = self.saveTexturesFromModel( self.exportSet,folderNewEntry+ "sourceimages" + "/")
			self.saveShadersFromModel( self.exportSet,folderNewEntry+ "shaders" + "/")
			## Export Model
			listModelFiles = self.saveModelEntry(folderNewEntry,self.nameNewEntry,self.exportSet,self.main_widget.checkBox_sgExportAbc.isChecked())
			# Add Model/Texture files
			listAllExportedFiles += listModelFiles
			listAllExportedFiles += listTextureFiles

			print("File Overwritten: " + folderNewEntry+ self.nameNewEntry+ ".ma" +  "\n")

		elif self.context == "Shaders":
			## Export Thumbnail
			self.nameNewEntryThumbnail=os.path.basename(self.thumbnailAddEntry(folderNewEntry,uuid))
			nakedIcon = self.nameNewEntryThumbnail.split(self.databaseSeparator)[-1]
			## Export Textures and Reassign path
			sourceImagesFolder = self.createNewFolder(folderNewEntry+ "sourceimages")
			listTextureFiles = self.saveTexturesFromModel( self.exportSet,folderNewEntry+ "sourceimages" + "/")
			## Export Shader
			self.saveShaderEntry(folderNewEntry,self.nameNewEntry,self.exportSet)
			## Get Textures exported files
			listAllExportedFiles += listTextureFiles
			#if in_maya:
			#	sg_mayaLibraryCommands.closeHypershade()

		elif self.context == "Textures": # Different from Batch textures
			## Export Thumbnail
			self.nameNewEntryThumbnail=os.path.basename(self.thumbnailAddEntry(folderNewEntry,uuid))
			nakedIcon = self.nameNewEntryThumbnail.split(self.databaseSeparator)[-1]
			## Export Textures
			listTextureFiles = self.saveTextureEntry(folderNewEntry,self.nameNewEntry,self.exportSet)
			## Get Textures exported files 
			listAllExportedFiles += listTextureFiles
			## Get manual ocio
			ocio = self.main_widget.comboBox_sgLTOCIO.currentText()

		elif self.context == "Lightrigs":
			## Export Thumbnail
			self.nameNewEntryThumbnail = os.path.basename(self.thumbnailAddEntry(folderNewEntry,uuid))
			nakedIcon = self.nameNewEntryThumbnail.split(self.databaseSeparator)[-1]
			## Export Textures and Reassign path
			sourceImagesFolder = self.createNewFolder(folderNewEntry+ "sourceimages")
			self.saveTexturesFromLight( self.exportSet,folderNewEntry+ "sourceimages" + "/")
			## Export Lightrigs
			self.saveLightrigEntry(folderNewEntry,self.nameNewEntry,self.exportSet)
			## Get manual ocio
			ocio = ""

		elif self.context == "IES":
			## Use Thumbnail. Set self.nameNewEntryThumbnail in the module
			listIESFiles = self.saveIESEntry(folderNewEntry,self.nameNewEntry,uuid)
			## Get Textures exported files 
			listAllExportedFiles += listIESFiles
			## Get manual ocio
			ocio = ""

		elif self.context == "DMP":
			## Create Thumbnail
			thumbnail = self.launchDMPThumbnail(folderNewEntry)
			if thumbnail:
				#TODO
				nameIcon = uuid+self.nameNewEntry+"_Preview.png"
				nakedIcon = self.nameNewEntry+"_Preview.png"
				self.nameNewEntryThumbnail = nameIcon
				outPath = os.path.join(folderNewEntry,nameIcon)
				self.simpleCopyFile(thumbnail,outPath)
			## Copy Files or Link Them
			listDMPFiles = self.saveDMPEntry(folderNewEntry,self.nameNewEntry)
			## Get Textures exported files 
			listAllExportedFiles += listDMPFiles
			## Get manual ocio
			ocio = self.main_widget.comboBox_sgDMPOCIO.currentText()

		elif self.context == "VDB":
			## Export Thumbnail
			self.nameNewEntryThumbnail= os.path.basename(self.thumbnailAddEntry(folderNewEntry,uuid))
			nakedIcon = self.nameNewEntryThumbnail.split(self.databaseSeparator)[-1]
			## Create Folder
			vdbFolder = os.path.join(folderNewEntry+ "vdb")
			self.createNewFolder(os.path.join(folderNewEntry+ "vdb"))
			## Copy VDB 
			listVDBFiles = self.saveVDBEntry(vdbFolder,self.nameNewEntry,self.exportSet)
			# Add Model/Texture files
			listAllExportedFiles += listVDBFiles
	
		elif self.context == "ArtBooks" or self.context == "Tutorials":
			## Export Thumbnail
			if self.dataNewATB['previewImage']:
				self.nameNewEntryThumbnail= os.path.basename(self.thumbnailAddEntry(folderNewEntry,uuid))
			## Create Folder
			ATBFolder = self.createNewFolder(os.path.join(folderNewEntry, "sources"))
			if ATBFolder == "Already Exist":
				ATBFolder = os.path.join(folderNewEntry, "sources")
			# Create/Copy Data
			listATBFiles = self.saveATBEntry(folderNewEntry,self.nameNewEntry,self.dataNewATB)
			# Add Model/Texture files
			listAllExportedFiles += listATBFiles

		## Extra Files
		if self.context == "Models" or self.context == "Shaders"  or self.context == "Lightrigs":
			if self.extraFile01 != "":
				try:
					self.copyExternalFile(self.extraFile01 ,folderNewEntry+self.nameNewEntry+"."+ self.extraFile01.split(".")[-1])
				except:
					if in_maya:
						cmds.confirmDialog(title='Warning',message ="Couldn't copy the extra files, check the path" )
					pass
			if self.extraFile02 != "":
				try:
					self.copyExternalFile(self.extraFile02 ,folderNewEntry+self.nameNewEntry+"."+self.extraFile02.split(".")[-1])
				except:
					if in_maya:
						cmds.confirmDialog(title='Warning',message ="Couldn't copy the extra files, check the path" )
					pass
		
		##  Find the available format
		listFilesExtension = self.findExtensionFiles(listAllExportedFiles)
		listExtraFiles = [self.extraFile01,self.extraFile02]
		listNameExportedFiles= [ x.split("/")[-1] for x in listAllExportedFiles]

		## Write Json
		self.writeJsonEntryInfos(jsonFile,self.nameNewEntry,listFilesExtension,listTextureFiles,self.notes,self.newversion,self.tags,ocio,time,meta)

		## Update Database Entry ,nameAsset,icon,iconName,uuid
		self.dicAssetDatabase = fcn.addEntryToAssetDatabase(self.dicAssetDatabase,self.databaseAssetsJson,self.libraryPath,self.nameNewEntry,self.nameNewEntryThumbnail,nakedIcon,uuid,str(self.nameNewEntry)+self.jsonInfoFileExtension,folderNewEntry,self.context,time,listFilesExtension,listExtraFiles,listTextureFiles,self.tags,listNameExportedFiles)
		self.dicAllDatabase = fcn.saveGlobalDatabase(self.dicAllDatabase,self.databaseJson,self.dicAssetDatabase,self.dicMegascansZip)

	######################################################  LOGGING ################################################################################

	def logInfos(self):
		############### Logger ###############
		### Crash in Mari and Unreal
		if not in_unreal or not in_mari:
			logging.config.fileConfig(self.pathLogIni, disable_existing_loggers=True)
			global logger
			logger = logging.getLogger("user: " + self.username + " ***** " + softwareUsed)

	def checkLogFile(self,defaultIniFiles,pathLogFile):
		for iniFile in defaultIniFiles:
			iniFile = "E:/Data/library/logging_win.ini"
			newPathIni = "E:/Data/library/logging_linTest.ini"
		data = []

		with open(defaulPathIni) as inifile:
			data = inifile.read().splitlines()
		#print(data)

		with open(newPathIni,"w") as saveFile:
			for item in data:
				if ".log" in item:
					print("Update log filepath to : " + pathLogFile)
					item = "args=(\"pathLogFile\",)"
				saveFile.write("%s\n" %item)
			print("Saved Log filepath in logfile: " + iniFile)

## Launch Unreal Version
if in_unreal:
	app = None
	for entry in QtWidgets.QApplication.allWidgets():
		if type(entry).__name__ == 'sgAlexandriaLibrary':
			entry.close()
		elif type(entry).__name__ == 'sgProgressBarLibrary':
			entry.close()

	if not QtWidgets.QApplication.instance():
		app = QtWidgets.QApplication(sys.argv)

	widget = sgAlexandriaLibrary()
	widget.show()
	try:
		unreal.parent_external_window_to_slate(widget.winId())
	except:
		pass

def register():
	if in_blen:
		bpy.utils.register_class(sgProgressBarLibrary)
		bpy.utils.register_class(sgInputNameDialog)
		bpy.utils.register_class(sgAddCollection)
		bpy.utils.register_class(sgPickLODsgEditInfos)
		bpy.utils.register_class(sgAlexandriaLibrary)

def unregister():
	if in_blen:
		bpy.utils.unregister_class(sgProgressBarLibrary)
		bpy.utils.unregister_class(sgInputNameDialog)
		bpy.utils.unregister_class(sgAddCollection)
		bpy.utils.unregister_class(sgPickLODsgEditInfos)
		bpy.utils.unregister_class(sgAlexandriaLibrary)

def sg_alexandriaLibrary_UI():
	print(" =================================================================== ")
	print( "Class Name: " + str(__name__))
	windowTitle = "Library v2.0.1"
	try:
		logger.info("\n")
		logger.info("Opening: %s",str(__name__))
		logger.info("Version: %s",windowTitle)
	except:
		pass

	if not in_katana:
		## Delete all previous instances
		for entry in QtWidgets.QApplication.allWidgets():
			if type(entry).__name__ == 'sgAlexandriaLibrary':
				entry.close()
				entry.deleteLater()
			elif type(entry).__name__ == 'sgProgressBarLibrary':
				entry.close()
				entry.deleteLater()
		if not in_blen:
			#### MAYA and dockable
			if in_maya:
				windowObject = "sgAlexandriaLibrary"
				if cmds.window(windowObject, q=True,exists=True):
					cmds.deleteUI(windowObject)
					
				if cmds.dockControl('MayaWindow_'+ windowTitle.replace(" ","_").replace(".","_"),q= True,ex=True):
					cmds.deleteUI('MayaWindow_'+ windowTitle.replace(" ","_").replace(".","_"))
				ui = sgAlexandriaLibrary()
				try:
					dockControl = cmds.dockControl('MayaWindow_'+windowTitle, label= windowTitle.replace("_"," "), area='right',floating = False,content=windowObject,allowedArea=['right','left'],w = 1150 ,h =1080,epo = True )
					# print(dockControl)
				except:
					ui.show()

			#### NUKE and Dockable
			elif in_nuke:
				panelMain = nuke.getPaneFor("Properties.1")
				ui = sgAlexandriaLibrary()
				if not nuke.getPaneFor('NukePanel.alexandriaLibrary'):
					panelLib = nukescripts.registerWidgetAsPanel("sg_alexandriaLibrary.sgAlexandriaLibrary", windowTitle , 'NukePanel.alexandriaLibrary', True).addToPane(panelMain)
				else:
					for obj in QtWidgets.QApplication.allWidgets():
						if obj.objectName() == 'NukePanel.alexandriaLibrary':
							obj.deleteLater()
					panelLib = nukescripts.registerWidgetAsPanel("sg_alexandriaLibrary.sgAlexandriaLibrary", windowTitle , 'NukePanel.alexandriaLibrary', True).addToPane(panelMain)

			#### MARI - HOUDINI
			else:
				ui = sgAlexandriaLibrary()
				ui.show()
		#### BLENDER
		else:
			if __name__ == "sg_alexandriaLibrary":
				#register()
				app = QtWidgets.QApplication.instance()
				if not app:
					app = QtWidgets.QApplication(sys.argv)
				ui = sgAlexandriaLibrary()
				ui.show()
	## KATANA
	else:
		for entry in QtWidgets.QApplication.allWidgets():
			##print(type(entry).__name__)
			if type(entry).__name__ == 'sgAlexandriaLibrary':
				entry.close()
			elif type(entry).__name__ == 'sgProgressBarLibrary':
				entry.close()
		ui = sgAlexandriaLibrary()
		ui.show()
		PluginRegistry = [('KatanaPanel',6.0,"LozLibrary",sgAlexandriaLibrary),('KatanaPanel',6.0,"Custom/LozLibrary",sgAlexandriaLibrary),]


