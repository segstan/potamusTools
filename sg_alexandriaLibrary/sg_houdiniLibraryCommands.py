import hou
import toolutils
import os
import sys
import json
from collections import OrderedDict
import nodegraphalign
import logging
import sg_alexandriaConstants
import re
import sg_functions as fcn

pythonVersion = (sys.version_info[0])
if pythonVersion == 3:
	import imp
	imp.reload(sg_alexandriaConstants)
	imp.reload(fcn)
if pythonVersion == 2:
	reload(sg_alexandriaConstants)
	reload(fcn)

##################################################### Generic ########################################################
def getCurrentContextNode():
	nodeEditor = toolutils.networkEditor()
	currentNode = nodeEditor.pwd()
	typeCategory = currentNode.childTypeCategory().name()
	path = currentNode.path()

	position = nodeEditor.visibleBounds().center()

	return currentNode,typeCategory,path,position

def createNetworkBox(listItems,text,nodeInfos):
	context = nodeInfos[1]
	pathContext = nodeInfos[2]
	positionCenterofNodework = nodeInfos[3]

	networkBox= hou.node(pathContext).createNetworkBox()
	networkBox.setComment(text)
	for item in listItems:
		# print(item.name())
		if item:
			if item.parentNetworkBox() is None:
				try:
					networkBox.addItem(item)
				except:
					#print("Error with: "+ item.name())
					pass

	networkBox.fitAroundContents()
	return networkBox

def cleanSelection():
	for node in hou.selectedNodes():
		node.setSelected( False, clear_all_selected = True)

def layoutSelection(container):
	listNodes = []
	for node in container.children():
		if node in hou.selectedNodes():
			listNodes.append(node)
	container.layoutChildren(items = (listNodes))

def layoutChildren(topNode):
	topNode.layoutChildren()

def getSnapshot(filename):
	curDesktop = hou.ui.curDesktop()
	desktop = curDesktop.name()
	curPanels = hou.ui.currentPaneTabs()
	#viewer = hou.paneTabType.SceneViewer
	#viewer = hou.paneTabType.IPRViewer
	for panel in curPanels:
		if panel.type() == hou.paneTabType.IPRViewer:
			viewer = hou.paneTabType.IPRViewer
			break
		elif panel.type() == hou.paneTabType.SceneViewer:
			viewer = hou.paneTabType.SceneViewer
			break
		else:
			viewer = ""
			print("Snapshot could not be done: ")
			return 
	# Switch for the screengrab between the 2 main viewports
	if viewer == hou.paneTabType.SceneViewer:
		panetab = curDesktop.paneTabOfType(viewer).name()
		camera = curDesktop.paneTabOfType(viewer).curViewport().name()
		cameraPath = desktop + "." + panetab + "." + "world." + camera 
		frame = hou.frame()
		image = hou.hscript("viewwrite -f %d %d %s '%s'" % (frame,frame,cameraPath,filename))
	elif viewer == hou.paneTabType.IPRViewer:
		image = curDesktop.paneTabOfType(hou.paneTabType.IPRViewer).saveFrame(filename)
	
	print("Snapshot Done: ", filename)

def findIntinString(word):
	listNumber = [int(s) for s in re.findall(r'\d+',word)]
	return listNumber

def findUpperLetterinWord(word):
	listUpper = []
	for letter in word:
		if letter.isupper():
			listUpper.append(letter)
	return listUpper

def findAllParents(node,listParent):
	# Return a node list
	listParent = node.inputs()
	if listParent:
		listParent += findAllParents(listParent[-1],listParent)

	return listParent

######################################################################################################################

def importVDB(vdbPath,nameAsset, nameModel,nodeInfos):
	context = nodeInfos[1]
	pathContext = nodeInfos[2]
	positionCenterofNodework = nodeInfos[3]

	if context == "Object":
		if hou.node(pathContext+"/"+nameModel):
			containerVDB = hou.node(pathContext+"/"+nameModel)
		else:
			containerVDB = hou.node(pathContext).createNode('geo',nameModel)
		vdbNode = containerVDB.createNode('file',"file_"+nameAsset)
		vdbNode.setPosition(positionCenterofNodework)
		parameter =vdbNode.parm('file').set(vdbPath)
	elif context == "Sop": # Geometry
		containerVDB = hou.node(pathContext)
		vdbNode = containerVDB.createNode('file',"file_"+ nameAsset)
		vdbNode.setPosition(positionCenterofNodework)
		parameter =vdbNode.parm('file').set(vdbPath)
	elif context == "Lop": ## Solaris
		if hou.node(pathContext+"/"+nameAsset):
			containerVDB = None
		else:
			containerVDB = None
		vdbNode = hou.node(nodeInfos[2]).createNode('volume',"volume_"+nameModel)
		vdbNode.setPosition(positionCenterofNodework)
		vdbNode.parm('filepath1').set(vdbPath)
		vdbNode.parm('primpath').set("/" + nameModel+ "/volume")

	## Set global Parameters
	if containerVDB != None:
		containerVDB.moveToGoodPosition()
	vdbNode.moveToGoodPosition()

	return [containerVDB,vdbNode]

