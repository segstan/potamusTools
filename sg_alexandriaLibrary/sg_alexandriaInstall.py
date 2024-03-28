import os
import sys
import re
import platform
import json
import glob

from functools import partial
from shutil import copyfile

pythonVersion = (sys.version_info[0])
if pythonVersion == 3:
	import importlib

################################################ Software Detection #####################################################
fileDir = os.path.dirname(os.path.abspath(__file__))
pathDetectSoftware = os.path.abspath(os.path.join(fileDir, '../sg_findSoftware/'))
sys.path.append( pathDetectSoftware )

import sg_findSoftware
if pythonVersion == 2:
	reload(sg_findSoftware)
elif  pythonVersion == 3:
	importlib.reload(sg_findSoftware)

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

#########################################################################################################

if in_katana == True :
	from PyQt5 import QtWidgets,QtGui,QtCore,uic 
	from PyQt5.QtGui import QMovie
else:
	from PySide2 import QtGui, QtCore, QtWidgets , QtUiTools
	from PySide2.QtUiTools import QUiLoader
	from PySide2.QtCore import QFile, QObject
	from PySide2.QtCore import QEvent
	from PySide2.QtGui import QMovie

##########################################################################################################

import sg_functions as fcn
if pythonVersion == 2:
	reload(fcn)
elif pythonVersion == 3:
	importlib.reload(fcn)

##########################################################################################################

def software_main_window():
	if in_maya == True:
		if pythonVersion == 2:
			mayaPtr = omu.MQtUtil.mainWindow()
			mainWindow = wrapInstance(long(mayaPtr),QtWidgets.QWidget)
		elif pythonVersion == 3:
			mainWindow = QtWidgets.QApplication.activeWindow()
	elif in_hou == True:
		import hou
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

