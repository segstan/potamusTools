# -*- coding: utf-8 -*-
########################################################################################################################
################# 								Batch Texture Convert 	  								################
#################									Version 1.0.1										################
########################################################################################################################


import sys
pythonVersion = (sys.version_info[0])


## Maya Version
try:
	from mtoa.core import createStandIn, createVolume
	##To attach the window to maya, sip is going to translate for pyqt some function
	import maya.OpenMayaUI as omu

	in_maya = True
except:
	in_maya = False

## Houdini Version
try:
	import hou
	in_hou = True
except:
	in_hou = False

## Nuke Version
try:
	import nuke
	in_nuke= True
except:
	in_nuke= False

## Mari Version
try:
	import mari
	in_mari= True
except:
	in_mari= False

## Katana Version
try:
	import Katana
	in_katana= True
except:
	in_katana= False

## Blender Version
try:
	import bpy
	in_blen = True
except:
	in_blen = False

try:
	import unreal
	in_unreal=True
except:
	in_unreal=False

if in_maya:
	import maya.cmds as cmds
	import maya.utils

	try:

		from shiboken import wrapInstance
	except:
		from shiboken2 import wrapInstance 

import os
import abc
import time
from functools import partial
import subprocess
from threading import Thread

if pythonVersion == 3:
	from queue import Queue, Empty
elif pythonVersion == 2:
	from Queue import Queue, Empty

import distutils.spawn
import inspect

if in_katana == True:
	from PyQt5 import QtWidgets,QtGui, QtCore, QtWidgets , uic
	##from Qt import QtCore, QtWidgets , uic
else:
	from PySide2 import QtGui, QtCore, QtWidgets , QtUiTools
	from PySide2.QtUiTools import QUiLoader
	from PySide2.QtCore import QFile, QObject

## Attach the window to Software Launch 
def software_main_window():
	if in_maya == True:
		if pythonVersion == 2:
			mayaPtr = omu.MQtUtil.mainWindow() 
			mainWindow = wrapInstance(long(mayaPtr),QtWidgets.QWidget)
		elif pythonVersion == 3:
			mainWindow = QtWidgets.QApplication.activeWindow()
	elif in_hou == True: 
		mainWindow = hou.qt.mainWindow()
	elif in_nuke == True or in_mari == True or in_katana == True or in_blen == True or in_unreal==True: 
		mainWindow = QtWidgets.QApplication.activeWindow()
	else:
		mainWindow = QtWidgets.QApplication.activeWindow()
	return mainWindow

