import mari

def currentProject():
	project = mari.projects.current()
	if project != None:
		projectName = project.name()
		print "Name of the Mari Project: " + str(projectName)
	else:
		projectName = "None"
		print "Creating a new project..."
		
	return project

def createNewProject(name,modelPath,channelsDict):
	project_meta_options = dict()
	listChannels = sorted(channelsDict['ImportChannels'])

	mari.projects.create( name, modelPath, [],listChannels, project_meta_options)

def importModel(pathModel):
	geo = mari.geo.load(pathModel)
	return geo

def createImportChannels(folder, pathModel,listTextures,lod,listChannels,new,colorspace):
	dicGeoChannels={}
	dicImportChannels = {}
	listImportChannels = []
	resolutionChannel = 2048

	##colorspace = 'linear'

	for texture in sorted(listTextures,reverse = True):
		## Channel Name
		channelName = texture.split(".")[0].split("_")[-1]
		if lod[0] in channelName:
			channelName = texture.split(".")[0].split("_")[-2]
			idRes = -3 
		else:
			idRes = -2 
		if channelName in listChannels:
			if channelName == "Cavity":
				dicGeoChannels[channelName] = folder+texture
			## Resolution Channel
			resolution = texture.split("_")[idRes]
			if resolution == "8K":
				resolutionChannel = 8192
			elif resolution == "4K":
				resolutionChannel = 4096
			elif resolution == "2K":
				resolutionChannel = 2048
			
			## CreateChannels from Textures
			colorConfig = mari.ColorspaceConfig()
			colorConfig.setAutomaticColorspace(mari.ColorspaceConfig.COLORSPACE_STAGE_NATIVE,colorspace)
			colorConfig.setColorspace(mari.ColorspaceConfig.COLORSPACE_STAGE_NATIVE,colorspace)
			importChannel = mari.ChannelInfo(channelName,resolutionChannel,resolutionChannel )
			
			## Create a new project or import Object
			if new == True:
				importChannel.setPath(folder)
				importChannel.setFileTemplate(texture)
				##if channelName == "Normal":
			else:
				importChannel.setPath("/tmp")
				importChannel.setFileTemplate(folder+texture)

			listImportChannels.append(importChannel)

	dicImportChannels.update({"name":channelName,'ImportChannels':listImportChannels})
		
	## GeoChannels
	options = {"GeoChannels": dicGeoChannels}

	return dicImportChannels,listImportChannels

def createMegascansShader(name,listImportChannels,shader,colorspace):
	currentGeo = mari.geo.current()
	allShaders = currentGeo.shaderList()
	shaderGeo = currentGeo.currentShader()
	shaderType = shaderGeo.shaderModel()
	##shaderType = curGeo.shaderStandaloneTypeList()
	##colorspace = 'linear'
	
	## Create and Assign to Object new shader
	newShader = currentGeo.createShader(name + '_shd',shader)
	currentGeo.setCurrentShader(newShader)
	
	listChannels = currentGeo.currentShader().inputNameList()

	## Shader Convertion
	if shader == "Lighting/Standalone/PxrSurface":
		baseColor = "diffuseColor"
		ambientOcclusion = "AmbientOcclusion"
		specRoughness = "specularRoughness"
		normal = "Normal"
	elif shader == "Shaders/Vendor Shaders/Unreal":
		baseColor = "BaseColor"
		ambientOcclusion = "AmbientOcclusion"
		specRoughness="Roughness"
		normal = "Normal"
	elif shader == "Shaders/Vendor Shaders/Arnold Standard Surface":
		baseColor = "DiffuseColor"
		ambientOcclusion = "AmbientOcclusion"
		specRoughness="SpecularRoughness"
		normal = "Normal"

	## Connect Channel to Shader
	for channel in listImportChannels:
		try:
			if channel.name() == "Albedo":
				newShader.setInput(baseColor, currentGeo.channel("Albedo"))
			elif channel.name() == "AO":
				newShader.setInput(ambientOcclusion, currentGeo.channel("AO"))
			elif channel.name() == "Roughness":
				newShader.setInput(specRoughness, currentGeo.channel("Roughness"))
			elif channel.name() == "Normal":
				newShader.setInput(normal, currentGeo.channel("Normal"))
			else:
				newShader.setInput(channel.name(), currentGeo.channel(channel.name()))
		except:
			print "Skip Shader Assignment, couldn't assign channel: " + str(channel.name())

		## Fix Colorspace after import
		chan = mari.geo.current().findChannel(channel.name())
		curConfig = chan.colorspaceConfig()
		curConfig.setColorspace(mari.ColorspaceConfig.COLORSPACE_STAGE_NATIVE,colorspace)
		chan.setColorspaceConfig(curConfig)

	return newShader

def createLighting(shader,hdrPath):
	envMap = hdrPath
	envLight = None
	listLights = mari.lights.list()
	for light in listLights:
		if light.isEnvironmentLight() == True:
			print("Update HDR for : " + light.name())
			envLight = light
			previousCubeMapFilename = light.cubeImageFilename()
			# Set map
			envLight.setCubeImageResolution( 512)
			envLight.setCubeImage(envMap, envLight.TYPE_2D_LATLONG)
			# match katana unit shader lights intensity
			envLight.setIntensity( 1.0)
			# match katana unit shader lights rotation
			# need to rotate by 180 to match flow
			envLight.setRotationUp(180)
			# Enable light
			envLight.setOn(True)

	if envLight == None:
		print("No Envlight in the scene")
		try:
			if shader.shaderModel() == "Lighting/Standalone/PxrSurface":
				print("Will Add envLight")
		except:
			if shader == "Lighting/Standalone/PxrSurface":
				print("Texture Mode - Will Add envLight")

def findEnvMap(hdr,libraryTexturePath):
	if hdr == "Luxo":
		path = libraryTexturePath + "/hdriDefault/luxo_pxr_1k/luxo_pxr_1k.exr"
	elif hdr == "MPC_sunny":
		path = libraryTexturePath+ "/hdri/lookdev_sunny/lookdev_sunny.exr"
	elif hdr == "MPC_overcast":
		path = libraryTexturePath+"/hdri/lookdev_overcast/lookdev_overcast.exr"

	return path

def importMegascansModel(pathModel,importChannels):
	mari.geo.load(pathModel,importChannels)

def importTexture(pathTexture,colorspace):
	pictures = mari.images.open(pathTexture)
	for pic in pictures:
		curColorspace = pic.colorspaceConfig()
		curColorspace.setColorspace(mari.ColorspaceConfig.COLORSPACE_STAGE_NATIVE,colorspace)
		pic.setColorspaceConfig(curColorspace)

def importTextureMegascans(pathTexture,colorspace):
	pictures = mari.images.open(pathTexture)
	if "diffuse" in pathTexture.lower() or "albedo" in pathTexture.lower():
		colorspace = "Automatic"

	for pic in pictures:
		curColorspace = pic.colorspaceConfig()
		curColorspace.setColorspace(mari.ColorspaceConfig.COLORSPACE_STAGE_NATIVE,colorspace)
		pic.setColorspaceConfig(curColorspace)


def createTextureCategory(name):
	listCategory = mari.images.categories()
	if name in listCategory:
		mari.images.selectCategory(name)
	else:
		mari.images.addCategory(name)
		mari.images.selectCategory(name)

