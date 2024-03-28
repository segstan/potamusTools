import maya.cmds as cmds
import pymel.core as pm
import glob
import sys
from collections import OrderedDict
import json
import sg_alexandriaConstants
import sg_functions as fcn

pythonVersion = (sys.version_info[0])
if pythonVersion == 3:
	import imp
	imp.reload(sg_alexandriaConstants)
	imp.reload(fcn)
if pythonVersion == 2:
	reload(sg_alexandriaConstants)
	reload(fcn)

######################################## Generic #########################################
def getShape(transform):
	shapes = cmds.listRelatives(transform, shapes=True)
	return shapes

def setAttrString(attribute,value):
	cmds.setAttr(attribute,value,type = "string")

def groupGeo(listGeo,name,lod):
	group = cmds.group( listGeo, n=name+ "_" + lod +"_GRP" )
	return group

def isGroup(node):
	try:
		children = cmds.listRelatives(node,children=True)
		for child in children:
			if not cmds.ls(child,transforms=True):
				return False
		return True
	except:
		return False

def createGroup(nameGrp):
	cmds.select(clear= True)
	grp = cmds.group(em = True, n = nameGrp)
	cmds.select(clear= True)
	return grp

def closeHypershade():
	panels = pm.lsUI(panels=True)
	panelsToClose = ["hyperShadePanel1"]
	try:
		for panel in panels:
			panelName = str(panel)
			##print("Found panel: " + panelName)
			for panelToClose in panelsToClose:
				if panelToClose in panelName:
					print("Closing panel: " + panelName)
					pm.deleteUI(panel, panel=True)
	except:
		pass

def renameGeo(group,nameMegascans):
	selection = cmds.ls(group, dag=True,transforms= True)
	for obj in selection:
		if obj != group:
			suffixe = "_" + obj.split("_")[-2] + "_" + obj.split("_")[-1]
			newName = nameMegascans + suffixe
			cmds.rename(obj,newName)

def setTransform(listObjects,scaleSize):
	# Apply Uniform scale on megascans
	for item in listObjects:
		try:
			cmds.scale(float(scaleSize),float(scaleSize),float(scaleSize),item)
		except:
			print(sys.exc_info())
			pass

def selectObjects(toSelect,action):
	if action == "replace":
		cmds.select(toSelect, replace= True)
	elif action == "add":
		cmds.select(toSelect, add= True)
	return True

def getSelection(longName):
	selection = cmds.ls(selection = True,long = longName)
	return selection

def inViewMessage(message):
	cmds.inViewMessage( amg=message, pos='botCenter', fade=True, fadeOutTime=500)

def waitCursor(boolState):
	# True or False
	cmds.waitCursor( state=boolState )

########################################### UI ###########################################
def set_actifViewVis(value, attrs=list):
	## Maya Related command to hide UI
	try:
		actView = cmds.getPanel(wf=True) # actView='modelPanel4'    
		flags = { i : value for i in attrs }
		cmds.modelEditor(actView, e=1, **flags)
	except:
		e = sys.exc_info()
		print(e)
		pass

##########################################################################################

def deleteNamespace(namespaces):
	# For Maya
	fixedName = ""
	for namespace in namespaces:
		## Enter namespace we want to empty
		cmds.namespace (set=":"+namespace)
		# List its content
		contentNamespace= cmds.namespaceInfo (listOnlyDependencyNodes=True)
		## Go back to world
		cmds.namespace( set=':' )
		for node in contentNamespace:
			try:
				## Sometimes the shapes have the same names than the transform
				newName = node.split(namespace+":")[-1]
				fixedName = cmds.rename(node,newName)
			except:
				e = sys.exc_info()
				print(e)
				pass
		try:
			cmds.namespace( removeNamespace = namespace)
		except :
			e = sys.exc_info()
			print(e)
			print("Couldn't remove Namespace " + namespace)
	return fixedName

################################## List Textures on Lights ###############################

def findLightsInHierarchy(topGroup):
	#listAllRendermanLights = cmds.listNodeTypes("light",ex="ai")
	listAllMayaLights = cmds.listNodeTypes("light")
	listAllLights = cmds.ls(type = listAllMayaLights)
	listLGTShapes = []

	for node in listAllLights:
		parentT = None
		stop = False
		while not stop:
			p = cmds.listRelatives(parentT or node, parent = True, f=True)
			if p is None:
				stop = True
			else:
				parentT = p[0]
		if parentT:
			#print('{} has top level parent {}'.format(node,parentT))
			if parentT == topGroup:
				listLGTShapes.append(node)
				print(node + " is part of the hierarchy. Collect textures information on the node")
		#else:
			#print('{} is top level parent {}'.format(node))
	return listLGTShapes

def findTextureFilesOnNodes(listLights):
	# Only look for first level of connections 
	dictMaps = {}
	for lgt in listLights:
		## Mostly for Rman Lights right now
		objectType = cmds.objectType(lgt)
		if objectType in sg_alexandriaConstants.sgDicAllLightTextures:
			attributes = sg_alexandriaConstants.sgDicAllLightTextures[objectType]
			for attribute in attributes:
				## Dodgy in case there are more than one attributes that can receive a map for Rman Lights
				textureMap = cmds.getAttr(lgt + "." + attribute)
				dictMaps[lgt]={
						'type': objectType,
						'textureMap': textureMap,
						'attribute': attribute,
						}
		connections = cmds.listConnections(lgt, type="aiImage" )
		if connections:
			for node in connections:
				textureMap = cmds.getAttr(node + ".filename")
				objectType = cmds.objectType(node)
				dictMaps[node]={
					'type': objectType,
					'textureMap': textureMap,
					'attribute': "filename",
					}
		connections = cmds.listConnections(lgt, type="file" )
		if connections:
			for node in connections:
				textureMap = cmds.getAttr(node + ".fileTextureName")
				objectType = cmds.objectType(node)
				dictMaps[node]={
					'type': objectType,
					'textureMap': textureMap,
					'attribute': "fileTextureName",
					}
	return dictMaps

