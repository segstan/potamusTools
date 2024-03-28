import os
import sys
import platform
import re
import json
import glob
import uuid
import subprocess

try:
	import openpype.lib.vendor_bin_utils
	OPLoaded= True
except:
	OPLoaded= False
	pass
################################################## Default Add Library #########################################

def dictionaryMenu(jsonMenuAction,listSupportedSoftware,listDefaultFolders):
	dataMenu = {}
	dataCategory = {}
	dataAction = {
				"module":"",
				"variables" : ""
			}
	dataActionImport = {
				"module":"extractingZip",
				"variables" : ""
			}
	dataActionView = {
				"module":"openExplorer",
				"variables" : ""
			}
	dataActionSelectZip = {
				"module":"openSelectFileInExplorer",
				"variables" : ""
			}
	dataActionCopyPath = {
				"module":"copyPath",
				"variables" : ""
			}
	dataActionAddCollection = {
				"module":"addToCollection",
				"variables" : ""
			}
	dataActionEditInfos = {
				"module":"launchEditInfosMenu",
				"variables" : ""
			}
	dataActionContactSheet = {
				"module":"createContactSheet",
				"variables" : ""
			}
	dataActionDelete = {
				"module":"deleteItemLibrary",
				"variables" : ""
			}		
			
	for software in listSupportedSoftware :
		for category in sorted(listDefaultFolders):
			dataCategory[category] = {
			'actionImport00_txt' : "Import for Renderman",
			'actionImport00_action' : dataActionImport,
			'actionImport00_vis' : True,
			'actionImport00_enabled' : True,
			'actionImport01_txt': "Import for Arnold",
			'actionImport01_action' :dataActionImport,
			'actionImport01_vis' : True,
			'actionImport01_enabled' : True,
			'actionImport02_txt' :"Import for Maya Default",
			'actionImport02_action' :dataActionImport,
			'actionImport02_vis' : True,
			'actionImport02_enabled' : True,
			'actionUnzip_txt' :"Unzip File",
			'actionUnzip_action' :dataActionImport,
			'actionUnzip_vis' : True,
			'actionUnzip_enabled' :False,
			'actionSelectZip_txt' :"View Zip",
			'actionSelectZip_action' :dataActionSelectZip,
			'actionSelectZip_vis' : True,
			'actionSelectZip_enabled' :False,
			'actionView_txt' :"View in Explorer",
			'actionView_action' :dataActionView,
			'actionView_vis' : True,
			'actionView_enabled' : True,
			'actionCopy_txt' :"Copy Path",
			'actionCopy_action' :dataActionCopyPath,
			'actionCopy_vis' : True,
			'actionCopy_enabled' : True,
			'actionAddToCollection_txt' : "Add to Collection",
			'actionAddToCollection_action' :dataActionAddCollection,
			'actionAddToCollection_vis' : True,
			'actionAddToCollection_enabled' : True,
			'actionEditInfos_txt' : "Edit Infos",
			'actionEditInfos_action' :dataActionEditInfos,
			'actionEditInfos_vis' : True,
			'actionEditInfos_enabled' : True,
			'actionGenerateContactSheet_txt' :"View Contact Sheet",
			'actionGenerateContactSheet_action' :dataActionContactSheet,
			'actionGenerateContactSheet_vis' : True,
			'actionGenerateContactSheet_enabled' : False,
			'actionDelete_txt' :"Delete",
			'actionDelete_action' :dataActionDelete,
			'actionDelete_vis' : True,
			'actionDelete_enabled' : True,
			}
		dataMenu[software] = dataCategory

	print(json.dumps(dataMenu,indent= 4)) 
	writeJsonFile(jsonMenuAction,dataMenu)
	print("- Regenerated menu action -")

