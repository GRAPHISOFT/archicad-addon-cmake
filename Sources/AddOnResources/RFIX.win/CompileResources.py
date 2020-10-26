import os
import sys
import subprocess

currentDir = os.path.dirname (os.path.abspath (__file__))
os.chdir (currentDir)

if len (sys.argv) != 5:
	print ('Usage: CompileResources.py <languageCode> <devKitPath> <resourceObjectsPath> <resultResourceFilePath>')
	sys.exit (1)

languageCode = sys.argv[1]
devKitPath = os.path.abspath (sys.argv[2])
resourceObjectsPath = os.path.abspath (sys.argv[3])
resultResourceFilePath = os.path.abspath (sys.argv[4])

resourcesPath = os.path.dirname (currentDir)
resConvPath = os.path.join (devKitPath, 'Support', 'Tools', 'Win', 'ResConv.exe')

# Compile localized resources
locResourcesFolder = os.path.join (resourcesPath, 'RINT');
for fileName in os.listdir (locResourcesFolder):
	extension = os.path.splitext (fileName)[1]
	if extension != '.grc':
		break
	grcFilePath = os.path.join (locResourcesFolder, fileName)
	rc2Path = os.path.join (resourceObjectsPath, fileName + '.rc2')
	result = subprocess.call ([
		resConvPath,
		'-m',
		'r',
		'-D', 'WINDOWS',
		'-T',
		'W',
		'-q', 'utf8', '1252',
		'-i', grcFilePath,
		'-o', rc2Path
	])
	if result != 0:
		print ('Failed to compile resource: ' + fileName)
		sys.exit (1)

# Compile fix resources
fixResourcesFolder = os.path.join (resourcesPath, 'RFIX');
imageResourcesFolder = os.path.join (fixResourcesFolder, 'Images')
for fileName in os.listdir (fixResourcesFolder):
	extension = os.path.splitext (fileName)[1]
	if extension != '.grc':
		break
	grcFilePath = os.path.join (fixResourcesFolder, fileName)
	rc2Path = os.path.join (resourceObjectsPath, fileName + '.rc2')
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
		'-o', rc2Path
	])
	if result != 0:
		print ('Failed to compile resource: ' + fileName)
		sys.exit (1)

# Compile native resources
result = subprocess.call ([
	'rc',
	'/i', os.path.join (devKitPath, 'Support', 'Inc'),
	'/i', os.path.join (devKitPath, 'Support', 'Modules', 'DGLib'),
	'/i', resourceObjectsPath,
	'/fo', resultResourceFilePath,
	os.path.join (resourcesPath, 'RFIX.win', 'AddOnMain.rc2')
])
if result != 0:
	print ('Failed to compile native resource')
	sys.exit (1)

sys.exit (0)