def listTexturesOnNode(dictMapLights,node):
	objectType = cmds.objectType(node)
	print(sg_alexandriaConstants.sgDicAllLightTextures)
	if objectType in sg_alexandriaConstants.sgDicAllLightTextures:
		attribute = sg_alexandriaConstants.sgDicAllLightTextures[objectType]
		textureMap = cmds.getAttr(light + "." + attribute)
	else:
		attribute = ""
		textureMap = ""

	dicMapsLight[node]={
		'type': objectType,
		'textureMap': textureMap,
		'attribute':attribute,
	}
	
	return dicMapsLight

##########################################################################################
def importModel(modelPath,action,namespaceName):
	model=[]
	if action != "abc":
		model = cmds.file(modelPath, i=True, f=True)
	elif action == "abc":
		# cmds.AbcImport(modelPath,mode="import")
		cmds.file(modelPath, i=True, f=True, namespace= namespaceName)
		model.append(cmds.ls( namespaceName+":*", type ="transform" ))

	return model

def buildMegascanShaderMaya(listTextures,renderer,nameAsset,geo):
	matName = "Mat_"+ renderer +"_"+ nameAsset
	importedMObject = geo
	opacityFlag = False

	## Maya Nodes
	if renderer == "mayaDefault":
		colorConnect = ".color"
		specularConnect = ".specularColor"
		specularRoughnessConnect = ".eccentricity"
		normal = ".normalCamera"
		opacity = ".transparency"
		outColor = ".outColor"
		outColorR = ".outColorR"
		outColorA = ".outAlpha"

		material = cmds.shadingNode("blinn", asShader=True, name=matName)
		cmds.setAttr(material+ ".specularRollOff", 0.1)
		cmds.setAttr(material+ ".specularColor", 0.125,0.125,0.125,type = "double3")
		shadingGroup= cmds.sets(name=nameAsset+"_SG", empty=True, renderable=True, noSurfaceShader=True)
		cmds.connectAttr(material+".outColor", shadingGroup+".surfaceShader", f= True)
		displacement = cmds.shadingNode("displacementShader", asShader=True, name= matName +"_displacement")
		cmds.connectAttr(displacement +".displacement",  shadingGroup+".displacementShader", f= True)

		cmds.binMembership( (shadingGroup,material,displacement), addToBin="bin_" + nameAsset )

		for texture in listTextures:
			cmds.binMembership( texture, addToBin="bin_" + nameAsset )
			if "Albedo" in texture:
				cmds.connectAttr(texture+ outColor, material + colorConnect, f = True)
			if "Specular" in texture:
				cmds.connectAttr(texture + outColor, material + specularConnect, f = True)
				try:
					cmds.setAttr(texture+ ".exposure", 1)
				except:
					pass
			if "Roughness" in texture:
				cmds.connectAttr(texture+ outColorR, material +specularRoughnessConnect,f= True)
			if "Normal" in texture:
				bump = cmds.shadingNode("bump2d", asUtility = True, name= "bump_"+ material)
				cmds.connectAttr(texture + outColorA, bump + ".bumpValue",force = True)
				cmds.connectAttr(bump + ".outNormal", matName + normal, force= True)
				cmds.setAttr(bump + ".bumpInterp", 0)
				cmds.setAttr(bump + ".bumpDepth", 0.1)
			if "Opacity"in texture:
				reverse = cmds.shadingNode("reverse", asTexture=True, name=matName + "_reverse_opacity")
				cmds.connectAttr(texture+ outColor, reverse +".input", f = True)
				cmds.connectAttr(reverse+ ".output", material + opacity,f = True)
			if "Displacement" in texture:
				print("Displacement ignored")
				##cmds.connectAttr(texture+ outColor, displacement +".vectorDisplacement", f= True)
				##cmds.setAttr(displacement + ".aiDisplacementAutoBump", 0)

		cmds.select(clear= True)
		## Graph in the hyperShade or the node Editor
		cmds.hyperShade(downStream = shadingGroup )
		##Assign Shader
		if not importedMObject == None:
			##for listObj in importedMObject:
			for obj in importedMObject:
				# print("Assign a shader to object: " + obj)
				cmds.setAttr(obj+ ".displayColors", False)
				if cmds.objectType( obj, isType="transform" ):
					print("Assigning shader to : " + obj)
					selection = cmds.select(obj, add= True)
					try:
						cmds.hyperShade(assign= material )
					except:
						print("Failed assign shader to: " + obj)
				else:
					print(obj + " is not a transform, can't assign shader")
		else:
			print("WARNING: No object imported to assign a shader to")

def createSharedMayaTexture(sharedUV,triplanar):
	manifold =""
	if triplanar == False and sharedUV == True:
		manifold =  cmds.shadingNode("place2dTexture", asUtility=True)
	elif triplanar == True and sharedUV == True:
		manifold = cmds.shadingNode("place2dTexture", asUtility=True)
	return manifold

