import nuke
import nukescripts
import random

################################################### Generic Utils ############################################################

def saveSelection():
	listSelection = []
	for node in nuke.selectedNodes():
		if node['selected'].value() == True:
			listSelection.append(node)
	return listSelection

def restoreSelection(listSelection,value):
	for node in listSelection:
		node['selected'].setValue(value)

def clearSelection():
	for node in nuke.selectedNodes():
		node['selected'].setValue(False)

################################################## Create Nodes #############################################################

def createTextureFileNuke(filepath):
	nameImage = filepath.split("/")[-1]
	read = nuke.nodes.Read(file="%s" %(filepath))
	
	if nuke.exists(nameImage.split(".")[0]):
		nameNode = nameImage.split(".")[0]+ "_" + str(random.randint(1,999999))
	else:
		nameNode = nameImage.split(".")[0]
	read["name"].setValue(nameNode)
	read["first"].setValue(1001)
	read["last"].setValue(1001)
	read["postage_stamp"].setValue(False)
	read["selected"].setValue(True)

	return read

def createSequenceTextureFileNuke(folder,sequence):
	nameImage = sequence.split(" ")[0].split(".")[0]
	read = nuke.createNode('Read')
	
	if nuke.exists(nameImage.split(".")[0]):
		nameNode = nameImage.split(".")[0]+ "_" + str(random.randint(1,999999))
	else:
		nameNode = nameImage.split(".")[0]
	
	read["name"].setValue(nameNode)
	read.knob('file').fromUserText(folder+sequence)
	read["postage_stamp"].setValue(False)
	read["selected"].setValue(True)

	return read

def createOCIONuke(readNode,megascans):
	## Create OCIO Node
	ocio = nuke.nodes.OCIOColorSpace()

	if megascans == True:
		in_colour = 0
		i = 0
		if "Albedo" in readNode['name'].value() or "Translucency" in readNode['name'].value():
			for cSpace in ocio["in_colorspace"].values():			
				if "sRGB" in cSpace:
					in_colour = i
					break
				i +=1
		else:
			for cSpace in ocio["out_colorspace"].values():
				if "linear" in cSpace:
					in_colour = i
					break
				i +=1	

		j = 0
		out_colour = 0
		for cSpace in ocio["out_colorspace"].values():
			if "linear" in cSpace:
				break
			out_colour+= 1

		ocio["in_colorspace"].setValue(in_colour)
		ocio["out_colorspace"].setValue(out_colour)

	## Connect
	ocio.setInput(0,readNode)
	## Select
	ocio["selected"].setValue(True)

	return ocio

def create3DProj(readNodeAlbedo):
	print("Creating New Projection Setup")
	## Create Nodes
	project3d = nuke.nodes.Project3D()
	if readNodeAlbedo != None:
		posRead= [int(readNodeAlbedo['xpos'].value()),int(readNodeAlbedo['ypos'].value())]
	else:
		posRead= [int(project3d['xpos'].value()),int(project3d['ypos'].value())]
	frameHold = nuke.nodes.FrameHold()
	frameHold.knob("setToCurrentFrame").execute()

	# Normal Camera
	camera = nuke.nodes.Camera()
	# USD Camera
	# camera= nuke.nodes.Camera4()
	# Transform camera to be able to use a card scale 1
	camera['translate'].setValue([0,2,0])
	camera['rotate'].setValue([-90,0,0])

	premult = nuke.nodes.Premult()

	copy = nuke.nodes.Copy()
	copy['from0'].setValue("rgba.red")
	copy['to0'].setValue("rgba.alpha")

	dotCopy = nuke.nodes.Dot()

	# Position
	project3d.setXYpos(posRead[0],posRead[1]+600)
	frameHold.setXYpos(posRead[0]-200,posRead[1]+505)
	camera.setXYpos(posRead[0]-190,posRead[1]+350)
	dotCopy.setXYpos(int(posRead[0]-450),int(posRead[1]+190))
	copy.setXYpos(int(posRead[0]),int(posRead[1]+175))  
	premult.setXYpos(int(posRead[0]),int(posRead[1]+450))  
	# Connect
	frameHold.setInput(0,camera)
	project3d.setInput(1,frameHold)
	project3d.setInput(0,premult)
	premult.setInput(0,copy)
	if readNodeAlbedo != None:
		#project3d.setInput(0,readNode)
		copy.setInput(0,readNodeAlbedo)
	copy.setInput(1,dotCopy)

	return [project3d,frameHold,camera]

