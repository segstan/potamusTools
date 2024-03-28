import maya.cmds as cmds
from mtoa.core import createStandIn, createVolume
import maya.cmds as cmds
import json
import pymel.core as pm
import os
import maya.mel as mel
import re


def buildMegascanShaderA(listTextures,triplanar,nameAsset,geo,manifold,idName):
	matName = "Mat_"+ nameAsset

	if cmds.objExists(matName):
		matName += idName
	else:
		idName = ""

	importedMObject = geo
	opacityFlag = False
	linear = False
	## Arnold
	colorConnect = ".baseColor"
	specularConnect = ".specularColor"
	specularRoughnessConnect = ".specularRoughness"
	translucency = ".subsurfaceColor"
	normal = ".normalCamera"
	opacity = ".opacity"
	outColor = ".outColor"
	outColorR = ".outColorR"
	outColorA = ".outAlpha"

	material = cmds.shadingNode("aiStandardSurface", asShader=True, name=matName)
	shadingGroup= cmds.sets(name=nameAsset+"_SG", empty=True, renderable=True, noSurfaceShader=True)
	cmds.connectAttr(material+".outColor", shadingGroup+".surfaceShader")
	displacement = cmds.shadingNode("displacementShader", asShader=True, name= matName +"_displacement")
	cmds.connectAttr(displacement +".displacement",  shadingGroup+".displacementShader")

	cmds.binMembership( (shadingGroup,material,displacement), addToBin="bin_" + nameAsset )

	try:
		mel.eval('refreshHyperShadeBinsUI "hyperShadePanel1Window|hyperShadePanel1|binsWrapForm" true;')
	except:
		pass

	for texture in listTextures:
		cmds.binMembership( texture, addToBin="bin_" + nameAsset )
		
		if "Albedo" in texture:
			cmds.connectAttr(texture+ outColor, material + colorConnect)
		if "Specular" in texture:
			cmds.connectAttr(texture + outColor, material + specularConnect, f = True)
			##cmds.setAttr(texture+ ".exposure", 4)
		if "Roughness" in texture:
			cmds.connectAttr(texture+ outColorR, material +specularRoughnessConnect)
		if "Translucency" in texture:
			cmds.connectAttr(texture+ outColor, material +translucency)
			cmds.setAttr(material + ".subsurface", 0.5 )
		if "Normal" in texture:
			bump = cmds.shadingNode("bump2d", asUtility = True, name= "bump2d_"+ material)
			if triplanar == False:
				cmds.connectAttr(texture + outColorA, bump + ".bumpValue",force = True)
				cmds.setAttr( texture + ".colorSpace", "Raw",type="string")
				cmds.setAttr( texture + ".ignoreColorSpaceFileRules", 1)
			else:
				cmds.connectAttr(texture + outColorR, bump + ".bumpValue",force = True)
			cmds.connectAttr(bump + ".outNormal", matName + normal, force= True)
			cmds.setAttr(bump + ".bumpInterp", 0)
			cmds.setAttr(bump + ".bumpDepth", 1)

		if "Opacity"in texture:
			cmds.connectAttr(texture+ outColor, material +opacity)
			opacityFlag = True
				
		if "Displacement" in texture:
			##cmds.connectAttr(texture+ outColor, displacement +".vectorDisplacement", f= True)
			cmds.connectAttr(texture+ outColorR, displacement +".displacement", f= True)
			cmds.setAttr(displacement + ".aiDisplacementAutoBump", 1)
			cmds.setAttr(displacement + ".aiDisplacementZeroValue", 0.5)
			cmds.setAttr(displacement + ".aiDisplacementPadding", 0.25)
			if triplanar == False:
				cmds.setAttr( texture + ".colorSpace", "Raw",type="string")
				cmds.setAttr( texture + ".ignoreColorSpaceFileRules", 1)
		if not importedMObject == None:
				for obj in importedMObject:
					try:
						shapes = cmds.listRelatives(obj, shapes=True)
						cmds.setAttr(shapes[0] + ".aiSubdivType", 1)
						cmds.setAttr(shapes[0] + ".aiSubdivIterations", 2)
						if opacityFlag == True:
							cmds.setAttr(shapes[0] + ".aiOpaque",0)
					except:
						pass

	cmds.select(clear= True)
	## Graph in the hyperShade
	cmds.hyperShade(downStream = shadingGroup )
	##Assign Shader
	if not importedMObject == None:
		##for listObj in importedMObject:
		for obj in importedMObject:
			cmds.setAttr(obj+".displayColors",False)
			print("Objects to assign a shader to " + obj)
			if cmds.objectType( obj, isType="transform" ):
				print("I am gonna assign a shader to : " + obj)
				selection = cmds.select(obj, add= True)
				try:
					cmds.hyperShade(assign= material )
				except:
					"No suitable object"
			else:
				print(obj)
	else:
		print("No object to assign to")

