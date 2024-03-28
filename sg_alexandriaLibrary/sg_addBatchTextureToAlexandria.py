
import sys
import os
import collections
import re
import time
import uuid

from PySide2 import QtGui,QtCore
import json

import logging
import logging.config

import sg_functions as fcn

import threading

# Linux Solution
try:
	import OpenImageIO as oiio
	# from OpenImageIO import ImageBuf
	ImageBufLoaded = True
except:
	ImageBufLoaded = False
	pass

# Open Pipe Linux Solution
try:
	import openpype.lib.vendor_bin_utils
	oiiotoolWork = True
except:
	oiiotoolWork = False
	pass

from shutil import copyfile
from shutil import copytree

def logger(logPath):
	logging.basicConfig(filename='batchTextureEntry.log', encoding='utf-8', level=logging.DEBUG, format='%(asctime)s %(name)s %(levelname)s:%(message)s')
	logging.config.fileConfig(logPath, disable_existing_loggers=False)
	global logger
	try:
		username = os.getenv("USER")
	except:
		username = os.getenv("USERNAME")
	logger = logging.getLogger(username + "  " + "addBatchTexture")

def mainAddBatchTexture(pathToAddFrom,pathLibraryCategory,category,user,thumbRes,ocio,notes,tags,displayMessage):
	try:
		logger.info('---------------- Started Process for Adding Textures to Library ----------------')
	except:
		print('---------------- Started Process for Adding Textures to Library ----------------')
		pass
	data = organiseDataInFolder(pathToAddFrom)
	t1= threading.Thread(target=createEntry, args=(pathLibraryCategory,user,thumbRes,ocio,notes,tags,category,data,displayMessage))
	t1.start()
	t1.join()
	try:
		logger.info('---------------- Finished Adding Batch Textures to Library ----------------')
	except:
		print('---------------- Finished Adding Batch Textures to Library ----------------')
		pass

	return data

def mainUniqueAddBatchTexture(pathToAddFrom,pathLibraryCategory,category,user,thumbRes,ocio,notes,tags,displayMessage):
	try:
		logger.info('---------------- Started Process for Adding Unique Texture to Library ----------------')
	except:
		print('---------------- Started Process for Adding Textures to Library ----------------')
		pass
	data = organiseUniqueDataInFolder(pathToAddFrom)
	t1= threading.Thread(target=createEntry, args=(pathLibraryCategory,user,thumbRes,ocio,notes,tags,category,data,displayMessage))
	t1.start()

	t1.join()
	try:
		logger.info('---------------- Finished Adding Unique Textures to Library ----------------')
	except:
		print('---------------- Finished Adding Unique Textures to Library ----------------')
		pass
	return data

def generateUUID():
	return str(uuid.uuid1())+"----"

def organiseDataInFolder(path):
	listImagesExtention = ["jpg","tif","exr","png","tga","hdr"]
	listFiles = []
	listFileExtension = []
	data = {}
	
	files = [pf for pf in os.listdir(path) if pf.split(".")[-1] in listImagesExtention]
	files.sort()

	delta = 0
	previousCommon = ""
	previousDelta = 0
	i = len(listFiles)

	if files:
		for f in files:
			listFiles.append(f)
			# Find Common Prefix
			common = os.path.commonprefix(listFiles)
			if previousCommon != common:
				result = re.search(common,previousCommon)
				if result != None:
					delta = result.span()[1] - result.span()[0]
					# If common prefix change more than 3 characters
					if delta + 3 < previousDelta :
						if i != 0:
							# Remove last file from list
							listFiles.remove(f)
							# Store Data
							data = generateDictionaryTexture(data,previousCommon,path,listFiles,listFileExtension)
							# Reboot
							listFiles = []
							listFiles.append(f)
							common = os.path.commonprefix(listFiles)
							previousDelta = 0
							i = 0
						
				elif result == None:
					delta = 0
					if i != 0:
						# Remove last file from list
						listFiles.remove(f)
						# Store Data
						data = generateDictionaryTexture(data,previousCommon,path,listFiles,listFileExtension)
						# Reboot
						listFiles = []
						listFiles.append(f)
						common = os.path.commonprefix(listFiles)
						previousDelta = 0
						i = 0

			i += 1
			previousCommon = common
			previousDelta = delta

	#print(json.dumps(data,indent = 4))
	try:
		logger.info("  ")
		logger.info(" ---- Data Treatment Finished ---- ")
	except:
		print("\n")
		print(" ---- Data Treatment Finished ---- ")
		pass
	return data

