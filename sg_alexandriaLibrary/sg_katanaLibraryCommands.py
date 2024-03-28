import Katana
from Katana import NodegraphAPI
from Katana import DrawingModule
from Katana import KatanaFile
from Katana import UI4
import os
import sys
import random
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


############################################################## Generic ###############################################################

def createNetworkMaterial(name):
	nMaterialCreate =  NodegraphAPI.CreateNode('NetworkMaterialCreate', NodegraphAPI.GetRootNode())
	nMaterialCreate.setName(name)

	for child in nMaterialCreate.getChildren():
		if child.getType() == "NetworkMaterial":
			child.getParameter('name').setValue(str(name),0)

	## Move Node to Center of NodeGraph
	centerNodePosition(nMaterialCreate)

	return nMaterialCreate

def centerNodePosition(node):
	root = NodegraphAPI.GetRootNode() 
	pos = NodegraphAPI.GetViewPortPosition(root) 
	# this returns a tuple containing the position and scale of the view information of a group network. This works because the Root node is also a Group node
	NodegraphAPI.SetNodePosition(node, (pos[0][0], pos[0][1]))

def createBackDrop(nameAsset,scale,typeAsset):
	nodegraphNode = UI4.App.Tabs.FindTopTab("Node Graph", alsoRaise=True)
	node = nodegraphNode.getEnteredGroupNode()

	backdrop = NodegraphAPI.CreateNode("Backdrop",node)
	colour = randomColour(typeAsset)
	attrs = backdrop.getAttributes()
	attrs['ns_text'] = nameAsset
	attrs['ns_fontScale'] = 2
	attrs['ns_sizeX'] = scale[0]
	attrs['ns_sizeY'] = scale[1]
	attrs['x'] = scale[2]
	attrs['y'] = scale[3]
	backdrop.setAttributes(attrs)

	NodegraphAPI.SetNodeSelected(backdrop,True)
	NodegraphAPI.SetNodeFloating(backdrop,True)

	return backdrop

def calculateBackdropBBox(listNodes):
	xSurface = 0
	ySurface = 0
	xPosition = 5
	yPosition = 5
	for node in listNodes:
		position = NodegraphAPI.GetNodePosition(node)
		ySurface += 500
		xPosition += position[0]
		yPosition += position[1]

	xSurface = 1000
	## Average Position
	xPosition = xPosition/len(listNodes)- xSurface/2
	yPosition = yPosition/len(listNodes)+ySurface/2

	return [abs(xSurface),abs(ySurface),xPosition,yPosition]

def createBackDropAutoFit(nameAsset):
	nodegraphNode = UI4.App.Tabs.FindTopTab("Node Graph", alsoRaise=True)
	node = nodegraphNode.getEnteredGroupNode()
	backdrop = nodegraphNode._NodegraphPanel__fitBackdropNode()
	return backdrop

def randomColour(typeNode):
	if typeNode == "texture":
		randomColour = [[0.30,0.24,0.25],[0.28,0.265,0.23],[0.248,0.27,0.24],[0.25,0.25,0.30],[0.29,0.24,0.29]]

	elif typeNode == "megascan":
		randomColour = [[0.28,0.25,0.19],[0.31,0.21,0.21],[0.21,0.27,0.20],[0.23,0.221,0.31],[0.29,0.21,0.29]]

	else:
		randomColour = [[0.48,0.45,0.49],[0.41,0.41,0.41],[0.41,0.47,0.40],[0.43,0.421,0.51],[0.49,0.41,0.49]]

	colour = random.choice(randomColour)
	return colour

def checkIfFile(path):
	if os.path.exists(path):
		return True
	else:
		return False

def checkIfTexture(path):
	if os.path.exists(path):
		fileFormat = [elmt for elmt in sg_alexandriaConstants.listTextureFileExtension if( elmt.split(".")[-1] in path)]
		if fileFormat:
			return True


##################################################################################################################################

def createTextures(sharedUV,triplanar,manifold,name,filepath,yOffset):
	TIME= 0

	##materialNode = NodegraphAPI.CreateNode('Material',NodegraphAPI.GetRootNode())
	##NodegraphAPI.SetNodePosition(materialNode, (300,400))   
	##materialNode.getParameter('name').setValue('pink_mat', TIME)
	##materialNode.getParameter('namespace').setValue('geo', TIME)
	##materialNode.addShaderType('prmanSurface')

