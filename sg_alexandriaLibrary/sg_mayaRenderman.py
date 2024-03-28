import maya.cmds as cmds
import json
import pymel.core as pm
import os
import sys
import maya.mel as mel
import re

	
from collections import OrderedDict

try:
	import rfm2
	from rfm2.config import cfg
except:
	print("RFM is NOT LOADED")
	pass

############################ To Suppress if possible
def createGroup(nameGrp):
	cmds.select(clear= True)
	grp = cmds.group(em = True, n = nameGrp)
	cmds.select(clear= True)
	return grp

def getShape(transform):
	shapes = cmds.listRelatives(transform, shapes=True)
	return shapes
#############################################################
def buildMegascanShaderR(listTextures,renderer,nameAsset,geo,manifold,idName):
	matName = "Mat_"+ renderer +"_"+ nameAsset
	if cmds.objExists(matName):
		matName += idName
	else:
		idName = ""
	importedMObject = geo

	if renderer == "rman":
		colorConnect = ".baseColor"
		specularConnect = ".specular"
		specularRoughnessConnect = ".roughness"
		translucency = ".subsurfaceColor"
		normal = ".bumpNormal"
		opacity = ".presence"

		outColor = ".resultRGB"
		outColorR = ".resultR"
		outColorA = ".resultA"

		displacementBound = 0.75

		## Create Material/Opengl/Displacement
		material = cmds.shadingNode("PxrDisney", asShader=True, name=matName)
		lambert = cmds.shadingNode("lambert", asShader=True, name= matName + "_lambert")
		shadingGroup= cmds.sets(name=nameAsset+"_SG", empty=True, renderable=True, noSurfaceShader=True)
		cmds.connectAttr(material+".outColor", shadingGroup+".rman__surface")
		cmds.connectAttr(lambert+".outColor", shadingGroup+".surfaceShader")
		
		displacementRemap = cmds.shadingNode("PxrDispTransform", asUtility=True, name= nameAsset +"_dispTransform")
		displacement = cmds.shadingNode("PxrDisplace", asShader=True, name= matName +"_displacement")

		cmds.connectAttr(displacement +".outColor",  shadingGroup+".rman__displacement")

		## Create Bin
		cmds.binMembership( (shadingGroup,material,displacement,lambert), addToBin="bin_" + nameAsset+ idName )

		for texture in listTextures:
			## Add to BIN
			cmds.binMembership( texture, addToBin="bin_" + nameAsset+ idName )
			## Find the filename
			multi = False
			if cmds.nodeType(texture) == "PxrTexture":
				filename = cmds.getAttr(texture+".filename")
			elif cmds.nodeType(texture) == "PxrMultiTexture":
				filename = cmds.getAttr(texture+".filename0")
				multi = True
			## Set to Linear if Albedo
			if (".jpg") in filename:
				linear = True
				##print(texture + " " + str(linear))
			else:
				linear = False
			## Create Connection per Channel
			if "Albedo" in texture:
				cmds.connectAttr(texture+ outColor, material + colorConnect, f = True)
				## OPGL
				cmds.connectAttr(texture+ outColor, lambert + ".color", f = True)
				##if linear == True:
				cmds.setAttr(texture+ ".linearize",1)
			if "Specular" in texture:
				cmds.connectAttr(texture + outColorR, material + specularConnect, f = True)
			if "Roughness" in texture:
				cmds.connectAttr(texture+ outColorR, material + specularRoughnessConnect, f = True)
			if "Translucency" in texture:
				cmds.connectAttr(texture+ outColor, material + translucency, f = True)
				cmds.setAttr(material + ".subsurface", 0.5 )
				cmds.setAttr(texture+ ".linearize",1)
			if "Normal" in texture:
				bump = cmds.shadingNode("PxrNormalMap", asUtility = True, name= material + "_normal")
				## Connect to Texture to Bump Node
				cmds.connectAttr(texture + outColor, bump + ".inputRGB",force = True)
				##	cmds.connectAttr(manifold + ".result", bump + ".manifold",force = True)
				## Connect to Material
				cmds.connectAttr(bump + ".resultN", matName + normal, force= True)
				cmds.setAttr(bump+".bumpScale",0.5)
				##cmds.setAttr(bump+".invertBump",1)
				##cmds.setAttr(texture+ ".linearize",1)
				cmds.setAttr(bump+ ".filename",filename, type="string")
			if "Opacity"in texture:
				cmds.connectAttr(texture+ outColorR, material +opacity, force= True)
				cmds.setAttr(texture+ ".linearize",1)
			if "Displacement" in texture:
				cmds.connectAttr(texture+ outColorR, displacementRemap +".dispScalar", f= True)
				cmds.connectAttr(displacementRemap + ".resultF", displacement +".dispScalar", f= True)
				cmds.setAttr(displacement +".dispAmount",1)
				cmds.setAttr(displacementRemap +".dispRemapMode",2)
				cmds.setAttr(displacementRemap +".dispHeight",0.5)
				cmds.setAttr(displacementRemap +".dispDepth",0.5)
				cmds.setAttr(displacementRemap +".dispCenter",0.5)
				cmds.setAttr(texture+ ".linearize",1)

			## Add Subdiv Attributes
			if not importedMObject == None:
				for obj in importedMObject:
					shapes = cmds.listRelatives(obj, shapes=True)
					try:
						cmds.setAttr(shapes[0] + ".rman_subdivScheme", 1)
						cmds.setAttr(shapes[0] + ".rman_preventPolyCracks", 1)
						cmds.setAttr(shapes[0] + ".rman_displacementBound", displacementBound)
					except:
						pass
		cmds.select(clear= True)
		## Graph in the hyperShade
		cmds.hyperShade(downStream = shadingGroup )
		##Assign Shader
		if not importedMObject == None:
			##for listObj in importedMObject:
			for obj in importedMObject:
				if cmds.objectType( obj, isType="transform" ):
					selection = cmds.select(obj, add= True)
					try:
						cmds.hyperShade(assign= material )
						print("Shader assigned to: " + obj)
					except:
						"No suitable object"
				else:
					print(obj)
		else:
			print("No object to assign to")

