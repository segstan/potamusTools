import json
import os


def writeCollection(pathToCollection,listIcons,dictionary,collectionName):
	dataCollection = {}
	collectionJson = pathToCollection+collectionName+"/"+collectionName+"_Collection.json"
	if os.path.exists(collectionJson):
		with open(collectionJson) as jfile:
			dataCollection = json.load(jfile)

	for item in listIcons:
		# Get Dictionary
		dataObject = dictionary[item][0]
		# Append dictionary from json
		dataCollection[item]= []
		dataCollection[item].append(dataObject)

	## Save Dict in Json File
	writeJson(dataCollection,collectionJson)

	return dataCollection


def removeFromCollection(pathToCollection,listIcons,collectionName):
	collectionJson = pathToCollection+collectionName+"/"+collectionName+"_Collection.json"
	print(collectionJson)
	if os.path.exists(collectionJson):
		with open(collectionJson) as jfile:
			dataCollection = json.load(jfile)

		print(dataCollection)
		for item in listIcons:
			dataCollection.pop(item)

		## Save Dict in Json File
		writeJson(dataCollection,collectionJson)

		return True
	else:
		return False

def writeJson(dictionary,jsonOutput):
	with open(jsonOutput,'w') as outJson:
		json.dump(dictionary,outJson,indent = 4)