def createTextureFileMaya(sharedUV,triplanar,manifold,filename):
	if sharedUV == False and triplanar == False:
		textureFile = cmds.shadingNode('file', asTexture=True)
		texturePlacement = cmds.shadingNode("place2dTexture", asUtility=True)
		cmds.defaultNavigation(connectToExisting=True, source=texturePlacement, destination=textureFile)
		cmds.select(textureFile)
	elif sharedUV == True and triplanar == False :
		textureFile = cmds.shadingNode('file', asTexture=True)
		cmds.defaultNavigation(connectToExisting=True, source= manifold, destination=textureFile)
		cmds.select(textureFile)
	elif sharedUV == False and triplanar == True:
		textureImage = cmds.shadingNode('file', asTexture=True)
		TwodPlacement = cmds.shadingNode("place2dTexture", asUtility=True)
		ThreedPlacement = cmds.shadingNode("place3dTexture", asUtility=True)
		textureFile = cmds.shadingNode("projection", asUtility=True)
		cmds.setAttr( textureFile + ".projType", 6)
		cmds.defaultNavigation(connectToExisting=True, source = TwodPlacement, destination=textureImage)
		cmds.connectAttr( textureFile + ".outColor", texturePlacement+".image", force = True)
		cmds.connectAttr( ThreedPlacement + ".matrix", texturePlacement+".placementMatrix", force = True)
		cmds.select(textureFile)
	elif sharedUV == True and triplanar == True:
		textureImage = cmds.shadingNode('file', asTexture=True)
		textureFile = cmds.shadingNode("projection", asUtility=True)
		ThreedPlacement = cmds.shadingNode("place3dTexture", asUtility=True)
		cmds.setAttr( textureFile + ".projType", 6)
		cmds.connectAttr( textureImage + ".outColor", textureFile+".image", force = True)
		cmds.connectAttr( ThreedPlacement + ".matrix", textureFile+".placementMatrix", force = True)
		cmds.defaultNavigation(connectToExisting=True, source = manifold, destination=textureImage)
		cmds.select(textureFile)

	if triplanar == True:
		# Set FileName
		cmds.setAttr(textureImage+".fileTextureName", filename, type="string")
	else:
		# Set FileName
		cmds.setAttr(textureFile+".fileTextureName", filename, type="string")
		# Set Colorspace

	# Rename Node
	cmds.rename(textureFile, "T_"+ filename.split("/")[-1].split(".")[0])
	textureFile = "T_"+ filename.split("/")[-1].split(".")[0]

	return textureFile

####################################################################################

def traverseGraph(node,children):
	listNodule = []
	listSkip = ["transform","expression","time" ]
	if cmds.objExists(node):
		listNodule =[]
		connections = cmds.listConnections(node,source=True,destination=False,skipConversionNodes=True) or {}
		for child in connections:
			typeID = str(cmds.nodeType(child))
			if typeID not in listSkip:
				children[child]= {}
				listNodule.append(child)
	return listNodule

def getNodes(node,children,listNodeName):
	listNodeName += traverseGraph(node,children)
	for child in children:
		if cmds.objExists(child):
			getNodes(child,children[child],listNodeName)
	return listNodeName

def texturesIntoGraph(initialNode):
	listNodes =[]
	listNodes.append(initialNode)
	listNodule =[]
	children={}
	dictFilePath= {}
	listNodes = getNodes(initialNode,children,listNodes)

	for node in listNodes:
		listFilepath = []
		textureFound = False
		data = {}
		if cmds.objExists(node):
			id = cmds.nodeType(node)
			if id == "PxrTexture" or id == 'aiImage' or id == 'PxrNormalMap':
				attributeFilename = ".filename"
				textureFound = True
			elif id =='PxrMultiTexture':
				attributeFilename = [".filename0",".filename1",".filename2",".filename3",".filename4",".filename5",".filename6",".filename7",".filename8",".filename9"]
				textureFound = True
			elif id == 'file':
				attributeFilename = ".fileTextureName"
				textureFound = True

			if id == "PxrTexture" or id == 'aiImage' or id == 'file' or id == 'PxrNormalMap':
				originalTexturePath = cmds.getAttr(node+attributeFilename)
				if textureFound == True and originalTexturePath != "" :
					data[node+attributeFilename] = {
					'filepath':originalTexturePath
					}
					dictFilePath[node] = data
			elif id == 'PxrMultiTexture':
				for attribute in attributeFilename:
					originalTexturePath = cmds.getAttr(node+attribute)
					if originalTexturePath not in listFilepath:
						listFilepath.append(originalTexturePath)
					if textureFound == True and originalTexturePath != "":
						data[node+attribute] = {
						'filepath':originalTexturePath
						}
						dictFilePath[node] = data

	return dictFilePath

def findShadersOnGeo(listObj):
	# selection = pm.core.ls(selection=True,transforms=True)
	listShaders = []
	attachmentShader={}

	for item in listObj:
		shadingEngine = cmds.listConnections(item,type="shadingEngine")
		if shadingEngine not in listShaders:
			if shadingEngine not in listShaders:
				listShaders.extend(shadingEngine)
			## Find Material Type
			try:
				materialRman = cmds.listConnections(shadingEngine[0]+".rman__surface",source= True, destination = False)
			except:
				materialRman = None
			try:
				materialArnold = cmds.listConnections(shadingEngine[0]+".aiSurfaceShader",source= True, destination = False)
			except:
				materialArnold=None

			if materialRman != None:
				shader =  'renderman'
				geoSettings = findGeoSettings(item,shader)
			elif materialArnold != None:
				shader =  'arnold'
			else:
				shader =  'arnold'
			## Get Geometry Transform Node
			# transform = cmds.listRelatives(item,parent=True,fullPath=True)
			transform = cmds.listRelatives(item,parent=True)
			##Create my dictionnary with infos
			attachmentShader[transform[0]]={
			'shaders':shadingEngine[0],
			'shape':item,
			'type':shader,
			}

	return listShaders,attachmentShader