class sgBatchTextureConvert(QtWidgets.QMainWindow):
	def __init__(self, parent = software_main_window()):
		super(sgBatchTextureConvert, self).__init__(parent)

		#Load in your UI file.
		#self.fileDir = os.path.dirname(os.path.abspath(inspect.stack()[0][1]))
		self.fileDir =  os.path.dirname(os.path.abspath(__file__))
		self.platform = sys.platform
		file_interface = os.path.abspath(self.fileDir + "/ui/ui_sg_batchTextureConvert.ui")
		file_interfaceKatana = os.path.abspath(self.fileDir + "/ui/ui_sg_batchTextureConvert_Katana.ui")

		self.stylesheetBUnreal = os.path.abspath(self.fileDir + "/ui/unreal_qtStyle.ssh")

		## StyleSheet
		if in_unreal:
			with open(self.stylesheetBUnreal,"r") as unrealStyleSheet:
				self.setStyleSheet(unrealStyleSheet.read())
			# self.main_widget.setStyle(QtWidgets.QStyleFactory.create("Fusion"))

		if not in_katana:
			self.loader = QUiLoader()
			self.main_widget = self.loader.load(file_interface,self)
			self.setWindowTitle("Batch Convert v1.0.1")
			self.resize(800,540)

		else:
			self.main_widget = uic.loadUi(file_interfaceKatana,self)
			self.main_widget.setWindowTitle("Batch Convert v1.0.1")
			self.main_widget.resize(800,540)

		self.installEventFilter(self)

		if in_nuke == True:
			self.main_widget.pushButton_sgConvertAndReplace.setText("Convert")

		self.commandlineDict = GenericCommand.getValidChildCommands()
		self.outputConverter = sorted(self.commandlineDict.keys(),reverse = True)
		##self.outputConverter = self.outputConverter.reverse()
		self.main_widget.comboBox_sgTypeConvert.addItems(self.outputConverter)

		self.main_widget.progressBar_sgConvertTextures.setFormat("%p % done (%v / %m textures)")
		self.main_widget.progressBar_sgConvertTextures.setValue(0)
		self.main_widget.progressBar_sgConvertTextures.setTextVisible(False)
		self.main_widget.progressBar_sgConvertTextures.setMaximum(100)

		self.main_widget.pushButton_sgConvertTScene.clicked.connect(partial(self.updateUITextures,False))
		self.main_widget.pushButton_sgConvertTSelection.clicked.connect(partial(self.updateUITextures,True))
		self.main_widget.pushButton_sgOpenFolder.clicked.connect(self.updateFolder)

		self.main_widget.pushButton_sgConvertAndReplace.clicked.connect(self.convert)
		self.main_widget.pushButton_sgReplacePath.clicked.connect(self.replacePath)
		self.main_widget.progressBar_sgConvertTextures.valueChanged.connect(self.updateProgressText)
		self.main_widget.comboBox_sgTypeConvert.currentIndexChanged.connect(self.updateFilter)

		self.texColorIn = QtGui.QColor(35, 125, 90)
		self.texColorOut = QtGui.QColor(220, 220, 220)
		self.filetype = ".tex"

		self.errorNoSelection = "No texture selected to convert"

		## Init Tool
		self.actionMenu()
		self.updateUITextures(False)

	def updateFilter(self):
		self.filetype = ""
		if self.main_widget.comboBox_sgTypeConvert.currentText() == "TEX (Prman)":
			self.filetype = ".tex"
			self.main_widget.comboBox_sgTypeTexture.setEnabled(True)
			self.main_widget.comboBox_sgBitDepth.setEnabled(True)
		if self.main_widget.comboBox_sgTypeConvert.currentText() == "RAT (Mantra)":
			self.filetype = ".rat"
			self.main_widget.comboBox_sgTypeTexture.setEnabled(False)
			self.main_widget.comboBox_sgBitDepth.setEnabled(False)
		self.updateUITextures(False)
		self.removeExtension()

	def removeExtension(self):
		print("Will remove extention")

	def listTextures(self,selection):
		dict_textures= {}
		list_textures = []
		list_texturesReal = []
		list_texturenodes = []
		listParent = []
		indexNumbers = [0,1,2,3,4,5,6,7,8,9]
		
		if in_maya:
			if selection != True:
				listNodes = cmds.ls(textures=True)
			else:
				listNodes = cmds.ls(selection = True,textures=True)
			for node in listNodes:
				if cmds.nodeType(node) == "file":
					textureFileName = cmds.getAttr(node + ".fileTextureName")
				elif cmds.nodeType(node) == "PxrTexture":
					textureFileName = cmds.getAttr(node + ".filename")
				elif cmds.nodeType(node) == "PxrOSL":
					print (node)
				elif cmds.nodeType(node) == "PxrMultiTexture":
					for index in indexNumbers:
						if cmds.getAttr(node+".filename"+str(index)) != "":
							textureFileName = cmds.getAttr(node + ".filename"+str(index))
				if 'textureFileName' in locals():
					list_texturesReal.append(textureFileName)
					textureFileName =textureFileName.split(self.filetype)[0]
					list_textures.append(textureFileName)
					list_texturenodes.append(node)
					dict_textures["Scene"]= []
					dict_textures["Scene"].append({
					'texturePath':list_textures,
					'textureRealName':list_texturesReal,
					'textureNodes':list_texturenodes
					})

		elif in_hou:
			if selection != True:
				listNodes = hou.node("/obj").allSubChildren() + hou.node("/stage").allSubChildren()
				for node in listNodes:
					path = node.path()
					nodeType = hou.nodeType(path)
					if nodeType.nameComponents()[2] == "pxrtexture" or nodeType.nameComponents()[2] == "texture" or nodeType.nameComponents()[2] == "pxrmultitexture":
						parent = node.parent()
						listParent.append(parent) if parent not in listParent else listParent
				for parent in listParent:
					listChild = hou.node(parent.path()).children()
					list_textures = []
					list_texturesReal = []
					list_texturenodes = []
					for child in listChild:
						nodeType = hou.nodeType(child.path())
						if nodeType.nameComponents()[2] == "pxrtexture" or nodeType.nameComponents()[2] == "texture" :
							try:
								textureFileNameReal = os.path.realpath(hou.evalParm(child.path()+"/filename"))
							except:
								textureFileNameReal = "ERROR File" + nodeType.name()
							list_texturesReal.append(textureFileNameReal)
							textureFileName = textureFileNameReal.split(self.filetype)[0]
							list_textures.append(textureFileName)
							list_texturenodes.append(child.name())
							dict_textures[parent.path()]= []
							dict_textures[parent.path()].append({
							'texturePath':list_textures,
							'textureRealName':list_texturesReal,
							'textureNodes':list_texturenodes
							})
						elif nodeType.nameComponents()[2] == "pxrmultitexture":
							for index in indexNumbers:
								try:
									textureFileNameReal = os.path.realpath(hou.evalParm(child.path()+"/filename"+str(index)))
									tempPath = hou.evalParm(child.path()+"/filename"+str(index))
								except:
									textureFileNameReal = "ERROR File " + nodeType.name()
									tempPath = ""
								if tempPath != "":
									list_texturesReal.append(textureFileNameReal)
									textureFileName = textureFileNameReal.split(self.filetype)[0]
									list_textures.append(textureFileName)
									list_texturenodes.append(child.name())
									dict_textures[node.path()]= []
									dict_textures[node.path()].append({
									'texturePath':list_textures,
									'textureRealName':list_texturesReal,
									'textureNodes':list_texturenodes
									})
			else:
				listNodes = hou.selectedNodes()
				for node in listNodes:
					nodeType = hou.nodeType(node.path())
					if not nodeType.nameComponents()[2] == "pxrtexture" or nodeType.nameComponents()[2] == "texture" or nodeType.nameComponents()[2] == "pxrmultitexture":
						for texture in node.children():
							textureType = hou.nodeType(texture.path())
							if textureType.nameComponents()[2] == "pxrtexture" or textureType.nameComponents()[2] == "texture":
								try:
									textureFileNameReal = os.path.realpath(hou.evalParm(texture.path()+"/filename"))
								except:
									textureFileNameReal = "ERROR File" + textureType.name()
								list_texturesReal.append(textureFileNameReal)
								textureFileName = textureFileNameReal.split(self.filetype)[0]
								list_textures.append(textureFileName)
								list_texturenodes.append(texture.name())
								dict_textures[node.path()]= []
								dict_textures[node.path()].append({
								'texturePath':list_textures,
								'textureRealName':list_texturesReal,
								'textureNodes':list_texturenodes
								})
							elif textureType.nameComponents()[2] == "pxrmultitexture":
								for index in indexNumbers:
									try:
										textureFileNameReal = os.path.realpath(hou.evalParm(texture.path()+"/filename"+str(index)))
										tempPath = hou.evalParm(child.path()+"/filename"+str(index))
									except:
										textureFileNameReal = "ERROR File " + textureType.name()
										tempPath = ""
										
									if tempPath != "":
										list_texturesReal.append(textureFileNameReal)
										textureFileName = textureFileNameReal.split(self.filetype)[0]
										list_textures.append(textureFileName)
										list_texturenodes.append(texture.name())
										dict_textures[node.path()]= []
										dict_textures[node.path()].append({
										'texturePath':list_textures,
										'textureRealName':list_texturesReal,
										'textureNodes':list_texturenodes
										})
					else:
						textureFileNameReal = os.path.realpath(hou.evalParm(node.path()+"/filename"))
						textureFileName = textureFileNameReal.split(self.filetype)[0]
						dict_textures[node.path()]= []
						dict_textures[node.path()].append({
						'texturePath':[textureFileName,],
						'textureRealName':[textureFileNameReal,],
						'textureNodes':[(node.name()),]
						})

		elif in_nuke:
			if selection != True:
				listNodes = nuke.allNodes(recurseGroups=True)
			else:
				listNodes = nuke.selectedNodes()
			for node in listNodes:
				if node.Class()=="Read":
					try:
						textureFileName = nuke.toNode(str(node.name())).knob('file').getValue()
						list_texturesReal.append(textureFileName)
						textureFileName =textureFileName.split(self.filetype)[0]
						list_textures.append(textureFileName)
						list_texturenodes.append(node)
						dict_textures["Scene"]= []
						dict_textures["Scene"].append({
						'texturePath':list_textures,
						'textureRealName':list_texturesReal,
						'textureNodes':list_texturenodes
						})
					except:
						print("Illegal caracteres in the read name: " + node.name() + " SKIPPED")
		
		return dict_textures					

	def updateFolder(self):
		filesToConvert = QtWidgets.QFileDialog.getOpenFileNames(self,"Choose a file","","(*.png *.jpg *.exr *.tif *.hdr)")
		parentFind = filesToConvert[0][0]
		parentFolder= os.path.dirname(parentFind)
		parent_itm = QtWidgets.QTreeWidgetItem(self.main_widget.treeWidget_sgConvertTextures, [parentFolder+"/"])
		for file in filesToConvert[0]:
			item = QtWidgets.QTreeWidgetItem(parent_itm, [file])
			if os.path.isfile(file.split(".")[0]+self.filetype):
				icon_path = os.path.abspath(self.fileDir+ "/icon/greenTex_icon_16.png")
			else:
				icon_path = os.path.abspath(self.fileDir+ "/icon/redTex_icon_16.png")
			icon = QtGui.QIcon(icon_path)
			item.setIcon(0,icon)

		parent_itm.setExpanded(True)
		##self.main_widget.treeWidget_sgConvertTextures.expandToDepth(0)

	def updateUITextures(self,selection):
		icon_Tex = os.path.abspath(self.fileDir+"/icon/iconTex_16.png")
		self.selection = selection
		self.main_widget.treeWidget_sgConvertTextures.clear()
		self.dict_textures = self.listTextures(selection)
		for key in self.dict_textures:
			j = 0
			parent_itm = QtWidgets.QTreeWidgetItem(self.main_widget.treeWidget_sgConvertTextures, [key])
			listReal = self.dict_textures[key][0]["textureRealName"]
			for texture in self.dict_textures[key][0]["texturePath"]:
				textureClean= texture.split(self.filetype)[0]
				if os.path.isfile(textureClean+self.filetype):
					icon_path = os.path.abspath(self.fileDir+ "/icon/greenTex_icon_16.png")
				else:
					icon_path = os.path.abspath(self.fileDir+ "/icon/redTex_icon_16.png")
				item = QtWidgets.QTreeWidgetItem(parent_itm, [texture])
				icon = QtGui.QIcon(icon_path)
				item.setIcon(0,icon)
				if ".tex" in listReal[j]:
					item.setForeground(0,self.texColorIn)
				j +=1
		if selection == True:
			parent_itm.setExpanded(True)

	def updateIconTex(self):
		icon_path = os.path.abspath(self.fileDir+ "/icon/greenTex_icon_16.png")
		for index in self.selectedIndexes:
			itemToChange =  self.main_widget.treeWidget_sgConvertTextures.itemFromIndex(index)
			icon = QtGui.QIcon(icon_path)
			itemToChange.setIcon(0,icon)

	def getCommandSettings(self):
		converter = str(self.main_widget.comboBox_sgTypeConvert.currentText())
		textureType = str(self.main_widget.comboBox_sgTypeTexture.currentText()).lower()
		horizontalWrap = str(self.main_widget.comboBox_sgWrapHorizontal.currentText()).lower()
		verticalWrap = str(self.main_widget.comboBox_sgWrapVertical.currentText()).lower()
		bitDepthRaw = str(self.main_widget.comboBox_sgBitDepth.currentText()).lower()
		if bitDepthRaw == "8 bit":
			bitDepth = "byte"
		elif bitDepthRaw == "16 bit":
			bitDepth = "short"
		else:
			bitDepth == bitDepthRaw
		listUserSettings = [converter,textureType,horizontalWrap,verticalWrap,bitDepth]
		return listUserSettings

	def replacePath(self):
		data = self.getSelectedTextures()
		mainNode = data[0]
		listTextureFiles = data[1]
		listNodes = data[2]
		self.togglePath(mainNode,listTextureFiles,listNodes)

	def getSelectedTextures(self):
		dictTextureFiles = {}
		listTextureFiles = []
		listNodes=[]
		self.selectedIndexes = []
		selectedItems = self.main_widget.treeWidget_sgConvertTextures.selectedItems()
		if len(selectedItems) != 0:
			currentItem = self.main_widget.treeWidget_sgConvertTextures.currentItem().parent()
			currentIndex = self.main_widget.treeWidget_sgConvertTextures.indexFromItem(currentItem)

			for item in selectedItems:
				self.selectedIndexes.append( self.main_widget.treeWidget_sgConvertTextures.indexFromItem(item))
				parentSelected = item.parent()
				parentIndex = self.main_widget.treeWidget_sgConvertTextures.indexFromItem(parentSelected)
				if parentIndex.isValid():
					mainNode = parentSelected.text(0)
					try:
						textures = self.dict_textures[mainNode][0]["texturePath"]
						index = textures.index(item.text(0))
					except:
						pass
					try:
						nodes = self.dict_textures[mainNode][0]["textureNodes"]
						node = nodes[index]
					except:
						node = ""
					dictTextureFiles[item.text(0)]= []
					dictTextureFiles[item.text(0)].append({
					'node':node,
					'parentNode':mainNode
					})
				else:
					node = ""

			for key in dictTextureFiles:
				mainNode = dictTextureFiles[key][0]["parentNode"]
				listTextureFiles.append(key)
				listNodes.append(dictTextureFiles[key][0]["node"])
			return mainNode,listTextureFiles,listNodes
		else:
			mainNode =""
			return None

	def convert(self):
		data = self.getSelectedTextures()
		if data != None: 
			mainNode = data[0]
			self.listTextureFiles = data[1]
			listNodes = data[2]
			
			converter = str(self.main_widget.comboBox_sgTypeConvert.currentText())
			self.convert_command = self.commandlineDict[converter]
			self.settings = self.getCommandSettings()

			makeTex(ui_obj=self,listTextures= self.listTextureFiles,commands = self.convert_command,settings= self.settings, bypass_UI= False)
			if in_nuke == False:
				self.updatePath(mainNode,self.listTextureFiles,listNodes)
		else:
			if in_maya:
				cmds.warning(self.errorNoSelection)
				cmds.inViewMessage( amg=self.errorNoSelection, pos='botCenter', fade=True, fadeOutTime=800)
			if in_hou:
				print(self.errorNoSelection)

	def actionMenu(self):
		self.actionViewImage = QtWidgets.QAction("View Image", self.main_widget.treeWidget_sgConvertTextures)
		self.actionOpenExplorer = QtWidgets.QAction("Open Explorer", self.main_widget.treeWidget_sgConvertTextures)
		self.actionCopyPath = QtWidgets.QAction("Copy Path", self.main_widget.treeWidget_sgConvertTextures)
		self.main_widget.treeWidget_sgConvertTextures.addAction(self.actionViewImage)
		self.main_widget.treeWidget_sgConvertTextures.addAction(self.actionOpenExplorer)
		self.main_widget.treeWidget_sgConvertTextures.addAction(self.actionCopyPath)
		
		self.actionViewImage.triggered.connect(partial(self.getPathForAction,"file"))
		self.actionOpenExplorer.triggered.connect(partial(self.getPathForAction,"explorer"))
		self.actionCopyPath.triggered.connect(partial(self.getPathForAction,"copy"))

	def getPathForAction(self,typeAction):
		selection = self.main_widget.treeWidget_sgConvertTextures.selectedItems()
		pathFolder = os.path.dirname(selection[0].text(0))
		pathImage = selection[0].text(0)
		if typeAction == "explorer":
			self.openExplorer(pathFolder+"/")
		elif typeAction == "file":
			self.openExplorer(pathImage)
		elif typeAction == "copy":
			self.copyPath(pathImage)

	def openExplorer(self,path):
		if self.platform == "win32":
			os.popen('start explorer "%s" ' % os.path.abspath(path))
		elif self.platform == "linux2":
			try:
				if in_nuke:
					os.system('xdg-open "%s" ' % os.path.abspath(path))
				else:
					os.system('caja "%s" ' % os.path.abspath(path))
			except:
				os.system('xdg-open "%s" ' % os.path.abspath(path))

	def copyPath(self,path):
		app = QtWidgets.QApplication.instance()
		clipboard = app.clipboard()
		clipboard.setText(path)

	def updateProgressText(self):
		"""
		updates progress_text label

		"""
		print(self.main_widget.progressBar_sgConvertTextures.text())

	def incProgressBar(self):
		"""
		gets signals from running threads and increments status, after finished, calls finishedConversion()
		"""
		val_max = self.main_widget.progressBar_sgConvertTextures.maximum()
		val = self.main_widget.progressBar_sgConvertTextures.value()
		val += 1
		self.main_widget.progressBar_sgConvertTextures.setValue(val)

		if val == val_max:
			time.sleep(2)
			self.main_widget.progressBar_sgConvertTextures.valueChanged.disconnect()
			self.finishedConversion()

	def finishedConversion(self):
		"""
		this method is called after conversion is finished and shows elapsed time, disables some not-needed-anymore buttons
		"""
		self.main_widget.progressBar_sgConvertTextures.setTextVisible(False)
		print("\n")
		print(" ---- Finished Convert Process ---- ")
		print("\n")

		self.main_widget.progressBar_sgConvertTextures.setValue(0)
		self.main_widget.pushButton_sgConvertAndReplace.setEnabled(True)
		self.main_widget.progressBar_sgConvertTextures.valueChanged.connect(self.updateProgressText)
		self.updateIconTex()

		## Update UI
		##self.updateUITextures(self.selection)

		##self.progress_text.setText( self.progress_bar.text() + " in {0:.3f} seconds".format(time.time() - self.start_conversion_time) )

	def updatePath(self,mainNode,listTextureFiles,listNodes):
		"""
		updates path on texturefile
		"""
		i = 0
		items = self.main_widget.treeWidget_sgConvertTextures.selectedItems()
		for node in listNodes:
			withTex = listTextureFiles[i]+self.filetype
			if in_maya:
				colorItem = self.texColorIn
				if node != "" and cmds.nodeType(node) =="file":
					filename = cmds.getAttr(node+".fileTextureName")
					if not self.filetype in filename:
						cmds.setAttr(node+".fileTextureName",withTex,type ="string")
						colorItem = self.texColorIn	
				elif node != "" and  cmds.nodeType(node) =="PxrTexture":
					filename = cmds.getAttr(node+".filename")
					if not self.filetype in cmds.getAttr(node+".filename"):
						cmds.setAttr(node+".filename",withTex,type ="string")
						colorItem = self.texColorIn
			if in_hou:
				if self.selection == True:
					nodeToUpdate = hou.node(mainNode)
				else:
					nodeToUpdate = hou.node(mainNode+"/"+node+"/")
				filename = hou.evalParm(nodeToUpdate.path()+"/filename")
				if not self.filetype in filename:
					nodeToUpdate.parm('filename').set(withTex)
					colorItem = self.texColorIn
				else:
					colorItem = self.texColorOut
			if in_nuke:
				filename =  nuke.toNode(str(node.name())).knob('file').getValue()
				if not self.filetype in filename:
					node['file'].setValue(withTex)
					colorItem = self.texColorIn
			for item in items:
				item.setForeground(0,colorItem)

			i += 1

	def togglePath(self,mainNode,listTextureFiles,listNodes):
		"""
		updates path on texturefile
		"""
		i = 0
		indexNumbers = [0,1,2,3,4,5,6,7,8,9]
		items = self.main_widget.treeWidget_sgConvertTextures.selectedItems()
		for node in listNodes:
			noTex=listTextureFiles[i].split(self.filetype)[0]
			withTex=listTextureFiles[i]+self.filetype
			if in_maya:
				if node != "" and cmds.nodeType(node) == "file":
					filename = cmds.getAttr(listTextureFiles[i]+".fileTextureName")
					if self.filetype in filename:
						cmds.setAttr(node+".fileTextureName",noTex,type ="string")
						colorItem = self.texColorOut			
					else:
						cmds.setAttr(node+".fileTextureName",withTex,type ="string")
						colorItem = self.texColorIn
				elif cmds.nodeType(node) == "PxrTexture":
					filename =cmds.getAttr(node+".filename")
					if self.filetype in filename:
						cmds.setAttr(node+".filename",noTex,type ="string")
						colorItem = self.texColorOut
					else:
						cmds.setAttr(node+".filename",withTex,type ="string")
						colorItem = self.texColorIn
				elif cmds.nodeType(node) == "PxrMultiTexture":
					for index in indexNumbers:
						filename =cmds.getAttr(node+".filename"+str(index))
						if self.filetype in filename:
							if filename != "":
								cmds.setAttr(node+".filename",noTex,type ="string")
								colorItem = self.texColorOut
						else:
							if filename != "":
								cmds.setAttr(node+".filename",withTex,type ="string")
								colorItem = self.texColorIn
			if in_hou:
				if self.selection == True:
					nodeToUpdate = hou.node(mainNode)
				else:
					nodeToUpdate = hou.node(mainNode+"/"+node+"/")
				filename = hou.evalParm(nodeToUpdate.path()+"/filename")
				if self.filetype in filename:
					nodeToUpdate.parm('filename').set(noTex)
					colorItem = self.texColorOut
				else:
					nodeToUpdate.parm('filename').set(withTex)
					colorItem = self.texColorIn
			if in_nuke:
				filename = nuke.toNode(str(node.name())).knob('file').getValue()
				if self.filetype in filename:
					node['file'].setValue(noTex)
					colorItem = self.texColorOut
				else:
					node['file'].setValue(withTex)
					colorItem = self.texColorIn

			for item in items:
				item.setForeground(0,colorItem)

			i += 1