def importMegascansModel(modelPath,nameMegascan,nameAsset,nodeInfos):
	context = nodeInfos[1]
	pathContext = nodeInfos[2]
	positionCenterofNodework = nodeInfos[3]

	if context == "Object": ## obj
		if hou.node(pathContext+"/"+nameMegascan):
			containerGeo = hou.node(pathContext+"/"+nameMegascan)
		else:
			containerGeo = hou.node(pathContext).createNode('geo',nameMegascan)

		modelGeo = containerGeo.createNode('file',"file_" + nameAsset)
		unpack = containerGeo.createNode('unpack',"unpack_" + nameAsset)
		getName = containerGeo.createNode('name',"name_" + nameAsset)
		materialAssign = containerGeo.createNode('material',"matAssign_"+ nameAsset)
		usdconfigure = containerGeo.createNode('usdconfigure',"usdconfigure_"+nameAsset)

	elif context == "Sop": ## Geometry
		containerGeo = hou.node(pathContext)
		modelGeo = hou.node(pathContext).createNode('file',"file_"+nameAsset)
		modelGeo.setPosition(positionCenterofNodework)
		unpack = containerGeo.createNode('unpack',"unpack_"+nameAsset)
		getName = containerGeo.createNode('name',"name_"+nameAsset)
		materialAssign = containerGeo.createNode('material',"matAssign_"+nameAsset)
		usdconfigure = containerGeo.createNode('usdconfigure',"usdconfigure_"+nameAsset)

		usdconfigure.setDisplayFlag(True)
		usdconfigure.setRenderFlag(True)

	elif context == "Lop": ## Solaris
		if hou.node(pathContext+"/"+nameMegascan):
			containerGeo = hou.node(pathContext+"/"+nameMegascan)
		else:
			containerGeo = hou.node(nodeInfos[2]).createNode('sopcreate',nameMegascan)
			containerGeo.setPosition(positionCenterofNodework)
			
		modelGeo = hou.node(containerGeo.path()+"/sopnet/create/").createNode('file',"file_"+nameAsset)
		containerGeo.parm('pathprefix').set("/$OS/model")

		unpack = hou.node(containerGeo.path()+"/sopnet/create/").createNode('unpack',"unpack")
		getName = hou.node(containerGeo.path()+"/sopnet/create/").createNode('name',"name")
		usdconfigure = hou.node(containerGeo.path()+"/sopnet/create/").createNode('usdconfigure',"usdconfigure_"+nameAsset)

	## Connect and set nodes 
	unpack.parm('detail_attributes').set(1)
	unpack.parm('transfer_attributes').set("*")
	unpack.setInput(0,modelGeo)
	unpack.moveToGoodPosition()

	getName.parm('attribname').set("name")
	getName.parm('donamefromgroup').set(1)
	getName.parm('namefromgroupmask').set("_*")
	getName.parm('numnames').set(0)
	getName.setInput(0,unpack)
	getName.moveToGoodPosition()

	materialAssign.parm('group1').set("*")
	materialAssign.setInput(0,getName)
	materialAssign.moveToGoodPosition()

	usdconfigure.parm('enable_polygonsassubd').set(1)
	usdconfigure.parm('polygonsassubd').set(1)
	usdconfigure.setInput(0,materialAssign)
	usdconfigure.setDisplayFlag(True)
	usdconfigure.moveToGoodPosition()
	connector = usdconfigure

	## Set global Parameters
	parameter= modelGeo.parm('file').set(modelPath)
	containerGeo.moveToGoodPosition()
	modelGeo.moveToGoodPosition()

	return [containerGeo,modelGeo,connector,materialAssign]

def importMPCMegascansLop(nameAsset):
	from mpc.tessa import uri
	from houdinitemplatemanager.shelftools import templateshelftools

	nodes = templateshelftools.importHipTemplateAsset('assetversion:MPC.faces.rnd.rnd_julien-b:houdiniTemplate.usd_propMegascans:vLatest',moveTemplate = True)
	lopLayerNode = nodes[0]
	lopLayerNode.moveToGoodPosition()

	if os.getenv("SHOT"):
		sequenceName = os.getenv("SHOT").split("/")[0]
		shotName = os.getenv("SHOT").split("/")[-1]
	else:
		sequenceName = ""
		shotName = ""

	### PROP Node ###
	lopLayerNode.parm('scene').set(sequenceName)
	lopLayerNode.parm('shot').set(shotName)
	lopLayerNode.parm('name').set(nameAsset)
	lopLayerNode.parm('name').pressButton()

	### MODEL NODE ###
	modelNode = lopLayerNode.node('EDIT/model')
	modelNode.parm('scene').set(sequenceName)
	modelNode.parm('shot').set(shotName)
	modelNode.parm('name').set(nameAsset+'_model')
	modelNode.parm('name').pressButton()

	### SHADER NODE ###
	shaderNode = lopLayerNode.node('EDIT/shader')
	shaderNode.parm('scene').set(sequenceName)
	shaderNode.parm('shot').set(shotName)
	shaderNode.parm('name').set(nameAsset+'_shader')
	shaderNode.parm('name').pressButton()

	return lopLayerNode,modelNode,shaderNode

def importMPCMegascansModel(assetLop,modelPath,mpcLOD):
	modelLop = hou.node(assetLop[1].path())
	sopImport= hou.node(assetLop[1].path()+'/EDIT/USD_sopImport/SOPNET')

	lods = hou.node(sopImport.path()).allSubChildren()

	modelGeo = hou.node(sopImport.path()).createNode('file',"file")
	modelGeo.parm('file').set(modelPath)

	unpack = hou.node(sopImport.path()).createNode('unpack',"unpack")
	unpack.parm('detail_attributes').set(1)
	unpack.parm('transfer_attributes').set("*")
	unpack.setInput(0,modelGeo)

	getName = hou.node(sopImport.path()).createNode('name',"name")
	getName.parm('attribname').set("name")
	getName.parm('donamefromgroup').set(1)
	getName.parm('namefromgroupmask').set("_*")
	getName.parm('numnames').set(0)
	getName.setInput(0,unpack)

	usdconfigure = hou.node(sopImport.path()).createNode('usdconfigure',"usdconfigure")
	usdconfigure.parm('enable_polygonsassubd').set(1)
	usdconfigure.parm('polygonsassubd').set(1)
	usdconfigure.setInput(0,getName)
	usdconfigure.setDisplayFlag(True)
	connector = usdconfigure

	for lod in lods:
		if lod.type().name() == "output":
			if mpcLOD in lod.name():
				lod.setInput(0,connector)

	hou.node(sopImport.path()).layoutChildren()

	return sopImport,modelGeo,connector