def findMeshInSelection():
	listMesh = cmds.ls(sl= True, dag= True,s = True)

	return listMesh

def findTexturesInSelection():
	listTexture = cmds.ls(sl= True, tex= True)
	return listTexture

def findGeoSettings(model,renderer):
	dictSettings= {}
	if renderer == "renderman":
		dictSettings[model] = {
		'subdiv'
		}
	return dictSettings

def renameMegascanUVSet(listObjects):
	for item in listObjects:
		try:
			cmds.polyUVSet(item,rename=True, newUVSet='map1')
		except:
			pass

def exportAlembic(pathAlembic,renderer):
	if renderer == "renderman":
		attrList = ["rman_subdivScheme","rman_displacementBound","rman_preventPolyCracks"]
	elif renderer == "arnold":
		attrList = ["aiSubdivType","aiSubdivIterations","aiOpaque","aiSubdivAdaptiveSpace"]
	attrString = ""
	root = " temp"
	for each in attrList:
		attrString += " -attr " + each

	command = "-framerange " + "1" + " " + "1" + attrString + " -uvWrite -worldSpace -sl" + " -file " + pathAlembic

	cmds.AbcExport(j=command)

def assignShaderOnModel(node,geo):
	shadingGroup = None
	if type(node) is list:
		## Find shadingGroup
		for item in node:
			if cmds.objectType(item) == "shadingEngine":
				shadingGroup = item
	else:
		shadingGroup = node

	## Assign to Geometry
	if shadingGroup != None:
		cmds.select(geo, replace= True)
		cmds.select(shadingGroup, add= True)
		try:
			cmds.hyperShade(assign = shadingGroup )
		except:
			"Can't assign shader: " + shadingGroup +" to " + geo

########################################################################################################################
############################################### Import/Export Lightrig ########################################################
########################################################################################################################

def hierarchyDict(parentObj,dictLights,dictConnections):
	## Init Variables
	children = cmds.listRelatives(parentObj, c =True, f= True,type = "transform")
	shapes = cmds.listRelatives(parentObj,shapes = True,fullPath = True) or []
	nodeTpe = cmds.nodeType(parentObj)
	name = parentObj.split("|")[-1]
	if not name:
		name = parentObj
	try:
		matrix = cmds.getAttr(parentObj + ".matrix")
	except:
		matrix = []
		pass

	xForm = cmds.getAttr(parentObj + ".translate")
	xForm += cmds.getAttr(parentObj + ".rotate")
	xForm += cmds.getAttr(parentObj + ".scale")

	expression = ""
	connections = []
	# If there is a shape it is an object to create so grab the shape type
	if shapes:
		nodeTpe = cmds.nodeType(parentObj)
		shapeType = cmds.nodeType(shapes[0])
	# if there is no shape it is a group,a shape or a 'shading' node and so we check
	else:
		shapeType = ""
		if nodeTpe == "transform":
			nodeTpe = "group"
		else:
			print("Unknown node, not stored: ", parentObj,nodeTpe)

	# Attributes Dictionary
	attributesDict ={}
	attributesShapeDict ={}
	dictConnectedNodes = {}
	attributesConnectionDict = {}

	#### Find Connections/Find Attributes
	## on Transform
	dictConnections = buildConnectionsDic(dictConnections,parentObj)
	attributesDict = findAttributesAndConnections(attributesDict,dictConnectedNodes,parentObj)
	# on Shape
	if shapes:
		dictConnections = buildConnectionsDic(dictConnections,shapes[0])
		attributesShapeDict = findAttributesAndConnections(attributesShapeDict,dictConnectedNodes,shapes[0])

	#### Write Hierarchy Dictionary
	if children :
		fcn.addEntryLgtRigDic(dictLights,name,parentObj,shapes,shapeType,nodeTpe,attributesShapeDict,dictConnectedNodes,expression,matrix,xForm,attributesDict)
		for child in children:
			hierarchyDict(child, dictLights[parentObj]["children"],dictConnections)
	else:
		fcn.addEntryLgtRigDic(dictLights,name,parentObj,shapes,shapeType,nodeTpe,attributesShapeDict,dictConnectedNodes,expression,matrix,xForm,attributesDict)

	return dictLights,dictConnections

def buildConnectionsDic(dictConnections,node):
	# Check connections
	connectNodes = cmds.listConnections(node ,source = True, destination = False,connections= False,shapes=True,fnn = True)
	connections = cmds.listConnections(node ,d=False, s=True,connections =True,plugs=True)
	if connections:
		# Connect nodes with long name, only work in 2023, for backward compatibility needs to see what can be done
		if "time1" not in connectNodes:
			connectNodesFilter = []
			for n in connectNodes:
				if n not in connectNodesFilter:
					connectNodesFilter.append(n)
			## Create a tupple with the node (with longname ) to be used as the outConnection as first member. The Key ( node ) is the node to use as in the inConnection
			i = 0
			tuppleData = ()
			dicConnectionInfos = {}
			for cNode in connectNodes:
				tuppleData = (cNode,[connections[i],connections[i+1]])
				dicConnectionInfos = fcn.addEntryConnectionDic(dicConnectionInfos,i,tuppleData)
				tuppleData = ()
				i += 2
			dictConnections[node]= {
				"connections": dicConnectionInfos,
				}
			# Check the node connected and repeat
			for f in connectNodesFilter:
				dictConnections = buildConnectionsDic(dictConnections,f)
	return dictConnections