class GenericCommand(object):
	"""
	abstract class that should be used as a base for classes implementing conversion for various renderers
	"""
	__metaclass__ = abc.ABCMeta

	@abc.abstractmethod
	def name(self):
		"""
		should return str name of output format, it will be shown in UI for user to choose
		"""
		pass

	@abc.abstractmethod
	def executable(self):
		"""
		should return an executable performing the conversion
		"""
		pass

	@abc.abstractmethod
	def generateCommand(self):
		"""
		should return a list containing command and arguments
		if some reason conversion shouldn't happend, then returns None
		"""
		pass

	@classmethod
	def getValidChildCommands(cls):
		"""
		finds implemented child classes and checks if their executable is present on the system
		"""
		command_classes = cls.__subclasses__()
		command_classes_dict = {}

		for cmd_class in command_classes:
			found = distutils.spawn.find_executable( cmd_class.executable() )
			if found:
				command_classes_dict[ cmd_class.name() ] = cmd_class.generateCommand
			else:
				print( 'Warning: "{executable}" executable was not found, hiding "{format}" option.'.format( executable=cmd_class.executable(), format=cmd_class.name() ) )
		return command_classes_dict

class TxPRMan(GenericCommand):
	"""
	converts textures for PRMan TX format  
	"""
	@staticmethod
	def name():
		return "TEX (Prman)"

	@staticmethod
	def executable():
		return "txmake"

	@staticmethod
	def generateCommand(texture_in,envLatlong,smode,tmode,bit):
		##texture_out = texture_in.split(".")
		##texture_out[-1] = "tex"
		texture_out = texture_in + "." + "tex"
		if str(envLatlong).lower() == "texture":
			latlong= ""
			return [TxPRMan.executable(), "-smode", str(smode), "-tmode", str(tmode), "-"+str(bit), texture_in, texture_out]
		else:
			
			latlong = "-"+str(envLatlong)
			return [TxPRMan.executable(), latlong, "-smode", str(smode), "-tmode", str(tmode), "-"+str(bit), texture_in, texture_out]

		##return [TxPRMan.executable(), latlong, "-smode", str(smode), "-tmode", str(tmode), "-"+str(bit), texture_in, texture_out]