def createMPCTextures(filepath):
	print("")
	##imageNode = NodegraphAPI.CreateNode('PrmanShadingNode', NodegraphAPI.GetRootNode())
	##imageNode = NodegraphAPI.CreateNode('ImageRead', NodegraphAPI.GetRootNode())
	##imageNode.getParameter('file').setValue("D:\Data\Projects\Maya\library\scenes\Antique_Sculpture_ugtkfevhw_3d/ugtkfevhw_4K_Albedo.jpg",TIME)
	##imageNode.getParameter('image.rawData').setValue("True",TIME)

def loadContainer(pathShaderLibrary,nameAsset,context,katanaShaderPath):
	TIME = 0
	listContainers = []
	container = None

	if container == None:
		nodegraphNode = UI4.App.Tabs.FindTopTab("Node Graph", alsoRaise=True)
		node = nodegraphNode.getEnteredGroupNode()
		if node.getName() == "rootNode" :
			container = createNetworkMaterial(nameAsset+"_SG")
		else:
			container = node 

	print("The container is: " + container.getName())
	
	## Find shader to load
	if context == "Megascans" or context == "Textures":
		if node.getName() == "rootNode":
			## At the root so will load an entire shader
			katanaShader = katanaShaderPath
		else:
			## In a group so will load the mpc setting
			katanaShader = pathShaderLibrary+ "renderman/" + "megascans/megascanMPCTextureDefault/megascanMPCTextureDefault.katana"
	else:
		katanaShader = katanaShaderPath

	if os.path.exists(katanaShader):
		print("Apply Shader Preset: " + katanaShader)

	##	 Import Preset
	nodes = KatanaFile.Import(katanaShader,False,container)
	NodegraphAPI.SetAllSelectedNodes(listContainers)

	newBGPreset = {}
	for node in nodes:
		NodegraphAPI.SetNodeSelected(node,True)
		NodegraphAPI.SetNodeFloating(node,True)
		if node.getType() == "NetworkMaterialCreate":
			print("NetworkMaterialCreator in the file, may cause error")
			# node.setName(nameAsset+"_SG",TIME)
			# container = node 
		# elif node.getType() == "Backdrop":
		# 	BGPreset = NodegraphAPI.GetNodeShapeAttrs(node)
		# 	BGPreset['text'] = nameAsset
		# 	##NodegraphAPI.SetNodeShapeNodeAttrs(node,BGPreset)
		# 	NodegraphAPI.SetNodeShapeAttr(node,"text",nameAsset)
		# 	DrawingModule.nodeWorld_setShapeAttr(node,"text",nameAsset)
		# 	DrawingModule.nodeWorld_setShapeAttr(node,"update",1)
		# 	for key in newBGPreset:
		# 		if key != "fromContext":
		# 			data = BGPreset.get(key,"")
		# 			newBGPreset[key]= data
		# 	print(newBGPreset)
		# 	newBGPreset['text'] = nameAsset
		# 	NodegraphAPI.SetNodeShapeNodeAttrs(node,newBGPreset)

	return container

def importKatanaShader(katanaShader,nameAsset):
	TIME = 0
	container = getContainer(nameAsset)
	nodes = KatanaFile.Import(katanaShader,False,container)

	for node in nodes:
		if node.getType() == "NetworkMaterialCreate":
			container = node 

	return container

def getContainer(nameAsset):
	container = None
	nodegraphNode = UI4.App.Tabs.FindTopTab("Node Graph", alsoRaise=True)
	node = nodegraphNode.getEnteredGroupNode()
	if node.getName() == "rootNode" :
		container = createNetworkMaterial(nameAsset+"_SG")
	else:
		container = node 

	print("The container is: " + container.getName())
	return container

def getContext():
	context = None
	nodegraphNode = UI4.App.Tabs.FindTopTab("Node Graph", alsoRaise=True)
	node = nodegraphNode.getEnteredGroupNode()
	if node.getName() == "rootNode" :
		context = "rootNode"
	else:
		context = node 

	print("The context is: " + node.getName())
	return context

def getChildren(node):
	listChildren = []
	# nodeToParse = NodegraphAPI.GetNode(node)
	for child in node.getChildren():
		listChildren.append(child)
	return listChildren

def convertTexAutomatic(listTextures):
	import sg_batchTextureConvert
	converter = "TEX (Prman)"
	commandlineDict = sg_batchTextureConvert.GenericCommand.getValidChildCommands()
	convert_command = commandlineDict[converter]
	settings = ["TEX (Prman)","Texture","periodic","periodic","short"]
	listActionsTex = [converter,convert_command,settings]
	return listActionsTex