class alexandriaFirstLaunch(QtWidgets.QMainWindow):
	def __init__(self, parent = software_main_window()):
		super(alexandriaFirstLaunch, self).__init__(parent)
		platform = sys.platform
		self.fileDir = os.path.dirname(os.path.abspath(__file__))
		self.fileDir = fcn.fixOSPath(self.fileDir)

		file_interface = os.path.join(self.fileDir + "/ui/ui_sgAlexandriaInstall.ui")
		stylesheet = os.path.join(self.fileDir + "/themes/flatDark.qss")

		# Load UI
		if not in_katana:
			self.loader = QUiLoader()
			self.flMainUI = self.loader.load(file_interface,self)
			self.setObjectName("alexandriaFirstLaunch")
		else:
			self.flMainUI = uic.loadUi(file_interface,self)
		self.setWindowTitle("Alexandria Installation")
		self.setWindowIcon(QtGui.QIcon(self.fileDir+"/icons/sg_alexandriaLibrary_icon64.png"))

		## BG Icon
		bgPixmap = QtGui.QPixmap(self.fileDir+"/icons/bgInstall.jpeg").scaled(900, 900, QtCore.Qt.KeepAspectRatio,QtCore.Qt.SmoothTransformation)
		self.flMainUI.labelBG.setPixmap(bgPixmap)
		#self.flMainUI.labelBG.setText("Test")

		## Attach Command
		self.flMainUI.pb_createFirstLibrary.clicked.connect(self.checkStep01Infos)
		self.flMainUI.pb_sgDefaultRoot.clicked.connect(lambda:self.openFolderSelectionUI(self.flMainUI.pb_sgDefaultRoot))
		self.flMainUI.le_sgDefaultName.textChanged.connect(self.previewStep01)
		self.flMainUI.le_sgDefaultRoot.textChanged.connect(self.previewStep01)

		self.flMainUI.pb_createMegascansZip.clicked.connect(self.checkStep02Infos)
		self.flMainUI.pb_sgFL_ZipFolders.clicked.connect(lambda:self.openFolderSelectionUI(self.flMainUI.pb_sgFL_ZipFolders))
		self.flMainUI.le_sgDefaultZipName.textChanged.connect(self.previewStep02)
		self.flMainUI.le_sgFL_ZipFolders.textChanged.connect(self.previewStep02)

		self.flMainUI.pb_installDCCTools.clicked.connect(self.checkStep03Infos)

		# Init
		self.initUISteps()

		# USe
		import sg_alexandriaLibrary
		self.inst = sg_alexandriaLibrary.sgAlexandriaLibrary()

	def initUISteps(self):
		self.flMainUI.tabWidget_install.setCurrentIndex(0)
		## Plateform
		system = platform.system()

		## User
		self.userFolder = os.path.expanduser("~")
		if "/Documents" in self.userFolder:
			self.userFolder = self.userFolder.replace("/Documents","")
		self.userFolder = fcn.fixOSPath(self.userFolder)

		self.detectDCC()

		## JsonFile
		self.defaultPathLibraryJson = os.path.join(self.fileDir,"setup/defaultPath.json")
		self.dataPathDefaultLibrary = fcn.readJsonfile(self.defaultPathLibraryJson)

		# Data DCC
		self.mayaInstPref = fcn.fixOSPath(os.path.join(self.fileDir,"installation/DCC/maya"))
		self.nukeInstPref = fcn.fixOSPath(os.path.join(self.fileDir,"installation/DCC/nuke"))
		self.houdiniInstPref = fcn.fixOSPath(os.path.join(self.fileDir,"installation/DCC/houdini"))

		## Set Placeholder
		# Default Steps 01
		self.flMainUI.le_sgDefaultName.setPlaceholderText("library")
		if system == "Windows":
			textDefaultRoot = "D:/mainDisk/folderOfYourChoice"
			textZipFolder =  "D:/mainDisk/megascanZips"
		elif system == "Linux":
			textDefaultRoot = "/mainDisk/folderOfYourChoice"
			textZipFolder = "/mainDisk/megascanZips"
		self.flMainUI.le_sgDefaultRoot.setPlaceholderText(textDefaultRoot)
		# Default Steps 02
		self.flMainUI.le_sgDefaultZipName.setPlaceholderText("megascansZips")
		self.flMainUI.le_sgFL_ZipFolders.setPlaceholderText(textZipFolder)

		## Set UI
		self.flMainUI.message_first.setText("System Detected: " + system)

	def checkStep01Infos(self):
		nameValid = False
		rootValid = False
		
		# Check Validity of Library Name
		if self.flMainUI.le_sgDefaultName.text() != "" :
			nameValid = fcn.checkNameValidity(self.flMainUI.le_sgDefaultName.text(),"Folder")
			nameLibrary = self.flMainUI.le_sgDefaultName.text()
		# Check Validity of Folders
		if self.flMainUI.le_sgDefaultRoot.text() != "":
			if os.path.isdir(self.flMainUI.le_sgDefaultRoot.text()) == True:
				rootValid = True
				rootDirectory = self.flMainUI.le_sgDefaultRoot.text()

		if nameValid == True and rootValid == True :
			# Create Directory Structure
			system = platform.system()
			self.createInitialLibraryFolder(rootDirectory,nameLibrary,system)
			# Update Default Path Json
			pathLibrary = fcn.fixOSPath(os.path.join(rootDirectory,nameLibrary))
			self.dataPathDefaultLibrary["Generalist Library"][0]["path_"+ system ] = pathLibrary+"/"
			## Update UI
			# Switch Tab
			self.flMainUI.tabWidget_install.setCurrentIndex(1)
		else:
			if nameValid == False:
				print("Name is not valid")
			if rootValid == False:
				print("Root Folder is not valid path")

	def previewStep01(self):
		self.flMainUI.labelStep01_Preview02.setText(fcn.fixOSPath(os.path.join(self.flMainUI.le_sgDefaultRoot.text(),self.flMainUI.le_sgDefaultName.text())))

	def checkStep02Infos(self):
		nameValid = False
		zipFolderValid = False
		# Check Validity of Megascans Folder Name
		if self.flMainUI.le_sgDefaultZipName.text() != "" :
			nameValid = fcn.checkNameValidity(self.flMainUI.le_sgDefaultZipName.text(),"Folder")
			nameMegascansFolder = self.flMainUI.le_sgDefaultZipName.text()

		# Check Validity of Folders
		if self.flMainUI.le_sgFL_ZipFolders.text() != "":
			if os.path.isdir(self.flMainUI.le_sgFL_ZipFolders.text()) == True:
				zipFolderValid = True
				megascansDirectory = self.flMainUI.le_sgFL_ZipFolders.text()
			if self.flMainUI.le_sgDefaultRoot.text() == self.flMainUI.le_sgDefaultZipName.text():
				zipFolderValid = False

		if nameValid == True and zipFolderValid == True :
			system = platform.system()
			self.createMegascansZipFolder(megascansDirectory,nameMegascansFolder,system)
			# Update Default Path Json
			pathMegascansZip = fcn.fixOSPath(os.path.join(megascansDirectory,nameMegascansFolder))
			self.dataPathDefaultLibrary["Generalist Library"][0]["megascans_"+ system ] = pathMegascansZip+"/"

			# Write Json to File
			fcn.writeJsonFile(self.defaultPathLibraryJson,self.dataPathDefaultLibrary)

			self.inst.sendMessage("Megascans Zip Folder Created in: " + "\n" + os.path.join(rootPath,nameNewLibrary) + "\n" + " Now let's do Step 03 ")

			# Update UI
			# Switch Tab
			self.flMainUI.tabWidget_install.setCurrentIndex(2)
		else:
			if nameValid == False:
				print("Name is not valid")
			if zipFolderValid == False:
				print("Megascans Folder is not valid path")

	def previewStep02(self):
		self.flMainUI.labelStep02_Preview02.setText(fcn.fixOSPath(os.path.join(self.flMainUI.le_sgFL_ZipFolders.text(),self.flMainUI.le_sgDefaultZipName.text())))

	def checkStep03Infos(self):
		# Houdini
		if self.flMainUI.cbHoudini_step03.isChecked():
			# Edit Toolbar Pref
			pathToFileHoudiniShelf = houdiniPref.shelf()
			fileHoudiniShelf = os.path.basename(pathToFileHoudiniShelf)

			inPathHoudiniShelf = fcn.fixOSPath(os.path.join(self.houdiniInstPref,pathToFileHoudiniShelf))

			for prefFolder in self.houdiniInstallPrefFolder:
				outPathHoudiniShelf = fcn.fixOSPath(os.path.join(prefFolder,"toolbar",fileHoudiniShelf))

				if os.path.exists(inPathHoudiniShelf):
					result = houdiniPref.editCommand(inPathHoudiniShelf,outPathHoudiniShelf,fileHoudiniShelf,self.fileDir)
					if result:
						print("Houdini Shelf installed for " + os.path.basename(prefFolder))
					else:
						print(inPathHoudiniShelf , " doesn't exist !")
			# Edit Panel Pref
			pathToFileHoudiniPanel = houdiniPref.panel()
			fileHoudiniPanel = os.path.basename(pathToFileHoudiniPanel)

			inPathHoudiniPanel = fcn.fixOSPath(os.path.join(self.houdiniInstPref,pathToFileHoudiniPanel))

			for prefFolder in self.houdiniInstallPrefFolder:
				outPathHoudiniPanel = fcn.fixOSPath(os.path.join(prefFolder,"python_panels",fileHoudiniPanel))
				if os.path.exists(inPathHoudiniPanel):
					result = houdiniPref.editCommand(inPathHoudiniPanel,outPathHoudiniPanel,fileHoudiniPanel,self.fileDir)
					if result:
						print("Houdini Panel installed for " + os.path.basename(prefFolder))
					else:
						print(fileHoudiniPanel , " doesn't exist !")

		# Maya
		if self.flMainUI.cbMaya_step03.isChecked():
			# Edit Shelf Pref
			pathToFileMayaShelf = mayaPref.shelf()
			fileMayaShelf = os.path.basename(pathToFileMayaShelf)
			
			inPathMayaShelf = fcn.fixOSPath(os.path.join(self.mayaInstPref,pathToFileMayaShelf))
			
			for prefFolder in mayaPref.findMayaVersion(self.mayaInstallPrefFolder):
				outPathMayaShelf = fcn.fixOSPath(os.path.join(prefFolder,"prefs/shelves",fileMayaShelf))

				if os.path.exists(inPathMayaShelf):
					result = mayaPref.editCommand(inPathMayaShelf,outPathMayaShelf,self.fileDir)
					if result:
						print("Maya Shelf installed for " + os.path.basename(prefFolder))
					else:
						print(inPathMayaShelf , " doesn't exist !")

		# Nuke
		if self.flMainUI.cbNuke_step03.isChecked():
			# Edit Init
			fileNukeInit = nukePref.initFile()
			inPathNukeInit = fcn.fixOSPath(os.path.join(self.nukeInstPref,fileNukeInit))
			
			outPathNukeInit = fcn.fixOSPath(os.path.join(self.nukeInstallPrefFolder,fileNukeInit))

			if not os.path.exists(outPathNukeInit):
				result = nukePref.editCommand(inPathNukeInit,outPathNukeInit,fileNukeInit,self.fileDir)
				if result:
					print("Nuke Init File installed in " + os.path.basename(self.nukeInstallPrefFolder))
				else:
					print(inPathNukeInit , " doesn't exist !")
			else:
				result = nukePref.appendCommand(inPathNukeInit,outPathNukeInit,fileNukeInit,self.fileDir)
				if result:
					print("Nuke Init File Extended  " + os.path.basename(self.nukeInstallPrefFolder))
				else:
					print(inPathNukeInit , " Error extending init.py. check that you haven't lost some data")
			
			# Copy Menu.py
			fileNukeMenu = nukePref.menuFile()
			inPathNukeMenu = fcn.fixOSPath(os.path.join(self.nukeInstPref,fileNukeMenu))
			
			outPathNukeMenu = fcn.fixOSPath(os.path.join(self.nukeInstallPrefFolder,fileNukeMenu))

			if not os.path.exists(outPathNukeMenu):
				try:
					copyfile(inPathNukeMenu,outPathNukeMenu)
					result = True
				except:
					result = False
					pass
				if result:
					print("Nuke Menu File copied in " + os.path.basename(self.nukeInstallPrefFolder))
				else:
					print(fileNukeMenu , " doesn't exist !")
			else:
				result = nukePref.appendCommand(inPathNukeMenu,outPathNukeMenu,fileNukeMenu,self.fileDir)
				if result:
					print("Nuke Init File Extended  " + os.path.basename(self.nukeInstallPrefFolder))
				else:
					print(fileNukeMenu , " Error extending init.py. check that you haven't lost some data")
			
		if self.flMainUI.cbKatana_step03.isChecked():
			print("Need to do manual Update")

		self.inst.sendMessage("Shelves and Menu Added per DCC" + "\n" + " Please Restart your software to see the menu ")

	def openFolderSelectionUI(self,button):
		selectedFolder = QtWidgets.QFileDialog.getExistingDirectory(self,"Choose RootFolder for Library",os.getenv("HOME"),QtWidgets.QFileDialog.ShowDirsOnly)
		#selectedFolder.setFixedSize(1000,600)
		if selectedFolder != "":
			if button == self.flMainUI.pb_sgDefaultRoot:
				self.flMainUI.le_sgDefaultRoot.setText(str(selectedFolder)+"/")
			elif button == self.flMainUI.pb_sgFL_ZipFolders:
				self.flMainUI.le_sgFL_ZipFolders.setText(str(selectedFolder)+"/")
		else:
			print("Top")

	def createInitialLibraryFolder(self,root,name,system):
		if "path_"+ system in self.dataPathDefaultLibrary["Generalist Library"][0]:
			print("Setting Library: "+ os.path.join(root,name)+"/" )
			self.dataPathDefaultLibrary["Generalist Library"][0]["path_"+ system] = os.path.join(root,name)+"/"

		# Create Library Folder Hierarchy
		self.inst.createNewLibrary(True,root,name)

	def createMegascansZipFolder(self,rootZipFolder,name,system):
		# Create Megascans Folder
		if "megascans_"+ system in self.dataPathDefaultLibrary["Generalist Library"][0]:
			print("Setting Megascans Zip Folder: " + os.path.join(rootZipFolder,name) )
			self.dataPathDefaultLibrary["Generalist Library"][0]["megascans_" + system] = os.path.join(rootZipFolder,name)

		fcn.createNewFolder(os.path.join(rootZipFolder,name))

	def detectDCC(self):
		#### We are gonna look into the user folder to see if there is some preferences
		# Houdini
		self.houdiniInstallPrefFolder = []
		stringHoudiniVersion = ""
		houdiniFolders = houdiniPref.findHoudiniVersion(self.userFolder)
		for houFold in houdiniFolders:
			if os.path.exists(houFold):
				self.flMainUI.cbHoudini_step03.setChecked(True)
				stringHoudiniVersion += fcn.fixOSPath(os.path.basename(houFold)) + ", "
				self.houdiniInstallPrefFolder.append(fcn.fixOSPath(houFold))
		self.flMainUI.labelAvHoudini_step03.setText("(Detected: "+ stringHoudiniVersion +" )")
		# Maya
		if os.path.exists(os.path.join(self.userFolder,"Documents/maya")):
			self.flMainUI.cbMaya_step03.setChecked(True)
			self.mayaInstallPrefFolder = os.path.join(self.userFolder,"Documents/maya")
			mayaVersion = mayaPref.findMayaVersion(self.mayaInstallPrefFolder)
			
			stringMayaVersion = ", ".join([os.path.basename(f) for f in mayaVersion])
			#print("Maya is installed",mayaVersion)
			self.flMainUI.labelAvMaya_step03.setText("(Detected: "+ stringMayaVersion +" )")
		# Nuke
		if os.path.exists(os.path.join(self.userFolder,".nuke")):
			self.flMainUI.cbNuke_step03.setChecked(True)
			self.nukeInstallPrefFolder = os.path.join(self.userFolder,".nuke")
			nukeVersion = nukePref.findNukeVersion(self.nukeInstallPrefFolder)
			stringNukeVersion = ", ".join([os.path.basename(f.split("preferences")[-1].split(".nk")[0]) for f in nukeVersion])
			self.flMainUI.labelAvNuke_step03.setText("(Detected: "+ stringNukeVersion +" )")
		# Katana
		if os.path.exists(os.path.join(self.userFolder,".katana")):
			self.flMainUI.cbKatana_step03.setChecked(True)
			stringKatanaVersion = ""
			self.flMainUI.labelAvKatana_step03.setText("(Detected: "+ stringKatanaVersion +" )")

