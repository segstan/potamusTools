import unreal
import os
from shutil import copyfile
from shutil import copytree
from shutil import copy2
import time
import glob

def createNewAssetFolder(typeFolder,nameNewFolder):
	if typeFolder != "":
		path = "/Game/"+ typeFolder + "/" + nameNewFolder
	else:
		path = "/Game/"+ nameNewFolder
	# if not os.path.exists(path):
	if not unreal.EditorAssetLibrary.does_directory_exist(path):
		unreal.EditorAssetLibrary.make_directory(path)
		folderExists = False
	else:
		# print("Directory already exists, skip")
		folderExists = True
	return [path,folderExists]

def directoryExist(path):
	if unreal.EditorAssetLibrary.does_directory_exist(path):
		return True
	else:
		return False

def createDirectory(fullpath):
	unreal.EditorAssetLibrary.make_directory(fullpath)
	
def duplicateAsset(newName,path,objectToCopy):
	unreal.AssetTools.duplicate_asset(newName,path,objectToCopy)

def duplicateAsset02(sourcePath,destinationPath):
	duplicate = unreal.EditorAssetLibrary.duplicate_asset(sourcePath,destinationPath)
	return duplicate

def doesAssetExist(assetPath):
	exist = unreal.EditorAssetLibrary.does_asset_exist(assetPath)
	return exist

def getProjectContentFolder():
	## Return a Relative path
	pathRelative = unreal.Paths().project_content_dir()
	return pathRelative

def getAbsoluteProjectContentFolder():
	## Return an absolute path
	pathRelative = unreal.Paths().project_content_dir()
	pathContent = unreal.Paths().convert_relative_path_to_full(pathRelative)
	return pathContent

def getAbsoluteProjectDir():
	pathRelative = unreal.Paths().project_dir()
	pathProject = unreal.Paths().convert_relative_path_to_full(pathRelative)
	return pathProject

def getSelectedActors():
	selectedActors = unreal.EditorLevelLibrary.get_selected_level_actors()
	return selectedActors

def getClassActors(actorClass):
	world = unreal.EditorLevelLibrary.get_editor_world()
	classActors = unreal.GameplayStatics.get_all_actors_of_class(world,actorClass)
	return classActors

def getTagActors(actorTag):
	world = unreal.EditorLevelLibrary.get_editor_world()
	tagActors = unreal.GameplayStatics.get_all_actors_with_tag(world,actorTag)
	return tagActors

def getLevelPath():
	## Get Level 
	worldLevel = unreal.EditorLevelLibrary.get_editor_world()
	worldLevelPath = worldLevel.get_path_name()
	tmp = worldLevelPath.split("/")

	## Rebuild Path and asset name
	i =0
	setLevelPath =""
	for word in tmp:
		if i < len(tmp) - 3:
			setLevelPath += word +"/"
		i+=1
	return setLevelPath		

def showAssetsInContentBrowser(path):
	##### Must be a list
	unreal.EditorAssetLibrary.sync_browser_to_objects(path)

def buildImportTask(modelPath,nameMegascan,nameAsset,destination_path,options):
	task = unreal.AssetImportTask()
	task.set_editor_property('automated', True)
	task.set_editor_property('destination_name', nameAsset)
	task.set_editor_property('destination_path', destination_path)
	task.set_editor_property('filename', modelPath)
	task.set_editor_property('replace_existing', True)
	task.set_editor_property('save', True)
	task.set_editor_property('options', options)
	return task