def findLOD(lod):
	print(lod)

def importMegascansShaderLop(assetLop,nameAsset):
	shaderLop = hou.node(assetLop[2].path())
	materialLibrary = hou.node(assetLop[2].path()+"/EDIT/materiallibrary")
	assignMaterial = hou.node(assetLop[2].path()+"/EDIT/assignmaterial")

	## Create Geometry Settings
	geometrySettings = hou.node(shaderLop.path()+"/EDIT").createNode('rendergeometrysettings',"rendergeometrysettings")
	## Settings
	geometrySettings.parm('primpattern').set("/`chs('../../../../name')`/model")
	## Shading
	geometrySettings.parm('xn__primvarstracedisplacements_hjbf').set(True)
	geometrySettings.parm('xn__primvarstracedisplacements_control_iwbf').set("set")
	geometrySettings.parm('xn__primvarsdisplacementboundsphere_mrbr').set(1)
	geometrySettings.parm('xn__primvarsdisplacementboundsphere_control_n4br').set("set")
	## Geometry
	geometrySettings.parm('xn__primvarspolygonsmoothdisplacement_vubh').set(1)
	geometrySettings.parm('xn__primvarspolygonsmoothdisplacement_control_w7bh').set("set")
	geometrySettings.parm('xn__primvarsdicepretessellate_uhbe').set(1)
	geometrySettings.parm('xn__primvarsdicepretessellate_control_vube').set("set")

	## Connection
	geometrySettings.setInput(0,materialLibrary)
	assignMaterial.setInput(0,geometrySettings)

	position = materialLibrary.position()
	geometrySettings.moveToGoodPosition()
	materialLibrary.moveToGoodPosition()

	## Fix small issue on assignment ( not really needed but cleaner )
	materialLibrary.parm('matpathprefix').set("/`chs('../../../../name')`/Looks/")

	return shaderLop,materialLibrary,assignMaterial,geometrySettings

def createMegascansAtlas(path,nameAsset,nodeInfos):
	context = nodeInfos[1]
	pathContext = nodeInfos[2]
	positionCenterofNodework = nodeInfos[3]

	if context == "Object":
		containerAtlas = hou.node('/obj').createNode('geo',nameAsset)
		atlasNode = hou.node(containerAtlas.path()).createNode('SCTR_megascansAtlas',"SCTR_atlas_"+nameAsset)
		containerAtlas.setPosition(positionCenterofNodework)
	elif context == "Sop": ## Geometry
		atlasNode = hou.node(pathContext).createNode('SCTR_megascansAtlas',"SCTR_atlas_"+nameAsset)
		atlasNode.setDisplayFlag(True)
		atlasNode.setPosition(positionCenterofNodework)
	elif context == "Lop": ## Solaris Not Really Needed
		containerAtlas = hou.node(pathContext).createNode('sopcreate',nameAsset)
		atlasNode = hou.node(containerAtlas.path()+"/sopnet/create/").createNode('SCTR_megascansAtlas',"SCTR_atlas_"+nameAsset)
		atlasNode.setPosition(positionCenterofNodework)
	atlasNode.parm('basedir').set(path)

	print( " - Atlas Created: " + atlasNode.name())

def createContainerShader(nameAsset,nodeInfos,containerGeometry):
	houdiniContext = nodeInfos[1]
	houdiniNodePath = nodeInfos[2]
	houdiniContextPos = nodeInfos[3]

	if type(containerGeometry) == list:
		containerGeo = containerGeometry[0]
		modelGeo = containerGeometry[1]
		try:
			modelPosition = modelGeo.position()
		except:
			modelPosition = houdiniContextPos
	else:
		containerGeo = containerGeometry
		modelPosition = houdiniContextPos

	if houdiniContext == "Object" or houdiniContext == "Sop" and not "/stage" in houdiniNodePath :
		if containerGeo :
			containerShader = hou.node(containerGeo.path()).createNode('matnet',nameAsset+"_Shader")
		else:
			containerShader = hou.node("/obj").createNode('matnet',nameAsset+"_Shader")
	elif houdiniContext == "Lop":
		containerShader = hou.node(houdiniNodePath).createNode('materiallibrary',nameAsset+"_Shader")
	elif houdiniContext == "Vop":
		containerShader = hou.node(houdiniNodePath)
	else:
		print("You are in the context: " + houdiniContext)
	try:
		position = (modelPosition[0]+ 5,modelPosition[1])
		containerShader.setPosition(position)
		containerShader.moveToGoodPosition()
	except:
		print("ERROR POSITIONNING CONTAINER MATERIAL")
		pass
	return containerShader

def createMaterialAssignSOP(nameShader,containerGeo):
	## Got the container geo list input
	##
	##Create the material Assign
	materialAssign = hou.node(containerGeo[0].path()).createNode('material',"material_"+nameShader)

	## connect to File
	materialAssign.setInput(0,containerGeo[2])

	materialAssign.setDisplayFlag(True)
	materialAssign.setRenderFlag(True)

	materialAssign.moveToGoodPosition()

	return materialAssign

def setLOPVariant(container):
	containerGeo = hou.node(container.path()+"/EDIT/")
	allNode = containerGeo.children()
	for node in allNode:
		#print (node.type().name())
		if node.type().name() == "USD_createvariantSet":
			#print(node.name())
			if "proxy" in node.name():
				node.parm('variantname1').set("LodA")
			if "model" in node.name():
				node.parm('variantname1').set("LodA")