class mayaPref():
	@staticmethod
	def name():
		return "maya"

	@staticmethod
	def shelf():
		return "prefs/shelves/shelf_Alexandria.mel"

	@staticmethod
	def findMayaVersion(rootPath):
		folders = os.listdir(rootPath)
		rx = re.compile(r'^\d+$')
		mayaVersion = [ fcn.fixOSPath(os.path.join(rootPath,str(folder))) for folder in (int(item) for item in folders if rx.match(item)) if 2000<= folder <=2050]

		return mayaVersion

	@staticmethod
	def editCommand(inFile,outFile,pathScriptLocation):
		with open(inFile, "r") as batData,open(outFile,"w") as batCopy:
			for line in batData:
				if "-image " in line:
					fixedLine = '        -image ' + '"' + pathScriptLocation + '/icons/sg_alexandriaLibrary_icon64.png"' + "\n"
					batCopy.write(fixedLine)
				if "-image1 " in line:
					fixedLine = '        -image1 ' + '"' + pathScriptLocation + '/icons/sg_alexandriaLibrary_icon64.png"' + "\n"
					batCopy.write(fixedLine)
				elif "-command " in line:
					fixedLine = '        -command "import sys\\nsys.path.append(\\"'+ pathScriptLocation +'\\")\\nimport sg_alexandriaLibrary\\nimport imp\\nimp.reload(sg_alexandriaLibrary)\\n\\nsg_alexandriaLibrary.sg_alexandriaLibrary_UI()"'+ "\n" 
					batCopy.write(fixedLine) 
				else:
					batCopy.write(line)
			batData.close()
			batCopy.close()

		return outFile