def buildStaticModelOptions(formatModel):
	if formatModel == "fbx" or formatModel == "obj":
		options = unreal.FbxImportUI()
		options.set_editor_property('import_mesh', True)
		options.set_editor_property('import_textures', False)
		options.set_editor_property('import_materials', False)
		options.set_editor_property('import_as_skeletal', False)

		options.static_mesh_import_data.set_editor_property('import_translation',unreal.Vector(0.0,0.0,0.0))
		options.static_mesh_import_data.set_editor_property('import_rotation',unreal.Rotator(0.0,0.0,0.0))
		options.static_mesh_import_data.set_editor_property('import_uniform_scale',1.0)
		
		options.static_mesh_import_data.set_editor_property('combine_meshes',False)
		options.static_mesh_import_data.set_editor_property('generate_lightmap_u_vs',True)
		options.static_mesh_import_data.set_editor_property('auto_generate_collision',True)

		options.static_mesh_import_data.set_editor_property('vertex_color_import_option',unreal.VertexColorImportOption.REPLACE)

		options.set_editor_property('auto_compute_lod_distances',False)
		options.set_editor_property('lod_number',3)
		options.set_editor_property('lod_distance0',0.60)
		options.set_editor_property('lod_distance1',0.30)
		options.set_editor_property('lod_distance2',0.05)

	elif formatModel == "abc":
		options = unreal.AbcImportSettings()

		options.material_settings.set_editor_property('create_materials',False)
		options.material_settings.set_editor_property('find_materials',False)

		options.static_mesh_settings.set_editor_property('merge_meshes',True)
		options.static_mesh_settings.set_editor_property('generate_lightmap_u_vs',True)
		options.static_mesh_settings.set_editor_property('propagate_matrix_transformations',True)

		# options.conversion_settings.set_editor_property('preset',unreal.AbcConversionPreset(1))
		options.conversion_settings.set_editor_property('rotation',unreal.Vector(90,0.0,0.0))
		options.conversion_settings.set_editor_property('scale',unreal.Vector(1.0,-1.0,1.0))

	return options

def executeImportModels(tasks):
	assets = unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks(tasks)
	imported_asset_paths = []
	for task in tasks:
		for path in task.get_editor_property('imported_object_paths'):
			imported_asset_paths.append(path)
		## return path of Geometry
		return imported_asset_paths

def importModel(modelPath,otherLODs,nameMegascan,nameAsset,category):
	formatModel =  modelPath.split(".")[-1]
	path = createNewAssetFolder("Library",nameMegascan)
	static_mesh_task = buildImportTask(modelPath,nameMegascan,nameAsset,path[0],buildStaticModelOptions(formatModel))
	models = executeImportModels([static_mesh_task])

	for pathModel in models:
		listAssets = unreal.EditorAssetLibrary.list_assets(pathModel)
		for asset in listAssets:
			index = 1
			staticMesh = unreal.load_asset(asset)
			nameAsset = staticMesh.get_name()
			if otherLODs:
				for lod in otherLODs:
					if "3dplant" in category:
						importPlantLOD(staticMesh,index,lod)
					else:
						importLOD(staticMesh,index,lod)
					index += 1
			## Create Foliage
			createStaticFoliageAsset(staticMesh,nameMegascan,nameAsset,pathModel)

	return models

def importLOD(staticMesh,index,lodPath):
	unreal.EditorStaticMeshLibrary.import_lod(staticMesh,index,lodPath)
	## Let use the automatic lod creation for now
	# print(dir(staticMesh))
	# staticMesh.set_lod_group("LargeProp",True)
	# staticMesh.set_editor_property('lod_group', "LargeProp")

def importPlantLOD(staticMesh,index,lodPath):
	unreal.EditorStaticMeshLibrary.import_lod(staticMesh,index,lodPath)

