import hou
import os
import json
import toolutils

def createSharedRmanTexture(sharedUV,triplanar,containerTexture,name):
	manifold =""
	if triplanar == False  and sharedUV == True:
		manifold= containerTexture.createNode('pxrmanifold2d',"manifold2D_"+name )
	elif triplanar == True and sharedUV == True:
		manifold = containerTexture.createNode('pxrroundcube',"pxrroundcube_"+name)
		manifold.parm("numberOfTextures").set(3)
	return manifold

def createTextureFileRman(sharedUV,triplanar,manifold,name,path,containerTexture):
	path +=".tex"
	if sharedUV == False and triplanar == False:
		textureFile = containerTexture.createNode('pxrtexture',name)
		textureFileName = hou.evalParm(textureFile.path()+"/filename")
		parameter = textureFile.parm('filename').set(path)
		manifold= containerTexture.createNode('pxrmanifold2d',name+"_manifold2D" )
		textureFile.setInput(3,manifold)
	elif sharedUV == True and triplanar == False :
		textureFile = containerTexture.createNode('pxrtexture',name)
		textureFileName = hou.evalParm(textureFile.path()+"/filename")
		parameter = textureFile.parm('filename').set(path)
		textureFile.setInput(3,manifold)
	elif sharedUV == False and triplanar == True:
		textureFile = containerTexture.createNode('pxrmultitexture',name)
		##textureFileName = hou.evalParm(textureFile.path()+"/filename")
		textureFileName = path
		parameter0 = textureFile.parm('filename0').set(path)
		parameter1 = textureFile.parm('filename1').set(path)
		parameter2 = textureFile.parm('filename2').set(path)
		manifold = containerTexture.createNode('pxrroundcube',name+"_pxrroundcube")
		manifold.parm("numberOfTextures").set(3)
		textureFile.setInput(0,manifold,1)
	elif sharedUV == True and triplanar == True:
		textureFile = containerTexture.createNode('pxrmultitexture',name)
		##textureFileName = hou.evalParm(textureFile.path()+"/filename")
		textureFileName = path
		parameter0 = textureFile.parm('filename0').set(path)
		parameter1 = textureFile.parm('filename1').set(path)
		parameter2 = textureFile.parm('filename2').set(path)
		textureFile.setInput(0,manifold,1)

	textureFile.moveToGoodPosition()
	manifold.moveToGoodPosition()

	subnetNode = hou.node(textureFile.path())
	subnetmanifold = hou.node(manifold.path())
	
	# textureFile.setSelected(True)
	# manifold.setSelected(True)

	return [textureFileName,subnetNode,subnetmanifold]

def createMaterialBuilder(nameShader,containerShader):
	pxrMaterialBuilder = hou.node(containerShader.path()).createNode('pxrmaterialbuilder',nameShader)

	uselessCollector = hou.node(pxrMaterialBuilder.path()+"/output_collect")
	uselessCollector.destroy()

	return pxrMaterialBuilder

def findAddSpareRmanParameters(nameShelf):
	script = ""
	#nameShelf = "RenderMan25"
	shelves = hou.shelves.shelves()
	for shelf in shelves:
		if shelf == nameShelf:
			listTools = shelves[nameShelf].tools()
			for tool in listTools:
				if tool.name() == 'rman_spareparms':
					script = tool.script()
					#print(script)
					#exec(script)
					return script
	if script == "":
		return False

def addRendermanParameters(listNodes):
	rfhtree = hou.getenv("RFHTREE")
	nameRenderman = rfhtree.split("/")[-1].split("For")[0]
	mainVersionRenderman = rfhtree.split("/")[-1].split("-")[-1].split(".")[0]
	nameShelf = nameRenderman+mainVersionRenderman
	print("Shelf Name: " + nameShelf)
	# Get addParameter Script
	script = findAddSpareRmanParameters(nameShelf)
	if script != False:
		hou.clearAllSelected()
		for node in listNodes:
			node.setSelected(True)
		# Add Renderman Parameters
		exec(script)
		# Set Renderman Parameters
		for node in listNodes:
			node.parm("rendersubd").set(True)
			node.parm("ri_polygon_smoothnormals").set(True)
			node.parm("ri_dice_watertight").set(True)
	else:
		print("RFH parameters not added - setup incomplete")