def loadMegascansShaderR(jsonShader, listTextures,nameAsset,geometry,manifold,idName,):
	nodes = readShaderJson(jsonShader)

	## Create Bin
	cmds.binMembership( nodes+listTextures, addToBin="bin_" + nameAsset + idName )
	try:
		mel.eval('refreshHyperShadeBinsUI "hyperShadePanel1Window|hyperShadePanel1|binsWrapForm" true;')
	except:
		pass

	outColor = ".resultRGB"
	outColorR = ".resultR"
	outColorA = ".resultA"

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
			renamedNode =cmds.rename(node, nameAsset+nodeSuffixe)
			if cmds.nodeType(renamedNode) == "shadingEngine":
				shadingGroup = renamedNode
			if cmds.nodeType(renamedNode) == "lambert" or cmds.nodeType(renamedNode) == "blinn":
				materialOGL = renamedNode
		else:
			if "albedo" in node.lower() and cmds.nodeType(node) == "PxrColorCorrect":
				albedoConnector = node
			if "roughness" in  node.lower() and cmds.nodeType(node) == "PxrColorCorrect":
				roughnessConnector = node
			if "specular" in  node.lower() and cmds.nodeType(node) == "PxrColorCorrect":
				specularConnector = node
			if "translucency" in  node.lower() and cmds.nodeType(node) == "PxrColorCorrect":
				translucencyConnector = node
			if "opacity" in  node.lower() and cmds.nodeType(node) == "PxrColorCorrect":
				opacityConnector = node
			if "fuzz" in  node.lower() and cmds.nodeType(node) == "PxrColorCorrect":
				fuzzConnector = node
			if "ao" in  node.lower() and cmds.nodeType(node) == "PxrColorCorrect":
				aoConnector = node
			if "metalness" in node.lower() and cmds.nodeType(node) == "PxrColorCorrect":
				metalnessConnector = node
			if "normal" in  node.lower() and cmds.nodeType(node) == "PxrColorCorrect":
				normalConnector = node
			if "displacement" in  node.lower() and cmds.nodeType(node) == "PxrColorCorrect":
				displacementConnector = node

	## Connect Texture to Shader Connector
	for texture in listTextures:
		# print (texture)
		if "albedo" in texture.lower() and albedoConnector != None:
			cmds.connectAttr(texture + outColor, albedoConnector+ ".inputRGB", f = True)
			if materialOGL != None:
				cmds.connectAttr(texture + outColor, materialOGL+ ".color", f = True)
			cmds.setAttr(texture+ ".linearize",1)
		if "specular" in texture.lower() and specularConnector != None:
			cmds.connectAttr(texture + outColor, specularConnector+ ".inputRGB", f = True)
		if "roughness" in texture.lower() and roughnessConnector !=None:
			cmds.connectAttr(texture + outColor, roughnessConnector+ ".inputRGB", f = True)
		if "translucency" in texture.lower()  and translucencyConnector!=None:
			cmds.connectAttr(texture + outColor, translucencyConnector+ ".inputRGB", f = True)
			cmds.setAttr(texture+ ".linearize",1)
		if "opacity" in texture.lower() and opacityConnector != None :
			cmds.connectAttr(texture + outColor, opacityConnector+ ".inputRGB", f = True)
		if "fuzz" in texture.lower()  and fuzzConnector != None:
			cmds.connectAttr(texture + outColor, fuzzConnector+ ".inputRGB", f = True)
		if "metalness" in texture.lower()  and metalnessConnector != None:
			cmds.connectAttr(texture + outColor, metalnessConnector+ ".inputRGB", f = True)
		if "normal" in texture.lower() and normalConnector !=None:
			cmds.connectAttr(texture + outColor, normalConnector+ ".inputRGB", f = True)
		if "displacement" in texture.lower() and displacementConnector !=None:
			cmds.connectAttr(texture + outColor, displacementConnector+ ".inputRGB", f = True)

	materials = cmds.listConnections( shadingGroup +'.rman__surface', d=False, s=True )

	cmds.select(clear= True)
	cmds.hyperShade(downStream = shadingGroup )

	## Assign Shader to Geo
	if not geometry == None:
		for geo in geometry:
			if cmds.objectType( geo, isType="transform" ):
				selection = cmds.select(geo, add= True)
				try:
					cmds.setAttr(geo+".displayColors",False)
				except:
					print("Could not set the display colors on the geometry")
					pass
				try:
					cmds.select(materials[0], add= True)
					cmds.hyperShade(assign= materials[0] )
					print("Shader assigned to: " + geo)
				except:
					"No suitable object to assign a shader"
			else:
				print (geo)

		## Set Subdiv and Displacement Settings
		setGeoDisplacementSettings(geometry)

