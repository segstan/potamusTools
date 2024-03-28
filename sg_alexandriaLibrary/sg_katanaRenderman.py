import os
import sys
import json
import random
from collections import OrderedDict

import Katana
from Katana import NodegraphAPI
from Katana import KatanaFile
from Katana import UI4

def createGroup(name):
	group = NodegraphAPI.CreateNode('Group', NodegraphAPI.GetRootNode())
	group.setName(str(name))

	## Move Node to Center of NodeGraph
	centerNodePosition(group)

	return group

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

def createSharedRmanManifold(sharedUV,triplanar,container,name,xPos):
	TIME= 0
	manifold =""
	if triplanar == False  and sharedUV == True:
		## Create Manifold 2D
		manifold = NodegraphAPI.CreateNode('PrmanShadingNode', container)
		## Setup to Manifold 2d
		manifold.getParameter('nodeType').setValue("PxrManifold2D",TIME)
		manifold.getParameter('name').setValue(str(name)+"_manifold2D",TIME)
		manifold.setName(name)
		manifold.checkDynamicParameters(True)
		## Offset Node
		NodegraphAPI.SetNodePosition(manifold, (xPos-750,0))
		
	elif triplanar == True and sharedUV == True:
		## Create Manifold RoundCube
		manifold = NodegraphAPI.CreateNode('PrmanShadingNode',container)
		## Setup to Manifold Triplanar
		manifold.getParameter('nodeType').setValue("PxrRoundCube",TIME)
		manifold.getParameter('name').setValue(str(name)+"_manifoldTriplanar",TIME)
		manifold.setName(name)
		manifold.checkDynamicParameters(True)
		## Offset Node
		NodegraphAPI.SetNodePosition(manifold, (xPos-750,0))
		## Setting Value
		manifold.getParameter('parameters.numberOfTextures.value').setValue(3.0,0)
		manifold.getParameter('parameters.numberOfTextures.enable').setValue(1.0,0)

	NodegraphAPI.SetNodeSelected(manifold,True)
	NodegraphAPI.SetNodeFloating(manifold,True)

	return manifold