def createRenderGeometrySettings(nodeToInsertAfter):
	## Get Container
	container = nodeToInsertAfter.parent().parent()
	if nodeToInsertAfter.parent() == "EDIT":
		container = nodeToInsertAfter.parent().parent()
	else:
		container = nodeToInsertAfter.parent()

	## Ancestor
	getAncestorNode = nodeToInsertAfter.inputs()
	position =  getAncestorNode[0].position()
	newPosition = (position[0],position[1] -10 )
	## Descendant
	node = nodeToInsertAfter.outputs()
	if type(node) == list:
		descendant = node[0]
	else:
		descendant = node

	# print(descendant.type().name())
	## Create Geometry Settings
	geometrySettings = hou.node(container.path()).createNode('rendergeometrysettings',"rendergeometrysettings")
	## Settings
	geometrySettings.parm('primpattern').set("/`chs('../../../../name')`/model")

	geometrySettings.setInput(0,getAncestorNode[0])
	# descendant.setInput(0,geometrySettings)
	geometrySettings.setPosition(newPosition)
	geometrySettings.moveToGoodPosition()

	setGeometrySettingsR(geometrySettings)

	return geometrySettings

def setGeometrySettingsR(geometrySettings):
	## Shading
	geometrySettings.parm('xn__primvarstracedisplacements_hjbf').set(True)
	geometrySettings.parm('xn__primvarstracedisplacements_control_iwbf').set("set")
	geometrySettings.parm('xn__primvarsdisplacementboundsphere_mrbr').set(1)
	geometrySettings.parm('xn__primvarsdisplacementboundsphere_control_n4br').set("set")
	## Geometry
	geometrySettings.parm('xn__primvarspolygonsmoothnormals_qmbh').set(1)
	geometrySettings.parm('xn__primvarspolygonsmoothnormals_control_rzbh').set("set")

	geometrySettings.parm('xn__primvarspolygonsmoothdisplacement_vubh').set(1)
	geometrySettings.parm('xn__primvarspolygonsmoothdisplacement_control_w7bh').set("set")

	geometrySettings.parm('xn__primvarsdicepretessellate_uhbe').set(1)
	geometrySettings.parm('xn__primvarsdicepretessellate_control_vube').set("set")

	geometrySettings.parm('xn__primvarsdicewatertight_ycbe').set(1)
	geometrySettings.parm('xn__primvarsdicewatertight_control_zpbe').set("set")