def organiseDataInFolder02(path):
	#listImagesExtention = [".jpg",".tif",".exr",".png",".tga",".hdr"]
	listImagesExtention = ["jpg","tif","exr","png","tga","hdr"]
	listFiles = []
	listFileExtension = []
	prefixListTmp=[]
	data = {}
	lengthPrefix=0
	savedFile = ""

	for root,dirs,files in os.walk(path):
		print(root,dirs)
		if files:
			for file in files:
				uuid = generateUUID()
				fileExtension = file.lower().split(".")[-1]
				
				if any(extension in fileExtension for extension in listImagesExtention):
					if listFiles:
						if lengthPrefix >= findCommonPrefLength(listFiles[-1],file):
							lengthPrefix = findCommonPrefLength(listFiles[-1],file)
					else:
						lengthPrefix= len(file)

					## Change of Pattern
					if lengthPrefix > 2:
						listFiles.append(file)
						savedLengthPrefix = lengthPrefix
						savedFile = file
						savedRoot = root
					else:
						newEntry= savedFile[:savedLengthPrefix]
						if newEntry[-1] == "_":
							name = savedFile[:savedLengthPrefix-1]
						else:
							name = savedFile[:savedLengthPrefix]

						if fileExtension not in listFileExtension:
							listFileExtension.append(fileExtension)
						data = storeDictionnaryTextures(data,name,name,savedRoot,listFiles,listFileExtension,uuid)

						## Empty the list because it's a new pattern
						listFiles =[]

	## Finally Add Last Entry
	if savedFile:
		uuid = generateUUID()
		newEntry= savedFile[:savedLengthPrefix]
		if newEntry[-1] == "_":
			name = savedFile[:savedLengthPrefix-1]
		else:
			name = savedFile[:savedLengthPrefix]

		data = storeDictionnaryTextures(data,name,name,root,listFiles,listFileExtension,uuid)
		
	#print(json.dumps(data,indent = 4))
	try:
		logger.info("  ")
		logger.info(" ---- Data Treatment Finished ---- ")
	except:
		print("\n")
		print(" ---- Data Treatment Finished ---- ")
		pass
	return data

def organiseUniqueDataInFolder(path):
	listImagesExtention = ["jpg","tif","exr","png","tga","hdr"]
	listFiles = []
	listFileExtension = []
	prefixListTmp=[]
	data = {}

	for root,dirs,files in os.walk(path):
		for file in files:
			fileExtension = file.lower().split(".")[-1]
			if any(extention in fileExtension for extention in listImagesExtention):
				uuid = generateUUID()
				listFiles.append(file)
				name = file.split(".")[0]
				if fileExtension not in listFileExtension:
					listFileExtension.append(fileExtension)
				data = storeDictionnaryTextures(data,name,name,root,listFiles,listFileExtension,uuid)
				# yield data
				## Empty the list because it's a new entry
				listFiles =[]
	try:
		logger.info("  ")
		logger.info(" ---- Data Treatment Finished ---- ")
	except:
		print("\n")
		print(" ---- Data Treatment Finished ---- ")
		pass

	return data

def generateDictionaryTexture(data,prefix,path,listFiles,listFileExtension):
	### Store Data
	uuid = generateUUID()
	# Fix if last characters is _
	nameEntry = prefix
	if nameEntry[-1] == "_":
		nameEntry = nameEntry[:-1]
	if "." in nameEntry:
		nameEntry.replace(".","_")
	# Add to Dictionary
	data = storeDictionnaryTextures(data,nameEntry,nameEntry,path,listFiles,listFileExtension,uuid)

	return data


def storeDictionnaryTextures(dictionary,newEntry,name,path,listTextures,listFileExtension,uuid):
	dictionary[newEntry]= []
	dictionary[newEntry].append({
	'path': path,
	'list textures':listTextures,
	'name':name,
	'extension':listFileExtension,
	'uuid':uuid,
	})
	try:
		logger.info("New Texture Entry Found: %s", newEntry)
		logger.debug("Folder: %s",path)
		logger.debug("Textures: %s",listTextures)
	except:
		print("New Texture Entry Found: "+ newEntry)
		print("Folder: " + path)
		print("Textures: " + str(listTextures))
		pass

	return dictionary

def findCommonPrefLength(x,w):
	prefixLength = 0
	for i in range(0,len(x)):
		if x[i] == w[i]:
			prefixLength += 1
		else:
			break
	return prefixLength

def makeFolder(newPath):
	folderCreated = os.makedirs(newPath,0o777)
	return folderCreated