def addNewPathLibrary(defaultPathJson,dataPathDefaultLibraries,nameNewLibrary,pathNewLibrary,megascanLibraryPath):
	'Take the jsonFile with all the different library, the dictionary output '
	'Name of the new library, the path of the new library and the megascanPath library'
	'Output a dictionary'
	with open(defaultPathJson) as jfile:
		dataPathDefaultLibraries = json.load(jfile)

	dataPathDefaultLibraries[nameNewLibrary] = [{
	'path_Windows':pathNewLibrary,
	'path_Linux':pathNewLibrary,
	'megascans_Windows':megascanLibraryPath,
	'megascans_Linux':megascanLibraryPath,
	}]
	with open(defaultPathJson,'w') as jfile:
		json.dump(dataPathDefaultLibraries,jfile,indent = 4)
	
	return dataPathDefaultLibraries

def deletePathLibrary(defaultPathJson,nameLibrary):
	with open(defaultPathJson) as jfile:
		dataPathDefaultLibraries = json.load(jfile)

	del dataPathDefaultLibraries[nameLibrary]

	with open(defaultPathJson,'w') as jfile:
		json.dump(dataPathDefaultLibraries,jfile,indent = 4)

##################################################### Write Json #######################################################

def readJsonfile(jsonFile):
	if os.path.exists(jsonFile):
		with open(jsonFile) as jfile:
			try:
				data = json.load(jfile)
			except:
				data = {}
				print("ERROR: ",jfile)
				pass
	else:
		data = {}
	return data

def writeJsonFile(outFile,dictionary):
	with open(outFile,'w') as outJson:
		json.dump(dictionary,outJson,indent = 4)

###################################################### Matrix Utils ####################################################

# Rotate Matrix by +180 deg
def reverseMatrix(matrixA):
	# for Matrix 4x4
	for i in range(4):
		j = 0
		k = 4-1
		while j<k:
			t = matrixA[j:i]
			matrixA[j][i] = matrixA[k][i]
			matrixA[k][i] = t
			j += 1
			k -= 1
	return matrixA

# Transpose of Matrix 4x4
def transpose(matrixA):
	for i in range(4):
		for j in range(i,4):
			t = matrixA[i:j]
			matrixA[i][j] = matrixA[j][i]
			matrixA[j][i] = t
	return matrixA

# Function to rotate by -180 deg Matrix 4x4
def rotateMatrix180(matrixA):
	matrixA = transpose(matrixA)
	matrixA = reverseMatrix(matrixA)
	matrixA = transpose(matrixA)
	matrixA = reverseMatrix(matrixA)
	return matrixA

########################################################			####################################################

def naturalSorting(l):
	convert = lambda text: int(text) if text.isdigit() else text.lower()
	alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
	return sorted(l, key=alphanum_key)

###################################################### Thumbnail ######################################################

def ffmpegThumbnail(inFile,outFile,wRes,hRes):
	#TODO Desaturate of 15%
	# Module for hdr and exr thumbnails
	mainDirectory = os.path.dirname(os.path.abspath(__file__))
	mainDirectory= mainDirectory.replace(os.sep,"/")

	if platform.system() == "Windows":
		ffmpeg = os.path.join(mainDirectory ,"bin/windows/ffmpeg.exe")
	elif platform.system() == "Linux":
		if OPLoaded == True:
			ffmpeg_dir = openpype.lib.vendor_bin_utils.get_vendor_bin_path("ffmpeg")
			ffmpeg = os.path.join(ffmpeg_dir ,"ffmpeg")
		else:
			ffmpeg = ""
	else:
		ffmpeg = ""
		print(platform.system(), "not supported yet")

	if subprocess.run('"%s" -y -i "%s" -vf scale="%s":"%s",tonemap=reinhard:param=0.9:desat=0:peak=2,eq=saturation=0.65 "%s"' %(ffmpeg,inFile,wRes,hRes,outFile)).returncode == 0:
		print ("FFmpeg converted Thumbnail Successfully")
		return outFile
	else:
		print ("There was an error running FFmpeg for Thumbnail")
		return None

###################################################### New Library ######################################################

def createLogFiles(path,nameLogFile):
	f = open(os.path.join(path,nameLogFile),"x")
	f = open(os.path.join(path,nameLogFile),"w")
	f.write("Log for Library: ")
	f.close()

	return os.path.join(path,nameLogFile)