########################################################################################################################
##################################### LightRig Import/Export ###########################################################
########################################################################################################################

def hierarchyDict(rootPackage,dictLights,dictConnections):
	packageName = rootPackage.getName()
	# Get Children
	children = rootPackage.getChildPackages()
	# Get Type
	packageType  = rootPackage.DEFAULT_NAME
	print("Name of rootPackage: " + packageName + " of type: " + packageType )
	# Get Parent
	parentPackage = getParentPackageName(rootPackage)
	parents = findAllParents(rootPackage, [])
	nameParents = [pack.getName() for pack in parents]
	nameParents.reverse()
	longNameNodeHierarchy = "|".join(nameParents)

	if parents :
		objWithParent =  "|" + longNameNodeHierarchy + "|" + packageName
	else:
		objWithParent =  packageName
		longNameNodeHierarchy = ""

	# Get Transform
	matrix = []
	xForm = []
	#matrix = rootPackage.getCreateNode().getParameter('transform.translate.x').getValue(1001)
	listTrans = [rootPackage.getCreateNode().getParameter('transform.translate.x').getValue(1001),rootPackage.getCreateNode().getParameter('transform.translate.y').getValue(1001),rootPackage.getCreateNode().getParameter('transform.translate.z').getValue(1001)]
	listRot = [rootPackage.getCreateNode().getParameter('transform.rotate.x').getValue(1001),rootPackage.getCreateNode().getParameter('transform.rotate.y').getValue(1001),rootPackage.getCreateNode().getParameter('transform.rotate.z').getValue(1001)]
	listScale = [rootPackage.getCreateNode().getParameter('transform.scale.x').getValue(1001),rootPackage.getCreateNode().getParameter('transform.scale.y').getValue(1001),rootPackage.getCreateNode().getParameter('transform.scale.z').getValue(1001)]

	xForm.append(listTrans)
	xForm.append(listRot)
	xForm.append(listScale)
	
	# Variables Missing
	expression = ""
	shapes = []
	
	# If the type is rig it is an object to create so grab the shape type
	if packageType == "rig":
		nodeTpe = "group"
		shapeType = ""
	# if it is not a rig, well it is potentially a light
	elif packageType in sg_alexandriaConstants.listRendermanLights:
		nodeTpe = "transform"
		parametersName = "shaders.prmanLightParams"
		shapeType = packageType
		shapes.append(packageName+"Shape")
	elif packageType in sg_alexandriaConstants.listRendermanBlockers:
		nodeTpe = "transform"
		parametersName = "shaders.prmanLightfilterParams"
		shapeType = packageType
		shapes.append(packageName+"Shape")
	else:
		print(packageType)
		nodeTpe = "transform"
		parametersName = "shaders.prmanLightParams"
		shapeType = packageType 

	# Attributes Dictionary
	attributesDict ={}
	attributesShapeDict ={}

	if packageType != "rig":
		# Get Material Node / Equivalent to the shape in maya
		material = rootPackage.getMaterialNode()
		parameters = material.getParameter("shaders.prmanLightParams")
		if parameters:
			# List all Attributes on the "shape"
			attributes = parameters.getChildren()
			if attributes:
				for attribute in attributes:
					rootPackage.getMaterialNode().checkDynamicParameters()
					# Get type of Attribute Parse the group to find the value attribute
					for attr in attribute.getChildren():
						if "value" in attr.getName():
							attributeType = attr.getType()
							if attributeType == "number":
								attributeType = "float"
							elif attributeType == "numberArray":
								attributeType = "float3"
					try:
						if attributeType != "float3":
							attributeValue = rootPackage.getMaterialNode().getParameter("shaders.prmanLightParams." + attribute.getName() +".value").getValue(1001)
						else:
							attributeValue = []
							for i in range(0,3):
								attributeValue.append(rootPackage.getMaterialNode().getParameter("shaders.prmanLightParams." + attribute.getName() +".value"+".i%d" %i).getValue(1001))
							# Maya Fix
							attributeValue = [attributeValue]
					except:
						#print("Ignore that parameter: " + attribute.getName())
						pass
					attributesShapeDict[attribute.getName()] = {
					'value': attributeValue,
					'type': attributeType,
					}

	## Connections
	listNodesConnections = []
	if packageType in sg_alexandriaConstants.listRendermanLights:
		# Check if parent is a light, if yes, it is a connection
		if children:
			for child in children:
				print("Looking for: ",child.DEFAULT_NAME)
				if child.DEFAULT_NAME in sg_alexandriaConstants.listRendermanBlockers:
					listNodesConnections.append(child)
	if listNodesConnections:
		#print(listNodesConnections,objWithParent)
		dictConnections = buildConnectionsDic(dictConnections,objWithParent,listNodesConnections)

	# Write Hierarchy Dictionary
	fcn.addEntryLgtRigDic(dictLights,packageName,objWithParent,shapes,shapeType,nodeTpe,attributesShapeDict,{},expression,matrix,xForm,attributesDict)
	if children :
		for child in children:
			hierarchyDict(child, dictLights[objWithParent]["children"],dictConnections)

	return dictLights,dictConnections