def assignShaderOnModel(shadingGroup,index,containerShader,containerGeo,shape,materialAssign,nodeInfos,houdiniMPC):
	pathContainer = containerShader.path()	
	context = nodeInfos[1]
	pathContext = nodeInfos[2]
	centerPosition= nodeInfos[3]

	allGroups= [g.name() for g in containerGeo[2].geometry().primGroups()]
	houMaterialExists = False
	if context == "Object" or context == "Sop" and not "/stage" in pathContainer:
		## List Group
		allGroups= [g.name() for g in containerGeo[2].geometry().primGroups()]
		if allGroups:
			amount = materialAssign.parm('num_materials').eval()
			for i in range(1,amount):
				material = materialAssign.parm('shop_materialpath%d' %i).eval()
				if material == containerShader.path()+ "/" + shadingGroup:
					for group in allGroups:
						if shape in group:
							geo = materialAssign.parm('group%d' %i).eval()
							materialAssign.parm('group%d' %i).set(geo + " " + group)
							materialAssign.parm('shop_materialpath%d' %i).set(containerShader.path()+ "/" + shadingGroup)
					houMaterialExists = True

			if houMaterialExists == False:
				amount += 1
				materialAssign.parm('num_materials').set(amount)
				for group in allGroups:
					if shape in group:
						materialAssign.parm('group%d' %amount).set(group)
						materialAssign.parm('shop_materialpath%d' %amount).set(containerShader.path()+ "/" + shadingGroup)
		materialAssign.setRenderFlag(True)
	elif context == "Lop":
		if index != 1:
			containerShader.parm('materials').insertMultiParmInstance(index-1)
			materialAssign.parm('nummaterials').insertMultiParmInstance(index-1)
		if houdiniMPC == True:
			## Material Library
			containerShader.parm('matnode%d' %index).set(containerShader.path()+ "/" + shadingGroup)
			containerShader.parm('matpath%d' %index).set("/`chs('../../../../name')`/Looks/" + shadingGroup)
			## Assign Material
			materialAssign.parm('primpattern%d' %index).set("/`chs('../../../../name')`/model/**/*" + shape)
			materialAssign.parm('matspecpath%d' %index).set("/`chs('../../../../name')`/Looks/"+shadingGroup)

	materialAssign.setDisplayFlag(True)
	
	
	return materialAssign

def convertTexAutomatic(listTextures):
	import sg_batchTextureConvert

	converter = "TEX (Prman)"
	commandlineDict = sg_batchTextureConvert.GenericCommand.getValidChildCommands()
	convert_command = commandlineDict[converter]
	settings = ["TEX (Prman)","Texture","periodic","periodic","short"]
	listActionsTex = [converter,convert_command,settings]
	return listActionsTex

###############################################################################################################################
############################################### Import/Export Lightrig ########################################################
###############################################################################################################################

def hierarchyDict(node,dictLights,dictConnections,listLights,nodeInfos):
	children = node.outputs()
	longname = node.name()
	name = node.name()
	nodePath = node.path() 
	containerPath = nodePath.split(name)[0]
	
	parents = findAllParents(node, [])
	nameParents = [input.name() for input in parents]
	nameParents.reverse()
	longNameHierarchy = "|".join(nameParents)
	# Check parenting
	if parents:
		longname = "|" + longNameHierarchy + "|" + name
	else:
		longname = node.name()
	nodeTpe = node.type().description()
	shapes = []
	shapeType = ""
	connectionSum = None
	expression = ""
	# Get Matrix
	try:
		matrix = node.worldTransform().asTuple()
		xForm = [(node.parm("tx").eval(),node.parm("ty").eval(),node.parm("tz").eval())]
		xForm.append((node.parm("rx").eval(),node.parm("ry").eval(),node.parm("rz").eval()))
		xForm.append((node.parm("sx").eval(),node.parm("sy").eval(),node.parm("sz").eval()))
	except:
		matrix = []
		xForm = []
		pass
	# Check if it is a light or a null
	if nodeTpe in listLights:
		# shapes = [node.name()]
		nodeTpe = "transform"
		shapes = [node.name()]
		shapeType = node.type().description()
	else:
		if nodeTpe == "Null":
			nodeTpe = "group"
		else:
			print("Unknown Node, will not be exported: ", name,nodeTpe)

	# Attributes Dictionary
	attributesDict ={}
	attributesShapeDict = {}
	
	# Take the attributes of the transform
	attributes = [ parm.name() for parm in node.parms()]
	#dictConnections = {}
	if attributes:
		for attribute in attributes:
			valueAttr  = node.parm(attribute).eval()
			typeAttr = node.parm(attribute).parmTemplate().type().name()
			# Need to check for nodes with non absolute path
			if typeAttr.lower() == "string" and containerPath in valueAttr:
				valueAttr = "../" + valueAttr.split(containerPath)[-1]
			if typeAttr != "Ramp":
				# Fill Attribute Dictionary
				attributesShapeDict = fcn.addEntryAttributesDic(attributesShapeDict,attribute,valueAttr,typeAttr)
			# Ramp 
			elif typeAttr == "Ramp":
				rampDic = {}
				parmRamp = node.parm(attribute).eval()
				amountPoints = len(parmRamp.keys())
				if parmRamp.isColor() == True:
					typeRamp = "colorRamp"
				else:
					typeRamp = "floatRamp"
				## Build ramp dictionary (mathing maya name convention)
				valueAttr = buildRampParmsDict(rampDic,attribute,parmRamp)

				## Fill the classic attributes Dic with extra Ramp Details where value is a dictionary now
				attributesShapeDict[attribute] = {
				'value': OrderedDict(valueAttr),
				'type': typeAttr,
				'points': amountPoints,
				'typeRamp': typeRamp,
				'dcc': "houdini",
				}
	
	## Emulate connections like maya
	dictConnections = buildConnectionsDic(dictConnections,node)
	# Write Hierarchy Dictionary
	if children :
		fcn.addEntryLgtRigDic(dictLights,name,longname,shapes,shapeType,nodeTpe,attributesShapeDict,{},expression,matrix,xForm,attributesDict)
		for child in children:
			hierarchyDict(child, dictLights[longname]["children"],dictConnections,listLights,nodeInfos)
	else:
		fcn.addEntryLgtRigDic(dictLights,name,longname,shapes,shapeType,nodeTpe,attributesShapeDict,{},expression,matrix,xForm,attributesDict)

	return dictLights,dictConnections

