import os
import sys
import subprocess

currentDir = os.path.dirname (os.path.abspath (__file__))
os.chdir (currentDir)

devKitPath = os.path.abspath (sys.argv[1])
resourceObjectsPath = os.path.abspath (sys.argv[2])
resultResFilePath = os.path.abspath (sys.argv[3])

addOnResourcesPath = os.path.dirname (currentDir)
resConvPath = os.path.join (devKitPath, 'Support', 'Tools', 'Win', 'ResConv.exe')
rintFolder = os.path.join (addOnResourcesPath, 'RINT');
rfixFolder = os.path.join (addOnResourcesPath, 'RFIX');
imagesFolder = os.path.join (rfixFolder, 'Images')

for fileName in os.listdir (rintFolder):
	extension = os.path.splitext (fileName)[1]
	if extension != '.grc':
		break
	grcFilePath = os.path.join (rintFolder, fileName)
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
	
for fileName in os.listdir (rfixFolder):
	extension = os.path.splitext (fileName)[1]
	if extension != '.grc':
		break
	grcFilePath = os.path.join (rfixFolder, fileName)
	rc2Path = os.path.join (resourceObjectsPath, fileName + '.rc2')
	result = subprocess.call ([
		resConvPath,
		'-m',
		'r',
		'-D', 'WINDOWS',
		'-T',
		'W',
		'-w', '2',
		'-p', imagesFolder,
		'-q', 'utf8', '1252',
		'-i', grcFilePath,
		'-o', rc2Path
	])
	if result != 0:
		print ('Failed to compile resource: ' + fileName)
		sys.exit (1)
		
result = subprocess.call ([
	'rc',
	'/i', os.path.join (devKitPath, 'Support', 'Inc'),
	'/i', os.path.join (devKitPath, 'Support', 'Modules', 'DGLib'),
	'/i', resourceObjectsPath,
	'/fo', resultResFilePath,
	os.path.join (addOnResourcesPath, 'RFIX.win', 'AddOnMain.rc2')
])
if result != 0:
	print ('Failed to compile native resource')
	sys.exit (1)

sys.exit (0)