def findAttributesAndConnections(attributesDict,dictConnectedNodes,node):
	## List all Attributes on shape, update with the attributes of the shape for now/Need to separate that
	attributes = cmds.listAttr(node,c=True,k=True,multi = True)
	attributesP = cmds.listAttr(node,st = "primaryVisibility")
	if attributesP:
		attributes = attributes + attributesP

	rampAttributes = (cmds.listAttr(node, ra = True))
	if attributes:
		attributes.sort()
		for attribute in attributes:
			attributesDict = buildAttributeAndConnectedDictionary(attributesDict,dictConnectedNodes,node,attribute)

	## Will store Ramp separately		
	if rampAttributes:
		for attribute in rampAttributes:
			rampDic = {}
			typeAttr = "Ramp"
			valueAttr = rampDic
			subAttributes = cmds.listAttr(node + "." + attribute,multi = True)
			amountPoints = cmds.getAttr(node +"."+attribute,size = True)
			# Fill a dictionary just for the ramp
			if subAttributes:
				for sub in subAttributes:
					try:
						typeSubAttr = cmds.getAttr(node +"."+ sub,type = True)
						valueSubAttr = cmds.getAttr(node +"."+ sub )
						# Fill Attribute Dictionary
						rampDic[sub] = {
						'value': valueSubAttr,
						'type': typeSubAttr,
						}
					except:
						#print(sys.exc_info())
						pass
			## Fill the classic attributes dictionary
			attributesDict[attribute] = {
			'value': valueAttr,
			'type': typeAttr,
			'points': amountPoints,
			'typeRamp':"",
			'dcc': "maya",
			}

	return attributesDict

def buildAttributeAndConnectedDictionary(attributesDict,dictConnectedNodes,node,attribute ):
	typeAttr = cmds.getAttr( node + "." + attribute,type = True)
	# if is a compoundAttribute it will fail, so bypassing that 
	try:
		valueAttr = cmds.getAttr(node + "." + attribute )
	except:
		valueAttr = ""
		pass

	# Check connections
	connectNode = cmds.listConnections(node + "." + attribute,source = True, destination = False,connections= True,shapes=True,fnn = True)
	connections = cmds.listConnections(node + "." + attribute,d=False, s=True,connections =True,plugs=True)
	
	if connections:
		valueAttr = connections
		typeAttr = "connection"
		## Create a new dictionary with attributes and all that will be saved as the connected nodes key
		dictConnectedNodes = connectionNodeHierarchy(dictConnectedNodes,connectNode[1])
	# Fill Attribute Dictionary
	attributesDict = fcn.addEntryAttributesDic(attributesDict,attribute,valueAttr,typeAttr)

	return attributesDict

def connectionNodeHierarchy(dic,topNode):
	transformName = cmds.listRelatives(topNode,allParents = True)
	if transformName:
		name = transformName[0]
	else:
		name = topNode.split("|")[-1]
	nodeTpe = cmds.nodeType(topNode)
	attributes = cmds.listAttr(topNode,c=True,r=True,se =True,multi = True)
	transform = cmds.listRelatives(topNode, p =True, f= True,type = "transform")
	expression = ""
	matrix = []
	xForm = []
	dictConnections = {}
	attributesDict = {}
	shapeAttributesDict = {}

	if transform: 
		matrix = cmds.getAttr(transform[0] + ".matrix")
		xForm = cmds.getAttr(transform[0] + ".translate")
		xForm += cmds.getAttr(transform[0] + ".rotate")
		xForm += cmds.getAttr(transform[0] + ".scale")
	if nodeTpe == "expression":
		expression = cmds.expression(topNode,q=True,s=True)
		fcn.addEntryLgtRigDic(dic,name,topNode,[],"",nodeTpe,{},{},expression,matrix,xForm,attributesDict)
	else:
		for attribute in attributes:
			#if cmds.attributeQuery(attribute,node = topNode,ex=True) == True:
			typeAttr = cmds.getAttr(topNode+ "."+ attribute,type = True)
			if typeAttr != "message" and typeAttr != "TdataCompound":
				valueAttr = cmds.getAttr(topNode+ "."+ attribute )
			else:
				if type(attribute) != str:
					valueAttr = cmds.getAttr(topNode + "."+ attribute )
				else:
					valueAttr = ""

			# Check connections
			connectNode = cmds.listConnections(topNode + "."+ attribute,source = True, destination = False,connections= True,shapes =True,fnn = True)
			connections = cmds.listConnections(topNode + "."+ attribute,d=False, s=True,connections =True,plugs=True)

			if connections :
				typeAttr = "connection"
				valueAttr = connections

			# Fill Attribute Shading Node Dictionary
			attributesDict = fcn.addEntryAttributesDic(attributesDict,attribute,valueAttr,typeAttr)

			# Write Hierarchy Dictionary
			if connections :
				print("Connection Found:",connectNode,connections)
				fcn.addEntryLgtRigDic(dic,name,topNode,[],"",nodeTpe,shapeAttributesDict,dictConnections,expression,matrix,xForm,attributesDict)
				dictConnections = connectionNodeHierarchy(dic[topNode]["connectedNodes"],connectNode[1])
			else:
				fcn.addEntryLgtRigDic(dic,name,topNode,[],"",nodeTpe,shapeAttributesDict,dictConnections,expression,matrix,xForm,attributesDict)

	return dic

########################################################################################################################