def buildConnectionsDic(dictConnections,node):
	attributes = [ parm.name() for parm in node.parms()]
	parents = findAllParents(node, [])
	nameParents = [input.name() for input in parents]
	nameParents.reverse()
	longNameNodeHierarchy = "|".join(nameParents)
	dictConnectionInfos = {}
	#print("Long name Parent ",longNameHierarchy, node.name())
	for attribute in attributes:
		if attribute in sg_alexandriaConstants.sgListConnectionParms:
			# Found connections
			if attribute == 'shop_lightfilterpaths':
				amount = node.parm(attribute).eval()
				for i in range(0,amount):
					valueConnection = node.parm('shop_lightfilterpath%d' %i).eval()
					lightBlocker = hou.node(valueConnection.split("matnet")[0])
					if lightBlocker:
						parents = findAllParents(lightBlocker, [])
						nameParents = [input.name() for input in parents]
						nameParents.reverse()
						longNameBlockerHierarchy = "|".join(nameParents)
						# it will be shape related for a blocker - Need a better solution
						nodeKey = longNameNodeHierarchy + "|" + node.name() + "|" + node.name() +"Shape"
						# Must assume that it will be outColor connected for a Blocker
						tuppleData = (longNameBlockerHierarchy + "|" + lightBlocker.name()+"|" + lightBlocker.name() +"Shape",(node.name()+"."+'rman__lightfilters[%d]' %i,lightBlocker.name()+".outColor"))
						dictConnectionInfos = fcn.addEntryConnectionDic(dictConnectionInfos,i,tuppleData)
	if dictConnectionInfos:
		dictConnections[nodeKey]= {
			"connections": dictConnectionInfos,
			}
	#print(json.dumps(dictConnections,indent = 4 ))
	return dictConnections

def rebuildHierarchy(container,dicLights,dicConnections,dicLightInfos,nodeInfos,listNodesCreated):
	dccAtCreation = dicLightInfos["dcc"]
	houdiniContext = nodeInfos[1]
	houdiniNodePath = nodeInfos[2]
	houdiniContextPos = nodeInfos[3]
	newObj = ""
	for key in dicLights:
		obj = key
		attributesDict = dicLights[obj]["attributes"]
		shapeAttributesDict = dicLights[obj]["shapeAttributes"]
		connectedNodes = dicLights[key]["connectedNodes"]
		objectToSetAttributes = ""
		parentObj = obj.rsplit("|",1)[0].split("|")[-1]
		if parentObj == obj:
			parentObj = "None"
		try:
			childrenDict = dicLights[obj]["children"]
		except:
			childrenDict = {}
		if dicLights[obj]["nodeType"] == "group":
			name = obj.split("|")[-1]
			if houdiniContext == "Object":
				# Create Transform
				newObj = container.createNode("null", name)
			elif houdiniContext == "Lop":
				# Create Null
				newObj = container.createNode("xform", name)
			print("\n-- Create Null: " + obj + " with parent: " + parentObj + " --")
			objectToSetAttributes = newObj
			# Adding for graph
			listNodesCreated.append(newObj)

		elif dicLights[obj]["nodeType"] == "transform":
			if houdiniContext == "Object":
				# Create Light
				name = obj.split("|")[-1]
				lgtType =  dicLights[obj]["shapeType"]
				shape = dicLights[obj]["shape"][0].rsplit("|",1)[0]
				if houdiniContext == "Object":
					try:
						newObj = container.createNode(lgtType.lower(), name,run_init_scripts = True)
					except:
						continue
				elif houdiniContext == "Lop":
					continue
				objectToSetAttributes = newObj
				print("\n-- Create Object: " + lgtType + " with parent: " + obj.rsplit("|",1)[0].split("|")[-1] + " --")
				# Adding for graph
				listNodesCreated.append(newObj)
			
		# Set Matrix/Transform
		matrix = dicLights[obj]["matrix"]
		matrix = matrixConvert(matrix)
		xForm = dicLights[obj]["xForm"]
		if newObj:
			if houdiniContext == "Object":
				print(" Set Transformation on  " + obj)
				if dccAtCreation != "katana":
					setMatrix(newObj,matrix)
				elif dccAtCreation == "katana":
					#print(" Set Xform instead of Matrix")
					setLGTxForm(xForm,newObj)
				if dccAtCreation == "maya" and  dccAtCreation == "katana" and dicLights[obj]["shapeType"] == "PxrDomeLight":
				## Difference of 180 deg between maya and houdini for the dome light
					extraRotY = 180
					newObj.parm("ry").set(newObj.parm("ry").eval()+extraRotY)

		# Parenting
		parenName = obj.rsplit("|",1)[0].split("|")[-1]
		parenPath =  container.path() + "/" + parenName
		paren = hou.node(parenPath)
		if paren != container.path() and newObj != paren:
			newObj.setInput(0,paren)
			newObj.moveToGoodPosition()

		# Set Attributes on node
		if objectToSetAttributes:
			print(" Set Attributes on: " + objectToSetAttributes.name())
			listAttributesNotFound = []
			if attributesDict:
				listAttributesNotFound = setAttributesForRig(attributesDict,dicLightInfos,objectToSetAttributes)
			if shapeAttributesDict:
				listAttributesNotFound = setAttributesForRig(shapeAttributesDict,dicLightInfos,objectToSetAttributes)
			if listAttributesNotFound and shapeAttributesDict:
				# Retry to see if there was dynamic paramaters:
				setDynamicAttributes(listAttributesNotFound,shapeAttributesDict,objectToSetAttributes)

		# Create Connected Nodes
		listNodesCreated = rebuildConnectedNodesHierarchy(container,connectedNodes,nodeInfos,listNodesCreated)

		# Traverse again with
		rebuildHierarchy(container,childrenDict,dicConnections,dicLightInfos,nodeInfos,listNodesCreated)

