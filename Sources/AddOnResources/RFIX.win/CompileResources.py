import os
import sys
import subprocess
import platform

def IsWindows ():
	return platform.system () == 'Windows'

def IsMacOS ():
	return platform.system () == 'Darwin'

class ResourceCompiler:
	def __init__ (self, devKitPath, languageCode, resourcesPath, resourceObjectsPath):
		self.devKitPath = devKitPath
		self.languageCode = languageCode
		self.resourcesPath = resourcesPath
		self.resourceObjectsPath = resourceObjectsPath

	def CompileLocalizedResources (self):
		locResourcesFolder = os.path.join (self.resourcesPath, 'R' + self.languageCode);
		grcFiles = self.CollectGrcFilesFromFolder (locResourcesFolder)
		for grcFile in grcFiles:
			fileName = os.path.split (grcFile)[1]
			nativeResourceFilePath = os.path.join (self.resourceObjectsPath, fileName + '.rc2')
			if not self.CompileLocalizedResourceFile (grcFile, nativeResourceFilePath):
				print ('Failed to compile resource: ' + fileName)
				return False
		return True

	def CompileFixResources (self):
		fixResourcesFolder = os.path.join (self.resourcesPath, 'RFIX');
		imageResourcesFolder = os.path.join (fixResourcesFolder, 'Images')
		grcFiles = self.CollectGrcFilesFromFolder (fixResourcesFolder)
		for grcFile in grcFiles:
			fileName = os.path.split (grcFile)[1]
			nativeResourceFilePath = os.path.join (self.resourceObjectsPath, fileName + '.rc2')
			if not self.CompileFixResourceFile (grcFile, imageResourcesFolder, nativeResourceFilePath):
				print ('Failed to compile resource: ' + fileName)
				return False
		return True

	def CollectGrcFilesFromFolder (self, folderPath):
		result = []
		for fileName in os.listdir (folderPath):
			extension = os.path.splitext (fileName)[1]
			if extension == '.grc':
				grcFilePath = os.path.join (folderPath, fileName)
				result.append (grcFilePath)
		return result

class WinResourceCompiler (ResourceCompiler):
	def __init__ (self, devKitPath, languageCode, resourcesPath, resourceObjectsPath):
		super ().__init__ (devKitPath, languageCode, resourcesPath, resourceObjectsPath)
		self.resConvPath = os.path.join (devKitPath, 'Support', 'Tools', 'Win', 'ResConv.exe')

	def CompileLocalizedResourceFile (self, grcFilePath, nativeResourceFilePath):
		result = subprocess.call ([
			self.resConvPath,
			'-m', 'r',						# resource compile mode
			'-T', 'W',						# windows target
			'-q', 'utf8', '1252',			# code page conversion
			'-i', grcFilePath,				# input path
			'-o', nativeResourceFilePath	# output path
		])
		return result == 0

	def CompileFixResourceFile (self, grcFilePath, imageResourcesFolder, nativeResourceFilePath):
		result = subprocess.call ([
			self.resConvPath,
			'-m', 'r',						# resource compile mode
			'-T', 'W',						# windows target
			'-q', 'utf8', '1252',			# code page conversion
			'-w', '2',						# HiDPI image size list
			'-p', imageResourcesFolder,		# search path
			'-i', grcFilePath,				# input path
			'-o', nativeResourceFilePath	# output path
		])
		return result == 0

	def CompileNativeResource (self, resultResourcePath):
		result = subprocess.call ([
			'rc',
			'/i', os.path.join (self.devKitPath, 'Support', 'Inc'),
			'/i', os.path.join (self.devKitPath, 'Support', 'Modules', 'DGLib'),
			'/i', self.resourceObjectsPath,
			'/fo', resultResourcePath,
			os.path.join (self.resourcesPath, 'RFIX.win', 'AddOnMain.rc2')
		])
		if result != 0:
			print ('Failed to compile native resource')
			return False
		return True

def Main (argv):
	if len (argv) != 6:
		print ('Usage: CompileResources.py <languageCode> <devKitPath> <resourcesPath> <resourceObjectsPath> <resultResourceFilePath>')
		return 1

	currentDir = os.path.dirname (os.path.abspath (__file__))
	os.chdir (currentDir)

	languageCode = argv[1]
	devKitPath = os.path.abspath (argv[2])
	resourcesPath = os.path.abspath (argv[3])
	resourceObjectsPath = os.path.abspath (argv[4])
	resultResourcePath = os.path.abspath (argv[5])

	resourceCompiler = None
	if IsWindows ():
		resourceCompiler = WinResourceCompiler (devKitPath, languageCode, resourcesPath, resourceObjectsPath)

	if resourceCompiler == None:
		print ('Platform is not supported')
		return 1

	if not resourceCompiler.CompileLocalizedResources ():
		return 1

	if not resourceCompiler.CompileFixResources ():
		return 1

	if not resourceCompiler.CompileNativeResource (resultResourcePath):
		return 1

	return 0

sys.exit (Main (sys.argv))