def rebuildHierarchy(namespace,dictLights,dictConnections,dictLightInfos,listNodesCreated):
	### Needs a nested dictionary with lgt and group, etc ....
	###
	dccAtCreation = dictLightInfos["dcc"]
	for key in dictLights:
		obj = key
		nameObj = obj.split("|")[-1]
		shapeToSetAttributes = ""
		objectToSetAttributes = ""
		attributesDictRig = dictLights[obj]["attributes"]
		shapeAttributesDict = dictLights[obj]["shapeAttributes"]
		if "|" in obj:
			paren = obj.rsplit("|",1)[0]
		else:
			paren= ""

		try:
			childrenDict = dictLights[obj]["children"]
		except:
			childrenDict = {}

		# Create Object
		if not cmds.objExists(nameObj):
			if dictLights[obj]["nodeType"] == "group":
				print("-- Create Group: " + obj + " with parent: " + paren + " --")
				# Create Group
				newObj = createGroup(nameObj)
				longNameNewObj = paren + "|" + nameObj
				objectToSetAttributes = newObj
				#
				listNodesCreated.append(newObj)
			elif dictLights[obj]["nodeType"] == "transform":
				shapeName = dictLights[obj]["shape"][0].rsplit("|",1)[-1]
				shapeLongName = dictLights[obj]["shape"]
				lgtType =  dictLights[obj]["shapeType"]
				longNameNewObj = paren+ "|" + nameObj
				# None Maya fix to avoid duplicated name
				if "Shape" not in shapeName:
					shapeName += "Shape"
				if shapeName not in listNodesCreated:
					# If it not a renderman node, create a shadingNode named with the shape name
					if lgtType not in sg_alexandriaConstants.listRendermanLights and lgtType not in sg_alexandriaConstants.listRendermanBlockers:
						newObj = cmds.shadingNode( lgtType , asLight=True, name = shapeName )
					else:
						try:
							newObj = createRmanLight(lgtType)
						except:
							continue
						if newObj != False:
							shapeNewObj = getShape(newObj)[0]
							cmds.rename(shapeNewObj,shapeName )

					# Rename Transform / May cause problem if renderman is not loaded
					cmds.rename(newObj,nameObj )
					newObj = nameObj
					print("-- Create Object: " + lgtType + " with parent: " + paren + " named: "+ newObj +" --")
					# 
					shapeToSetAttributes = paren + "|" + newObj + "|" + shapeName
					objectToSetAttributes = paren + "|" + newObj 
					#
					listNodesCreated.append(newObj)
				else:
					shapeToSetAttributes = paren + "|" + newObj + "|" + shapeName
					objectToSetAttributes = paren + "|" + newObj 
					print("-- Object Already Exist: " + longNameNewObj + " --")
			else :
				# Object is not a transform, so probably a shading node
				newObj = nameObj
				shapeToSetAttributes = paren + "|" + newObj + "|" + shapeName
				objectToSetAttributes = paren + "|" + newObj 

			# Set Matrix
			if newObj:
				# Matrix
				if dccAtCreation != "katana":
					matrix = dictLights[obj]["matrix"]
					setMatrix(newObj,matrix)
				# Cartesian Value
				elif dccAtCreation == "katana":
					setLGTxForm(newObj,dictLights[obj]["xForm"][0],dictLights[obj]["xForm"][1],dictLights[obj]["xForm"][2])
				
				print("Set Transformation on: " + newObj)
				
				if dccAtCreation == "houdini" and dictLights[obj]["shapeType"] == "PxrDomeLight":
					# Difference of -180 deg between maya and houdini for the dome light
					extraRotY = -180
					cmds.setAttr(newObj + ".rotateY",cmds.getAttr(newObj + ".rotateY")+extraRotY)
				cmds.select(clear= True)

			# Parenting
			if paren != "":
				cmds.parent(newObj,paren)

			# Set Attributes on node
			if objectToSetAttributes != "":
				print("Set Attributes on Transform: " + objectToSetAttributes)
				setAttributesForRig(attributesDictRig,dictLightInfos,objectToSetAttributes)
				print("Set Attributes on Shape: " + shapeToSetAttributes)
				setAttributesForRig(shapeAttributesDict,dictLightInfos,shapeToSetAttributes)
				
			# Create Connected Nodes
			connectedNodes = dictLights[obj]["connectedNodes"]
			listNodesCreated = rebuildConnectedNodesHierarchy(connectedNodes,dictLightInfos,listNodesCreated)
			cmds.select(clear= True)

			# Traverse again with
			rebuildHierarchy(namespace,childrenDict,dictConnections,dictLightInfos,listNodesCreated)
	#print("\n")
			
