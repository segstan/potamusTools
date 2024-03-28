import bpy
import os

def importModel(pathModel):
	geo = bpy.ops.import_scene.fbx(filepath=pathModel)

def importTexture(path,name):
	img = bpy.data.images.load(path)
	textureFile = bpy.data.textures.new(name, type='IMAGE')
	textureFile.image = img

def createThumbnail(thumbnailPath,imgWidth,imgHeight,contextOverride):
	# current Context
	context = bpy.context

	## set render settings
	bpy.data.scenes[0].render.resolution_x = imgWidth
	bpy.data.scenes[0].render.resolution_y = imgHeight
	bpy.data.scenes[0].render.resolution_percentage = 100
	## render
	if bpy.ops.render.opengl.poll() == False:
		with context.temp_override(**contextOverride):
			bpy.ops.render.opengl(view_context = False)
	else:
		bpy.ops.render.opengl(view_context = False)
		
	## save image
	img_name = os.path.basename(thumbnailPath)
	bpy.data.images['Render Result'].save_render(thumbnailPath)
	#bpy.ops.image.open(filepath = thumbnailPath)
	#bpy.data.images[img_name].pack()

	return img_name

def importMegascansModel(pathModel,name,contextOverride):
	context = contextOverride
	typeFile = pathModel.split(".")[-1]
	geo = name
	imported_objects=[]
	context['area']= "VIEW_3D"
	override = {'region': "WINDOW", 'area':  "VIEW_3D"}

	# Create a set out of the objects in the current scene (unique by default)
	objs = set(bpy.context.scene.objects)

	if typeFile == "fbx":
		bpy.ops.import_scene.fbx(filepath=pathModel)
	elif typeFile == "obj":
		bpy.ops.import_scene.obj(filepath=pathModel)
	elif typeFile == "abc":
		print(bpy.context.window_manager.windows[0])
		with context.temp_override(window = bpy.context.window_manager.windows[0]):
			#if bpy.ops.wm.alembic_import.poll() == False:
			bpy.ops.wm.alembic_import(override,filepath=pathModel,as_background_job=False)

	# Substract all previous items from the current items and print their names
	imported_objs = set(bpy.context.scene.objects) - objs
	#print(", ".join(o.name for o in imported_objs))

	return imported_objs

def createTextureFileBlender(name,path):
	img = bpy.data.images.load(path)
	textureFile = bpy.data.textures.new("T_"+ name.split(".")[0], type='IMAGE')
	textureFile.image = img
	return textureFile

def buildMegascanShaderBlender(listTextures,renderer,nameAsset,geo,):
	print(geo)
	for obj in geo:
		bpy.data.objects[obj].select_set(True)
		# print the name of the current obj
		print (obj.name)

		# set current object to the active one
		bpy.context.scene.objects.active = obj
		bpy.context.view_layer.objects.active = obj
		# Get material
		mat = bpy.data.materials.get("Material")
		if mat is None:
			# create material
			mat = bpy.data.materials.new(name="Material")

		# Assign it to object
		if obj.data.materials:
			# assign to 1st material slot
			obj.data.materials[0] = mat
		else:
			# no slots
			obj.data.materials.append(mat)

		for texture in listTextures:
			##Making a slot for the texture to go in:
			slot = mat.texture_slots.add()

			##Connecting the texture to the material:
			slot.texture = tex