class MakeTxPRMan(GenericCommand):
	"""
	converts textures for PRMan TX format with color conversion 
	"""
	@staticmethod
	def name():
		return "Prman OCIO"

	@staticmethod
	def executable():
		return "maketx"

	@staticmethod
	def generateCommand(texture_in,envLatlong,smode,tmode,inputCIO,outputCIO):
		##texture_out = texture_in.split(".")
		##texture_out[-1] = "tex"
		texture_out = texture_in + "." + "tx"
		if str(envLatlong).lower() == "texture":
			latlong= ""
			return [TxPRMan.executable(), "-prman ", "-colorconvert", str(inputCIO), str(outputCIO), "-swrap", str(smode), "-twrap", str(tmode), texture_in, "-o", texture_out]
		else:
			
			latlong = "-"+str(envlatl)
			return [TxPRMan.executable(), "-prman ", latlong, "-colorconvert", str(inputCIO), str(outputCIO), "-swrap", str(smode), "-twrap", str(tmode), texture_in, "-o", texture_out]

		##return [TxPRMan.executable(), latlong, "-smode", str(smode), "-tmode", str(tmode), "-"+str(bit), texture_in, texture_out]

class Rat(GenericCommand):
	"""
	converts textures to Mantra RAT format    
	"""
	@staticmethod
	def name():
		return "RAT (Mantra)"

	@staticmethod
	def executable():
		return "iconvert"

	@staticmethod
	def generateCommand(texture_in,smode,tmode):
		texture_out = texture_in.split(".")
		texture_out[-1] = "rat"
		texture_out = ".".join(texture_out)

		return [Rat.executable(), texture_in, texture_out]