def createTextureFileRman(sharedUV,triplanar,manifold,filepath,container,name,xPos,yPos):
	TIME= 0
	filepath += ".tex"
	name = str(name)

	if sharedUV == False and triplanar == False:
		## Create Texture Prman Node and Create Manifold
		textureFile = NodegraphAPI.CreateNode('PrmanShadingNode',container)
		## Setup to Texture
		textureFile.getParameter('nodeType').setValue("PxrTexture",TIME)
		textureFile.checkDynamicParameters(True)
		## Set Parameters and Enable it 
		textureFile.getParameter('parameters.filename.value').setValue(str(filepath),TIME)
		textureFile.getParameter('parameters.filename.enable').setValue(1.0,TIME)
		## Rename Node
		textureFile.getParameter('name').setValue(name,TIME)
		textureFile.setName(name)
		## Offset Node
		NodegraphAPI.SetNodePosition(textureFile, (xPos,yPos))
		## Create Manifold 2D
		manifold = NodegraphAPI.CreateNode('PrmanShadingNode', container)
		## Setup to Manifold 2d
		manifold.getParameter('nodeType').setValue("PxrManifold2D",TIME)
		manifold.checkDynamicParameters(True)
		## Rename Node
		manifold.getParameter('name').setValue(name+"_manifold2D",TIME)
		## Offset Node
		NodegraphAPI.SetNodePosition(manifold, (0,0))
		## Get I/O
		manifoldOutPort = manifold.getOutputPort("result")
		textureFileInPort = textureFile.getInputPort("manifold")
		## Connect Manifold2d to texture
		textureFileInPort.connect(manifoldOutPort)
	elif sharedUV == True and triplanar == False :
		## Create Texture Prman Node and Reuse Manifold
		textureFile = NodegraphAPI.CreateNode('PrmanShadingNode',container)
		## Setup to Texture
		textureFile.getParameter('nodeType').setValue("PxrTexture",TIME)
		textureFile.checkDynamicParameters(True)
		## Set Parameters and Enable it 
		textureFile.getParameter('parameters.filename.value').setValue(str(filepath),TIME)
		textureFile.getParameter('parameters.filename.enable').setValue(1.0,TIME)
		## Rename Node
		textureFile.getParameter('name').setValue(name,TIME)
		textureFile.setName(name)
		## Offset Node
		NodegraphAPI.SetNodePosition(textureFile, (xPos,yPos))
		## Offset Manifold Node
		NodegraphAPI.SetNodePosition(manifold, (-400+xPos,yPos))
		## Get I/O
		manifoldOutPort = manifold.getOutputPort("result")
		textureFileInPort = textureFile.getInputPort("manifold")
		## Connect Manifold2d to texture
		textureFileInPort.connect(manifoldOutPort)
	elif sharedUV == False and triplanar == True:
		## Create Texture Prman Node and Create Manifold
		textureFile = NodegraphAPI.CreateNode('PrmanShadingNode', container)
		## Setup to Texture
		textureFile.getParameter('nodeType').setValue("PxrMultiTexture",TIME)
		textureFile.checkDynamicParameters(True)
		## Set Parameters and Enable it 
		textureFile.getParameter('parameters.filename0.value').setValue(str(filepath),TIME)
		textureFile.getParameter('parameters.filename0.enable').setValue(1.0,TIME)
		textureFile.getParameter('parameters.filename1.value').setValue(str(filepath),TIME)
		textureFile.getParameter('parameters.filename1.enable').setValue(1.0,TIME)
		textureFile.getParameter('parameters.filename2.value').setValue(str(filepath),TIME)
		textureFile.getParameter('parameters.filename2.enable').setValue(1.0,TIME)
		## Rename Node
		textureFile.getParameter('name').setValue(name,TIME)
		textureFile.setName(name)
		## Offset Node
		NodegraphAPI.SetNodePosition(textureFile, (xPos,yPos))
		## Create Manifold RoundCube
		manifold = NodegraphAPI.CreateNode('PrmanShadingNode', container)
		manifold.getParameter('nodeType').setValue("PxrRoundCube",0)
		manifold.checkDynamicParameters(True)
		## Rename Manifold
		manifold.getParameter('name').setValue(name+"_manifoldTriplanar",TIME)
		## Offset Node
		NodegraphAPI.SetNodePosition(manifold, (-400+xPos,yPos))
		## Setting Value
		manifold.getParameter('parameters.numberOfTextures.value').setValue(3.0,0)
		manifold.getParameter('parameters.numberOfTextures.enable').setValue(1.0,0)
		## Get I/O
		manifoldOutPort = manifold.getOutputPort("resultMulti")
		textureFileInPort = textureFile.getInputPort("manifoldMulti")
		## Connect Manifold2d to texture
		textureFileInPort.connect(manifoldOutPort)
	elif sharedUV == True and triplanar == True:
		## Create Texture Prman Node and Reuse Manifold
		textureFile = NodegraphAPI.CreateNode('PrmanShadingNode', container)
		## Setup to Texture
		textureFile.getParameter('nodeType').setValue("PxrMultiTexture",TIME)
		textureFile.checkDynamicParameters(True)
		## Set Parameters and Enable it 
		textureFile.getParameter('parameters.filename0.value').setValue(str(filepath),TIME)
		textureFile.getParameter('parameters.filename0.enable').setValue(1.0,TIME)
		textureFile.getParameter('parameters.filename1.value').setValue(str(filepath),TIME)
		textureFile.getParameter('parameters.filename1.enable').setValue(1.0,TIME)
		textureFile.getParameter('parameters.filename2.value').setValue(str(filepath),TIME)
		textureFile.getParameter('parameters.filename2.enable').setValue(1.0,TIME)
		## Rename Node
		textureFile.getParameter('name').setValue(name,TIME)
		textureFile.setName(name)
		## Offset Node
		NodegraphAPI.SetNodePosition(textureFile, (xPos,yPos))
		## Get I/O
		manifoldOutPort = manifold.getOutputPort("resultMulti")
		textureFileInPort = textureFile.getInputPort("manifoldMulti")
		## Connect Manifold2d to texture
		textureFileInPort.connect(manifoldOutPort)

	NodegraphAPI.SetNodeSelected(textureFile,True)
	NodegraphAPI.SetNodeFloating(textureFile,True)
	return textureFile