def rebuildConnectedNodesHierarchy(connectedNodes,dictLightInfos,listNodesCreated):
	# Will build all the connected nodes
	#print("Node(s) Created: ", listNodesCreated)
	if connectedNodes :
		for key in connectedNodes:
			nameNewNode = key.split("|")[-1]
			newNode = ""
			nodeToCreate = connectedNodes[key]["nodeType"]
			connectedNewNodes = connectedNodes[key]["connectedNodes"]
			#listConnections = connectedNodes[key]["connections"]
			matrix = connectedNodes[key]["matrix"]
			transform = ""
			# Create New nodes
			if not cmds.objExists(nameNewNode):
				## For now don't separate between renderman node or utility node
				if nodeToCreate not in sg_alexandriaConstants.listRendermanLights and nodeToCreate not in sg_alexandriaConstants.listRendermanBlockers:
					newNode = cmds.shadingNode( nodeToCreate , asUtility=True, name = nameNewNode )
				else:
					try:
						newNode = createRmanLight(nodeToCreate)
					except:
						continue
					# Needs renaming
					if newNode != "" and newNode != False:
						shapeNewObj = getShape(newNode)[0]
						# Rename Shape and transform
						if "Shape" not in nameNewNode:
							cmds.rename(newNode,nameNewNode)
							cmds.rename(shapeNewObj,nameNewNode+"Shape" )
						else:
							cmds.rename(shapeNewObj,nameNewNode )
							cmds.rename(newNode,nameNewNode.split("Shape")[0])
				listNodesCreated.append(nameNewNode)
				print("-- Create Shading Node: " + nameNewNode + " as: " + nodeToCreate + " --")

				transform = cmds.listRelatives(nameNewNode, p =True, f= True,type = "transform")
				if transform:
					parent = "|".join(key.split("|")[:-2])
				else:
					parent = "|".join(key.split("|")[:-1])
				# Parent to group as it is a transform not a node
				if parent:
					cmds.parent(nameNewNode,parent)
					newTransform = parent + transform[0]
				else:
					newTransform= nameNewNode
			else:
				newTransform = nameNewNode
				print( "-- Node Already exist: " + nameNewNode + ", reuse it" )

			if transform:
				setMatrix(newTransform,matrix)

			if nodeToCreate == "expression":
				valueExpression = connectedNodes[key]["expression"]
				cmds.expression(nameNewNode,s= valueExpression,edit = True)
				print("Setting Expression: " , connectedNodes[key]["expression"] , " on  " + nameNewNode)
			else:
				# Set Nodes Attributes
				setAttributesForRig(connectedNodes[key]["attributes"],dictLightInfos,newTransform)
				print("Set Attributes on: " + newTransform)

			if connectedNewNodes:
				rebuildConnectedNodesHierarchy(connectedNewNodes,dictLightInfos,listNodesCreated)
			#if listConnections != "null":
			#	rebuildConnections("test",listConnections)

	return listNodesCreated

def rebuildConnections(dictConnections):
	for key in dictConnections:
		node = key
		dictLink = dictConnections[node]["connections"]
		for key in dictLink:
			nodeIn = node
			nodeOut = dictLink[key]["link"][0]
			linkIn = dictLink[key]["link"][1][0]
			linkOut = dictLink[key]["link"][1][1]

			channelConnectionIn = linkIn.split(".")[-1]
			channelConnectionOut = linkOut.split(".")[-1]

			filteredLinkIn = nodeIn + "." + channelConnectionIn
			filteredLinkOut = nodeOut + "." + channelConnectionOut

			try:
				cmds.connectAttr(filteredLinkOut,filteredLinkIn,force =True)
				#print("  Connection Done: " + filteredLinkOut + " to " + filteredLinkIn )
			except:
				#print(" Could not connect " + filteredLinkOut + " and " + filteredLinkIn )
				#print(sys.exc_info())
				pass

def setMatrix(obj,matrixA):
	if matrixA:
		cmds.xform(obj,matrix = matrixA)

def setLGTxForm(obj,translate,rotate,scale):
	cmds.xform(obj, r=True, t=translate )
	cmds.xform(obj, r=True, ro=rotate )
	cmds.xform(obj, r=True, s=scale )

def setAttributesForRig(attributesDict,dictLightInfos,node):
	listParametersSet = []
	listParametersNotSet = []
	listParametersIgnored = []
	listParametersConverted = []
	dccAtCreation = dictLightInfos["dcc"]
	for key in attributesDict:
		attribute = key
		typeAttr = attributesDict[attribute]["type"]
		# convert Attribute to Maya Name but keep the key value in dictionary as original name to find it back 
		if attribute in sg_alexandriaConstants.sgDicConvertLightNameParameter[dccAtCreation+"-maya"]:
			attribute = sg_alexandriaConstants.sgDicConvertLightNameParameter[dccAtCreation+"-maya"][key]
			listParametersConverted.append(attribute)
		if typeAttr == "Ramp":
			dictRamp = attributesDict[attribute]["value"]
			points = attributesDict[attribute]["points"]
			#print("Ramp Detected - Amount of points to create: " + str(points) + " on ramp: " + attribute )
			setAttributesForRig(dictRamp,dictLightInfos,node)
		else:
			if typeAttr.lower() == "float3" or  typeAttr.lower() == "double3":
				try:
					cmds.setAttr( node + "." + attribute, attributesDict[attribute]["value"][0][0],attributesDict[attribute]["value"][0][1],attributesDict[attribute]["value"][0][2], type = "double3")
					listParametersSet.append(attribute)
				except:
					if attribute not in listParametersNotSet:
						listParametersNotSet.append(attribute)
					#print("Could not set " + str(attributesDict[attribute]["value"]) + " for " + attribute +" as " + typeAttr + " on " + node)
					#print(sys.exc_info())
					pass
			if typeAttr.lower() == "float2" :
				try:
					cmds.setAttr( node + "." + attribute, attributesDict[attribute]["value"][0][0],attributesDict[attribute]["value"][0][1], type = typeAttr.lower())
					listParametersSet.append(attribute)
				except:
					if attribute not in listParametersNotSet:
						listParametersNotSet.append(attribute)
					#print("Could not set " + str(attributesDict[attribute]["value"]) + " for " + attribute +" as " + typeAttr + " on " + node)
					#print(sys.exc_info())
					pass
			elif typeAttr.lower() == "string" or typeAttr.lower() == "Int32Array" or typeAttr.lower() == "matrix":
				try:
					cmds.setAttr( node + "." + attribute, attributesDict[attribute]["value"], type = typeAttr.lower())
					listParametersSet.append(attribute)
				except:
					if attribute not in listParametersNotSet:
						listParametersNotSet.append(attribute)
					#print("Could not set " + str(attributesDict[attribute]["value"]) + " for " + attribute +" as " + typeAttr + " on " + node)
					#print(sys.exc_info())
					pass
			elif typeAttr == "TdataCompound":
				listParametersIgnored.append(attribute)
				#print("- " + attribute + " IGNORED " )
			else:
				try:
					cmds.setAttr( node + "." + attribute, attributesDict[attribute]["value"])
					listParametersSet.append(attribute)
				except:
					if attribute not in listParametersNotSet:
						listParametersNotSet.append(attribute)
					#print("Could not set " + str(attributesDict[attribute]["value"]) + " for " + attribute +" as " + typeAttr + " on " + node)
					#print(sys.exc_info())
					pass
				
	#print("  Parameters Set on "+ node + ": " + "\n" + '\n'.join("- " + str(p) for p in sorted(listParametersSet)))
	#print("  Parameters Not Set on "+ node + ": " + "\n" + '\n'.join("- " + str(p) for p in sorted(listParametersNotSet)))
	