class IncSignal(QtCore.QObject):
	"""
	a class used for sending signals
	"""
	if not in_katana:
		sig = QtCore.Signal()
	else:
		sig= QtCore.pyqtSignal()

class WorkerThread(QtCore.QThread):
	def __init__(self, queue, convert_command,settings, id):
		super(WorkerThread, self).__init__()
		self.incSignal = IncSignal()
		self.queue = queue
		self.convert_command = convert_command

		self.id = id
		self.stop = False
		self.userSettings = settings

	def run(self):
		while not self.stop:
			try:
				texture_in = self.queue.get(False)
				if self.userSettings[0]== "TEX (Prman)":
					cmd = self.convert_command(texture_in,self.userSettings[1],self.userSettings[2],self.userSettings[3],self.userSettings[4])
				elif self.userSettings[0]== "RAT (Mantra)":
					cmd = self.convert_command(texture_in,self.userSettings[2],self.userSettings[3])
				startupinfo = None
				if os.name == 'win32':
					startupinfo = subprocess.STARTUPINFO()
					startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

				if cmd:
					p = subprocess.Popen(cmd, stdout=subprocess.PIPE, startupinfo=startupinfo)
					out = p.communicate()[0]
					print("\nThread #{}".format(self.id))
					print("Command: {}".format( " ".join(cmd) ))
					print("Command output:\n{dashes}\n{out}{dashes}".format(out=out, dashes="-"*50))
					print("Return code: {}\n".format(p.returncode))
				else:
					print("Cmd is None, skipping...")

				if not self.stop:
					self.incSignal.sig.emit()

			except Empty:
				reason = "Empty queue"
				break

		if self.stop:
			reason = "Stopped"

		print("Thread #{} finished ({})".format(self.id, reason))
		return