def rebuildHierarchy(gaffer,root,dictLights,dictConnections,dictLightInfos,listTexturesToConvert):
	dccAtCreation = dictLightInfos["dcc"]
	#Find the root package on the gaffer to add Packages
	for key in dictLights:
		obj = key
		attributesDict = dictLights[key]["attributes"]
		shapeAttributesDict = dictLights[key]["shapeAttributes"]
		objectToSetAttributes = ""
		objectCreated = ""
		name = key.split("|")[-1]
		parent = key.split("|")[0]
		## Connected Node
		try:
			childrenDict = dictLights[key]["children"]
		except:
			childrenDict = {}

		# Create Hierarchy
		if dictLights[key]["nodeType"] == "group":
			print("-- Create Group: " + name + " with parent: " + key.rsplit("|",1)[0] + " --")
			# Create Group
			grp = createRigInGT(name,root)
			objectCreated = grp

		elif dictLights[key]["nodeType"] == "transform":
			objType = dictLights[key]["shapeType"]
			objTypePackage = dictLights[key]["shapeType"]+"Package"
			shape = dictLights[key]["shape"][0].rsplit("|",1)[0]
			parent = ""
			print("-- Create Object: " + objType + " with parent: " + key.rsplit("|",1)[0] + " --")
			# Create Light
			if objType in sg_alexandriaConstants.listRendermanLights or objType in sg_alexandriaConstants.listRendermanBlockers:
				lgt = createLightInGT(name,objTypePackage,root)
				objectCreated = lgt
			else:
				print(objType + " is not a supported light for now")
				continue

		# Set Transform Not Ideal, needs improvemnt,it should dealt with matrix
		matrix = dictLights[key]["matrix"]
		xForm = dictLights[key]["transform"]
		if objectCreated != "":
			if dccAtCreation == "katana":
				objectCreated.getCreateNode().getParameter('transform.interface').setValue("Transform Matrix",1001)
				setLGTMatrix(matrix,objectCreated)
			elif dccAtCreation != "katana":
				objectCreated.getCreateNode().getParameter('transform.interface').setValue("SRT Values",1001)
				setLGTxForm(xForm,objectCreated)
				if dccAtCreation == "houdini" and dictLights[obj]["shapeType"] == "PxrDomeLight":
					# Difference of -180 deg between maya and houdini for the dome light
					extraRotY = 180
					actual = objectCreated.getCreateNode().getParameter("transform.rotate.y").getValue(1001)
					objectCreated.getCreateNode().getParameter("transform.rotate.y").setValue(actual + extraRotY,1001)
			print("Set Transformation on  " + obj)

		# Set Attributes
		if objectCreated != "":
			# It was stored as a transform but we are acting as it is the maya shape
			if dictLights[key]["nodeType"] == "transform":
				listTexturesToConvert += setLGTDynAttributes(shapeAttributesDict,objectCreated,dictLightInfos)
				print("Set Attributes on  " + obj)

		# Set Connections - will only look into blocker and parenting to the correct light
		if objectCreated != "":
			rebuildConnections(dictConnections,objectCreated,gaffer)
			print("Set Connection(s) on  " + obj)

		# Traverse again with
		rebuildHierarchy(gaffer,objectCreated,childrenDict,dictConnections,dictLightInfos,listTexturesToConvert)

	return listTexturesToConvert

def getRootNode():
	rootNode = NodegraphAPI.GetRootNode()
	return rootNode

def getRootPackage(gaffer):
	rootPackage = gaffer.getRootPackage()
	return rootPackage

def getParentPackageName(package):
	try:
		parentPackageName = package.getParentPackage().getName()
		parentPackage = package.getParentPackage()
	except:
		parentPackage = None
		pass
	return parentPackage