def importTextures(listTextures,nameAsset):
	textureDestinationPath = "/Game/Library/" + nameAsset  
	destinationFolder= createNewAssetFolder("Library",nameAsset)
	## Import the textures in the right place
	data = unreal.AutomatedAssetImportData()
	data.set_editor_property('destination_path', textureDestinationPath)
	data.set_editor_property('filenames', listTextures)
	texturesImported = unreal.AssetToolsHelpers.get_asset_tools().import_assets_automated(data)

	for texture in texturesImported:
		# print(texture.get_name())
		if "Roughness" in texture.get_name():
			## Change the Compression
			texture.set_editor_property('compression_settings', unreal.TextureCompressionSettings.TC_ALPHA)
			# texture.set_editor_property('srgb', False)
		if "Opacity" in texture.get_name():
			## Change the mipmaps
			texture.set_editor_property('compression_settings', unreal.TextureCompressionSettings.TC_ALPHA)
			texture.set_editor_property('mip_gen_settings', unreal.TextureMipGenSettings.TMGS_NO_MIPMAPS)
		try:
			texture.set_editor_property('virtual_texture_streaming',False)
		except:
			pass
	return texturesImported

def importTexturesForMPC(listTextures,nameAsset,path):
	textureDestinationPath = path + nameAsset  
	
	## Import the textures in the right place
	data = unreal.AutomatedAssetImportData()
	data.set_editor_property('destination_path', path)
	data.set_editor_property('filenames', listTextures)
	texturesImported = unreal.AssetToolsHelpers.get_asset_tools().import_assets_automated(data)

	for texture in texturesImported:
		# print(texture.get_name())
		if "Roughness" in texture.get_name():
			## Change the Compression
			texture.set_editor_property('compression_settings', unreal.TextureCompressionSettings.TC_ALPHA)
			# texture.set_editor_property('srgb', False)
		if "Opacity" in texture.get_name():
			## Change the mipmaps
			texture.set_editor_property('compression_settings', unreal.TextureCompressionSettings.TC_ALPHA)
			texture.set_editor_property('mip_gen_settings', unreal.TextureMipGenSettings.TMGS_NO_MIPMAPS)
		try:
			texture.set_editor_property('virtual_texture_streaming',False)
		except:
			pass
	return texturesImported

def createMegascansMaterial(nameMegascan,objectsPath,textureNodes,shaderToLoad,slot):
	basePath = "/Game/Library/"+nameMegascan

	## Import Shader
	shaderName = shaderToLoad.split("/")[-1].split(".")[0]
	# shaderName = os.path.basename(shaderToLoad).split(".")[0]
	shaderPath = shaderToLoad.split(shaderName)[0] +shaderName+"/"

	shader = importMegascanTemplateShader("Utilities",shaderName,shaderPath)
	if slot == 0:
		extraName = "_instance"
	elif slot > 0:
		extraName = "_billboard"+ str(slot)

	if shader != None:
		## Create Instance Material
		mat = unreal.AssetToolsHelpers.get_asset_tools()
		nameNewInstance = nameMegascan+extraName
		materialInstance = mat.create_asset(nameNewInstance, basePath, unreal.MaterialInstanceConstant, unreal.MaterialInstanceConstantFactoryNew())

		if materialInstance :
			materialInstance.modify()
			materialInstance.set_editor_property('Parent',shader)

			## Connect Textures
			connectTexturesToMaterialInstance(textureNodes,materialInstance)

			## Assign Shader
			# for i in range(slot):
			assignShaderToObject(objectsPath,materialInstance,slot)

			## Save Instance Material and textures
			unreal.EditorAssetLibrary.save_directory(basePath)

		return materialInstance
	else:
		print("Shader was not created correctly")