########################################################################################################################
################################################# Import LightRig ######################################################
########################################################################################################################

def createLight(objType,names,attrDico):
	# type of the node to create, names (list) and attribute dictionary
	#
	#
	#
	if objType != "expression":
		#rfm2.api.nodes.create_and_select(objType)
		#lgt = cmds.ls(selection = True,long = True)[0]
		lgt = cmds.shadingNode(objType, asLight=True, name = names[1])
	elif objType == "expression":
		lgt = cmds.shadingNode(objType, asUtility=True, name = names[0] )

	matrix = []
	shapes = cmds.listRelatives(lgt,shapes =True,f =True)
	if shapes:
		for key in attrDico:
			print("Setting component: " , key , " on  " + shapes[0])
			if key == "attributes":
				for key in attrDico["attributes"]:
					setAttributesOnLight(key,shapes[0],attrDico)
			elif key == "matrix":
				matrix = attrDico[key]
			else:
				setAttributesOnLight(key,shapes[0],attrDico)

	elif objType == "expression":
		print("Setting Expression: " , attrDico["expression"] , " on  " + attrDico["parent"])
		valueExpression = attrDico["expression"]
		cmds.expression(attrDico["parent"],s= valueExpression,edit = True)

	# Now working on transform node
	newName = cmds.rename(lgt,names[0])
	print("**** Renaming occured, potential error and dictionary update required ****")

	if matrix:
		print( "- Transform Matrix Applied -")
		cmds.xform(newName,matrix = matrix)

	return newName
	
def createRmanLight(lgtType):
	## Check would have been done previously
	import rfm2 
	rfm2.api.nodes.create_and_select(lgtType)
	newLgt = cmds.ls(selection = True)[0]

	return newLgt

def setParentMatrix(obj,matrixP):
	if matrixP:
		cmds.xform(obj,matrix = matrixP)

def setAttributesOnLight(attribute,node,attrDico):
	if cmds.attributeQuery(attribute,node = node,ex=True) == True:
		typeAttr = cmds.getAttr(node + "." + attribute,type = True)
		if typeAttr == "float3":
			try:
				cmds.setAttr( node + "." + attribute, attrDico["attributes"][attribute]["value"][0][0],attrDico["attributes"][attribute]["value"][0][1],attrDico["attributes"]["value"][attribute][0][2], type = 'double3')
				# print(attribute + " set to " + str(attrDico["attributes"][attribute]) + " as " + typeAttr)
			except:
				print("Could not set " + str(attrDico["attributes"][attribute]["value"]) + " for " + attribute +" as " + typeAttr + " on " + node)
				# print(sys.exc_info())
				pass
		elif typeAttr == "string":
			try:
				cmds.setAttr( node + "." + attribute, attrDico["attributes"][attribute]["value"], type = typeAttr)
				# print(attribute + " set to " + str(attrDico["attributes"][attribute]["value"]) + " as " + typeAttr)
			except:
				print("Could not set " + str(attrDico["attributes"][attribute]["value"]) + " for " + attribute +" as " + typeAttr + " on " + node)
				# print(sys.exc_info())
				pass

		else:
			try:
				cmds.setAttr( node + "." + attribute, attrDico["attributes"][attribute]["value"])
				# print(attribute + " set to " + str(attrDico["attributes"][attribute]["value"]) + " as " + typeAttr)
			except:
				# print("Could not set " + str(attrDico["attributes"][attribute]["value"]) + " for " + attribute +" as " + typeAttr + " on " + node)
				# print(sys.exc_info())
				pass
	if attribute == "matrix":
		matrix = attrDico[attribute]

def setConnectionsOnLight(attributeDico):
	for key in attributeDico:
		if attributeDico[key]["type"]=="connection":
			try:
				cmds.connectAttr(attributeDico[key]["value"][1], attributeDico[key]["value"][0], f = True)
				print("Connection done for: ", attributeDico[key]["value"])
			except:
				print("Could not connect " + attributeDico[key]["value"][1] + " and " + attributeDico[key]["value"][0])
				pass

def getOrderDict(item):
	# Get Order value from Dict
	order = item[1]['order']
	return order

def importLgtRig(nameAsset,dictLights,dictConnections,dictLightInfos):
	listNodesCreated = []
	if cmds.objExists(nameAsset):
		cmds.confirmDialog(title='WARNING',message = "Set is empty or No correct path has been selected!")
	else:
		#nameLgtRig = createGroup(nameAsset)
		# namespace = cmds.namespace(add = nameAsset)
		# cmds.namespace(set = namespace)
		namespace = "truc"
		
		rebuildHierarchy(namespace,dictLights,dictConnections,dictLightInfos,listNodesCreated)
		rebuildConnections(dictConnections)


	return listNodesCreated