def buildMegascanShaderR(listTextures,renderer,nameAsset,geo,manifold,containerShader,assignShaderNode,nodeInfos,nameMegascan,houdiniMPC):
	matName = "Mat_"+ renderer +"_"+ nameAsset
	importedMObject = geo

	pathContainer = containerShader.path()
	parentNode = nodeInfos[0].parent()
	context = nodeInfos[1]
	pathContext = nodeInfos[2]
	centerPosition= nodeInfos[3]

	texExtention= ".tex"

	normalOGL= False
	print "\n"
	print " ---- Shader Building ---- "
	## Create Node
	material = containerShader.createNode("pxrdisney",matName)

	shadingGroup= containerShader.createNode("collect",nameAsset+"_SG")
	shadingGroup.setInput(0,material,0)
	displacementRemap = containerShader.createNode("pxrdisptransform",matName + "_dispTransform")
	displacement = containerShader.createNode("pxrdisplace",matName + "_displace")
	shadingGroup.setInput(1,displacement,0)

	## OpenGL Shader For Solaris
	parm_group = shadingGroup.parmTemplateGroup()
	parm_folder = hou.FolderParmTemplate("folder", "OpenGL")
	if context == "Lop":
		shaderOGLStage = containerShader.createNode("principledshader",matName + "_OGL")
		shadingGroup.setInput(2,shaderOGLStage,0)
		shadingGroup.setInput(3,shaderOGLStage,1)
		shaderOGLStage.parm('ior').set(1.2)
		shaderOGLStage.parm('rough').set(0.4)
		shaderOGLStage.parm('basecolorr').set(1)
		shaderOGLStage.parm('basecolorg').set(1)
		shaderOGLStage.parm('basecolorb').set(1)
		## Connect Textures to Nodes
	for texture in listTextures:
		textureNode = hou.node(pathContainer+"/"+texture)
		## Find the filename
		multi = False
		print textureNode.type().name()
		if "pxrtexture" in textureNode.type().name():
			filename =  hou.evalParm(pathContainer+"/"+texture+"/filename")
		elif "pxrmultitexture" in textureNode.type().name() :
			filename =  hou.evalParm(pathContainer+"/"+texture+"/filename0")
			multi = True
		##filename =  hou.evalParm(pathContainer+"/"+texture+"/filename")
		if "Albedo" in texture:
			## OpenGL
			filenameAlbedo =  filename
			parm_folder.addParmTemplate(hou.ToggleParmTemplate("Toggle_Diffuse", "Use Diffuse",default_value= True,tags={'ogl_use_tex1':'1'}))
			parm_folder.addParmTemplate(hou.StringParmTemplate("DiffuseMap", "Diffuse Map", 1, string_type =hou.stringParmType.FileReference,file_type =hou.fileType.Image,default_value= (filenameAlbedo,),tags={'ogl_tex1':'1'}))
			if context == "Lop":
				shaderOGLStage.parm('basecolor_useTexture').set(True)
				shaderOGLStage.parm('basecolor_texture').set(filenameAlbedo)
				shaderOGLStage.parm('albedomult').set(0.18)
			## Renderman
			material.setInput(0,textureNode,0)
			textureNode.parm('linearize').set(True)
		if "Specular" in texture:
			## OpenGL
			filenameSpecular =  filename
			parm_folder.addParmTemplate(hou.ToggleParmTemplate("Toggle_Specular", "Use Specular",default_value= True,tags={'ogl_use_specmap':'1'}))
			parm_folder.addParmTemplate(hou.StringParmTemplate("SpecularMap", "Specular Map", 1, string_type =hou.stringParmType.FileReference,file_type =hou.fileType.Image,default_value= (filenameSpecular,),tags={'ogl_specmap':'1'}))
			## Renderman
			material.setInput(5,textureNode,1)
		if "Roughness" in texture:
			## OpenGL
			filenameRoughness =  filename
			parm_folder.addParmTemplate(hou.ToggleParmTemplate("Toggle_Roughness", "Use Roughness",default_value= True,tags={'ogl_use_roughmap':'1'}))
			parm_folder.addParmTemplate(hou.StringParmTemplate("RoughnessMap", "Roughness Map", 1, string_type =hou.stringParmType.FileReference,file_type =hou.fileType.Image,default_value= (filenameRoughness,),tags={'ogl_roughmap':'1'}))
			if context == "Lop":
				shaderOGLStage.parm('rough_useTexture').set(True)
				shaderOGLStage.parm('rough_texture').set(filenameRoughness)
			## Renderman
			material.setInput(7,textureNode,1)
		if "Translucency" in texture:
			material.setInput(3,textureNode,0)
			material.parm('subsurface').set(0.5)
			textureNode.parm('linearize').set(True)
		if "Normal" in texture:
			## OpenGL
			if normalOGL != True:
				filenameNormal =  filename
				parm_folder.addParmTemplate(hou.ToggleParmTemplate("Toggle_Normal", "Use Normal",default_value= True,tags={'ogl_use_Normalmap':'1'}))
				parm_folder.addParmTemplate(hou.StringParmTemplate("NormalpMap", "Normal Map", 1, string_type =hou.stringParmType.FileReference,file_type =hou.fileType.Image,default_value= (filenameNormal,),tags={'ogl_normalmap':'1'}))
			if context == "Lop":
				shaderOGLStage.parm('baseBumpAndNormal_enable').set(True)
				shaderOGLStage.parm('baseNormal_texture').set(filenameNormal)
			## Renderman
			bump = containerShader.createNode("pxrnormalmap","PxrNormalMap_" + str(material.name()))
			material.setInput(13,bump,0)
			bump.setInput(1,textureNode,0)
			filenameNormal = textureNode.parm('filename')
			bump.parm('bumpScale').set(0.5)
			bump.parm('invertBump').set(False)
			bump.parm('filename').set(filenameNormal)
			normalOGL = True
		if "Opacity"in texture:
			## OpenGL
			filenameOpacity =  filename
			parm_folder.addParmTemplate(hou.ToggleParmTemplate("Toggle_Opacity", "Use Opacity",default_value= True,tags={'ogl_use_opacitymap':'1'}))
			parm_folder.addParmTemplate(hou.StringParmTemplate("OpacityMap", "Opacity Map", 1, string_type =hou.stringParmType.FileReference,file_type =hou.fileType.Image,default_value= (filenameOpacity,),tags={'ogl_opacitymap':'1'}))
			if context == "Lop":
				shaderOGLStage.parm('transparency_useTexture').set(True)
				shaderOGLStage.parm('transparency_texture').set(filenameOpacity)
			## Renderman
			material.setInput(14,textureNode,0)
		if "Displacement" in texture:
			displacementRemap.setInput(0,textureNode,1)
			displacement.setInput(1,displacementRemap,1)
			displacementRemap.parm('dispScalar').set(1)
			displacementRemap.parm('dispRemapMode').set(2)
			displacementRemap.parm('dispDepth').set(0.5)
			displacementRemap.parm('dispHeight').set(0.5)
			displacementRemap.parm('dispCenter').set(0.5)

	## Turn on Renderman Parameters if possible Sop/Object
	if not importedMObject == None and not "/stage" in pathContainer:
		for obj in importedMObject:
			nodeGeo = hou.node(obj.path())
			nodeGeo.setSelected(True,clear_all_selected=True)
			try:
				addRmanParameters()
				nodeGeo.parm('rendersubd').set(1)
			except:
				print " Couldn't add renderman parameters, add them manually"

	parm_group.append(parm_folder)
	shadingGroup.setParmTemplateGroup(parm_group)

	## Organise the nodes inside the container
	containerShader.layoutChildren()

	## Assign Shader
	assignMaterial = ""
	if not importedMObject == None:
		for containerObj in importedMObject:
			if context == "Object" or context == "Sop" and not "/stage" in pathContainer:
				nodeGeo = hou.node(containerObj.path())
				nodeGeo.parm('shop_materialpath').set(containerShader.path()+"/"+shadingGroup.name())
			elif context == "Lop":
				if houdiniMPC == True:
					## Assign Shader
					assignMaterial = ""
					containerShader.parm('containerpath').set("/Looks/")
					containerShader.parm('matpathprefix').set("/`chs('../../../../name')`/Looks/")
					##Assign to object
					containerShader.parm('matnode1').set(shadingGroup.name())
					containerShader.parm('geopath1').set("/`chs('../../../../name')`/model")
					if assignShaderNode != "":
						assignShaderNode.parm('matspecpath1').set("/`chs('../../../../name')`/Looks/" + nameAsset+"_SG")

				else:
					modelsop = hou.node(pathContext+ "/" + containerObj.name())

					geometrySettings = hou.node(pathContext).createNode('rendergeometrysettings',containerObj.name()+"_geoSettings")
					geometrySettings.parm('primpattern').set("/"+containerObj.name()+"/model")

					containerShader.setInput(0,geometrySettings)
					containerShader.parm('containerpath').set("/Looks/")
					geometrySettings.setInput(0,modelsop)
					geometrySettings.setPosition(centerPosition)

					containerShader.parm('containerpath').set("/"+ containerObj.name()+"/Looks/")
					containerShader.parm('matpathprefix').set("/"+ containerObj.name()+"/Looks/")
					##Assign to object
					containerShader.parm('matnode1').set("/stage/"+containerShader.name()+"/"+shadingGroup.name())
					containerShader.parm('geopath1').set("/"+nameMegascan+"/"+"*")

					containerShader.setDisplayFlag(True)

			containerShader.moveToGoodPosition()
			print " - Shader Assigned to : " + containerObj.name()
	else:
		print "No object to assign to"

	return assignMaterial