def buildMegascanShader(textureNodes, nameAsset, objectsPath):
	nodeAlbedo = None
	nodeAO = None
	nodeEmissive = None
	nodeNormal= None
	nodeMetallic = None
	nodeOpacity = None
	nodeRoughness = None
	nodeSpecular = None
	nodeTranslucency = None
	linearMap = False
	xPos = -400

	## Create shader
	shader = createMegascansMaterial(nameAsset)
	## Notify Editor we are about to modify the shader
	shader.modify()

	## Create TextureSampler
	for texture in textureNodes:
		if ".exr" in texture.get_editor_property("asset_import_data").get_first_filename():
			linearMap = True
		else:
			linearMap = False
		# create the node
		if "Albedo" in texture.get_name():
			yPos =-350
			nodeAlbedo = unreal.MaterialEditingLibrary.create_material_expression(shader,unreal.MaterialExpressionTextureSampleParameter2D,xPos,yPos)
			nodeAlbedo.texture = texture
			nodeAlbedo.set_editor_property('parameter_name',"in_Albedo") 
			if linearMap == True:
				nodeAlbedo.set_editor_property('sampler_type', unreal.MaterialSamplerType.SAMPLERTYPE_LINEAR_COLOR)
		elif "Specular" in texture.get_name():
			yPos = -100
			nodeSpecular = unreal.MaterialEditingLibrary.create_material_expression(shader,unreal.MaterialExpressionTextureSampleParameter2D,-400,yPos)
			nodeSpecular.texture = texture
			nodeSpecular.set_editor_property('parameter_name',"in_Specular") 
			if linearMap == True:
				nodeSpecular.set_editor_property('sampler_type', unreal.MaterialSamplerType.SAMPLERTYPE_LINEAR_COLOR)
		elif "Roughness" in texture.get_name():
			yPos = 120
			nodeRoughness = unreal.MaterialEditingLibrary.create_material_expression(shader,unreal.MaterialExpressionTextureSampleParameter2D,-400,yPos)
			nodeRoughness.texture = texture
			nodeRoughness.set_editor_property('parameter_name',"in_Roughness") 
			nodeRoughness.set_editor_property('sampler_type', unreal.MaterialSamplerType.SAMPLERTYPE_LINEAR_COLOR)
			# nodeRoughness.set_editor_property('sampler_type', unreal.MaterialSamplerType.SAMPLERTYPE_GRAYSCALE)
		elif "Opacity" in texture.get_name():
			yPos = 340
			nodeOpacity = unreal.MaterialEditingLibrary.create_material_expression(shader,unreal.MaterialExpressionTextureSampleParameter2D,-400,yPos)
			nodeOpacity.texture = texture
			nodeOpacity.set_editor_property('parameter_name',"in_Opacity") 
			if linearMap == True:
				nodeOpacity.set_editor_property('sampler_type', unreal.MaterialSamplerType.SAMPLERTYPE_LINEAR_COLOR)
			## Material Update Assuming it's a thin object
			shader.set_editor_property('blend_mode',unreal.BlendMode.BLEND_MASKED)
			shader.set_editor_property('two_sided',True)
			shader.set_editor_property('shading_model',unreal.MaterialShadingModel.MSM_TWO_SIDED_FOLIAGE)
			 
		elif "Normal" in texture.get_name() and not "Bump" in texture.get_name():
			yPos = 560
			nodeNormal = unreal.MaterialEditingLibrary.create_material_expression(shader,unreal.MaterialExpressionTextureSampleParameter2D,-400,yPos)
			nodeNormal.texture = texture
			nodeNormal.set_editor_property('parameter_name',"in_Normal") 
			nodeNormal.set_editor_property('sampler_type', unreal.MaterialSamplerType.SAMPLERTYPE_NORMAL)
		elif "Translucency" in texture.get_name():
			yPos = 780
			nodeTranslucency = unreal.MaterialEditingLibrary.create_material_expression(shader,unreal.MaterialExpressionTextureSampleParameter2D,-400,yPos)
			nodeTranslucency.texture = texture
			nodeTranslucency.set_editor_property('parameter_name',"in_Translucency") 
			if linearMap == True:
				nodeTranslucency.set_editor_property('sampler_type', unreal.MaterialSamplerType.SAMPLERTYPE_LINEAR_COLOR)
		elif "AO" in texture.get_name():
			yPos = 1000
			nodeAO = unreal.MaterialEditingLibrary.create_material_expression(shader,unreal.MaterialExpressionTextureSampleParameter2D,-400,yPos)
			nodeAO.texture = texture
			nodeAO.set_editor_property('parameter_name',"in_AmbientOcclusion") 
			if linearMap == True:
				nodeAO.set_editor_property('sampler_type', unreal.MaterialSamplerType.SAMPLERTYPE_LINEAR_COLOR)

		## Color Space
	## Assign nodes to the material
	# MP_BASE_COLOR, MP_NORMAL, MP_ROUGHNESS, MP_SPECULAR, MP_EMISSIVE_COLOR, MP_OPACITY, MP_AMBIENT_OCCLUSION
	unreal.MaterialEditingLibrary.connect_material_property(nodeAlbedo, "rgba", unreal.MaterialProperty.MP_BASE_COLOR)
	unreal.MaterialEditingLibrary.connect_material_property(nodeRoughness, "r", unreal.MaterialProperty.MP_ROUGHNESS)
	if nodeOpacity != None:
		unreal.MaterialEditingLibrary.connect_material_property(nodeOpacity, "r", unreal.MaterialProperty.MP_OPACITY_MASK)
	unreal.MaterialEditingLibrary.connect_material_property(nodeNormal, "rgb", unreal.MaterialProperty.MP_NORMAL)
	unreal.MaterialEditingLibrary.connect_material_property(nodeSpecular, "rgb", unreal.MaterialProperty.MP_SPECULAR)
	unreal.MaterialEditingLibrary.connect_material_property(nodeTranslucency, "rgb", unreal.MaterialProperty.MP_SUBSURFACE_COLOR)
	unreal.MaterialEditingLibrary.connect_material_property(nodeAO, "r", unreal.MaterialProperty.MP_AMBIENT_OCCLUSION)

	## Assign Parameter

	## Assign Shader to object
	if objectsPath != None:
		for paths in objectsPath:
			try:
				for path in paths:
					listAssets = unreal.EditorAssetLibrary.list_assets(path)
					for asset in listAssets:
						staticMesh = unreal.load_asset(asset)
						staticMesh.set_material(0, shader)

			except Exception as e:
				print(e,"##### ERROR #####" + "\n")
				pass
	else:
		print("No object to assign to")

	## Compile Shader
	unreal.MaterialEditingLibrary.recompile_material(shader)

	return shader