def importModel(filepath,uniformScale):
	if nuke.exists(filepath.split("/")[-1].split(".")[0]):
		nameGeo = filepath.split("/")[-1].split(".")[0]+ "_" +str(random.randint(1,99999))
	else:
		nameGeo = filepath.split("/")[-1].split(".")[0]
	# readGeo = nuke.nodes.ReadGeo2(file="%s" %(filepath))
	## Alembic loading is tricky
	readGeo= nuke.createNode('ReadGeo2', 'file {'+filepath+'}')
	readGeo["name"].setValue(nameGeo)
	readGeo["uniform_scale"].setValue(uniformScale)
	if ".abc" not in filepath:
		readGeo["read_from_file"].setValue(False)
	if ".abc" in filepath:
		sceneView = readGeo["scene_view"]
		allItems = sceneView.getAllItems()
		if allItems:
			sceneView.setImportedItems(allItems)
			sceneView.setSelectedItems(allItems)

	readGeo["selected"].setValue(True)
	readGeo.autoplace()

def panelCustomLODLoad(listLOD):
	p = nuke.Panel("Pick LOD")
	p.addEnumerationPulldown("LOD available: ",listLOD)
	p.show()

def importVDB(filepath,name):
	vdb = nuke.nodes.EddyCacheLoader(file=filepath)
	vdb["selected"].setValue(True)
	channelSet = nuke.nodes.EddyChannelSet()
	channelSet["selected"].setValue(True)
	channelSet.setInput(0,vdb)

	shader = nuke.nodes.EddyRenderVolume(rendervolume_nodescript=2)
	shader["selected"].setValue(True)
	shader.setInput(0,channelSet)

	refresh = vdb.knob("btn_reload").execute()
	return vdb

def refreshVDB(vdb):
	refresh = vdb.knob("btn_reload").execute()

def writeTextureToExport(node,folder,name):
	node['selected'].setValue(True)
	print(name)
	image = folder + name + ".exr"
	write= nuke.nodes.Write(channels = "rgba", create_directories = True, file_type = "exr", file = image)
	write.setInput(0,node)

	nuke.execute(write,nuke.frame(),nuke.frame())
	nuke.delete(write)

def createThumbnail(path,node):
	reformat = nuke.nodes.Reformat(format="square_256",resize=5)
	## set a color convertion from linear to srgb to get a decent thumbnail
	ocio = nuke.nodes.OCIOColorSpace(in_colorspace = 2,out_colorspace=6)
	writeTh = nuke.nodes.Write(channels= "rgba", create_directories= True, file_type ="jpg", file=path)
	
	reformat.setInput(0,node)
	ocio.setInput(0,reformat)
	writeTh.setInput(0,ocio)

	nuke.execute(writeTh,nuke.frame(),nuke.frame())

	nuke.delete(reformat)
	nuke.delete(ocio)
	nuke.delete(writeTh)



#################################################################### UI ###############################################################

def autoPlaceSelectedNodes():
	for n in nuke.selectedNodes():
		nuke.autoplace(n)
		nuke.autoplaceSnap(n)

def createBackDrop(name):
	randomColour = [0x386638ff,0x664837ff,0x376660ff,0x375266ff,0x4b3766ff,0x66374cff,0x663a37ff]
	backDrop = nukescripts.autoBackdrop()

	colour = random.choice(randomColour)
	backDrop["label"].setValue(name)
	backDrop["note_font"].setValue("Verdana Bold")
	backDrop["note_font_size"].setValue(35)
	backDrop['tile_color'].setValue(colour)
	backDrop['selected'].setValue(True)
	backDrop['bdheight'].setValue(backDrop.height()+10)
	backDrop['bdwidth'].setValue(backDrop.width()+5)

################################################################## MPC ################################################################

def createHubCamera(sequence):
	camera = nuke.createNode('hubCamera')
	camera["selected"].setValue(0)
	if sequence != None:
		camera["sceneHub"].setValue(sequence.split("/")[0])
		camera["shotHub"].setValue(sequence.split("/")[-1])
		#camera["elementHub"].setValue('build_sequence')
	print("New Hub Camera")

	return camera