def matrixConvert(listMatrix):
	if type(listMatrix) == list:
		try:
			matrix = hou.Matrix4(listMatrix)
		except:
			matrix = []
			pass
	else:
		matrix = hou.Matrix4()

	return matrix

def setMatrix(obj,matrixA):
	if matrixA:
		obj.setWorldTransform(matrixA)

def setLGTxForm(xForm,newObj):
	newObj.parm("tx").set(xForm[0][0])
	newObj.parm("ty").set(xForm[0][1])
	newObj.parm("tz").set(xForm[0][2])

	newObj.parm("rx").set(xForm[1][0])
	newObj.parm("ry").set(xForm[1][1])
	newObj.parm("rz").set(xForm[1][2])

	newObj.parm("sx").set(xForm[2][0])
	newObj.parm("sy").set(xForm[2][1])
	newObj.parm("sz").set(xForm[2][2])

def rebuildConnectedNodesHierarchy(container,connectedNodes,nodeInfos,listNodesCreated):
	# Will build all the connected nodes
	if connectedNodes :
		for key in connectedNodes:
			nameNewNode = connectedNodes[key]["name"]                                                                                                                                                                                            
			nodeToCreate = connectedNodes[key]["nodeType"]
			connectedNewNodes = connectedNodes[key]["connectedNodes"]
			node = hou.node(container.path() + "/"+ nameNewNode)
			# Create New nodes
			if not node:
				print("-- Create Node: " + nameNewNode + " as: " + nodeToCreate + " --")
			else:
				print( "-- Node Already exist: " + nameNewNode + ", reuse it" )
			# iterate and build all the nodes
			if connectedNewNodes:
				rebuildConnectedNodesHierarchy(connectedNewNodes)

	return listNodesCreated

def rebuildConnections(container,dictConnections,dicLightInfos):
	dccAtCreation = dicLightInfos["dcc"]
	for key in dictConnections:
		node = key
		print("-- Setting Connections on "+ node + " --")
		dictLink = dictConnections[node]["connections"]
		for key in dictLink:
			# if json was generated from maya or katana. the connections will be treated like that
			if dccAtCreation == "maya" or dccAtCreation == "katana":
				linkIn = dictLink[key]["link"][1][0]
				linkOut = dictLink[key]["link"][1][1]
				nodeIn = linkIn.split(".")[0]
				nodeOut = linkOut.split(".")[0]

				channelConnectionIn = linkIn.split(".")[-1]
				channelConnectionOut = linkOut.split(".")[-1]
				
				# Will Detect blocker connections for now
				if "rman__lightfilters" in channelConnectionIn:
					if "Shape" in nodeIn:
						nodeIn = nodeIn.split("Shape")[0]
					if "Shape" in nodeOut:
						nodeOut = nodeOut.split("Shape")[0]
					node =  hou.node(container.path() + "/" + nodeOut)
					light = hou.node(container.path() + "/" + nodeIn)
					if light and node:
						print(" Set Connections between: ",light.name(), " and ", node.name())
						shaderType = node.type().description().lower()
						# Add to the Shader Parms
						addLightFilterShader(light,node,shaderType)
			elif dccAtCreation == "houdini":
				print(" No Need to Connections - Ignored")

def setAttributesForRig(attributesDict,dicLightInfos,node):
	listParametersSet = []
	listParametersNotSet = []
	listParametersNotFound = []
	listParametersConverted = []
	dccAtCreation = dicLightInfos["dcc"]

	if node != "":
		for key in attributesDict:
			attribute = key
			typeAttr = attributesDict[key]["type"]
			if typeAttr == "Ramp":
				if node.parm(attribute) :
					dictRamp = attributesDict[attribute]["value"]
					points = attributesDict[attribute]["points"]
					dcc = attributesDict[attribute]["dcc"]
					# Create Ramp
					if "color" in attribute.lower():
						rampType = "colorRamp"
					else:
						rampType = "floatRamp"
					rampData = createRampParameter(points,rampType)
					print("Ramp Detected - Amount of points to create: " + str(points) + " on ramp: " + attribute )
					node.parm(attribute).set(rampData)
					setRampAttributesForRig(dictRamp,node,dcc)
			else:
				# convert Attribute to Houdini Name but keep the key value in dictionary as original name to find it back 
				if attribute in sg_alexandriaConstants.sgDicConvertLightNameParameter[dccAtCreation+"-houdini"]:
					attribute = sg_alexandriaConstants.sgDicConvertLightNameParameter[dccAtCreation+"-houdini"][key]
					listParametersConverted.append(attribute)
					#print("Convert attribute name to Houdini Friendly Name: " + attribute)
				
				typeAttr = attributesDict[key]["type"]
				if typeAttr == "float3":
					if type(attribute) == list:
						for i in range(0,len(attribute)):
							if node.parm(attribute[i]) :
								node.parm(attribute[i]).set(attributesDict[key]["value"][0][i])
							else:
								listParametersNotFound.append(attribute)
					else:
						if node.parm(attribute) :
							try:
								node.parm(attribute).set(attributesDict[key]["value"][0][0],attributesDict[key]["value"][0][1],attributesDict[key]["value"][0][2])
								listParametersSet.append(key)
							except:
								#print(sys.exc_info())
								listParametersNotSet.append(key)
								pass
						else:
							listParametersNotFound.append(attribute)
				else:
					if node.parm(attribute) :
						try:
							node.parm(attribute).set(attributesDict[key]["value"])
							listParametersSet.append(key)
						except:
							#print(sys.exc_info())
							listParametersNotSet.append(key)
							pass
					else:
						listParametersNotFound.append(attribute)
				
				## Fix for Blocker and Renderman 
				if attribute == "coordsys":
					node.parm("coordsys").set(node.path())

		#print("  Parameters Set on "+ node.name() + ": " + "\n" + '\n'.join("- " + str(p) for p in sorted(listParametersSet)))
		if listParametersNotSet:
			print("  Parameters Not Set on "+ node.name() + ": " + "\n" + '\n'.join("- " + str(p) for p in sorted(listParametersNotSet)))
		#print("  Parameters Not Found on "+ node.name() + ": " + "\n" + '\n'.join("- " + str(p) for p in sorted(listParametersNotFound)))
	else:
		print("Node is empty, check json")

	return listParametersNotFound

