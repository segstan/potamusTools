import os
import sys
import json
import zipfile
import re
import glob
import time

pythonVersion = (sys.version_info[0])
if pythonVersion == 3:
	import imp

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
#########################################################################################################################
fileDir = os.path.dirname(os.path.abspath(__file__))
pathDetectSoftware = os.path.abspath(os.path.join(fileDir, '../sg_findSoftware/'))
if pathDetectSoftware:
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

##########################################################################################################################

if in_hou:
	import hou

if in_katana:
	from PyQt5 import QtWidgets,QtGui, QtCore, QtWidgets , uic 
	from PyQt5.QtGui import QMovie
else:
	from PySide2 import QtGui, QtCore, QtWidgets , QtUiTools
	from PySide2.QtUiTools import QUiLoader
	from PySide2.QtCore import QFile, QObject
	from PySide2.QtCore import QEvent
	from PySide2.QtGui import QMovie

class sgConvertToBook(QtWidgets.QDialog):
	def __init__(self, parent= QtWidgets.QApplication.activeWindow(),title='Convert Images to Book', label='Convert_Images_to_Book',softwareInUse = detectSoftware()):
		super(sgConvertToBook,self).__init__(parent)

		self.fileDir = os.path.dirname(os.path.abspath(__file__))
		file_convertToBookUI = os.path.abspath(self.fileDir+ "/ui/ui_sgConvertToBook.ui")
		self.stylesheetUnreal = os.path.abspath(self.fileDir+ "/ui/unreal_qtStyle.ssh")

		if softwareInUse != "Katana":
			self.loaderP = QUiLoader()
			self.convertToBookWidget = self.loaderP.load(file_convertToBookUI,self)
		else:
			self.convertToBookWidget = uic.loadUi(file_convertToBookUI,self)
			
		self.convertToBookWidget.setWindowTitle("Convert Images to Book v0.8")
		
		#self.setFixedSize(850,325)
		self.setFixedSize(850,375)
		if in_hou:
			self.setFixedSize(895,375)
			stylesheet = hou.qt.styleSheet()
			self.setStyleSheet(stylesheet)

		if softwareInUse == "Unreal":
			with open(self.stylesheetUnreal,"r") as unrealStyleSheet:
				self.setStyleSheet(unrealStyleSheet.read())
			self.convertToBookWidget.setStyle(QtWidgets.QStyleFactory.create("Fusion"))

		# Legacy from library
		self.thumbnailSuffix = "_Preview."
		self.dataNewATB={}

		self.convertToBookWidget.pushButton_sgToolsConvertDirectory.clicked.connect(self.updateDialog)
		self.convertToBookWidget.pb_convertimages.clicked.connect(lambda:self.createBook(self.dataNewATB))
		


	def createPDF(self,path,outputPath):
		# Take some a folder with images (jpg) and create a pdf
		#
		if pilLoaded == True:
			## UI
			progressBarValue = 0
			self.resetProgressBar("Converting Images to PDF... ")

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
				# Update UI
				progressBarValue = 30.0
				self.convertToBookWidget.progressBar.setValue(progressBarValue)
				self.convertToBookWidget.progressBar.setFormat("Converting Images to PDF... "+'%p%')
				try:
					imagesForPDF[0].save(pdfOutput,"PDF",resolution = 100.0,save_all =True,append_images = imagesForPDF[1:])
				except:
					print("Can't combine images for pdf")
					print(sys.exc_info())
					return ""
				# Update UI
				progressBarValue = 100.0
				self.convertToBookWidget.progressBar.setValue(progressBarValue)
				self.convertToBookWidget.progressBar.setFormat("Conversion Done... "+'%p%')
			else:
				self.sendMessage("No images in folder to create pdf")
				pdfOutput = ""
		else:
			print("PIL python library is not loaded, cannot create a pdf")
			pdfOutput = ""

		self.progressBarFinish(2.0)
		return pdfOutput

	def createCBZ(self,path,outputPath):
		## UI
		progressBarValue = 0
		self.resetProgressBar("")

		 # Only read jpg and jpeg
		images=[]
		listExt = ["*.jpg","*.jpeg"]

		# Will convert jp2 format if it is there
		# Otherwise use jpeg
		jp2 = glob.glob(path + "*.jp2")
		if jp2:
			## UI
			progressBarValue = 0
			self.resetProgressBar("Converting Images to Jpg... ")
			progr = 100.0/len(jp2)

			tmpFolder = os.path.join(path,"tmpJPG")
			self.createNewFolder(tmpFolder)
			for img in jp2:
				outImage= os.path.join(tmpFolder,os.path.basename(img).split(".")[0]+".jpg")
				images.append(self.convertToJPG(img,outImage))
				# Update UI
				progressBarValue += int(progr)
				self.convertToBookWidget.progressBar.setValue(progressBarValue)
			# Update UI
			progressBarValue = 100.0
			self.convertToBookWidget.progressBar.setValue(progressBarValue)
			self.convertToBookWidget.progressBar.setFormat("Conversion Done... "+'%p%')
		else:
			for ext in listExt:
				images.extend(glob.glob(path + ext))

		images = self.naturalSorting(images)
		cbzOutput = outputPath
		
		if images:
			## UI
			progressBarValue = 0
			self.resetProgressBar("Converting To Zip... ")
			progr = 100.0/len(images)

			z = zipfile.ZipFile(cbzOutput,'w')
			for img in images:
				z.write(img)
				# Update UI
				progressBarValue += int(progr)
				self.convertToBookWidget.progressBar.setValue(progressBarValue)
			z.close()
			# Update UI
			progressBarValue = 100.0
			self.convertToBookWidget.progressBar.setValue(progressBarValue)
			self.convertToBookWidget.progressBar.setFormat("Conversion Finished... "+'%p%')
		else:
			cbzOutput = ""
			# Update UI
			progressBarValue = 100.0
			self.convertToBookWidget.progressBar.setValue(progressBarValue)
			self.convertToBookWidget.progressBar.setFormat("Process Finished... "+'%p%')

		self.progressBarFinish(2.0)
		return cbzOutput

	def createNewFolder(self,newpath):
		if not os.path.exists(newpath):
			os.umask(0)
			folderCreated = os.makedirs(newpath,0o777)
		else:
			folderCreated = "Already Exist"
		return folderCreated

	def convertToJPG(self,image,output):
		if pilLoaded == True:
			img = pilimage.open(image)
			rgbIm = img.convert('RGB')
			rgbIm.save(output)
			return output
		else:
			return ""

	def naturalSorting(self,l):
		convert = lambda text: int(text) if text.isdigit() else text.lower()
		alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
		return sorted(l, key=alphanum_key)

	def selectFolderDialog(self):
		dialogFolder = QtWidgets.QFileDialog(self,"Pick Folder with Images")
		dialogFolder.setFileMode(QtWidgets.QFileDialog.Directory)
		dialogFolder.setOption(QtWidgets.QFileDialog.DontUseNativeDialog,True)
		dialogFolder.setOption(QtWidgets.QFileDialog.ShowDirsOnly,False)
		dialogFolder.exec_()

		selected_Folder = dialogFolder.selectedFiles()[0]
		if dialogFolder.result() == True:
			return selected_Folder
		else:
			return None

	def updateDialog(self):
		# Open Dialog box
		selectedFolder = self.selectFolderDialog()
		if selectedFolder != None:
			# UI
			self.convertToBookWidget.lineEdit_sgToolsConvertToPDF.setText(str(selectedFolder)+"/")
			files = self.findImginFolder(selectedFolder)
		else:
			self.convertToBookWidget.lineEdit_sgToolsConvertToPDF.setText("")

	def findImginFolder(self,folder):
		preview = glob.glob(folder+"/*_Preview.*")
		textUI = ""
		tutorialFolder = ""
		self.dataNewATB={}

		artBookImages = [img for img in glob.glob(folder+"/*.jp*") if self.thumbnailSuffix not in os.path.basename(img)]

		# Check if needed to create a pdf
		if artBookImages:
			textUI += "Found: "+ str(len(artBookImages)) + " Image(s) compatible to convert as PDF or as CBZ, "
			# Show UI
			self.convertToBookWidget.groupBox_ToolsConvertToPDF.setEnabled(True)
			suggestedName = self.suggestBookName(folder,artBookImages[0])
			self.setBookNameUI(suggestedName)
		else:
			# Hide UI
			self.convertToBookWidget.groupBox_ToolsConvertToPDF.setEnabled(False)

		self.convertToBookWidget.label_sgFoundInFolder.setText(textUI)

		# Fill Dictionary with Info
		self.dataNewATB={
			'previewImage':"",
			'artBookImages':artBookImages,
		}
		#print(json.dumps(self.dataNewATB,indent = 4))

	def resetProgressBar(self,text):
		self.convertToBookWidget.message.setText("")
		progressBarValue = 0
		self.convertToBookWidget.progressBar.setValue(progressBarValue)
		self.convertToBookWidget.progressBar.setTextVisible(True)
		self.convertToBookWidget.progressBar.setFormat(text+'%p%')
		self.convertToBookWidget.progressBar.setAlignment(QtCore.Qt.AlignCenter)

	def progressBarFinish(self,timeSleep):
		time.sleep(timeSleep)
		self.convertToBookWidget.progressBar.setTextVisible(False)
		self.convertToBookWidget.progressBar.setFormat(""+'%p%')
		self.convertToBookWidget.progressBar.setValue(0)


	def createBook(self,dictNewATB):
		# Folder is the root folder -  Needs to add the atb source folder for copy of file 
		#
		listATBCopied = []

		## Copy Images 
		if dictNewATB['artBookImages']:
			if len(dictNewATB['artBookImages']) > 1:
				folder = os.path.dirname(dictNewATB['artBookImages'][0])
				nameBook = self.getBookName()
				# Take in account the UI
				if self.convertToBookWidget.radioButton_sgToolsConvertCBZ.isChecked() == True and self.convertToBookWidget.groupBox_ToolsConvertToPDF.isEnabled() == True:
					nameNewCBZ = os.path.join(folder,nameBook+".cbz")
					nameNewCBZ.replace('\\',os.sep)
					# Create CBZ
					outCBZ = self.createCBZ(os.path.dirname(dictNewATB['artBookImages'][0])+"/",nameNewCBZ)
					# Copy
					if outCBZ:
						listATBCopied.append(outCBZ)
						# UI
						self.convertToBookWidget.message.setText(nameNewCBZ)
					else:
						userMessage = "CBZ Not Created, please check the error log"
						self.convertToBookWidget.message.setText(userMessage)

				elif self.convertToBookWidget.radioButton_sgToolsConvertPDF.isChecked() == True and self.convertToBookWidget.groupBox_ToolsConvertToPDF.isEnabled() == True:
					nameNewPDF = os.path.join(folder,nameBook+".pdf")
					nameNewPDF.replace("\\",os.sep)
					# Create PDF
					outPDF = self.createPDF(os.path.dirname(dictNewATB['artBookImages'][0])+"/",nameNewPDF)
					# Copy
					if outPDF:
						listATBCopied.append(outPDF)
						self.convertToBookWidget.message.setText(nameNewPDF)
					else:
						userMessage = "PDF Not Created, please check the error log"
						self.convertToBookWidget.message.setText(userMessage)

		return listATBCopied

	def getBookName(self):
		bookName = self.convertToBookWidget.lineEdit_sgBookRename.text()
		# need to Check if name is legit 

		return bookName

	def suggestBookName(self,folder,file):
		#nameFile = os.path.basename(file).split(".")[0]
		nameFile = folder.split("/")[-1]

		return nameFile

	def setBookNameUI(self,text):
		self.convertToBookWidget.lineEdit_sgBookRename.setPlaceholderText(text)
		self.convertToBookWidget.lineEdit_sgBookRename.setText(text)


def sg_convertToBook_UI():
	print(" =================================================================== ")
	print( "Class Name: " + str(__name__))
	windowTitle = "Convert Images to Book v0.8"

	## Delete all previous instances
	for entry in QtWidgets.QApplication.allWidgets():
		if type(entry).__name__ == 'sgConvertToBook':
			entry.close()
			entry.deleteLater()
		elif type(entry).__name__ == 'sgConvertToBook':
			entry.close()
			entry.deleteLater()
	
	ui = sgConvertToBook()
	ui.show()