def loadMegascanShaderR(jsonShader, listTextures,nameAsset,geometry,manifold,idName,containerShader,nodeInfos):
	pathContainer = containerShader.path()
	context = nodeInfos[1]
	pathContext = nodeInfos[2]
	centerPosition= nodeInfos[3]
	normalOGL = False

	## Load Shader
	nodes = readShaderJson(jsonShader,nameAsset,containerShader)

	###### Connections Process
	shadingGroup = None
	shaderOGL = None
	typeConstructor = "pxrcolorcorrect"

	albedoConnector = None
	aoConnector= None
	specularConnector = None
	roughnessConnector = None
	translucencyConnector = None
	opacityConnector = None
	fuzzConnector = None
	normalConnector = None
	displacementConnector = None

	## Rename Nodes and Find where to connect the Textures
	for node in nodes:
		nodeType = node.type().name().split("::")[0]
		nodeName = node.name()
		if "CONSTRUCTOR" in node.name():
			nodeSuffixe = node.name().split("CONSTRUCTOR")[-1]
			node.setName(nameAsset+nodeSuffixe)
			if nodeType == "collect":
				shadingGroup = node
			elif nodeType == "principledshader":
				shaderOGL = node

		else:
			if "albedo" in nodeName.lower() and nodeType == typeConstructor:
				albedoConnector = node
			if "roughness" in  nodeName.lower() and nodeType == typeConstructor:
				roughnessConnector = node
			if "specular" in  nodeName.lower() and nodeType == typeConstructor:
				specularConnector = node
			if "translucency" in nodeName.lower() and nodeType == typeConstructor:
				translucencyConnector = node
			if "opacity" in nodeName.lower() and nodeType == typeConstructor:
				opacityConnector = node
			if "fuzz" in nodeName.lower() and nodeType == typeConstructor:
				fuzzConnector = node
			if "ao" in nodeName.lower() and nodeType == typeConstructor:
				aoConnector = node
			if "normal" in nodeName.lower() and nodeType == typeConstructor:
				normalConnector = node
			if "displacement" in nodeName.lower() and nodeType == typeConstructor:
				displacementConnector = node

	## Connect Texture to Shader Connector
	for texture in listTextures:
		textureNode = hou.node(pathContainer+"/"+texture)
		if "albedo" in texture.lower():
			albedoConnector.setInput(0,textureNode,0)
			textureNode.parm('linearize').set(True)
		if "specular" in texture.lower():
			specularConnector.setInput(0,textureNode,0)
		if "roughness" in texture.lower():
			roughnessConnector.setInput(0,textureNode,0)
		if "translucency" in texture.lower():
			translucencyConnector.setInput(0,textureNode,0)
			textureNode.parm('linearize').set(True)
		if "opacity" in texture.lower():
			opacityConnector.setInput(0,textureNode,0)
		if "fuzz" in texture.lower():
			fuzzConnector.setInput(0,textureNode,0)
		if "normal" in texture.lower():
			normalConnector.setInput(0,textureNode,0)
		if "displacement" in texture.lower():
			displacementConnector.setInput(0,textureNode,0)

	## Organise the nodes inside the container
	containerShader.layoutChildren()

	return shadingGroup,shaderOGL