def nukeMakeTex(queue,convert_command,settings,id):
	##incSignal = IncSignal()
	userSettings = settings
	startupinfo = None
	
	try:
		if os.name == 'win32':
			startupinfo = subprocess.STARTUPINFO()
			print(startupinfo)
			startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
		print("Queue size is now : ", str(queue.qsize()))
		texture_in = queue.get(False)
		cmd = convert_command(texture_in,userSettings[1],userSettings[2],userSettings[3],userSettings[4])
		print("Converting Textures... ")

		p = subprocess.Popen(cmd)
		out = p.communicate()[0]
		# sgBatchTextureConvert().incProgressBar()

		print("\nThread #{}".format(id))
		print("Command: {}".format( " ".join(cmd) ))
		print("Command output:\n{dashes}\n{out}{dashes}".format(out=out, dashes="-"*50))

	except Empty:
		print("Empty Queue - Finished Tex Creation")
	return 

def makeTex(ui_obj,listTextures,commands,settings,bypass_UI):
	pythonVersion= (sys.version_info[0])
	if bypass_UI == False:
		ui_obj.main_widget.progressBar_sgConvertTextures.setMaximum(len(listTextures))
		ui_obj.main_widget.progressBar_sgConvertTextures.show()
		if in_nuke != True:
			ui_obj.main_widget.pushButton_sgConvertAndReplace.setEnabled(False)
			ui_obj.main_widget.progressBar_sgConvertTextures.setTextVisible(True)

	# convert list to a queue
	texturesQueue = Queue(maxsize=0)

	print("Amount of textures to render: ",str(len(listTextures)))
	## Python Switch for blender
	if pythonVersion == 3:
		for x in range(len(listTextures)):
			texturesQueue.put(listTextures[x])
	elif pythonVersion == 2:
		for x in xrange(len(listTextures)):
			texturesQueue.put(listTextures[x])

	ui_obj.processes = []
	for i in range(2):
		if not in_nuke:
			proc = WorkerThread(queue=texturesQueue, convert_command=commands, settings=settings,id=i)
		else:
			proc = nukeMakeTex(queue=texturesQueue, convert_command=commands, settings=settings,id=i)

		if bypass_UI == False:
			if not in_nuke:
				proc.incSignal.sig.connect(ui_obj.incProgressBar)
		ui_obj.processes.append(proc)

	for proc in ui_obj.processes:
		if in_nuke == False:
			proc.start()

	return

def showBatchConvertUI():
	uiB = sgBatchTextureConvert()
	for entry in QtWidgets.QApplication.allWidgets():
		if type(entry).__name__ == "sgBatchTextureConvert":
			entry.close()

	uiB.show()