def createLoggingFile(path,nameIni,logPath):
	f = open(os.path.join(path,nameIni),"x")
	f = open(os.path.join(path,nameIni),"w")
	lines01 = ["[loggers]\n","keys=root\n","\n","[handlers]\n","keys=fileHandler\n","\n","[formatters]\n","keys=simpleFormatter\n","\n","[logger_root]\n","level=DEBUG\n","handlers=fileHandler\n","\n"]
	lines02 = ["[handler_fileHandler]\n","class=FileHandler\n","level=DEBUG\n","formatter=simpleFormatter\n","args=(" + "\""+ logPath + "\""+ ",)\n","\n","[formatter_simpleFormatter]\n","format=%(asctime)s %(name)s - %(levelname)s:%(message)s\n"]
	f.writelines(lines01)
	f.writelines(lines02)
	f.close()

def createSuperUserFile(path,nameSupUserFile,user):
	f = open(os.path.join(path,nameSupUserFile),"x")
	f = open(os.path.join(path,nameSupUserFile),"w")
	f.write("{\n    \"superUsers\": [\n")
	f.write("        \""+user+"\"\n")
	f.write("    ]\n}")
	f.close()

def createTagsFile(path,nameTagsFile):
	f = open(os.path.join(path,nameTagsFile),"x")
	f = open(os.path.join(path,nameTagsFile),"w")
	f.write("[\n]")
	f.close()

def dictionaryNewLibrary():
	dataNewLibrary = {}
	dataNewLibrary["new"]={
	'ArtBooks':'ArtBooks',
	'Collections':"Collections",
	'IES':"IES",
	'DMP':"DMP",
	'Lightrigs': {
		'arnold':"arnold",
		'renderman':"renderman"
	},
	'Megascans':"Megascans",
	'Models':{
		'previs':"previs",
		'prod':"prod"
	},
	'Shaders':{
		'arnold':"arnold",
		'renderman':"renderman",
		'unreal':"unreal",
		'vray':"vray"
	},
	'Textures':"Textures",
	'Tutorials':'Tutorials',
	'VDB':"VDB"
	}

	return dataNewLibrary

def createNewFolder(newpath):
	if not os.path.exists(newpath):
		os.umask(0)
		folderCreated = os.makedirs(newpath,0o777)
	else:
		folderCreated = "Already Exist"
	return folderCreated

########################################################################################################################

def fixOSPath(path):
	path = path.replace(os.sep,"/")
	return path

########################################################################################################################
####################################################### Database #######################################################
########################################################################################################################