def assignShader(containerShader,shadingGroup,nameAsset,nameMegascan,geometry,assignShaderNode,nodeInfos,houdiniMPC):
	pathContainer = containerShader.path()	
	context = nodeInfos[1]
	pathContext = nodeInfos[2]
	centerPosition= nodeInfos[3]

	## Assign Shader
	assignMaterial = ""
	if not geometry == None:
		for containerObj in geometry:
			if context == "Object" or context == "Sop" and not "/stage" in pathContainer:
				nodeGeo = hou.node(containerObj.path())
				nodeGeo.parm('shop_materialpath').set(containerShader.path()+"/"+ shadingGroup.name())
				assignShaderNode.parm('shop_materialpath1').set(containerShader.path()+"/"+ shadingGroup.name())
				print " - Shader Assigned to : " + assignShaderNode.name()
			elif context == "Lop":
				if houdiniMPC == True:
					## Assign Shader
					assignMaterial = ""
					containerShader.parm('containerpath').set("/Looks/")
					containerShader.parm('matpathprefix').set("/`chs('../../../../name')`/Looks/")
					##Assign to object
					containerShader.parm('matnode1').set(shadingGroup.name())
					containerShader.parm('geopath1').set("/`chs('../../../../name')`/model")
					if assignShaderNode != "":
						assignShaderNode.parm('matspecpath1').set("/`chs('../../../../name')`/Looks/" + nameMegascan+"_SG")
						
				else:
					modelsop = hou.node(pathContext+ "/" + containerObj.name())

					geometrySettings = hou.node(pathContext).createNode('rendergeometrysettings',containerObj.name()+"_geoSettings")
					geometrySettings.parm('primpattern').set("/"+containerObj.name()+"/model")

					containerShader.setInput(0,geometrySettings)
					containerShader.parm('containerpath').set("/Looks/")
					geometrySettings.setInput(0,modelsop)
					geometrySettings.setPosition(centerPosition)
					setGeometrySettingsR(geometrySettings)

					containerShader.parm('containerpath').set("/"+ containerObj.name()+"/Looks/")
					containerShader.parm('matpathprefix').set("/"+ containerObj.name()+"/Looks/")
					##Assign to object
					containerShader.parm('matnode1').set("/stage/"+containerShader.name()+"/"+shadingGroup.name())
					containerShader.parm('geopath1').set("/"+nameMegascan+"/"+"*")

					containerShader.setDisplayFlag(True)

			containerShader.moveToGoodPosition()
			print " - Shader Assigned to : " + containerObj.name()
	else:
		print "No object to assign to"

	return assignMaterial

