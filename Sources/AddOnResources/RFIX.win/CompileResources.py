import os
import sys
import subprocess

def CompileOneLocalizedResourceFile (resConvPath, grcFilePath, nativeResourceFilePath):
	result = subprocess.call ([
		resConvPath,
		'-m',
		'r',
		'-D', 'WINDOWS',
		'-T',
		'W',
		'-q', 'utf8', '1252',
		'-i', grcFilePath,
		'-o', nativeResourceFilePath
	])
	return result == 0

def CompileOneFixResourceFile (resConvPath, grcFilePath, imageResourcesFolder, nativeResourceFilePath):
	result = subprocess.call ([
		resConvPath,
		'-m',
		'r',
		'-D', 'WINDOWS',
		'-T',
		'W',
		'-w', '2',
		'-p', imageResourcesFolder,
		'-q', 'utf8', '1252',
		'-i', grcFilePath,
		'-o', nativeResourceFilePath
	])
	return result == 0

def CompileLocalizedResources (resConvPath, resourcesPath, resourceObjectsPath):
	locResourcesFolder = os.path.join (resourcesPath, 'RINT');
	for fileName in os.listdir (locResourcesFolder):
		extension = os.path.splitext (fileName)[1]
		if extension != '.grc':
			continue
		grcFilePath = os.path.join (locResourcesFolder, fileName)
		nativeResourceFilePath = os.path.join (resourceObjectsPath, fileName + '.rc2')
		if not CompileOneLocalizedResourceFile (resConvPath, grcFilePath, nativeResourceFilePath):
			print ('Failed to compile resource: ' + fileName)
			return False
	return True

def CompileFixResources (resConvPath, resourcesPath, resourceObjectsPath):
	fixResourcesFolder = os.path.join (resourcesPath, 'RFIX');
	imageResourcesFolder = os.path.join (fixResourcesFolder, 'Images')
	for fileName in os.listdir (fixResourcesFolder):
		extension = os.path.splitext (fileName)[1]
		if extension != '.grc':
			continue
		grcFilePath = os.path.join (fixResourcesFolder, fileName)
		nativeResourceFilePath = os.path.join (resourceObjectsPath, fileName + '.rc2')
		if not CompileOneFixResourceFile (resConvPath, grcFilePath, imageResourcesFolder, nativeResourceFilePath):
			return False
	return True

def CompileNativeResources (devKitPath, resourcesPath, resourceObjectsPath, resultResourceFilePath):
	result = subprocess.call ([
		'rc',
		'/i', os.path.join (devKitPath, 'Support', 'Inc'),
		'/i', os.path.join (devKitPath, 'Support', 'Modules', 'DGLib'),
		'/i', resourceObjectsPath,
		'/fo', resultResourceFilePath,
		os.path.join (resourcesPath, 'RFIX.win', 'AddOnMain.rc2')
	])
	return result == 0

def Main (argv):
	if len (argv) != 5:
		print ('Usage: CompileResources.py <languageCode> <devKitPath> <resourceObjectsPath> <resultResourceFilePath>')
		return 1

	currentDir = os.path.dirname (os.path.abspath (__file__))
	os.chdir (currentDir)

	languageCode = argv[1]
	devKitPath = os.path.abspath (argv[2])
	resourceObjectsPath = os.path.abspath (argv[3])
	resultResourceFilePath = os.path.abspath (argv[4])

	resourcesPath = os.path.dirname (currentDir)
	resConvPath = os.path.join (devKitPath, 'Support', 'Tools', 'Win', 'ResConv.exe')

	# Compile localized resources
	if not CompileLocalizedResources (resConvPath, resourcesPath, resourceObjectsPath):
		return 1

	# Compile fix resources
	if not CompileFixResources (resConvPath, resourcesPath, resourceObjectsPath):
		return 1

	# Compile native resources
	if not CompileNativeResources (devKitPath, resourcesPath, resourceObjectsPath, resultResourceFilePath):
		print ('Failed to compile native resource')
		return 1

	return 0

sys.exit (Main (sys.argv))