def findAllParents(package,listParent):
	# Return a node list
	if package:
		tmpParent = package.getParentPackage()
		if tmpParent != None : 
			if tmpParent.DEFAULT_NAME != "group":
				if tmpParent not in listParent :
					listParent.append(tmpParent)
				if listParent:
					findAllParents(listParent[-1],listParent)
			else:
				return listParent
		else:
			return listParent
	return listParent

def createGafferThree(name,rootNode):
	gaffer = NodegraphAPI.CreateNode("GafferThree",rootNode)
	gaffer.setName(name)
	return gaffer

def createRigInGT(name,rootPackage):
	rigPackage = rootPackage.createChildPackage("RigPackage",str(name))
	return rigPackage

def createLightInGT(name,typeLight,rootPackage):
	lightPackage = rootPackage.createChildPackage(str(typeLight),str(name))
	return lightPackage

def rebuildConnections(dictConnections,node,gaffer):
	nodeName = node.getName()
	for key in dictConnections:
		obj = key
		dictNodeConnections = dictConnections[obj]["connections"]
		connectInName = obj.split("|")[-1]
		listConnectOutPackage = []
		if "Shape" in connectInName:
			connectInName = obj.split("|")[-2]
		for num in dictNodeConnections:
			links = dictNodeConnections[num]["link"]
			connectOut = links[0]
			connectOutName = connectOut.split("|")[-1]
			# If the node created is in the connections dictionary 
			if "Shape" in connectOutName:
				connectOutName = connectOut.split("|")[-2]
			if connectOutName == nodeName:
				connectionsI = links[1][0]
				connectionsO = links[1][1]
				## Only for light Filters in renderman for now 
				if "rman__lightfilters" in connectionsI:
					childGaffer = gaffer.getRootPackage().getChildPackages()
					for child in childGaffer:
						connectInPackage = (findPackageByName(child,connectInName,listConnectOutPackage))
					if connectInPackage:
						print("Connecting package: " + nodeName + " to " + connectInName)
						connectInPackage[0].adoptPackage(node)

def buildConnectionsDic(dictConnections,longNameLight,childrenNodes):
	dictConnectionInfos = {}
	nodeName = longNameLight.split("|")[-1]
	amount = len(childrenNodes)
	print(amount)
	for i in range(0,amount):
		tuppleData = (longNameLight + "|" + childrenNodes[i].getName() + "|" + childrenNodes[i].getName() + "Shape",(nodeName+"."+'rman__lightfilters[%d]' %i,childrenNodes[i].getName()+".outColor"))
		dictConnectionInfos = fcn.addEntryConnectionDic(dictConnectionInfos,i,tuppleData)

	#if dictConnectionInfos:
	dictConnections[longNameLight+"|" + nodeName +"Shape"]= {
		"connections": dictConnectionInfos,
		}

	print(json.dumps(dictConnections,indent = 4))

	return dictConnections

def findPackageByName(topNode,searchName,result):
	children = topNode.getChildPackages()
	for package in children:
		if package.getName() == searchName:
			print("Connection Package Found: " + package.getName())
			result.append(package)
		else:
			findPackageByName(package,searchName,result)
	return result

def setLGTMatrix(matrix,objectCreated):
	# Need to set every component not the matrix by itself
	# The naming of the parameter is 0,1,2,3,10,11,12,13,20,21,etc ...
	i = 0
	while i < len(matrix):
		if i < 4:
			j = i
			parameterMatrix = 'transform.matrix.m' + str(j).zfill(2)
		elif 4<=i<8:
			j = 6+i
			parameterMatrix = 'transform.matrix.m' +  str(j).zfill(2)
		elif 8<=i<12:
			j = 12+i
			parameterMatrix = 'transform.matrix.m' +  str(j).zfill(2)
		elif 12<=i<16:
			j = 18+i
			parameterMatrix = 'transform.matrix.m' + str(j).zfill(2)
		objectCreated.getCreateNode().getParameter(parameterMatrix).setValue(matrix[i],1001)
		i += 1

def setLGTxForm(xForm,objectCreated):
	if xForm:
		objectCreated.getCreateNode().getParameter("transform.translate.x").setValue(xForm[0][0],1001)
		objectCreated.getCreateNode().getParameter("transform.translate.y").setValue(xForm[0][1],1001)
		objectCreated.getCreateNode().getParameter("transform.translate.z").setValue(xForm[0][2],1001)

		objectCreated.getCreateNode().getParameter("transform.rotate.x").setValue(xForm[1][0],1001)
		objectCreated.getCreateNode().getParameter("transform.rotate.y").setValue(xForm[1][1],1001)
		objectCreated.getCreateNode().getParameter("transform.rotate.z").setValue(xForm[1][2],1001)

		objectCreated.getCreateNode().getParameter("transform.scale.x").setValue(xForm[2][0],1001)
		objectCreated.getCreateNode().getParameter("transform.scale.y").setValue(xForm[2][1],1001)
		objectCreated.getCreateNode().getParameter("transform.scale.z").setValue(xForm[2][2],1001)
		