def importMegascanTemplateShader(folderName,shaderType,shaderPath):
	os.chdir(shaderPath)
	shader = None
	listUAssets = []
	## Import dependencies
	for file in glob.glob('**/*.uasset'):
		extraFolder = file.split("\\")[0]
		shaderToLoad= file.split("\\")[-1]

		importShaderUnreal(os.path.abspath(os.path.join(shaderPath,file)),shaderToLoad,folderName,shaderType+"/"+extraFolder)
		listUAssets.append(os.path.abspath(os.path.join(shaderPath,file)))
		
	## Import Parent  Shader
	for file in glob.glob('*.uasset'):
		shader = importShaderUnreal(os.path.abspath(os.path.join(shaderPath,file)),shaderType+".uasset",folderName,shaderType)
		listUAssets.append(os.path.abspath(os.path.join(shaderPath,file)))
	# print("That shader is the parent Shader: ")
	# print(shader)
	return shader

def assignShaderToObject(objectsPath,shader,slot):
	## Assign Shader to object
	if objectsPath != None:
		for paths in objectsPath:
			try:
				for path in paths:
					listAssets = unreal.EditorAssetLibrary.list_assets(path)
					for asset in listAssets:
						staticMesh = unreal.load_asset(asset)
						if slot > 0:
							staticMesh.add_material(shader)
						staticMesh.set_material(slot, shader)

			except Exception as e:
				print(e, "##### ERROR #####" + "\n")
				pass
	else:
		print("No object to assign to")