def buildDatabase(jsonInfoFile,databaseJson,dicAllDatabase,databaseAssetsJson,dicAssetDatabase,dicMegascansZip,libraryPath,artbooksLibraryPath,collectionLibraryPath,iesLibraryPath,modelLibraryPath,lightrigLibraryPath,metaHumanLibraryPath,dmpLibraryPath,textureLibraryPath,shaderLibraryPath,vdbLibraryPath):
	listIcons = []
	exclude = [".mayaSwatches","Megascans"]
	print(" ---- Rebuilding Database ---- ")
	if os.path.exists(databaseJson):
		databaseAssets = readJsonfile(databaseJson)

	## Refresh asset database
	dicAssetDatabase = {}
	print(" Processing ArtBooks ")
	for dirpath, subdirs, files in os.walk(artbooksLibraryPath) :
		[subdirs.remove(d) for d in list(subdirs) if d in exclude]
		for x in files:
			buildDictDatabase(libraryPath,x,dirpath,"ArtBooks",dicAssetDatabase,jsonInfoFile)
	print(" Processing Collections ")
	for dirpath, subdirs, files in os.walk(collectionLibraryPath) :
		[subdirs.remove(d) for d in list(subdirs) if d in exclude]
		for x in files:
			buildDictDatabase(libraryPath,x,dirpath,"Collections",dicAssetDatabase,jsonInfoFile)
	print(" Processing DMP ")
	for dirpath, subdirs, files in os.walk(dmpLibraryPath) :
		[subdirs.remove(d) for d in list(subdirs) if d in exclude]
		for x in files:
			buildDictDatabase(libraryPath,x,dirpath,"DMP",dicAssetDatabase,jsonInfoFile)
	print(" Processing IES ")
	for dirpath, subdirs, files in os.walk(iesLibraryPath) :
		[subdirs.remove(d) for d in list(subdirs) if d in exclude]
		for x in files:
				buildDictDatabase(libraryPath,x,dirpath,"IES",dicAssetDatabase,jsonInfoFile)
	print(" Processing Models ")
	for dirpath, subdirs, files in os.walk(modelLibraryPath) :
		[subdirs.remove(d) for d in list(subdirs) if d in exclude]
		for x in files:
				buildDictDatabase(libraryPath,x,dirpath,"Models",dicAssetDatabase,jsonInfoFile)
	print(" Processing Lightrigs ")
	for dirpath, subdirs, files in os.walk(lightrigLibraryPath) :
		[subdirs.remove(d) for d in list(subdirs) if d in exclude]
		for x in files:
				buildDictDatabase(libraryPath,x,dirpath,"Lightrigs",dicAssetDatabase,jsonInfoFile)
	print(" Processing MetaHumans ")
	for dirpath, subdirs, files in os.walk(metaHumanLibraryPath) :
		[subdirs.remove(d) for d in list(subdirs) if d in exclude]
		for x in files:
				buildDictDatabase(libraryPath,x,dirpath,"MetaHumans",dicAssetDatabase,jsonInfoFile)
	print(" Processing Textures ")
	for dirpath, subdirs, files in os.walk(textureLibraryPath) :
		[subdirs.remove(d) for d in list(subdirs) if d in exclude]
		for x in files:
				buildDictDatabase(libraryPath,x,dirpath,"Textures",dicAssetDatabase,jsonInfoFile)
	print(" Processing Shaders ")
	for dirpath, subdirs, files in os.walk(shaderLibraryPath) :
		[subdirs.remove(d) for d in list(subdirs) if d in exclude]
		for x in files:
			buildDictDatabase(libraryPath,x,dirpath,"Shaders",dicAssetDatabase,jsonInfoFile)
	print(" Processing VDB ")
	for dirpath, subdirs, files in os.walk(vdbLibraryPath) :
		[subdirs.remove(d) for d in list(subdirs) if d in exclude]
		for x in files:
			buildDictDatabase(libraryPath,x,dirpath,"VDB",dicAssetDatabase,jsonInfoFile)

	print(" ---- Database Updated ---- ")
	
	dicAllDatabase = mergeDictionaries(dicAssetDatabase,dicMegascansZip)

	## Save that as a jsonfile
	writeJsonFile(databaseAssetsJson,dicAssetDatabase)
	writeJsonFile(databaseJson,dicAllDatabase)

	return (dicAllDatabase,dicAssetDatabase)