def createEntry(libraryPath,user,thumbRes,ocio,notes,tags,category,dictionary,displayMessage):
	####### Step 1 - Copy the file ########
	listExtension =[]
	listTextures = []
	for key in dictionary:
		newEntryInfos = dictionary[key]
		for element in newEntryInfos:
			nameNewEntry = element['name']
			pathOrg = element['path']
			listTextures = element['list textures']
			uuid = element['uuid']
			folderDestination = os.path.abspath(os.path.join(libraryPath,category,nameNewEntry))
			#folderImagesDestination = os.path.abspath(os.path.join(libraryPath,category,nameNewEntry))
			folderImagesDestination = os.path.abspath(os.path.join(libraryPath,category,nameNewEntry,"sourceimages"))
			folderCategory = os.path.abspath(os.path.join(libraryPath,category))

			if not os.path.exists(folderImagesDestination):
				folder = makeFolder(folderImagesDestination)
				# print("Folder Created: " + folder)

			while not os.path.exists(folderDestination):
				time.sleep(1)

			colImage = None

			for texture in listTextures:
				fileO = os.path.abspath(os.path.join(pathOrg,texture))
				fileD = os.path.abspath(os.path.join(folderImagesDestination,texture))

				if fileD !=None:
					if fileD.split(".")[-1].lower() not in listExtension:
						listExtension.append(fileD.split(".")[-1])
					if "albedo" in texture.lower() or "diff" in texture.lower() or "col" in texture.lower():
						colImage = fileD
					try:
						copyfile(fileO,fileD)
					except:
						print("File Not Copied from: " + fileO + " to " + fileD)
						print(sys.exc_info())
						pass
					try:
						logger.info("File Copied: %s", texture)
					except:
						print("File Copied: " + fileO + " to " + fileD)
						pass
		# Infos User
		nameNewEntry = key
		try:
			logger.info("New Entry Created Successfully: %s", key)
		except:
			print(" -- New Entry Created Successfully: " + key + " -- ")
			pass
		
		####### Step 2 - Add the Thumbnail ########
		# Works on Linux 
		size = thumbRes
		if colImage == None:
			colImage = fileD

		#### Resize
		img = QtGui.QPixmap(colImage)
		previewImage = folderDestination + "/"+ uuid +nameNewEntry+"_Preview."+"png"
		
		### Test for a 16 bits image 
		if img:
			imgResized = img.scaled(int(size[0]),int(size[1]),QtCore.Qt.KeepAspectRatio)	
			imgResized.save(previewImage,"PNG")
			try:
				logger.info("Preview Image Saved: %s",previewImage)
			except:
				print("Preview Image Saved: "+ previewImage)
				pass
		else:
			try:
				logger.warning("Preview Image Not Created: %s", colImage)
			except:
				("Preview Image Not Created Yet: " + colImage + " .Depth is superior to 8 bits, trying a different method")
				pass
			## 16 bits (HDR,EXR) thumbnail on linux
			if ImageBufLoaded == True:
				# It does a fancy clamp on the image 
				img =  oiio.ImageBuf(colImage)
				spec= img.spec()
				colorspace = oiio.ImageBufAlgo.colorconvert(img,img,"Linear","sRGB")
				imgResized = oiio.ImageBuf(oiio.ImageSpec(int(size[0]),int(size[1]),spec.nchannels,oiio.FLOAT))
				oiio.ImageBufAlgo.resize(imgResized,img)
				imgResized.write(previewImage)
			# OpenPype Solution
			elif oiiotoolWork == True:
				oiiotoolDir = openpype.lib.vendor_bin_utils.get_vendor_bin_path("oiio")
				oiiotoolApp = os.path.join(oiiotoolDir ,"bin/oiiotool")
				returnImage = os.popen('%s %s -resize %sx%s --colorconvert linear sRGB -o %s' % (oiiotoolApp,colImage,size[0],size[1],previewImage))
			else:
				## 16 bits (HDR,EXR) thumbnail on linux/windows
				returnImage = fcn.ffmpegThumbnail(colImage,previewImage,size[0],size[1])
				print("Preview Image Saved: "+ previewImage)
				# if FFMpeg failed for the thumbnail then use default thumbnail
				if returnImage ==  None:
					## Will use default thumbnail to let the user know it could not generated a thumbnail
					defaultDir = os.path.dirname(os.path.abspath(__file__))
					defaultThumb = os.path.abspath(defaultDir + "/icons/defaultThumbnail.png")
					copyfile(defaultThumb, previewImage)
					try:
						logger.warning(" - No Preview Image Created for: %s", colImage)
					except:
						print(" - No Preview Image Created for:" + colImage)
						pass

		####### Step 3 - Add json file ########
		if colImage.split(".")[-1].lower() not in listExtension:
			listExtension.append(colImage.split(".")[-1])
			
		if notes == "":
			notes = "automatic process"
		
		time = os.path.getmtime(folderDestination)
		version = "1"
		jsonFileInfo = nameNewEntry+"_infos.json"
		pathJsonFileInfo = os.path.join(folderDestination,jsonFileInfo)
		writeJsonInfos(pathJsonFileInfo,listExtension,user,time,ocio,notes,listTextures,version,tags,nameNewEntry)
		try:
			logger.info("Json File Saved: %s", nameNewEntry+"_infos.json")
		except:
			print("Json File Saved: " + nameNewEntry +"_infos.json") 
			pass

		####### Step 4 - Add to database ########
			
	try:
		logger.info(' ---------------- Finished Adding Textures to Library ---------------- ')
	except:
		print(' ---------------- Finished Adding Textures to Library ---------------- ')
		print("\n")
		pass

	return (pathJsonFileInfo,listExtension,user,time,notes,version,tags,nameNewEntry,uuid)

def writeJsonInfos(path,listExtension,user,time,ocio,notes,listFiles,version,tags,nameNewEntry):
	# TODO Add textures list
	data = {}
	data["releaseInfos"]= []
	data["releaseInfos"].append({
	'author': user,
	'timeEntry':time,
	'lock':False,
	'version':version,
	'ocio':ocio,
	'name':nameNewEntry,
	'extension': listExtension,
	'textures' :listFiles,
	'meta':"",
	'tags':tags,
	'note':notes
	})

	with open(path,'w') as outJson:
		json.dump(data,outJson,indent = 4)