def setGeoDisplacementSettings(geometries):
	displacementBound = 0.75
	for geo in geometries:
		shapes = cmds.listRelatives(geo, shapes=True)
		try:
			cmds.setAttr(shapes[0] + ".rman_subdivScheme", 1)
			cmds.setAttr(shapes[0] + ".rman_preventPolyCracks", 1)
			cmds.setAttr(shapes[0] + ".rman_displacementBound", displacementBound)
		except:
			pass

def createSharedRmanTexture(sharedUV,triplanar):
	manifold =""
	if triplanar == False  and sharedUV == True:
		manifold = cmds.shadingNode("PxrManifold2D", asUtility=True)
	elif triplanar == True and sharedUV == True:
		manifold = cmds.shadingNode("PxrRoundCube", asUtility=True)
		cmds.setAttr( manifold + ".numberOfTextures", 3)
	return manifold

def createTextureFileRman(sharedUV,triplanar,manifold,filename,newName):
	if sharedUV == False and triplanar == False:
		textureFile = cmds.shadingNode('PxrTexture', asTexture=True)
		texturePlacement = cmds.shadingNode("PxrManifold2D", asUtility=True)
		cmds.connectAttr( texturePlacement + ".result", textureFile+".manifold", force = True)
		cmds.select(textureFile)
	elif sharedUV == True and triplanar == False :
		textureFile = cmds.shadingNode('PxrTexture', asTexture=True)
		cmds.connectAttr( manifold + ".result", textureFile+".manifold", force = True)
		cmds.select(textureFile)
	elif sharedUV == False and triplanar == True:
		textureFile = cmds.shadingNode('PxrMultiTexture', asTexture=True)
		texturePlacement = cmds.shadingNode("PxrRoundCube", asUtility=True)
		cmds.setAttr( texturePlacement + ".numberOfTextures", 3)
		cmds.connectAttr( texturePlacement + ".resultMulti", textureFile+".manifoldMulti", force = True)
		cmds.select(textureFile)
	elif sharedUV == True and triplanar == True:
		textureFile = cmds.shadingNode('PxrMultiTexture', asTexture=True)
		cmds.connectAttr( manifold + ".resultMulti", textureFile+".manifoldMulti", force = True)

	if triplanar == False:
		cmds.setAttr(textureFile+".filename", filename, type="string")
	else:
		cmds.setAttr(textureFile+".filename0", filename, type="string")
		cmds.setAttr(textureFile+".filename1", filename, type="string")
		cmds.setAttr(textureFile+".filename2", filename, type="string")

	textureFile =cmds.rename(textureFile, newName)

	try:
		cmds.select(textureFile)
		return textureFile
	except:
		print("No texture to select")

def findVDBCommand():
	shelf = cfg().config_dir.join('shelf.json')
	with open(shelf) as jfile:
		dictionary = json.load(jfile,object_pairs_hook=OrderedDict)
			
	#print(dictionary["shelf"]["buttons"].keys())
	commandVDB = dictionary["shelf"]["buttons"]["rfmShelfPxrVolume"]["popup"]["items"]["rfmShelfVDB"]["command"]
	return commandVDB