def loadMegascansShaderA(jsonShader, listTextures,nameAsset,geometry,manifold,idName):
	nodes = readShaderJson(jsonShader)

	## Create Bin
	cmds.binMembership( nodes+listTextures, addToBin="bin_" + nameAsset + idName )
	try:
		mel.eval('refreshHyperShadeBinsUI "hyperShadePanel1Window|hyperShadePanel1|binsWrapForm" true;')
	except:
		pass

	outColor = ".outColor"
	outColorR = ".outColorR"
	outColorA = ".outColorA"
	outTransparency = ".outTransparency"

	colorCorrectNode = "aiColorCorrect"
	opaque = True

	albedoConnector = None
	aoConnector= None
	specularConnector = None
	roughnessConnector = None
	translucencyConnector = None
	opacityConnector = None
	fuzzConnector = None
	metalnessConnector = None
	normalConnector = None
	displacementConnector = None
	materialOGL = None

	## Rename Nodes and Find where to connect the Textures
	for node in nodes:
		if "CONSTRUCTOR" in node:
			nodeSuffixe= node.split("CONSTRUCTOR")[-1]
			renamedNode = cmds.rename(node, nameAsset+nodeSuffixe)
			if cmds.nodeType(renamedNode) == "shadingEngine":
				shadingGroup = renamedNode
			if cmds.nodeType(renamedNode) == "lambert" or cmds.nodeType(renamedNode) == "blinn":
				materialOGL = renamedNode
		else:
			if "albedo" in node.lower() and cmds.nodeType(node) == colorCorrectNode:
				albedoRenamed = cmds.rename(node, nameAsset + "_" + node  )
				albedoConnector = albedoRenamed
			if "roughness" in  node.lower() and cmds.nodeType(node) == colorCorrectNode:
				roughnessRenamed = cmds.rename(node, nameAsset + "_" + node  )
				roughnessConnector = roughnessRenamed
			if "specular" in  node.lower() and cmds.nodeType(node) == colorCorrectNode:
				specularRenamed = cmds.rename(node, nameAsset + "_" + node  )
				specularConnector = specularRenamed
			if "translucency" in  node.lower() and cmds.nodeType(node) == colorCorrectNode:
				translucencyRenamed = cmds.rename(node, nameAsset + "_" + node  )
				translucencyConnector = translucencyRenamed
			if "opacity" in  node.lower() and cmds.nodeType(node) == colorCorrectNode:
				opacityRenamed = cmds.rename(node, nameAsset + "_" + node  )
				opacityConnector = opacityRenamed
			if "fuzz" in node.lower() and cmds.nodeType(node) == colorCorrectNode:
				fuzzRenamed = cmds.rename(node, nameAsset + "_" + node  )
				fuzzConnector = fuzzRenamed
			if "metalness" in node.lower() and cmds.nodeType(node) == colorCorrectNode:
				metalnessRenamed = cmds.rename(node, nameAsset + "_" + node  )
				metalnessConnector = metalnessRenamed
			if "ao" in node.lower() and cmds.nodeType(node) == colorCorrectNode:
				aoRenamed = cmds.rename(node, nameAsset + "_" + node  )
				aoConnector = aoRenamed
			if "normal" in node.lower() and cmds.nodeType(node) == colorCorrectNode:
				normalRenamed = cmds.rename(node, nameAsset + "_" + node  )
				normalConnector = normalRenamed
			if "displacement" in  node.lower() and cmds.nodeType(node) == colorCorrectNode:
				displacementRenamed = cmds.rename(node, nameAsset + "_" + node  )
				displacementConnector = displacementRenamed

	## Connect Texture to Shader Connector
	for texture in listTextures:
		if "albedo" in texture.lower() and albedoConnector != None:
			cmds.connectAttr(texture + outColor, albedoConnector+ ".input", f = True)
			if materialOGL != None:
				cmds.connectAttr(texture + outColor, materialOGL+ ".color", f = True)
		if "specular" in texture.lower() and specularConnector != None:
			cmds.connectAttr(texture + outColor, specularConnector+ ".input", f = True)
		if "roughness" in texture.lower() and roughnessConnector !=None:
			cmds.connectAttr(texture + outColor, roughnessConnector+ ".input", f = True)
		if "translucency" in texture.lower() and translucencyConnector!=None:
			cmds.connectAttr(texture + outColor, translucencyConnector+ ".input", f = True)
		if "opacity" in texture.lower() and opacityConnector != None :
			cmds.connectAttr(texture + outColor, opacityConnector+ ".input", f = True)
			if materialOGL != None:
				cmds.connectAttr(texture + outTransparency, materialOGL+ ".transparency", f = True)
			opaque = False
		if "fuzz" in texture.lower() and fuzzConnector != None:
			cmds.connectAttr(texture + outColor, fuzzConnector+ ".input", f = True)
		if "metalness" in texture.lower() and metalnessConnector != None:
			cmds.connectAttr(texture + outColor, metalnessConnector+ ".input", f = True)
		if "normal" in texture.lower() and normalConnector !=None:
			cmds.connectAttr(texture + outColor, normalConnector+ ".input", f = True)
		if "displacement" in texture.lower() and displacementConnector !=None:
			cmds.connectAttr(texture + outColor, displacementConnector+ ".input", f = True)

	materials = cmds.listConnections( shadingGroup +'.surfaceShader', d=False, s=True )

	cmds.select(clear= True)
	cmds.hyperShade(downStream = shadingGroup )

	## Assign Shader to Geo
	if not geometry == None:
		for geo in geometry:
			if cmds.objectType( geo, isType="transform" ):
				selection = cmds.select(geo, add= True)
				cmds.setAttr(geo+".displayColors",False)
				try:
					cmds.select(materials[0], add= True)
					cmds.hyperShade(assign= materials[0] )
					print("Shader assigned to: " + geo)
				except:
					"No suitable object to assign a shader"
			else:
				print (geo)

		## Set Subdiv and Displacement Settings
		setGeoDisplacementSettings(geometry,opaque)