def connectMegascansShaderR(listTextures,container,nameAsset,geometry,manifold,idName,childrenAlreadyPresent):
	TIME = 0
	albedoConnector = None
	aoConnector= None
	specularConnector = None
	roughnessConnector = None
	translucencyConnector = None
	opacityConnector = None
	fuzzConnector = None
	normalConnector = None
	
	materialConnector = None
	displaceConnector = None
	shadingGroupConnector=None
	shadingDisplaceConnector=None

	backdrop = None

	outColor = "resultRGB"
	outColorR = "resultR"
	outColorA = "resultA"
	inColor = "inputRGB"

	listManifolds=[]

	xOffset = 400
	yOffset = 50
	
	## Find the network Material to connect Shader aka shadingGroup
	for shader in container.getChildren():
		## Check that the node already present are not gonna be taken in account 
		if shader not in childrenAlreadyPresent:
			## Get shading Group
			if shader.getType() == "NetworkMaterial":
				shadingGroup = NodegraphAPI.GetNode(shader.getName())
				shadingGroupConnector = shader.getInputPort("prmanBxdf")
				shadingDisplaceConnector = shader.getInputPort("prmanDisplacement")
			## Rename the constructor Node
			if "CONSTRUCTOR" in shader.getName():
				nodeSuffixe= shader.getName().split("CONSTRUCTOR")[-1]
				renamedNode = shader.getParameter('name').setValue(str(nameAsset+nodeSuffixe),TIME)

			if shader.getType() == "Backdrop":
				backdrop = shader
				NodegraphAPI.SetNodeFloating(shader,True)
				## Fix position
				# position = NodegraphAPI.GetNodePosition(backdrop)
				# NodegraphAPI.SetNodePosition(shader,(position[0]-xOffset*3.8,position[1]*3.8))
				## Set attr
				attrs = backdrop.getAttributes()
				print(attrs.get('ns_text'))
				if attrs.get('ns_text') == None:
					attrs['ns_text']= nameAsset
					attrs['ns_fontScale']= 6
				else:
					attrs['ns_text'] += "_"+ nameAsset
					attrs['ns_fontScale']= 2
				backdrop.setAttributes(attrs)

			if shader.getType()== "PrmanShadingNode":
				typeNode = str(shader.getParameter("nodeType").getValue(0))
				if typeNode == "PxrSurface":
					materialConnector = shader.getOutputPort("out")
					material = shader
				if typeNode == "PxrDisplace":
					displaceConnector = shader.getOutputPort("out")
					displace = shader
				if typeNode == "PxrManifold2D" or typeNode == "PxrRoundCube":
					listManifolds.append(shader)
				if "albedo" in shader.getName().lower() and typeNode == "PxrColorCorrect":
					albedoConnector = shader.getInputPort(inColor)
					albedo = shader
				if "roughness" in  shader.getName().lower() and typeNode == "PxrColorCorrect":
					roughnessConnector =  shader.getInputPort(inColor)
					roughness = shader
				if "specular" in  shader.getName().lower() and typeNode == "PxrColorCorrect":
					specularConnector =  shader.getInputPort(inColor)
					specular = shader
				if "translucency" in  shader.getName().lower() and typeNode == "PxrColorCorrect":
					translucencyConnector =  shader.getInputPort(inColor)
					translucency = shader
				if "opacity" in  shader.getName().lower() and typeNode == "PxrColorCorrect":
					opacityConnector =  shader.getInputPort(inColor)
					opacity = shader
				if "fuzz" in  shader.getName().lower() and typeNode == "PxrColorCorrect":
					fuzzConnector =  shader.getInputPort(inColor)
					fuzz = shader
				if "ao" in  shader.getName().lower() and typeNode== "PxrColorCorrect":
					aoConnector =  shader.getInputPort(inColor)
					ao = shader
				if "normal" in  shader.getName().lower() and typeNode == "PxrColorCorrect":
					normalConnector =  shader.getInputPort(inColor)
					normal = shader
				if "displacement" in  shader.getName().lower() and typeNode == "PxrColorCorrect":
					displace = shader
					displacementConnector = shader.getInputPort(inColor)

	## If it's a material will connect it to shading group
	if materialConnector != None and shadingGroupConnector !=None:
		materialConnector.connect(shadingGroupConnector)
	if displaceConnector != None and shadingDisplaceConnector != None:
		displaceConnector.connect(shadingDisplaceConnector)
	
	## Connect the textures
	for texture in listTextures:
		textureNode = NodegraphAPI.GetNode(texture)
		if textureNode == None:
			print( "Can't find: " + texture)
		else:
			print( "Found Texture: " + texture)
			NodegraphAPI.SetNodeSelected(textureNode,True)
			NodegraphAPI.SetNodeFloating(textureNode,True)
			if "Albedo" in texture:
				textureOutPort = textureNode.getOutputPort(outColor)
				if albedoConnector:
					albedoConnector.connect(textureOutPort)
					position = NodegraphAPI.GetNodePosition(albedo)
					NodegraphAPI.SetNodePosition(textureNode,(position[0]-xOffset,position[1]))
				textureNode.getParameter('parameters.linearize.value').setValue(1.0,TIME)
				textureNode.getParameter('parameters.linearize.enable').setValue(1.0,TIME)
			elif "Opacity"in texture:
				textureOutPort = textureNode.getOutputPort(outColor)
				if opacityConnector:
					opacityConnector.connect(textureOutPort)
					position = NodegraphAPI.GetNodePosition(opacity)
					NodegraphAPI.SetNodePosition(textureNode,(position[0]-xOffset,position[1]))
			elif "Roughness" in texture:
				textureOutPort = textureNode.getOutputPort(outColor)
				if roughnessConnector:
					roughnessConnector.connect(textureOutPort)
					position = NodegraphAPI.GetNodePosition(roughness)
					NodegraphAPI.SetNodePosition(textureNode,(position[0]-xOffset,position[1]))
			elif "Specular" in texture:
				textureOutPort = textureNode.getOutputPort(outColor)
				if specularConnector:
					specularConnector.connect(textureOutPort)
					position = NodegraphAPI.GetNodePosition(specular)
					NodegraphAPI.SetNodePosition(textureNode,(position[0]-xOffset,position[1]))
				else:
					position = NodegraphAPI.GetNodePosition(albedo)
					NodegraphAPI.SetNodePosition(textureNode,(position[0]-xOffset*2,position[1]))
			elif "Translucency" in texture:
				textureOutPort = textureNode.getOutputPort(outColor)
				if translucencyConnector:
					translucencyConnector.connect(textureOutPort)
					position = NodegraphAPI.GetNodePosition(translucency)
					NodegraphAPI.SetNodePosition(textureNode,(position[0]-xOffset,position[1]))
				textureNode.getParameter('parameters.linearize.value').setValue(1.0,TIME)
				textureNode.getParameter('parameters.linearize.enable').setValue(1.0,TIME)
			elif "Fuzz" in texture:
				textureOutPort = textureNode.getOutputPort(outColor)
				if fuzzConnector:
					fuzzConnector.connect(textureOutPort)
					position = NodegraphAPI.GetNodePosition(fuzz)
					NodegraphAPI.SetNodePosition(textureNode,(position[0]-xOffset,position[1]))
			elif "AO" in texture:
				textureOutPort = textureNode.getOutputPort(outColor)
				if aoConnector:
					aoConnector.connect(textureOutPort)
					position = NodegraphAPI.GetNodePosition(ao)
					NodegraphAPI.SetNodePosition(textureNode,(position[0]-xOffset,position[1]))
			elif "Normal" in texture:
				textureOutPort = textureNode.getOutputPort(outColor)
				## Connection Normal Node to Shader
				if normalConnector:
					normalConnector.connect(textureOutPort)
					position = NodegraphAPI.GetNodePosition(normal)
					NodegraphAPI.SetNodePosition(textureNode,(position[0]-xOffset,position[1]))
			elif "Displace" in texture:
				textureOutPort = textureNode.getOutputPort(outColor)
				if displacementConnector:
					displacementConnector.connect(textureOutPort)
					position = NodegraphAPI.GetNodePosition(displace)
					NodegraphAPI.SetNodePosition(textureNode,(position[0]-xOffset,position[1]))
			else:
				position = NodegraphAPI.GetNodePosition(albedo)
				NodegraphAPI.SetNodePosition(textureNode,(position[0]-xOffset*7,position[1]))

	for manifold in listManifolds:
		position = NodegraphAPI.GetNodePosition(albedo)
		NodegraphAPI.SetNodePosition(manifold,(position[0]-xOffset*4,position[1]))