### Needs an improvement
def createVDB(name,commandLine,pathVDB):
	## Create VDB
	command = findVDBCommand()
	if command:
		exec("mel.eval('"+command+"')")
	else:
		print("Could not create the VDB Container")
		return ""
		
	## Find it back Read VDB
	vdbContainer = cmds.ls (sl =True)
	## Set File Path
	cmds.setAttr(vdbContainer[0]+".VdbFilePath",pathVDB,type = "string")
	## Find the OpenVDBVisualiser
	parent = cmds.listConnections(vdbContainer[0],plugs = False, type="OpenVDBVisualize")
	shape = cmds.listRelatives(parent,shapes=True)
	## Cannot work for now, as it can only appear after loading
	try:
		cmds.setAttr(shapes[0]+"VdbAllGridNames",1)
	except Exception as e:
		print(e)

	## Rename
	cmds.rename(parent,name)

	return vdbContainer
	
######################################## Lights ###############################################

def createLight(lgtType):
	rfm2.api.nodes.create_and_select(lgtType)
	newLgt = cmds.ls(selection = True,long = True)[0]
	return newLgt

####################################################################################################################
############################################## Shader Export #######################################################

def traverse(node,children):
	listNodule =[]
	listSkip = ["transform","expression","time","groupId" ]
	if cmds.objExists(node) :
		listNodule =[]
		connections = cmds.listConnections(node,source=True,destination=False,skipConversionNodes=True) or {}
		for child in connections:
			typeID = str(cmds.nodeType(child))
			if typeID not in listSkip:
				if typeID != 'groupId':
					children[child]= {}
					listNodule.append(child)
			# elif typeID == "transform":
				# listShapes = getShape(child)
				# listNodule.append(listShapes[0])
				# print("Skipped: ", child, typeID)

	return listNodule

def get_nodes(node,children,listNodeName):
	listNodeName += traverse(node,children)
	for child in children:
		get_nodes(child,children[child],listNodeName)
	return listNodeName

def buildDictionary(shadingGroup):
	listNodes =[]
	listNodes.append(shadingGroup)
	listNodule =[]
	children={}
	cleanDic= {}
	# if shader == True:
	listSkip = ["transform","expression","time","groupId" ]
	# else:
		# listSkip = ["expression","time","groupId" ]
	# Test it is a shading Group
	if str(cmds.nodeType(shadingGroup)) not in listSkip:	
		listItem = get_nodes(shadingGroup,children,listNodes)
		for item in listItem:
			attribAll = {}
			attribMulti = {}
			attribString = {}
			idShad = cmds.nodeType(item)
			if idShad not in listSkip:
				listAttribAll = cmds.listAttr(item,c=True,k=True,multi = True)
				if listAttribAll:
					for attribute in listAttribAll:
						try:
							valueAttr = cmds.getAttr(item + "."+ attribute )
							attribAll[attribute] = valueAttr
						except:
							pass

				connectionsAttr = cmds.listConnections(item,d=False, s=True,connections =True,plugs=True)
				data = {}
				data[idShad] = []
				data[idShad].append({
				'connections':connectionsAttr,
				'attributes':attribAll
				})
				cleanDic[item] = data
	elif str(cmds.nodeType(shadingGroup)) == "transform":
		print("Test")
	else:
		print("Wrong type of data detected: " + str(cmds.nodeType(shadingGroup)))
	# print("Dictionary Created: ", cleanDic)
	return cleanDic

def findWholeWord(word):
	return re.compile(r'\b({0})\b'.format(word), flags=re.IGNORECASE).search

def readShaderJson(jsonFile):
	listConnect = []
	listNodesCreated = []
	listShaders = ["PxrBlack","PxrConstant","PxrSurface","PxrConstant","PxrLayerSurface","PxrMarschnerHair","PxrVolume","PxrDiffuse","PxrDisney","PxrDisneyBsdf","aiStandardSurface","aiStandardHair","aiTwoSided","aiLayerShader"]
	listLights = ['PxrEnvDayLight','PxrMeshLight','PxrSphereLight',"PxrDomeLight","PxrRectLight","PxrDistantLight","PxrDiskLight","PxrCylinderLight","PxrPortalLight","PxrAovLight"]
	
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
					elif "principledshader" in nodeToCreate:
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
												print("Attribute Value is none, do nothing")
											else:
												pm.setAttr(node+"."+nameAttribute, valueAttribute)
									except:
										# print ("Couldn't set: " + nameAttribute + " " + str(valueAttribute))
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
						# print("Couldn't connect :" +outputParameter + " to " + inputParameter)
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