def buildDictDatabase(libraryPath,x,dirpath,typeAsset,dicAssetDatabase,jsonInfoFile):
	listIcons = []
	exclude=["Thumbs.db",jsonInfoFile,"_Preview"]
	if "Preview" in x:
		path= os.path.abspath(os.path.join(dirpath, x))
		newPath = path.replace(os.sep, '/')
		modifiedTime = os.path.getmtime(path)
		listIcons.append(newPath)
		## Need to parse folder and find the _Preview
		#icon = os.path.basename(newPath) 
		iconList = [ f for f in glob.glob(os.path.dirname(newPath)+"/*_Preview.*")]
		icon = iconList[0].replace("\\","/")
		icon = icon.split("/")[-1]
	   
		uuid = icon.split("----")[0]
		iconName = icon.split("----")[-1]
		zipFile= ""
		
		name = newPath.split("/")[-2]
		jsonFiles = name + jsonInfoFile
		if os.path.isfile(dirpath+"/"+jsonFiles):
			jsonFiles = name + jsonInfoFile
		else:
			jsonFiles = ""
		
		listTmpFiles = glob.glob(dirpath+"/*")
		listFiles = []
		i = 0
		for file in listTmpFiles:
			if os.path.isfile(file):
				if not file.endswith(".db") :
					if not "_Preview" in file:
						if not file.endswith (".tex"):
							if not file.endswith (jsonInfoFile):
								if not file.endswith (".zip"):
									listFiles.append(os.path.basename(file))
								else:
									zipFile = file
		# Build Data depending of depth of graph # TODO Simplify that
		if  typeAsset== "Textures" or typeAsset== "VDB" or typeAsset== "DMP" or typeAsset== "IES" or typeAsset== "ArtBooks":
			subType = newPath.split("/")[-4] + "/" + newPath.split("/")[-3]
			category = newPath.split("/")[-3]
			refPath = typeAsset+ "/" + category 
		elif typeAsset== "Models" or typeAsset== "Shaders" or typeAsset== "Lightrigs":
			subType = newPath.split("/")[-4] + "/" + newPath.split("/")[-3]
			category = newPath.split("/")[-3]
			refPath =  typeAsset + "/" + subType
		elif typeAsset== "MetaHumans":
			subType = ""
			category = newPath.split("/")[-2]
			refPath =  typeAsset + "/" + category
		elif typeAsset== "Collections":
			subType = ""
			category = ""
			refPath =  typeAsset + "/"
		else:
			print(typeAsset)
		
		tags =[]

		if jsonFiles != "":
			if os.path.exists(libraryPath + refPath +"/" + name + "/" + jsonFiles):
				assetInfo = readJsonfile(libraryPath + refPath +"/" + name + "/" + jsonFiles)
				if assetInfo and "tags" in assetInfo["releaseInfos"][0]:
					tags = assetInfo["releaseInfos"][0]["tags"]
				else:
					print(libraryPath + refPath +"/" + jsonFiles,assetInfo)
					print("Could not get File")
			else:
				tags = ""

		dicAssetDatabase[icon]= []
		dicAssetDatabase[icon].append({
		'name':name,
		'icon':iconName,
		'uuid':uuid,
		'zipFile':zipFile,
		'timeEntry':modifiedTime,
		'refPath':refPath,
		'json':jsonFiles,
		'lods':[],
		'extension':[],
		'extraFiles' : [],
		'tags':tags,
		"files":[],
		'textures': [],
		'type': typeAsset,
		'subType': subType,
		'category': category
		})

def mergeDictionaries(x,y):
	# if pythonVersion == 2:
	z= x.copy()
	z.update(y)

	# elif pythonVersion == 3:
		# z = {**x,**y}

	return z

def rebuildMegascansLibrary(libraryPath,jsonMegascans):
	print(" ---- Rebuilding Megascans Database ---- ")
	megascansDic = readJsonfile(jsonMegascans)
	fixDic = {}
	tagsStr= ""
	for key in megascansDic:
		name = megascansDic[key][0]["name"]
		icon = megascansDic[key][0]["icon"]
		timeEntry = megascansDic[key][0]["timeEntry"]
		extensionFiles = megascansDic[key][0]["extension"]
		extraFiles = megascansDic[key][0]["extraFiles"]
		textureFiles = megascansDic[key][0]["textures"]
		resolution = megascansDic[key][0]["resolution"]
		zipFile = megascansDic[key][0]["zipFile"]
		refPath = megascansDic[key][0]["refPath"]
		jsonFiles = megascansDic[key][0]["json"]
		lods = megascansDic[key][0]["lods"]
		listFiles = megascansDic[key][0]["files"]
		typeAsset = megascansDic[key][0]["type"]
		subType = megascansDic[key][0]["subType"]
		category = megascansDic[key][0]["category"]
		tags = []
		if jsonFiles != "":
			assetInfo = readJsonfile(libraryPath + refPath + "/" + jsonFiles)
			if assetInfo:
				try:
					tagsStr = ",".join(assetInfo['tags'])
				except:
					pass
				try:
					tagsStr += ",".join(assetInfo['semanticTags']['contains'])
					tagsStr += ",".join(assetInfo['semanticTags']['descriptive'])
					tagsStr += ",".join(assetInfo['semanticTags']['theme'])
				except:
					print(libraryPath + refPath +"/" + jsonFiles)
					print(name,sys.exc_info())
					pass
			else:
				print("The json file is empty: " + libraryPath + refPath + "/" + jsonFiles)
			tags = tagsStr.split(",")
		
		fixDic[icon]= []
		fixDic[icon].append({
		'name':name,
		'icon':icon,
		'zipFile':zipFile,
		'timeEntry':timeEntry,
		'refPath':refPath,
		'resolution':resolution,
		'json':jsonFiles,
		'lods':lods,
		'extension':extensionFiles,
		'extraFiles' :extraFiles,
		'textures': textureFiles,
		'tags':tags,
		'files':listFiles,
		'type': typeAsset,
		'subType': subType,
		'category': category
		})

	## Save that as a jsonfile
	writeJsonFile(jsonMegascans,fixDic)

	print(" ---- Megascans Database Updated ---- ")