class nukePref():
	@staticmethod
	def name():
		return "nuke"

	@staticmethod
	def initFile():
		return "init.py"

	@staticmethod
	def menuFile():
		return "menu.py"

	@staticmethod
	def findNukeVersion(rootPath):
		preferences = glob.glob(rootPath+"/preferences*")
		return preferences

	@staticmethod
	def editCommand(inFile,outFile,file,pathScriptLocation):
		if file == "init.py":
			with open(inFile, "r") as batData,open(outFile,"w") as batCopy:
				for line in batData:
					if "nuke.pluginAddPath(" in line:
						fixedLine = 'nuke.pluginAddPath(' + '"' + pathScriptLocation + '")' + "\n"
						batCopy.write(fixedLine)
					else:
						batCopy.write(line)
				batData.close()
				batCopy.close()
		elif file == "menu.py":
			with open(inFile, "r") as batData,open(outFile,"w") as batCopy:
				for line in batData:
					batCopy.write(line)
				batData.close()
				batCopy.close()

		return outFile

	@staticmethod
	def appendCommand(inFile,outFile,file,pathScriptLocation):
		if file == "init.py":
			with open(inFile) as prefInput:
				fileInput = prefInput.readlines()
			with open(outFile,"a+") as prefOutput:
				for line in fileInput:
					if "nuke.pluginAddPath(" in line:
						fixedLine = 'nuke.pluginAddPath(' + '"' + pathScriptLocation + '")' + "\n"
						prefOutput.write(fixedLine)
					else:	
						prefOutput.write(line)
						prefOutput.flush()
			prefInput.close()
			prefOutput.close()
		elif file == "menu.py":
			with open(inFile) as prefInput:
				fileInput = prefInput.readlines()
			with open(outFile,"a+") as prefOutput:
				for line in fileInput:
					prefOutput.write(line)
					prefOutput.flush()
			prefInput.close()
			prefOutput.close()
		return outFile