def buildOGLShader(listTextures,containerShader,shadingGroup,shaderOGL,nameAsset,nodeInfos):
	pathContainer = containerShader.path()
	context = nodeInfos[1]
	pathContext = nodeInfos[2]
	centerPosition= nodeInfos[3]

	## OpenGL Shader For Solaris
	parm_group = shadingGroup.parmTemplateGroup()
	parm_folder = hou.FolderParmTemplate("folder", "OpenGL")
	filename = ""
	normalOGL = False

	shaderOGL.parm('ior').set(1.2)
	shaderOGL.parm('rough').set(0.3)
	shaderOGL.parm('basecolorr').set(1)
	shaderOGL.parm('basecolorg').set(1)
	shaderOGL.parm('basecolorb').set(1)

	for texture in listTextures:
		textureNode = hou.node(pathContainer+"/"+texture)
		if "pxrtexture" in textureNode.type().name():
			filename =  hou.evalParm(pathContainer+"/"+texture+"/filename")
		elif "pxrmultitexture" in textureNode.type().name() :
			filename =  hou.evalParm(pathContainer+"/"+texture+"/filename0")

		if "albedo" in texture.lower():
			## OpenGL
			filenameAlbedo = filename
			try:
				parm_folder.addParmTemplate(hou.ToggleParmTemplate("Toggle_Diffuse", "Use Diffuse",default_value= True,tags={'ogl_use_tex1':'1'}))
				parm_folder.addParmTemplate(hou.StringParmTemplate("DiffuseMap", "Diffuse Map", 1, string_type =hou.stringParmType.FileReference,file_type =hou.fileType.Image,default_value= (filenameAlbedo,),tags={'ogl_tex1':'1'}))
				if context == "Lop":
					shaderOGL.parm('basecolor_useTexture').set(True)
					shaderOGL.parm('basecolor_texture').set(filenameAlbedo)
					shaderOGL.parm('albedomult').set(0.4)
			except:
				pass
		if "specular" in texture.lower():	
			try:	
				## OpenGL
				filenameSpecular =  filename
				parm_folder.addParmTemplate(hou.ToggleParmTemplate("Toggle_Specular", "Use Specular",default_value= True,tags={'ogl_use_specmap':'1'}))
				parm_folder.addParmTemplate(hou.StringParmTemplate("SpecularMap", "Specular Map", 1, string_type =hou.stringParmType.FileReference,file_type =hou.fileType.Image,default_value= (filenameSpecular,),tags={'ogl_specmap':'1'}))
			except:
				pass
		if "roughness" in texture.lower():
			try:
				## OpenGL
				filenameRoughness =  filename
				parm_folder.addParmTemplate(hou.ToggleParmTemplate("Toggle_Roughness", "Use Roughness",default_value= True,tags={'ogl_use_roughmap':'1'}))
				parm_folder.addParmTemplate(hou.StringParmTemplate("RoughnessMap", "Roughness Map", 1, string_type =hou.stringParmType.FileReference,file_type =hou.fileType.Image,default_value= (filenameRoughness,),tags={'ogl_roughmap':'1'}))
				if context == "Lop":
					shaderOGL.parm('rough_useTexture').set(True)
					shaderOGL.parm('rough_texture').set(filenameRoughness)
			except:
				pass
		if "normal" in texture.lower():
			try:
				## OpenGL
				if normalOGL != True:
					filenameNormal =  filename
					parm_folder.addParmTemplate(hou.ToggleParmTemplate("Toggle_Normal", "Use Normal",default_value= True,tags={'ogl_use_Normalmap':'1'}))
					parm_folder.addParmTemplate(hou.StringParmTemplate("NormalpMap", "Normal Map", 1, string_type =hou.stringParmType.FileReference,file_type =hou.fileType.Image,default_value= (filenameNormal,),tags={'ogl_normalmap':'1'}))
				if context == "Lop":
					shaderOGL.parm('baseBumpAndNormal_enable').set(True)
					shaderOGL.parm('baseNormal_texture').set(filenameNormal)
				normalOGL = True
			except:
				pass
		if "opacity" in texture.lower():
			try:
				## OpenGL
				filenameOpacity =  filename
				parm_folder.addParmTemplate(hou.ToggleParmTemplate("Toggle_Opacity", "Use Opacity",default_value= True,tags={'ogl_use_opacitymap':'1'}))
				parm_folder.addParmTemplate(hou.StringParmTemplate("OpacityMap", "Opacity Map", 1, string_type =hou.stringParmType.FileReference,file_type =hou.fileType.Image,default_value= (filenameOpacity,),tags={'ogl_opacitymap':'1'}))
				if context == "Lop":
					shaderOGL.parm('transparency_useTexture').set(True)
					shaderOGL.parm('transparency_texture').set(filenameOpacity)
			except:
				pass
	try:
		parm_group.append(parm_folder)
		shadingGroup.setParmTemplateGroup(parm_group)
	except:
		pass

	try:
		shadingGroup.setInput(2,shaderOGL,0)
		shadingGroup.setInput(3,shaderOGL,1)
	except:
		pass

	## Organise the nodes inside the container
	containerShader.layoutChildren()