def cleanUpDatabase(dicMegascansZip):
	print("---- Cleaning Megascans Database ----")
	listKeyDelete = []
	for key in dicMegascansZip:
		# print(key,self.dicMegascansZip.pop(key,None))
		zipFile = dicMegascansZip[key][0]["zipFile"]
		nameKey = dicMegascansZip[key][0]["name"]
		if os.path.exists(zipFile):
				print("Entry: " + nameKey + " exist")
		else:
				listKeyDelete.append(key)
				print("To Delete: " + nameKey + " in database" )
	print("Megascans Database Checked")
	for obj in listKeyDelete:
		delete = dicMegascansZip.pop(key,None)
		if delete != None:
				print("Deleted: " + obj.split(".")[0] + " in database" )
		else:
				print( "Key is not in dictionnary: " + obj.split(".")[0])
	print("---- Megascans Database Cleaned ----")

def saveGlobalDatabase(dicAllDatabase,databaseJson,dicAssetDatabase,dicMegascansZip):
	## Merge again to be sure then save
	print("---- Global Database Saved ----")
	dicAllDatabase = mergeDictionaries(dicAssetDatabase,dicMegascansZip)

	## Save that as a jsonfile
	writeJsonFile(databaseJson,dicAllDatabase)
	return dicAllDatabase

def saveAssetDatabase(databaseAssetsJson,dicAssetDatabase):
	## Save that as a jsonfile
	writeJsonFile(databaseAssetsJson,dicAssetDatabase)
	
def generateUUID():
	separator = "----"
	return str(uuid.uuid1())+separator

#######################################################################################################################

def checkNameValidity(stringToTest,invalidType):
	if invalidType == "Folder":
		forInvalidChar = re.compile(r'[^0-9a-zA-Z_-]+')
	elif invalidType == "ListFolders":
		forInvalidChar = re.compile(r'[^0-9a-zA-Z_ ,-]+')
	listInvalidCharacters = forInvalidChar.findall(stringToTest)
	if listInvalidCharacters:
		return False
	else:
		return True

#######################################################################################################################

def createDictJsonEntryInfos(name,listExtensionAvailable,listTextures,notes,version,tags,ocio,timeEntry,meta):
	## available is kept for 
	if os.getenv("USER"):
		user = os.getenv("USER")
	else:
		user = os.environ.get("USERNAME")
	data = {}
	data["releaseInfos"]= []
	data["releaseInfos"].append({
	'author': user,
	'timeEntry':timeEntry,
	'lock': False,
	'version':version,
	'ocio':ocio,
	'name':name,
	'extension': listExtensionAvailable,
	'textures' :listTextures,
	'tags':tags,
	"available":[],
	'meta': meta,
	'note':notes
	})

	return data

#######################################################################################################################