def setDynamicAttributes(listParms,attributesDict,node):
	## Dynamic attributes created previously, need a reset to be working
	listParametersSet = []
	listParametersNotSet = []
	listParametersNotFound = []
	for parm in listParms:
		if parm in attributesDict:
			valueAttr = attributesDict[parm]["value"]
			typeAttr = attributesDict[parm]["type"]
			if typeAttr == "float3":
				try:
					node.parm(parm).set(valueAttr[0][0],valueAttr[0][1],valueAttr[0][2])
					listParametersSet.append(parm)
				except:
					#print(sys.exc_info())
					listParametersNotSet.append(parm)
					pass
			else:
				try:
					node.parm(parm).set(valueAttr)
					listParametersSet.append(parm)
				except:
					#print(sys.exc_info())
					listParametersNotSet.append(parm)
					pass
		else:
			#print("Attribute not found: " + attribute + " on node: " + node.name() + " - IGNORED ")
			listParametersNotFound.append(parm)
	if listParametersSet:
		print("  Parameters Finally Set on "+ node.name() + ": " + "\n" + '\n'.join("- " + str(p) for p in sorted(listParametersSet)))
	return listParametersNotFound

def buildRampParmsDict(rampDic,attribute,parmRamp):
	## basis is Interp, key is Position, value is value or color
	## Will store that as Maya with a base 0 
	## Ramp are build with 3 different types of variables: Position(position),Value(value) and Interpolation (interp)
	## Maya = attributeName[index].attributeName_typeV with an index at base 0
	## Houdini = attributeNameIndexType with an index a base 1
	## Katana = 

	amountPoints = len(parmRamp.keys())
	for i in range(0,amountPoints):
		# position
		nameRampPointPositionParm = attribute + "[" + str(i) + "]." + attribute + "_Position"
		valueRampPointPositionParm = parmRamp.keys()[i]
		typeRampPointPositionParm = "Float"
		# interp
		nameRampPointBasis = attribute + "[" + str(i) + "]." + attribute + "_Interp"
		valueRampPointBasisParm = getMenuIndexForInterpolation(parmRamp.basis()[i])
		typeRampPointBasisParm = "Enum"

		if parmRamp.isColor() == True:
			# Color value
			nameRampPointValue = attribute + "[" + str(i) + "]." + attribute + "_Color"
			valueRampPointValueParm = [parmRamp.values()[i]]
			typeRampPointValueParm = "Float3"
		else:
			# value
			nameRampPointValue = attribute + "[" + str(i) + "]." + attribute + "_Value"
			valueRampPointValueParm = parmRamp.values()[i]
			typeRampPointValueParm = "Float"

		## Add to Dictionary
		# Position
		rampDic[nameRampPointPositionParm] = {
		'value': valueRampPointPositionParm,
		'type': typeRampPointPositionParm,
		}

		# Interp
		rampDic[nameRampPointBasis] = {
		'value': valueRampPointBasisParm,
		'type': typeRampPointBasisParm,
		}

		# Value
		rampDic[nameRampPointValue] = {
		'value': valueRampPointValueParm,
		'type': typeRampPointValueParm,
		}
	
	OrderedDict(rampDic)
	return rampDic

def getMenuIndexForInterpolation(interp):
	if "Constant" in str(interp):
		menu = 0
	elif "Linear" in str(interp):
		menu = 1
	elif "Catmull-Rom" in str(interp):
		menu = 2
	elif "MonotoneCubic" in str(interp):
		menu = 3
	elif "Bezier" in str(interp):
		menu = 3
	elif "B-Spline" in str(interp):
		menu = 4
	elif "Hermite" in str(interp):
		menu = 4
	else:
		menu = 2
	return menu

def setRampAttributesForRig(attributesDict,node,dcc):
	## Ramp are build with 3 different types of variables: Position(position),Value(value) and Interpolation (interp)
	## Maya = attributeName[index].attributeName_typeV with an index at base 0
	## Houdini = attributeNameIndexType with an index a base 1
	## Katana = 
	for key in attributesDict:
		attribute = key
		typeAttr = attributesDict[key]["type"]
		valueAttr = attributesDict[key]["value"]

		if dcc == "houdini":
			if node.parm(attribute) :
				if typeAttr == "float3":
					node.parm(attribute).set(valueAttr[0][0],valueAttr[0][1],valueAttr[0][2])
				else:
					node.parm(attribute).set(valueAttr)
		elif dcc == "maya":
			# Need conversion
			attributeName = attribute.split("[")[0]
			index = findIntinString(attribute)
			if "." in attribute:
				typeV =  attribute.split(".")[-1].split("_")[-1]
			else:
				typeV = ""
			if "Position" in typeV:
				typeV = "pos"
			elif "Interp" in typeV or "Value" in typeV:
				typeV = typeV.lower()
			elif "Color" in typeV:
				upper = findUpperLetterinWord(typeV)
				typeV = "".join(upper).lower()
				# Skip Color and a float3
				if typeV == "c":
					typeV = ""

			convertedAttribute = attributeName+str(index[0]+1)+typeV
			if typeV != "" and node.parm(convertedAttribute) :
				#print("SUCCEED: " + convertedAttribute)
				node.parm(convertedAttribute).set(valueAttr)
		elif dcc == "katana":
			print("TO BE IMPLEMENTED")