def importShaderUnreal(pathShaderOnDisk,nameShader,folderBaseMaterial,folderAsset):
	pathContent = getAbsoluteProjectContentFolder()
	pathNewShader = os.path.abspath(os.path.join(pathContent,folderBaseMaterial,folderAsset))+"\\"
	
	pathGameMaterial=[]

	## Check if folder to import Shader exists
	if not os.path.exists(pathNewShader):
	# if not unreal.EditorAssetLibrary.does_directory_exist(pathNewShader):
		pathGameMaterial= createNewAssetFolder(folderBaseMaterial,folderAsset)
		print("Path Shader: ",pathNewShader)
		print("Path Shader: ",pathGameMaterial[0])
	else:
		pathGameMaterial.append("/Game/"+folderBaseMaterial+"/"+folderAsset)
		print("Path Folder created for Shader: ",pathGameMaterial[0])	
	pathMaterials = pathNewShader	
	pathDestination = os.path.join(pathMaterials, nameShader)

	## Copy file
	if not os.path.exists( pathDestination ):
		copyfile(pathShaderOnDisk, pathDestination )
		copying = True
		size2 = -1
		while copying:
			size = os.path.getsize(pathMaterials + nameShader)
			if size == size2:
				break
			else:
				size2 = os.path.getsize(pathMaterials + nameShader)
				time.sleep(1)

	## Find Parent Shader and Compile it
	shader = None
	asset_reg = unreal.AssetRegistryHelpers.get_asset_registry()
	assets = asset_reg.get_assets_by_path(pathGameMaterial[0])

	## Find the shader based on path
	for asset in assets:
		if asset.asset_class == 'Material':
			full_name = asset.get_full_name()
			path = full_name.split(' ')[-1]
			shader = unreal.load_asset(path)
	
	if shader != None:
		shader.modify()
		unreal.MaterialEditingLibrary.recompile_material(shader)

	return shader

def connectTexturesToMaterialInstance(textureNodes,material):
	material_util = unreal.MaterialEditingLibrary()
	for texture in textureNodes:
		try:
			if "Albedo" in texture.get_name():
				material_util.set_material_instance_texture_parameter_value(material, "Albedo", texture)
			if "AO" in texture.get_name():
				material_util.set_material_instance_texture_parameter_value(material, "AO", texture)
			if "Roughness" in texture.get_name():
				material_util.set_material_instance_texture_parameter_value(material, "Roughness", texture)
			if "Normal" in texture.get_name():
				material_util.set_material_instance_texture_parameter_value(material, "Normal", texture)
			if "Metal" in texture.get_name():
				material_util.set_material_instance_texture_parameter_value(material, "Metalness", texture)
			if "Fuzz" in texture.get_name():
				material_util.set_material_instance_texture_parameter_value(material, "Fuzz", texture)
			if "Transmission" in texture.get_name():
				material_util.set_material_instance_texture_parameter_value(material, "Transmission", texture)
			if "Translucency" in texture.get_name():
				material_util.set_material_instance_texture_parameter_value(material, "Translucency", texture)
			if "Specular" in texture.get_name():
				material_util.set_material_instance_texture_parameter_value(material, "Specular", texture)
			if "Displacement" in texture.get_name():
				material_util.set_material_instance_texture_parameter_value(material, "Displacement", texture)
			if "Opacity" in texture.get_name():
				# material_util.set_material_instance_scalar_parameter_value(material, "Enable SSS Parameters", 1)
				material_util.set_material_instance_texture_parameter_value(material, "Opacity", texture)

				## Material Instance Update Assuming it's a thin object
				# material.set_editor_property('blend_mode',unreal.BlendMode.BLEND_MASKED)
				# material.set_editor_property('two_sided',True)
				# material.set_editor_property('shading_model',unreal.MaterialShadingModel.MSM_TWO_SIDED_FOLIAGE)

		except Exception as e:
			print(e,"Error with Texture: " + texture.get_name())
			pass

	material_util.update_material_instance(material)