def setGeoDisplacementSettings(geometries,opaque):
	for geo in geometries:
		shapes = cmds.listRelatives(geo, shapes=True)
		try:
			cmds.setAttr(shapes[0] + ".aiSubdivType", 1)
			cmds.setAttr(shapes[0] + ".aiSubdivIterations", 2)
			if opaque == False:
				cmds.setAttr(shapes[0] + ".aiOpaque",0)
		except:
			pass

def createSharedArnoldTexture(sharedUV,triplanar):
	manifold =""
	if triplanar == False and sharedUV == True:
		manifold =  cmds.shadingNode("place2dTexture", asUtility=True)
	elif triplanar == True and sharedUV == True:
		manifold = cmds.shadingNode("place2dTexture", asUtility=True)
	return manifold

def createTextureFileArnold(sharedUV,triplanar,manifold,filename,newName,dataTexture):
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
		textureFile = cmds.shadingNode('file', asTexture=True)
		TwodPlacement = cmds.shadingNode("place2dTexture", asUtility=True)
		texturePlacement = cmds.shadingNode("aiTriplanar", asUtility=True)
		texturePlacement = cmds.rename(texturePlacement, "aiTriplanar_"+newName)
		cmds.setAttr( texturePlacement + ".blend", 0.5)
		cmds.defaultNavigation(connectToExisting=True, source = TwodPlacement, destination=textureFile)
		cmds.connectAttr( textureFile + ".outColor", texturePlacement+".input", force = True)
		cmds.select(textureFile)
	elif sharedUV == True and triplanar == True:
		textureFile = cmds.shadingNode('file', asTexture=True)
		texturePlacement = cmds.shadingNode("aiTriplanar", asUtility=True)
		texturePlacement = cmds.rename(texturePlacement, "aiTriplanar_"+newName)
		cmds.setAttr( texturePlacement + ".blend", 0.5)
		cmds.connectAttr( textureFile + ".outColor", texturePlacement+".input", force = True)
		cmds.defaultNavigation(connectToExisting=True, source = manifold, destination=textureFile)
		
		cmds.select(textureFile)
	# Set FileName
	cmds.setAttr(textureFile+".fileTextureName", filename, type="string")
	# Set ColorSpace
	if dataTexture:
		if "colorSpace" in dataTexture:
			colorSpace = dataTexture["colorSpace"]
		else:
			colorSpace = dataTexture["ocio"]
		if colorSpace.lower() == "linear":
			colorSpace = "Raw"
	else:
		colorSpace = "Raw"
	setColorSpaceOnTexture(textureFile,colorSpace)
	# Rename Node
	textureFile =cmds.rename(textureFile, newName)

	if triplanar == True:
		textureFile = texturePlacement
		print("- Triplanar Node : ", textureFile)

	return textureFile