def createRampParameter(points,rampType):
	bases = [hou.rampBasis.Linear]*points
	keys = []
	values = []

	colorValues = []
	colorDefault = (0,0,0)
	if points != 0:
		keyFactor = 1.0/int(points)
	else:
		keyFactor = 0.0
	keyVal = 0.0

	if rampType == "floatRamp":
		for p in range(0,points):
			keyVal += keyFactor
			keys.append(keyVal)
			values.append(keyVal)
		rampData = hou.Ramp(bases,keys,values)
	elif rampType == "colorRamp":
		for p in range(0,points):
			keyVal += keyFactor
			keys.append(keyVal)
			colorValues.append(colorDefault)
		rampData = hou.Ramp(bases,keys,colorValues)
	else:
		rampData = hou.Ramp()
	return rampData

def addLightFilterShader(light,lightFilter,shader):
	# Get size of Parameter - Add a new one, then set it back 
	if light:
		if light.parm('shop_lightfilterpaths'):
			amount = light.parm('shop_lightfilterpaths').eval()
			# Create a new one
			light.parm('shop_lightfilterpaths').set(amount+1)
			# Set it 
			light.parm('shop_lightfilterpath%d' %amount).set(lightFilter.path() + "/matnet/" + shader )

def findLightsInHierarchy(topNode,listLGTShapes,listLightsType):
	nodeType = topNode.type().description()
	nodePath = topNode.path()
	if nodeType in listLightsType:
		listLGTShapes.append(nodePath)

	if topNode.outputConnections():
		children = [findLightsInHierarchy(child,listLGTShapes,listLightsType) for child in topNode.outputs() ]

	return listLGTShapes

def findTextureFilesOnNodes(listLights):
	# Only look for first level of connections 
	dictMaps = {}
	for lgt in listLights:
		## Mostly for Rman Lights right now
		node = hou.node(lgt)
		objectType =  node.type().description()
		if objectType in sg_alexandriaConstants.sgDicAllLightTextures:
			attributes = sg_alexandriaConstants.sgDicAllLightTextures[objectType]
			for attribute in attributes:
				## Dodgy in case there are more than one attributes that can receive a map for Rman Lights
				textureMap = node.parm(attribute).eval()
				dictMaps[lgt]={
						'type': objectType,
						'textureMap': textureMap,
						'attribute': attribute,
						}
		# connections = cmds.listConnections(lgt, type="aiImage" )
		# if connections:
		# 	for node in connections:
		# 		textureMap = cmds.getAttr(node + ".filename")
		# 		objectType = cmds.objectType(node)
		# 		dictMaps[node]={
		# 			'type': objectType,
		# 			'textureMap': textureMap,
		# 			'attribute': "filename",
		# 			}
		# connections = cmds.listConnections(lgt, type="file" )
		# if connections:
		# 	for node in connections:
		# 		textureMap = cmds.getAttr(node + ".fileTextureName")
		# 		objectType = cmds.objectType(node)
		# 		dictMaps[node]={
		# 			'type': objectType,
		# 			'textureMap': textureMap,
		# 			'attribute': "fileTextureName",
		# 			}
	return dictMaps

##################################### Import Light Rig ###############################################

def importLgtRig(nameAsset,dicLights,dicConnections,dicLightInfos,houdiniInfos):
	listNodesCreated = []
	if houdiniInfos[1] == "Object":
		container = hou.node("obj/").createNode("subnet",nameAsset)
		listNodesCreated.append(container)
	elif houdiniInfos[1] == "Lop":
		container =  hou.node("stage/").createNode("subnet",nameAsset)
		listNodesCreated.append(container)
	else:
		print("Unknown context: not Supported by the tool ", listNodesCreated,type(listNodesCreated))

	rebuildHierarchy(container,dicLights,dicConnections,dicLightInfos,houdiniInfos,listNodesCreated)
	rebuildConnections(container,dicConnections,dicLightInfos)

	return listNodesCreated

##################################################################################################

def traverseGraph(node,children):
	listNodule =[]
	if node!= None:
		listNodule =[]
		connections = node.inputs() or {}
		for child in connections:
			if child != None:
				children[child]= {}
				listNodule.append(child)
	return listNodule

def getNodes(node,children,listNodeName):
	listNodeName += traverseGraph(node,children)
	for child in children:
		if child!= None :
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

		id = node.type().name().split("::")[0]
		if id == "pxrtexture":
			attributeFilename = "filename"
			textureFound = True
		elif id =='pxrmultitexture':
			attributeFilename = ["filename0","filename1","filename2","filename3","filename4","filename5","filename6","filename7","filename8","filename9"]
			textureFound = True

		if id == "pxrtexture":
			originalTexturePath = hou.node(node.path()).parm(attributeFilename).eval()
			if textureFound == True:
				data[node.name()+"."+attributeFilename] = {
				'filepath':originalTexturePath
				}
				dictFilePath[node] = data
		elif id == 'PxrMultiTexture':
			for attribute in attributeFilename:
				originalTexturePath = hou.node(node.path()).parm(attribute).eval()
				if originalTexturePath not in listFilepath:
					listFilepath.append(originalTexturePath)
				if textureFound == True and originalTexturePath != "":
					data[node.name()+"."+attribute] = {
					'filepath':originalTexturePath
					}
					dictFilePath[node] = data
		
	return dictFilePath

## Need conversion
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