def buildMegascanShaderR(listTextures,renderer,nameAsset,geo,manifold,container):
	TIME = 0
	matName = str("Mat_"+ renderer +"_"+ nameAsset)
	importedMObject = geo

	xPosBase = 1200
	yPosBase = 2000

	## Connection Shader
	colorConnect = "diffuseColor"
	specularConnect = "specularFaceColor"
	specularRoughnessConnect = "roughSpecularRoughness"
	scalarDisplacement = "dispScalar"
	translucency = "subsurfaceColor"
	bumpShader = "bumpNormal"
	outputNormal = "resultN"
	inputNormal = "inputRGB"
	opacity = "presence"
	fuzz= "fuzzGain"

	outColor = "resultRGB"
	outColorR = "resultR"
	outColorA = "resultA"

	## Find the network Material to connect Shader aka shadingGroup
	for shader in container.getChildren() :
		if shader.getType() == "NetworkMaterial":
			shadingGroup = NodegraphAPI.GetNode(shader.getName())

	## Find shadingGroup port
	shadingGroupBxdfInPort = shadingGroup.getInputPort("prmanBxdf")
	shadingGroupDisplaceInPort = shadingGroup.getInputPort("prmanDisplacement")

	##### Create Material and port out
	material = NodegraphAPI.CreateNode('PrmanShadingNode', container)
	material.getParameter('nodeType').setValue("PxrSurface",TIME)
	material.getParameter('name').setValue(matName,TIME)
	material.checkDynamicParameters(True)

	material.getParameter('parameters.specularFresnelMode.value').setValue(1.0,TIME)
	material.getParameter('parameters.specularFresnelMode.enable').setValue(1.0,TIME)
	material.getParameter('parameters.roughSpecularFresnelMode.value').setValue(1.0,TIME)
	material.getParameter('parameters.roughSpecularFresnelMode.enable').setValue(1.0,TIME)
	material.getParameter('parameters.specularEdgeColor.value.i0').setValue(0.05,TIME)
	material.getParameter('parameters.specularEdgeColor.value.i1').setValue(0.05,TIME)
	material.getParameter('parameters.specularEdgeColor.value.i2').setValue(0.05,TIME)
	material.getParameter('parameters.specularEdgeColor.enable').setValue(1.0,TIME)
	material.getParameter('parameters.specularModelType.value').setValue(1.0,TIME)
	material.getParameter('parameters.specularModelType.enable').setValue(1.0,TIME)
	
	materialOutPort = material.getOutputPort("out")
	# Put it in Position
	NodegraphAPI.SetNodePosition(material, (xPosBase,yPosBase))

	##### Create Displacement Node
	displacement = NodegraphAPI.CreateNode('PrmanShadingNode',container)
	displacement.getParameter('nodeType').setValue("PxrDisplace",TIME)
	displacement.getParameter('name').setValue(matName+"_displace",TIME)
	displacement.checkDynamicParameters(True)
	# Put it in Position
	NodegraphAPI.SetNodePosition(displacement, (xPosBase,yPosBase-2500))
	## Find Diplacement Port
	displacementInPort = displacement.getInputPort("dispScalar")
	displacementOutPort = displacement.getOutputPort("out")

	##### Create Displacement Remap
	displacementRemap = NodegraphAPI.CreateNode('PrmanShadingNode', container)
	displacementRemap.getParameter('nodeType').setValue("PxrDispTransform",TIME)
	displacementRemap.getParameter('name').setValue(matName+"_dispTransform",TIME)
	displacementRemap.checkDynamicParameters(True)
	## Setting disp Transform
	displacementRemap.getParameter('parameters.dispHeight.value').setValue(0.5,TIME)
	displacementRemap.getParameter('parameters.dispHeight.enable').setValue(1.0,TIME)
	displacementRemap.getParameter('parameters.dispDepth.value').setValue(0.5,TIME)
	displacementRemap.getParameter('parameters.dispDepth.enable').setValue(1.0,TIME)
	displacementRemap.getParameter('parameters.dispRemapMode.value').setValue(2.0,TIME)
	displacementRemap.getParameter('parameters.dispRemapMode.enable').setValue(1.0,TIME)
	
	displacementRemapOutPort = displacementRemap.getOutputPort("resultF")
	# Put it in Position
	NodegraphAPI.SetNodePosition(displacementRemap, (xPosBase-800,yPosBase-2500))

	## Connect Port to ShadingGroup
	shadingGroupBxdfInPort.connect(materialOutPort)
	shadingGroupDisplaceInPort.connect(displacementOutPort)
	## Connect Disp Remap to Displacement Node
	displacementInPort.connect(displacementRemapOutPort)

	for texture in listTextures:
		textureNode = NodegraphAPI.GetNode(texture)
		if textureNode == None:
			print( "Can't find: " + texture)
		else:
			print( "Found Texture: " + texture)
			if "Albedo" in texture:
				textureOutPort = textureNode.getOutputPort(outColor)
				textureNode.getParameter('parameters.linearize.value').setValue(1.0,TIME)
				textureNode.getParameter('parameters.linearize.enable').setValue(1.0,TIME)
				materialInPort = material.getInputPort(colorConnect)
				materialInPort.connect(textureOutPort)
			if "Opacity"in texture:
				textureOutPort = textureNode.getOutputPort(outColorR)
				textureNode.getParameter('parameters.linearize.value').setValue(1.0,TIME)
				textureNode.getParameter('parameters.linearize.enable').setValue(1.0,TIME)
				materialInPort = material.getInputPort(opacity)
				materialInPort.connect(textureOutPort)
			if "Roughness" in texture:
				textureOutPort = textureNode.getOutputPort(outColorR)
				materialInPort = material.getInputPort(specularRoughnessConnect)
				materialInPort.connect(textureOutPort)
			if "Specular" in texture:
				textureOutPort = textureNode.getOutputPort(outColor)
				materialInPort = material.getInputPort(specularConnect)
				materialInPort.connect(textureOutPort)
			if "Translucency" in texture:
				textureOutPort = textureNode.getOutputPort(outColor)
				materialInPort = material.getInputPort(translucency)
				textureNode.getParameter('parameters.linearize.value').setValue(1.0,TIME)
				textureNode.getParameter('parameters.linearize.enable').setValue(1.0,TIME)

				material.getParameter('parameters.subsurfaceGain.value').setValue(0.5,TIME)
				material.getParameter('parameters.subsurfaceGain.enable').setValue(1.0,TIME)
				materialInPort.connect(textureOutPort)
			if "Fuzz" in texture:
				textureOutPort = textureNode.getOutputPort(outColorR)
				materialInPort = material.getInputPort(fuzz)
				materialInPort.connect(textureOutPort)
			if "Normal" in texture:
				##### Create Normal Node
				normal = NodegraphAPI.CreateNode('PrmanShadingNode',container)
				normal.getParameter('nodeType').setValue("PxrNormalMap",TIME)
				normal.getParameter('name').setValue(matName+"_normal",TIME)
				normal.checkDynamicParameters(True)
				NodegraphAPI.SetNodePosition(normal, (xPosBase-800,yPosBase-700))
				
				normal.getParameter('parameters.bumpScale.value').setValue(0.5,TIME)
				normal.getParameter('parameters.bumpScale.enable').setValue(1.0,TIME)

				normalRemapInPort = normal.getInputPort(inputNormal)
				normalRemapOutPort = normal.getOutputPort(outputNormal)

				textureOutPort = textureNode.getOutputPort(outColor)
				materialInPort = material.getInputPort(bumpShader)
				## Connection Normal Node to Shader
				materialInPort.connect(normalRemapOutPort)
				## Connection Texture toNormal Node
				normalRemapInPort.connect(textureOutPort)
				
			if "Displace" in texture:
				textureOutPort = textureNode.getOutputPort(outColorR)
				displacement.getParameter('parameters.dispAmount.value').setValue(0.5,TIME)
				displacement.getParameter('parameters.dispAmount.enable').setValue(1.0,TIME)
				displacementRemapInPort = displacementRemap.getInputPort(scalarDisplacement)
				displacementRemapInPort.connect(textureOutPort)