class houdiniPref():
	@staticmethod
	def name():
		return "houdini"

	@staticmethod
	def shelf():
		return "toolbar/alexandria.shelf"

	@staticmethod
	def panel():
		return "python_panels/alexandria.pypanel"

	@staticmethod
	def findHoudiniVersion(rootPath):
		houdiniVersion= glob.glob(fcn.fixOSPath(os.path.join(rootPath,"Documents/houdini"))+"*")
		return houdiniVersion

	@staticmethod
	def editCommand(inFile,outFile,file,pathScriptLocation):
		if file == os.path.basename(houdiniPref.shelf()):
			with open(inFile, "r") as batData,open(outFile,"w") as batCopy:
				for line in batData:
					if '  <tool name="Alexandria" label="Library" icon=' in line:
						fixedLine = '  <tool name="Alexandria" label="Library" icon=' + '"' + pathScriptLocation + '/icons/sg_alexandriaLibrary_icon64.png">' + "\n"
						batCopy.write(fixedLine)
					elif 'sys.path.append("' in line:
						fixedLine = 'sys.path.append("' + pathScriptLocation + '")' + "\n"
						batCopy.write(fixedLine)
					else:
						batCopy.write(line)
				batData.close()
				batCopy.close()
		elif file == os.path.basename(houdiniPref.panel()):
			with open(inFile, "r") as batData,open(outFile,"w") as batCopy:
				for line in batData:
					if '  <interface name="Library" label="Alexandria Library" icon=' in line:
						fixedLine = '  <interface name="Library" label="Alexandria Library" icon=' + '"' + pathScriptLocation + '/icons/sg_alexandriaLibrary_icon64.png" showNetworkNavigationBar="false" help_url="">' + "\n"
						batCopy.write(fixedLine)
					elif 'sys.path.append("' in line:
						fixedLine = 'sys.path.append("' + pathScriptLocation + '")' + "\n"
						batCopy.write(fixedLine)
					else:
						batCopy.write(line)
				batData.close()
				batCopy.close()

		return outFile

def launchFirstLaunch_UI():
	for entry in QtWidgets.QApplication.allWidgets():
		if type(entry).__name__ == 'alexandriaFirstLaunch':
			entry.close()
			entry.deleteLater()
		elif type(entry).__name__ == 'alexandriaFirstLaunch':
			entry.close()
			entry.deleteLater()

	if in_maya or in_hou or in_nuke:
		win = alexandriaFirstLaunch()
		win.show()
	# else:
	# 	app = QtWidgets.QApplication(sys.argv)

	# 	win = alexandriaFirstLaunch()
	# 	win.show()

	# 	app.exec()
	# 	sys.exit()