def setLGTDynAttributes(shapeAttrDict,objectCreated,dicLightInfos):
	# 
	dccAtCreation = dicLightInfos["dcc"]
	#
	objectCreated.getMaterialNode().checkDynamicParameters()
	nameObject = objectCreated.getName()
	material = "shaders.prmanLightParams."
	
	listParametersSet = []
	listParametersNotSet = []
	listTextures = []
	for key in shapeAttrDict:
		attribute = key
		typeAttr = str(shapeAttrDict[attribute]["type"])
		# Get Value/Filter by type
		if typeAttr.lower() == "string":
			value = str(shapeAttrDict[attribute]["value"])
			# Check if path exists
			isTexture = checkIfTexture(value)
			if isTexture == True:
				# Replace for tex ?
				value += ".tex"
				# Add to list for processing 
				listTextures.append(value)
		elif typeAttr.lower() == "float3":
			# need to check in maya how that value is stored, it should not be a list of a list
			value = shapeAttrDict[attribute]["value"][0]
		else:
			value = shapeAttrDict[attribute]["value"]
		# Check Correspondance between attributes name
		if attribute in sg_alexandriaConstants.sgDicConvertLightNameParameter[dccAtCreation+"-katana"]:
			attribute = sg_alexandriaConstants.sgDicConvertLightNameParameter[dccAtCreation+"-katana"][key]
		
		####### Check if it is an object or a shader attributes
		if "prmanStatements" in attribute:
			setLightStatementParameter(objectCreated,attribute,typeAttr,value)
		# Set Attribute here
		else:
			try:
				if typeAttr == "float3":
					j = 0
					objectCreated.getMaterialNode().getParameter(material+ attribute+".enable").setValue(True,1001)
					while j < 3:
						objectCreated.getMaterialNode().getParameter(material+ attribute + ".value" + ".i"+str(j)).setValue(value[j],1001)
						j +=1
				else:
					# it is for float3 decomposed - in general coming from houdini
					if ".$$" in attribute:
						attributeEnable =  attribute.split(".$$")[0]+".enable"
						attributeValue =  attribute.replace(".$$",".value")
						print(attributeValue,material+ attributeValue,material+ attributeEnable)
						objectCreated.getMaterialNode().getParameter(material+ attributeEnable).setValue(True,1001)
						objectCreated.getMaterialNode().getParameter(material+ attributeValue).setValue(value,1001)
					# Normal case
					else:
						objectCreated.getMaterialNode().getParameter(material+ attribute + ".enable").setValue(True,1001)
						objectCreated.getMaterialNode().getParameter(material+ attribute + ".value").setValue(value,1001)
				#print("Set attribute: " + material + attribute + " " + str(value))
				listParametersSet.append(material + attribute)
			except:
				listParametersNotSet.append(material + attribute)
				#print(attribute,sys.exc_info())
	#print("Parameters Set on "+ nameObject + ": " + "\n" + '\n'.join("- " + str(p) for p in sorted(listParametersSet)))
	#print("Parameters Not Set "+ nameObject + ": " + "\n" + '\n'.join("- " + str(p) for p in sorted(listParametersNotSet)))
	return listTextures

def setLightStatementParameter(node,parameter,typeParameter,value):
	params =  node.getPackageNode().getChildren()
	for parm in params:
		if parm.getType() == "PrmanLightStatements":
			parm.getParameter(parameter+ ".value").setValue(value,1001)

def setLGTObjectAttributes(attributesDict,objectCreated):
	nameObject = objectCreated.getName()

def importLgtRig(nameAsset,dictLights,dictConnections,dicLightInfos):
	# Get root
	rootNode = getRootNode()
	# Create Gaffer
	gaffer = createGafferThree(nameAsset,rootNode)
	rootPackage = getRootPackage(gaffer)
	namespace = "truc"
	#
	listTexturesToConvert = []
	listNodesCreated = []
	# Rebuild the hierarchy
	listTexturesToConvert = rebuildHierarchy(gaffer,rootPackage,dictLights,dictConnections,dicLightInfos,listTexturesToConvert)

	return listTexturesToConvert