def buildMegascanShaderROLD(listTextures,renderer,nameAsset,geo,manifold,container):
	TIME = 0
	matName = str("Mat_"+ renderer +"_"+ nameAsset)
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

		## Create Material/Opengl/Displacement
		material = NodegraphAPI.CreateNode('PrmanShadingNode', container)
		material.getParameter('nodeType').setValue("PxrSurface",TIME)
		material.getParameter('name').setValue(matName,TIME)
		materialOutPort = material.getOutputPort("out")

		shadingGroup =  NodegraphAPI.CreateNode('NetworkMaterial', container)
		shadingGroup.addShaderInputPort( "prman", "bxdf")
		shadingGroup.addShaderInputPort( "prman", "displacement")
		shadingGroupBxdfInPort = shadingGroup.getInputPort("prmanBxdf")
		shadingGroupDisplaceInPort = shadingGroup.getInputPort("prmanDisplacement")
		shadingGroup.setName(matName+"_SG")

		displacementRemap = NodegraphAPI.CreateNode('PrmanShadingNode', container)
		displacementRemap.getParameter('nodeType').setValue("PxrDispTransform",TIME)
		displacementRemap.getParameter('name').setValue(matName+"_dispTransform",TIME)
		displacementRemap.checkDynamicParameters(True)
		displacementRemapOutPort = displacementRemap.getOutputPort("resultF")

		displacement = NodegraphAPI.CreateNode('PrmanShadingNode', container)
		displacement.getParameter('nodeType').setValue("PxrDisplace",TIME)
		displacement.getParameter('name').setValue(matName+"_displace",TIME)
		displacement.checkDynamicParameters(True)
		displacementInPort = displacement.getInputPort("dispScalar")
		displacementOutPort = displacement.getOutputPort("out")

		shadingGroupBxdfInPort.connect(materialOutPort)
		shadingGroupDisplaceInPort.connect(displacementOutPort)
		displacementInPort.connect(displacementRemapOutPort)