def addEntryToAssetDatabase(dicAssetDatabase,databaseAssetsJson,libraryPath,nameAsset,icon,iconName,uuid,jsonFile,fullPath,typeAsset,timeEntry,extension,extraFiles,textures,tags,listFiles):
	## needs the fullpath (with the asset name ex: "E:/Projects/library/Textures/asphalt/road01/") of the assset that needs to be saved
	## all the database as dictionary, and all the relevant data to be saved
	print("\n")
	print("---- Adding Element to Asset Database: ----")
	print(" Full Path: " + fullPath)
	
	refPathTmp = fullPath.split(libraryPath)[-1].split("/")
	subTypeTmp = fullPath.split(typeAsset)[-1].split("/")
	if refPathTmp[-1] == "":
		refPath = '/'.join(refPathTmp[:-2])
		subType = '/'.join(subTypeTmp[:-2])
	else:
		refPath = '/'.join(refPathTmp[:-1])
		subType = '/'.join(subTypeTmp[:-1])

	#category = fullPath.split(typeAsset)[-1].split("/")[-1]
	category = os.path.dirname(fullPath).split(typeAsset)[-1]
	#print(category)

	if category == "":
		category = fullPath.split(typeAsset)[-1].split("/")[-3]
	else:
		lengthSplit = len(category.split("/"))-1
		category = category.split("/")[-lengthSplit]

	print("Name Asset: " + nameAsset, "\n" + "Name Icon: " + icon, "\n" +"UUID: " + uuid ,"\n" +"Name JsonFile: " + jsonFile, "\n" +"Path: " + fullPath," - RefPath: " + refPath," - Category: " + category,"\n" +"Type Asset: " + typeAsset," - Subtype: " + subType  )
	
	dicAssetDatabase[icon]= []
	dicAssetDatabase[icon].append({
	'name':nameAsset,
	'icon':iconName,
	'uuid':uuid,
	'zipFile': "",
	'timeEntry': timeEntry,
	'refPath':refPath,
	'resolution': "",
	'json':jsonFile,
	'lods':[],
	'extension': extension,
	'extraFiles':extraFiles,
	'textures':textures,
	'tags':tags,
	"files":listFiles,
	'type': typeAsset,
	'subType': subType,
	'category': category
	})

	#dicAllDatabase = mergeDictionaries(dicAssetDatabase,dicMegascansZip)

	print("-- Asset Database Saved --")
	## Save that as a jsonfile
	writeJsonFile(databaseAssetsJson,dicAssetDatabase)
	return dicAssetDatabase

def addEntryToAssetDictionary(nameAsset,icon,iconName,uuid,jsonFile,fullPath,typeAsset,timeEntry,note,tags):
	dicAssetDatabase = {}
	dicAssetDatabase[icon]= []
	dicAssetDatabase[icon].append({
	'name':nameAsset,
	'icon':iconName,
	'uuid':uuid,
	'zipFile': "",
	'timeEntry': timeEntry,
	'refPath':typeAsset+"/",
	'resolution': "",
	'json':jsonFile,
	'lods':[],
	'extension': [],
	'extraFiles':[],
	'textures':[],
	'tags':tags,
	"files":[],
	'type': typeAsset,
	'subType': "",
	'category': ""
	})

	return dicAssetDatabase

def setDefaultLightrigDict(dicLights,dicConnections,dcc,version,idString):
	dicLightRig = {}
	dicLightRig["infos"] = {
	'dcc':dcc,
	'version':version,
	'id':idString,
	}
	dicLightRig['lightHierarchy'] = dicLights
	dicLightRig['connectionsHierarchy'] = dicConnections
	return dicLightRig

def addEntryAttributesDic(attributesDict,attribute,valueAttr,typeAttr):
	attributesDict[attribute] = {
	'value': valueAttr,
	'type': typeAttr,
	}
	return attributesDict

def addEntryConnectionDic(dicConnectionInfos,input,connection):
	dicConnectionInfos[input] = {
	'link': connection,
	}
	return dicConnectionInfos

def addEntryLgtRigDic(dictLights,name,parentObj,shapes,shapeType,nodeTpe,shapeAttributesDict,dictConnections,expression,matrix,transform,attributesDict):
	# transform is 
	dictLights[parentObj] = {
		"children":{},
		"name":name,
		"nodeType":nodeTpe,
		"shape":shapes,
		"shapeType":shapeType,
		"shapeAttributes": shapeAttributesDict,
		"connectedNodes":dictConnections,
		"expression": expression,
		"matrix":matrix,
		"xForm":transform,
		"attributes": attributesDict,
		}

	return dictLights