def connectTexturesToLight(texture,material):
	material_util = unreal.MaterialEditingLibrary()
	material_util.set_material_instance_texture_parameter_value(material, "Emissive", texture)

def createStaticFoliageAsset(staticMesh,nameMegascan,nameAsset,destination_path):
	path = createNewAssetFolder("Library/"+nameMegascan,"Foliage")
	
	foliage = unreal.AssetToolsHelpers.get_asset_tools()
	foliageStaticMesh = foliage.create_asset(nameAsset+"_foliage", path[0], unreal.FoliageType_InstancedStaticMesh, unreal.FoliageType_InstancedStaticMeshFactory())

	foliageStaticMesh.set_editor_property('mesh',staticMesh)
	# unreal.FoliageInstancedStaticMeshComponent.set_editor_property('static_mesh ',staticMesh)

def setMaterialInstanceParameter(material_instance, param_name, param_value):
	param_info = unreal.MaterialParameterInfo(name=unreal.Name(param_name), association=unreal.MaterialParameterAssociation.GLOBAL_PARAMETER, index=-1)
	if type(param_value) == float:
		parameters = material_instance.scalar_parameter_values
		parameter = unreal.ScalarParameterValue(parameter_info=param_info, parameter_value=param_value)
	elif type(param_value) == unreal.LinearColor:
		parameters = material_instance.vector_parameter_values
		parameter = unreal.VectorParameterValue(parameter_info=param_info, parameter_value=param_value)
	elif type(param_value) == unreal.Texture:
		parameters = material_instance.texture_parameter_values
		parameter = unreal.TextureParameterValue(parameter_info=param_info, parameter_value=param_value)
	elif str(type(param_value)) == 'Texture2D':
		parameters = material_instance.texture_parameter_values
		parameter = unreal.TextureParameterValue(parameter_info=param_info, parameter_value=param_value)
	elif type(param_value) == unreal.Material:
		parameters = material_instance(parent = param_value)
		parameter = param_value
	else:
		parameters = [""]
		parameter = None

	if parameter != None:
		parameter_names = getMaterialInstanceParameters(material_instance, parameters)

		if param_name not in parameter_names:
			#todo: check if the parameter exists in the parent material: parent_material = material_instance.parent.get_base_material()
			parameters.append(parameter)
		else:
			for i in range(len(parameters)):
				# print(parameters[i])
				if parameters[i].parameter_info.name == param_name:
					new_params = parameters[i].copy() #struct copy
					new_params.parameter_value = param_value
					parameters[i] = new_params               
	else:
		print("Can't find parameter")
	return parameters

def getMaterialInstanceParameters(material_instance, parameters):
	param_names = []
	for param_info in parameters:
		str_name = str(param_info.parameter_info.name)
		if str_name:
			param_names.append(str_name)

		return param_names

def getMaterialOnLight(light):
	print("Material: " + light)

def copyUnrealShaderLibrary(pathLibrary):
	## Copy ShaderLibrary
	pathProject= getAbsoluteProjectContentFolder()
	for folder in os.listdir(pathLibrary):
		pathSource = os.path.abspath(os.path.join(pathLibrary,folder))
		pathDestination = os.path.abspath(os.path.join(pathProject, "Utilities/",folder))
		if not os.path.exists(pathDestination):
			print("Copying " + pathSource + " to " + pathDestination)
			copytree(pathSource,pathDestination)

def copyToContentFolder(source, destination):
	for folder in os.listdir(source):
		pathSource = os.path.abspath(os.path.join(source,folder))
		pathDestination = os.path.abspath(os.path.join(destination))
		if not os.path.exists(pathDestination):
			print("Copying " + pathSource + " to " + pathDestination)
			copytree(pathSource,pathDestination)

def saveDirectory(path):
	## Save Directory
	print("Save Directory: " + path)
	unreal.EditorAssetLibrary.save_directory(path)