def readShaderJson(jsonFile,nameAsset,containerShader):
	TIME = 0
	xPos = 0
	yPos = 0
	listConnect = []
	listNodesCreated = []
	for shader in containerShader.getChildren() :
		if shader.getType() == "NetworkMaterial":
			shadingGroup = NodegraphAPI.GetNode(shader.getName())

	listNodesCreated.append(shadingGroup)
	if os.path.exists(jsonFile):
		with open(jsonFile) as jfile:
			data = json.load(jfile)
			for key in data:
				nameComponent = key
				dictionnaryInfo = data[key]
				for key in dictionnaryInfo:
					nodeToCreate = key
					if str(nodeToCreate) == "shadingEngine" or str(nodeToCreate) == "collect":
						shadingGroup.setName(nameComponent)
						nodeToCreate = containerShader
					elif str(nodeToCreate) == "lambert" or str(nodeToCreate) == "principledshader":
						continue
					else:
						## Create Node
						node =  NodegraphAPI.CreateNode('PrmanShadingNode', containerShader)
						node.getParameter('nodeType').setValue(str(nodeToCreate),TIME)
						node.getParameter('name').setValue(str(nameComponent),TIME)
						NodegraphAPI.SetNodePosition(node, (0,yPos))
						node.checkDynamicParameters(True)
						## List Parameters on created nodes
						nodeParameters = node.getParameters().getChildren()
						for p in nodeParameters:
							if p.getName()== "parameters":
								parameters =  p.getChildren()
								for parm in parameters:
									nodeParameters.append(parm)
						listParameters = []
						listParametersLower = []
						for parm in nodeParameters:
							listParameters.append(node.getParameter('name').getValue(TIME))
							listParametersLower.append(node.getParameter('name').getValue(TIME).lower())
						
						listNodesCreated.append(node)

					typeAction = dictionnaryInfo[key]
					for action in typeAction:
						j=0
						listType = action
						for key in listType:
							action = key
							actionTypes = listType[action]
							if "attributes" in action:
								for key in actionTypes:
									nameAttribute = key
									valueAttribute = actionTypes[nameAttribute]
									if action == "attributes" and valueAttribute != None:
										if type(valueAttribute) is list :
											valueAttribute = str(valueAttribute)
										elif type(valueAttribute) is bool :
											if valueAttribute == "true" or valueAttribute =="True":
												valueAttribute = 1.0
											elif valueAttribute == "false" or valueAttribute =="False":
												valueAttribute = 1.0
										elif type(valueAttribute) is str :
											valueAttribute = str(valueAttribute)
										else:
											valueAttribute = str(valueAttribute)
										## Check Parameters and Set it
										## Filter individual Color 
										if str(nameAttribute)[-1] == "R" or str(nameAttribute)[-1] == "X":
											add = ".i0"
											nameAttribute = removeLastLetter(str(nameAttribute),-1)
										elif str(nameAttribute)[-1] == "G" or str(nameAttribute)[-1] == "Y":
											add = ".i1"
											nameAttribute = removeLastLetter(str(nameAttribute),-1)
										elif str(nameAttribute)[-1] == "B" or str(nameAttribute)[-1] == "Z":
											add = ".i2"
											nameAttribute = removeLastLetter(str(nameAttribute),-1)
										else:
											add= ""
										## Check Parameters and Set it
										try:
											## Set and Enable the change 
											node.getParameter('parameters.'+str(nameAttribute)+'.value' + add).setValue(valueAttribute,TIME)
											##defaultValue = node.getParameter('parameters.'+str(nameAttribute)+'.value' + add).getValue(TIME)
											##if defaultValue != valueAttribute:
											node.getParameter('parameters.'+str(nameAttribute)+'.enable').setValue(1.0,TIME)

											print("Set: "+ nameComponent +"."+nameAttribute+add + " " +str(valueAttribute) + " "+ str(type(valueAttribute)))
										except:
											indexAttribute = None
											print("Couldn't set: " + nameComponent+ '.parameters.'+str(nameAttribute)+'.value'+add + " "+ str(type(valueAttribute)))
											pass
							elif action == "connections":
								if actionTypes != None:
									for connection in actionTypes:
										listConnect.append(connection)
				yPos += 100
			k=0
			for connect in listConnect:
				if k<len(listConnect)-1 and k % 2 == 0:
					nodeOutToFind = listConnect[k+1].split(".")[0]
					nodeInToFind = connect.split(".")[0]
					nodeOut = None
					nodeIn = None
					node.getBaseType()
					for node in listNodesCreated:
						if node.getBaseType() == "PrmanShadingNode":
							if node.getParameter('name').getValue(TIME) == nodeOutToFind:
								nodeOut = node
							elif node.getParameter('name').getValue(TIME) == nodeInToFind:
								nodeIn = node

							if listConnect[k+1].split(".")[-1] == "outColor" or listConnect[k+1].split(".")[-1] == "bxdf_out":
								connectionOut = "out"
							else:
								connectionOut = listConnect[k+1].split(".")[-1]	
								
							if connect.split(".")[-1] ==  "rman__surface" or connect.split(".")[-1] ==  "shader1":
								connectionIn = "prmanBxdf"
							elif connect.split(".")[-1] ==  "rman__displacement" or connect.split(".")[-1] ==  "shader2":
								connectionIn = "prmanDisplacement"
							else:
								connectionIn = connect.split(".")[-1]
							
						else :
							if node.getName() == nodeOutToFind:
								nodeOut = node
							elif node.getName() == nodeInToFind:
								nodeIn = node

							if listConnect[k+1].split(".")[-1] == "outColor"or listConnect[k+1].split(".")[-1] == "bxdf_out":
								connectionOut = "out"
							else:
								connectionOut = listConnect[k+1].split(".")[-1]

							if connect.split(".")[-1] ==  "rman__surface" or connect.split(".")[-1] ==  "shader1":
								connectionIn = "prmanBxdf"
							elif connect.split(".")[-1] ==  "rman__displacement" or connect.split(".")[-1] ==  "shader2":
								connectionIn = "prmanDisplacement"
							else:
								connectionIn = connect.split(".")[-1]

					print("Connecting : "+ listConnect[k+1].split(".")[0]+ "." +connectionOut + " to " + connect.split(".")[0]+ "." + connectionIn)

					if nodeOut!= None and nodeIn != None:
						OutPort = nodeOut.getOutputPort(connectionOut)
						InPort = nodeIn.getInputPort(connectionIn)

						## Position
						position = NodegraphAPI.GetNodePosition(nodeIn)
						print(nodeIn.getParameter('name').getValue(0) + "     " + str(position))
						NodegraphAPI.SetNodePosition(nodeOut, (position[0]-500,position[1]-500))
						NodegraphAPI.SetNodePosition(nodeIn, (position[0]+500,position[1]))

						try:
							InPort.connect(OutPort)
						except:
							print("Couldn't connect :" +listConnect[k+1].split(".")[0]+ "." +connectionOut + " to " + connect.split(".")[0]+ "." + connectionIn)
							pass
					else:
						print("Couldn't find nodes: "+ listConnect[k+1] + " and " + connect)

					k +=1
				else:
					k +=1
	##containerShader.layoutChildren()
	return listNodesCreated

def removeLastLetter(word,position):
	l = list(word)  # convert to list

	l[position] = ""    # "delete" letter h (the item actually still exists but is empty)
	del(l[position])    #  delete it

	word = "".join(l)  # convert back to string
	return word

def getOrderDict(item):
	# Get Order value from Dict
	order = item[1]['order']
	return order