def buildVDBShaderR(nameAsset,vdb):
	print "Build Shader"

################################################################################################################
################################################################################################################

def traverse(node,children):
	listNodule =[]
	if hou.node(node.path()):
		listNodule =[]
		connections = hou.node(node.path()).inputs() or {}
		##connections = cmds.listConnections(node,source=True,destination=False,skipConversionNodes=True)
		for child in connections:
			if child != None:
				children[child]= {}
				listNodule.append(child)
	return listNodule

def get_nodes(node,children,listNodeName):
	listNodeName += traverse(node,children)
	for child in children:
		if hou.node(child.path()):
			get_nodes(child,children[child],listNodeName)
	return listNodeName

def buildDictionary(shadingGroup):
	listNodes =[]
	listNodes.append(hou.node(shadingGroup))
	listNodule =[]
	children={}
	cleanDic= {}
	shadingGroup = hou.node(shadingGroup)
	listItem = get_nodes(shadingGroup,children,listNodes)

	for item in listItem:
		attribAll = {}
		attribMulti = {}
		attribString = {}
		if hou.Node.type(item).name().split("::")[0] == "collect":
			id = hou.Node.type(item).name().split("::")[0]
		else:
			id = hou.node(item.path()).shaderName()
		listAttribAll=[]
		listAttribAllTmp = sorted(hou.node(item.path()).parms())

		for attr in sorted(listAttribAllTmp):
			if attr != None:
				listAttribAll.append(attr)

		if listAttribAll:
			for attribute in listAttribAll:
				try:
					valueAttr = hou.node(item.path()).parm(attribute.name()).eval()
					attribAll[attribute.name()] = valueAttr
				except:
					pass
		connectionsAttr =[]
		node = hou.node(item.path())
		nodeConnections = node.outputConnections()

		for connection in nodeConnections:
			inputConnection = connection.inputNode().name()+"."+connection.inputName()
			outputConnection = connection.outputNode().name()+"."+connection.outputName()
			connectionsAttr.append(outputConnection)
			connectionsAttr.append(inputConnection)

		data = {}
		data[id] = []
		data[id].append({
		'connections':connectionsAttr,
		'attributes':attribAll
		})
		cleanDic[item.name()] = data
	return cleanDic