def createStandin(name,model):
	node = createStandIn(path= model)
	parent= cmds.listRelatives(node,type='transform',p=True)
	cmds.rename(parent, name)

def createVDB(name,pathVDB,sequence):
	createVolume()
	volume = cmds.ls (sl =True)
	cmds.setAttr(volume[0]+".filename",pathVDB,type = "string")
	if sequence == True:
		cmds.setAttr(volume[0]+".useFrameExtension",1)
	parent= cmds.listRelatives(volume[0],type='transform',p=True)
	cmds.rename(parent, name)

	return name

def buildVdbShader(nameAsset):
	material = cmds.shadingNode("aiStandardVolume", asShader=True, name="Mat_"+str(nameAsset))
	selection = cmds.select(nameAsset, replace= True)
	try:
		cmds.hyperShade(assign= material )
	except:
		"No suitable object"

def setColorSpaceOnTexture(textureNode,colorspace):
	cmds.setAttr( textureNode + ".colorSpace", colorspace,type="string")

################################################################################################################
################################################################################################################

def traverse(node,children):
	listNodule =[]
	if cmds.objExists(node):
		listNodule =[]
		connections = cmds.listConnections(node,source=True,destination=False,skipConversionNodes=True) or {}
		for child in connections:
			typeID = str(cmds.nodeType(child))
			if typeID != 'transform':
				if typeID != 'groupId':
					children[child]= {}
					listNodule.append(child)
	return listNodule

def get_nodes(node,children,listNodeName):
	listNodeName += traverse(node,children)
	for child in children:
		if cmds.objExists(child):
			get_nodes(child,children[child],listNodeName)
	return listNodeName

def buildDictionary(shadingGroup):
	listNodes =[]        
	listNodes.append(shadingGroup)
	listNodule =[]
	children={}
	cleanDic= {}
	listItem = get_nodes(shadingGroup,children,listNodes)

	for item in listItem:
		attribAll = {}
		attribMulti = {}
		attribString = {}
		id = cmds.nodeType(item)
		## Attributes are different between Renderman and Arnold in Maya
		listAttribAll = cmds.listAttr(item,c=True,se=True,multi = True)
		if listAttribAll:
			for attribute in listAttribAll:
				try:
					valueAttr = cmds.getAttr(item + "."+ attribute )
					attribAll[attribute] = valueAttr
				except:
					pass

		connectionsAttr = cmds.listConnections(item,d=False, s=True,connections =True,plugs=True)
		data = {}
		data[id] = []
		data[id].append({
		'connections':connectionsAttr,
		'attributes':attribAll
		})
		cleanDic[item] = data
	return cleanDic

def findWholeWord(word):
	return re.compile(r'\b({0})\b'.format(word), flags=re.IGNORECASE).search

