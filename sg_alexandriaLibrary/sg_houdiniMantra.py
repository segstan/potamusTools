import hou
import os
import json

def createSharedMantraTexture(sharedUV,triplanar,containerTexture,name):
	manifold =""
	if triplanar == False  and sharedUV == True:
		manifold= containerTexture.createNode('uvcoords',"uvcoords_"+name )
	elif triplanar == True and sharedUV == True:
		manifold = ""
	return manifold

def createTextureFileMantra(sharedUV,triplanar,manifold,name,path,containerTexture):
	if sharedUV == False and triplanar == False:
		textureFile = containerTexture.createNode('texture',"T_"+name)
		parameter = textureFile.parm('map').set(path)
		manifold= containerTexture.createNode('uvcoords',"uvcoords_"+name )
		textureFile.setInput(0,manifold,0)
		textureFile.moveToGoodPosition()
		manifold.moveToGoodPosition()
	elif sharedUV == True and triplanar == False :
		textureFile = containerTexture.createNode('texture',"T_"+name)
		parameter = textureFile.parm('map').set(path)
		textureFile.setInput(0,manifold,0)
		textureFile.moveToGoodPosition()
		manifold.moveToGoodPosition()
	elif sharedUV == False and triplanar == True:
		textureFile = containerTexture.createNode('uvtriplanarproject',"T_"+name)
		parameter0 = textureFile.parm('xposmap').set(path)
		parameter1 = textureFile.parm('yposmap').set(path)
		parameter2 = textureFile.parm('zposmap').set(path)
		parameterTintx = textureFile.parm('xTint').set(False)
		parameterTinty = textureFile.parm('yTint').set(False)
		parameterTintz = textureFile.parm('zTint').set(False)
		##manifold = containerTexture.createNode('pxrroundcube',"pxrroundcube_"+name)
		##textureFile.setInput(0,manifold,1)
		textureFile.moveToGoodPosition()
		##manifold.moveToGoodPosition()
	elif sharedUV == True and triplanar == True:
		textureFile = containerTexture.createNode('uvtriplanarproject',"T_"+name)
		parameter0 = textureFile.parm('xposmap').set(path)
		parameter1 = textureFile.parm('yposmap').set(path)
		parameter2 = textureFile.parm('zposmap').set(path)
		##textureFile.setInput(0,manifold,1)
		textureFile.moveToGoodPosition()
		##manifold.moveToGoodPosition()

	containerTexture.layoutChildren()
	return textureFile

