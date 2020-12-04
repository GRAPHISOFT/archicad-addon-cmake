import os
import sys
import platform
import subprocess
import shutil
import codecs

class ResourceCompiler (object):
	def __init__ (self, devKitPath, languageCode, sourcesPath, resourcesPath, resourceObjectsPath):
		self.devKitPath = devKitPath
		self.languageCode = languageCode
		self.sourcesPath = sourcesPath
		self.resourcesPath = resourcesPath
		self.resourceObjectsPath = resourceObjectsPath
		self.resConvPath = None
		
	def IsValid (self):
		if self.resConvPath == None:
			return False
		if not os.path.exists (self.resConvPath):
			return False
		return True

	def CompileLocalizedResources (self):
		locResourcesFolder = os.path.join (self.resourcesPath, 'R' + self.languageCode)
		grcFiles = self.CollectGrcFilesFromFolder (locResourcesFolder)
		for grcFilePath in grcFiles:
			if not self.CompileResourceFile (grcFilePath):
				print ('Failed to compile resource: ' + grcFilePath)
				return False
		return True

	def CompileFixResources (self):
		fixResourcesFolder = os.path.join (self.resourcesPath, 'RFIX')
		grcFiles = self.CollectGrcFilesFromFolder (fixResourcesFolder)
		for grcFilePath in grcFiles:
			if not self.CompileResourceFile (grcFilePath):
				print ('Failed to compile resource: ' + grcFilePath)
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
	def __init__ (self, devKitPath, languageCode, sourcesPath, resourcesPath, resourceObjectsPath):
		super (WinResourceCompiler, self).__init__ (devKitPath, languageCode, sourcesPath, resourcesPath, resourceObjectsPath)
		self.resConvPath = os.path.join (devKitPath, 'Support', 'Tools', 'Win', 'ResConv.exe')

	def CompileResourceFile (self, grcFilePath):
		grcFileName = os.path.split (grcFilePath)[1]
		nativeResourceFilePath = os.path.join (self.resourceObjectsPath, grcFileName + '.rc2')
		imageResourcesFolder = os.path.join (self.resourcesPath, 'RFIX', 'Images')
		result = subprocess.call ([
			self.resConvPath,
			'-m', 'r',						# resource compile mode
			'-T', 'W',						# windows target
			'-q', 'utf8', '1252',			# code page conversion
			'-w', '2',						# HiDPI image size list
			'-p', imageResourcesFolder,		# image search path
			'-i', grcFilePath,				# input path
			'-o', nativeResourceFilePath	# output path
		])
		if result != 0:
			return False
		return True

	def CompileNativeResource (self, resultResourcePath):
		result = subprocess.call ([
			'rc',
			'/i', os.path.join (self.devKitPath, 'Support', 'Inc'),
			'/i', os.path.join (self.devKitPath, 'Support', 'Modules', 'DGLib'),
			'/i', self.sourcesPath,
			'/i', self.resourceObjectsPath,
			'/fo', resultResourcePath,
			os.path.join (self.resourcesPath, 'RFIX.win', 'AddOnMain.rc2')
		])
		if result != 0:
			print ('Failed to compile native resource')
			return False
		return True

class MacResourceCompiler (ResourceCompiler):
	def __init__ (self, devKitPath, languageCode, sourcesPath, resourcesPath, resourceObjectsPath):
		super (MacResourceCompiler, self).__init__ (devKitPath, languageCode, sourcesPath, resourcesPath, resourceObjectsPath)
		self.resConvPath = os.path.join (devKitPath, 'Support', 'Tools', 'OSX', 'ResConv')

	def CompileResourceFile (self, grcFilePath):
		grcFileName = os.path.split (grcFilePath)[1]
		precompiledGrcFilePath = os.path.join (self.resourceObjectsPath, grcFileName + '.i')
		result = subprocess.call ([
			'clang',
			'-x', 'c++',
			'-E',
			'-P',
			'-Dmacintosh',
			'-I', self.sourcesPath,
			'-o', precompiledGrcFilePath,
			grcFilePath,
		])
		if result != 0:
			return False
		nativeResourceFilePath = os.path.join (self.resourceObjectsPath, grcFileName + '.ro')
		imageResourcesFolder = os.path.join (self.resourcesPath, 'RFIX', 'Images')
		result = subprocess.call ([
			self.resConvPath,
			'-m', 'r',						# resource compile mode
			'-T', 'M',						# macos target
			'-q', 'utf8', 'utf16',			# code page conversion
			'-w', '2',						# HiDPI image size list
			'-p', imageResourcesFolder,		# image search path
			'-i', precompiledGrcFilePath,	# input path
			'-o', nativeResourceFilePath	# output path
		])
		if result != 0:
			return False
		return True

	def CompileNativeResource (self, resultResourcePath):
		resultLocalizedResourcePath = os.path.join (resultResourcePath, 'English.lproj')
		if not os.path.exists (resultLocalizedResourcePath):
			os.makedirs (resultLocalizedResourcePath)
		resultLocalizableStringsPath = os.path.join (resultLocalizedResourcePath, 'Localizable.strings')
		resultLocalizableStringsFile = codecs.open (resultLocalizableStringsPath, 'w', 'utf-16')
		for fileName in os.listdir (self.resourceObjectsPath):
			filePath = os.path.join (self.resourceObjectsPath, fileName)
			extension = os.path.splitext (fileName)[1]
			if extension == '.tif':
				shutil.copy (filePath, resultResourcePath)
			elif extension == '.rsrd':
				shutil.copy (filePath, resultLocalizedResourcePath)
			elif extension == '.strings':
				stringsFile = codecs.open (filePath, 'r', 'utf-16')
				resultLocalizableStringsFile.write (stringsFile.read ())
				stringsFile.close ()
		resultLocalizableStringsFile.close ()
		return True

def Main (argv):
	if len (argv) != 7:
		print ('Usage: CompileResources.py <languageCode> <devKitPath> <sourcesPath> <resourcesPath> <resourceObjectsPath> <resultResourcePath>')
		return 1

	currentDir = os.path.dirname (os.path.abspath (__file__))
	os.chdir (currentDir)

	languageCode = argv[1]
	devKitPath = os.path.abspath (argv[2])
	sourcesPath = os.path.abspath (argv[3])
	resourcesPath = os.path.abspath (argv[4])
	resourceObjectsPath = os.path.abspath (argv[5])
	resultResourcePath = os.path.abspath (argv[6])

	resourceCompiler = None
	system = platform.system ()
	if system == 'Windows':
		resourceCompiler = WinResourceCompiler (devKitPath, languageCode, sourcesPath, resourcesPath, resourceObjectsPath)
	elif system == 'Darwin':
		resourceCompiler = MacResourceCompiler (devKitPath, languageCode, sourcesPath, resourcesPath, resourceObjectsPath)

	if resourceCompiler == None:
		print ('Platform is not supported')
		return 1

	if not resourceCompiler.IsValid ():
		print ('Invalid resource compiler')
		return 1

	if not resourceCompiler.CompileLocalizedResources ():
		return 1

	if not resourceCompiler.CompileFixResources ():
		return 1

	if not resourceCompiler.CompileNativeResource (resultResourcePath):
		return 1

	return 0

sys.exit (Main (sys.argv))