def readShaderJson(jsonFile):
	listConnect = []
	listNodesCreated = []
	listShaders = ["PxrDisney","PxrSurface","PxrConstant","PxrDiffuse","PxrLayerSurface","PxrVolume","aiStandardSurface","aiStandardHair","aiTwoSided","aiLayerShader"]

	shaderNamespace= cmds.namespace( add = 'ASSET' )
	cmds.namespace( set=shaderNamespace )
	
	if os.path.exists(jsonFile):
		with open(jsonFile) as jfile:
			data = json.load(jfile)
			for key in data:
				nameComponent = key
				dictionnaryInfo = data[key]
				for key in dictionnaryInfo:
					nodeToCreate = key
					if nodeToCreate == "shadingEngine" or nodeToCreate == "collect":
						node = cmds.sets(name=nameComponent, empty=True, renderable=True, noSurfaceShader=True)
					elif nodeToCreate in listShaders  :
						 node = cmds.shadingNode(nodeToCreate, asShader=True,name = nameComponent)
					elif "principledshader" in nodeToCreate  :
						 node = cmds.shadingNode("lambert", asShader=True,name = nameComponent)
					elif "transform" in nodeToCreate:
						continue
					else:
						node = cmds.shadingNode(nodeToCreate, asUtility=True,name = nameComponent)
					listNodesCreated.append(node)
					typeAction = dictionnaryInfo[key]
					for action in typeAction:
						listType = action
						for key in listType:
							action = key
							attributes = listType[key]
							if "attributes" in action:
								for key in attributes:
									nameAttribute = key
									valueAttribute = attributes[key]
									try:
										if action == "attributes" and valueAttribute != None:
											if type(valueAttribute) is list :
												if nameAttribute == "utilityPattern" :
													m = 0
													for value in valueAttribute[0]:
														if m <len( valueAttribute[0]):
															pm.setAttr(node + "." + nameAttribute+"["+str(m)+"]", value)
															m+=1
												if len(valueAttribute[0])== 3 :
													pm.setAttr(node + "." + nameAttribute, valueAttribute[0][0],valueAttribute[0][1],valueAttribute[0][2])
											elif type(valueAttribute) is str :
												pm.setAttr(node+"."+nameAttribute, valueAttribute)
											elif type(valueAttribute) is None :
												print("Do nothing")
											else:
												pm.setAttr(node+"."+nameAttribute, valueAttribute)
									except:
										# print ("Couldn't set: " +nameAttribute + " " + str(valueAttribute))
										pass
									
							elif action == "connections":
								if attributes != None:
									for connection in attributes:
										listConnect.append(connection)

			k=0
			for connect in listConnect:
				if k<len(listConnect)-1 and k % 2 == 0:
					try:
						outputParameter =listConnect[k+1]
						inputParameter = connect
						## Houdini Fix
						if findWholeWord("bxdf_out")(outputParameter):
							outputParameter = outputParameter.split(".")[0] + "." + outputParameter.split(".")[-1].replace("bxdf_out","outColor")
						if findWholeWord("surface")(outputParameter):
							outputParameter = outputParameter.split(".")[0] + "." + outputParameter.split(".")[-1].replace("surface","outColor")
						if findWholeWord("displace")(outputParameter.split(".")[-1]):
							outputParameter = outputParameter.split(".")[0] + "." + outputParameter.split(".")[-1].replace("displace","outColor")
						if findWholeWord("shader1")(connect):
							inputParameter = inputParameter.split(".")[0] + "." + inputParameter.split(".")[-1].replace("shader1","rman__surface")
						if findWholeWord("shader2")(connect):
							inputParameter = inputParameter.split(".")[0] + "." + inputParameter.split(".")[-1].replace("shader2","rman__displacement")
						if findWholeWord("shader3")(connect):
							inputParameter = inputParameter.split(".")[0] + "." + inputParameter.split(".")[-1].replace("shader3","surfaceShader")
						if findWholeWord("resultRGBR")(connect):
							inputParameter = inputParameter.split(".")[0] + "." + inputParameter.split(".")[-1].replace("resultRGBR","resultR")
							
						# print("Connecting : " + outputParameter + " to " + inputParameter)
						cmds.connectAttr( shaderNamespace+ ":"+outputParameter, shaderNamespace+":"+inputParameter, force = True)
					except:
						# print("Couldn't connect :" + outputParameter + " to " + inputParameter)
						pass
					k +=1
				else:
					k +=1

	else:
		print(" -- Shader file doesn't exist -- ")

	## Namespace
	listNodeCreated=[]
	cmds.namespace (set=":"+shaderNamespace)
	listNodesToClean= cmds.namespaceInfo (listOnlyDependencyNodes=True)
	cmds.namespace( set=':' )
	if listNodesToClean:
		for node in listNodesToClean:
			nodeClean = cmds.rename(node,node.split(shaderNamespace+":")[-1])
			listNodeCreated.append(nodeClean)

	cmds.namespace( removeNamespace = shaderNamespace)
	return listNodeCreated