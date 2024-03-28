import sys
import os

class sgFindSoftware():
	def softwareUsed(self):
		pythonVersion = (sys.version_info[0])
		if pythonVersion == 3:
			import imp
			
		## Nuke Version
		try:
			import nuke
			in_nuke= True
		except:
			in_nuke= False

		## Mari Version
		try:
			import mari
			in_mari= True
		except:
			in_mari= False

		## Katana Version
		try:
			import Katana
			from Katana import NodegraphAPI
			in_katana= True
		except:
			in_katana= False

		## Maya Version
		try:
			# cmds is loaded in different tool, using Arnold as maya specific
			from mtoa.core import createStandIn, createVolume
			in_maya= True
		except:
			in_maya= False

		## Houdini Version
		try:
			import hou
			in_hou= True
		except:
			in_hou= False

		## Blender
		try:
			import bpy
			in_blen = True
		except:
			in_blen = False

		## Unreal
		try:
			import unreal
			in_unreal = True
		except:
			in_unreal = False

		## Variables Software
		if in_maya:
			softwareUsed = "Maya"
		elif in_nuke:
			softwareUsed = "Nuke"
		elif in_hou:
			softwareUsed = "Houdini"
		elif in_mari:
			softwareUsed = "Mari"
		elif in_unreal:
			softwareUsed = "Unreal"
		elif in_katana:
			softwareUsed = "Katana"
		elif in_blen:
			softwareUsed = "Blender"
		else:
			softwareUsed = "Python"

		return softwareUsed

	def isNuke(self):
		## Nuke Version
		try:
			import nuke
			return True
		except:
			return False
	def isMaya(self):
		## Maya Version
		try:
			# cmds is loaded in different tool, using Arnold as maya specific
			from mtoa.core import createStandIn, createVolume
			return True
		except:
			return False
	def isKatana(self):
		## Katana Version
		try:
			import Katana
			from Katana import NodegraphAPI
			return True
		except:
			return False
	def isMari(self):
		## Mari Version
		try:
			import mari
			return True
		except:
			return False
	def isHoudini(self):
		## Houdini Version
		try:
			import hou
			return True
		except:
			return False
	def isBlender(self):
		## Blender
		try:
			import bpy
			return True
		except:
			return False
	def isUnreal(self):
		## Unreal
		try:
			import unreal
			return True
		except:
			return False
	def isPython(self):
		return False