def readShaderJson(jsonFile,nameAsset,containerShader):
	listConnect = []
	listNodesCreated = []
	listErroredNodes = []
	listNodesCreated.append(containerShader)
	if os.path.exists(jsonFile):
		with open(jsonFile) as jfile:
			data = json.load(jfile)
			for key in data:
				nameComponent = key
				dictionnaryInfo = data[key]
				for key in dictionnaryInfo:
					nodeToCreate = key
					if str(nodeToCreate) == "shadingEngine":
						nodeToCreate = "collect"
					# elif str(nodeToCreate) == "lambert" and "OGL" in nameComponent:
					# 	continue
					elif str(nodeToCreate) == "transform" :
					 	continue
					elif str(nodeToCreate) == "lambert" and "OGL" in nameComponent:
						nodeToCreate = "principledshader"
					## Create Node
					try:
						node= containerShader.createNode(nodeToCreate.lower(),nameComponent)
					except:
						listErroredNodes.append(nodeToCreate)
						continue
					node.moveToGoodPosition()
					## List Parameters on created nodes
					nodeParameters = node.parms()
					listParameters = []
					listParametersLower = []
					for parm in nodeParameters:
						listParameters.append(parm.name())
						listParametersLower.append(parm.name().lower())
					listNodesCreated.append(node)

					typeAction = dictionnaryInfo[key]
					for action in typeAction:
						listType = action
						for key in listType:
							action = key
							attributes = listType[action]
							if "attributes" in action:
								for key in attributes:
									nameAttribute = key
									valueAttribute = attributes[nameAttribute]
									if action == "attributes" and valueAttribute != None:
										## Check Parameters and Set it
										try:
											indexAttribute = listParametersLower.index(nameAttribute.lower())
										except:
											indexAttribute = None
											pass
										if indexAttribute!= None:
											try:
												if type(valueAttribute) == list:
													valueAttributeList = valueAttribute[0]
													parameter = node.parmTuple(listParameters[indexAttribute]).set(valueAttributeList)
												else:
													parameter = node.parm(listParameters[indexAttribute]).set(valueAttribute)
											except:
												print("Couldn't set: " + nameAttribute + " " + str(valueAttribute) )
												pass
							elif action == "connections":
								if attributes != None:
									for connection in attributes:
										listConnect.append(connection)
			k=0
			for connect in listConnect:
				if k<len(listConnect)-1 and k % 2 == 0:
					index_IN = None
					index_OUT = None
					outConnectName = listConnect[k+1].split(".")[-1]
					inConnectName = connect.split(".")[-1]
					#print "Connecting : "+ outConnectName + " to " + inConnectName
					outputObject= hou.node(containerShader.path() +'/'+str(listConnect[k+1].split(".")[0])) 
					inputObject = hou.node(containerShader.path() +'/'+str(connect.split(".")[0]))
					if inputObject != None and outputObject != None :
						## Check if output or input exist
						if outputObject.outputNames():
							ins = inputObject.inputNames()
							outs = outputObject.outputNames()
						else:
							pass

						try:
							## Conversion with RfM/Need a better way 
							if outConnectName == "outColor":
								nameOutConnection = hou.Node.type(outputObject).name() 
								#print(nameOutConnection)
								if nameOutConnection == "pxrdisney::22" or nameOutConnection == "pxrsurface::3.0" :
									outConnectName= "bxdf_out"
								elif nameOutConnection == "pxrdisplace::2.0" or nameOutConnection == "pxrdisplace::3.0":
									outConnectName= "displace_out"
								else:
									pass
							if outConnectName == "resultRGBR":
								outConnectName= "resultR"
							index_OUT = outs.index(str(outConnectName))
						except:
							print("Couldn't find the attribute out: " + str(outConnectName))
						try:
							## Conversion with RfM
							if inConnectName == "rman__surface" or inConnectName == "rman__displacement" :
								index = 0
								listCollectorConnections = inputObject.inputConnectors()
								index_IN = index
								for collectCon in listCollectorConnections:
									isconnected = len(collectCon)
									if isconnected == 0:
										index_IN = index
										inputObject.setNextInput(collectCon, r)
									else:
										index +=1
							else:
								index_IN = ins.index(str(inConnectName))
						except:
							print("Couldn't find the attribute in: " + str(inConnectName))
						if index_IN !=None or index_OUT !=None:
							try:
								inputObject.setInput(index_IN,outputObject,index_OUT)
							except:
								pass
					k +=1
				else:
					k +=1
	containerShader.layoutChildren()
	print("NODES ERRORED: ")
	print(listErroredNodes)
	return listNodesCreated
