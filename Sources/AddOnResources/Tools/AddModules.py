import os
import sys
import platform
import subprocess
import shutil
import codecs
import argparse
import xml.etree.ElementTree as ET
import re

DEBUG = True


class WinModulesCollector(object):
    def __init__(self, devKitPath, cmakeFilePath, vcxprojectFolder):
        # - The path to the Dev Kit Directory
        self.devKitPath = os.path.join(devKitPath)
        # - The path to the CMakeList.txt CMAKE_CURRENT_LIST_DIR
        self.cmakeFilePath = os.path.join(cmakeFilePath, "CMakeLists.txt")
        # - The path to the AddOn.vcxprojx CMAKE_CURRENT_BINARY_DIR
        self.vcxprojectFilePath = os.path.join(vcxprojectFolder, "AddOn.vcxprojx")
        # {Devkit}\Support\Mopdules
        self.MODULESPATH = os.path.join(self.devKitPath, "Support\\Modules")
        # The list of all modules added from archicad library
        self.modulesList = self.GetExistingProjectModules()

    def Namespace(self, element):
        m = re.match(r"\{.*\}", element.tag)
        return m.group(0) if m else ""

    def GetPath(self, textPath):
        return os.path.join(textPath)

    def FilterPaths(self, path):
        if self.MODULESPATH in path:
            return True
        else:
            return False

    def GetModuleNameFromPath(self, path):
        return path.replace(self.MODULESPATH + "\\", "")

    def GetModulePathFromName(self, moduleName):
        return os.path.join(self.MODULESPATH, moduleName)

    def GetExistingProjectModules(self):
        modulesList = []
        listOfModulesPaths = []
        print(self.vcxprojectFilePath)
        # TODO change to the self.vcxprojectFilePath
        tree = ET.parse(os.path.abspath("AddOn.vcxproj"))
        root = tree.getroot()
        namespace = self.Namespace(root)
        AdditionalIncludeDirectories = root.findall(
            f"{namespace}ItemDefinitionGroup/{namespace}ClCompile/{namespace}AdditionalIncludeDirectories"
        )
        for includeDirectory in AdditionalIncludeDirectories:
            listOfModules = includeDirectory.text.split(";")
            listOfModulesPaths = map(self.GetPath, listOfModules)
            listOfModulesPaths = filter(self.FilterPaths, listOfModulesPaths)

            for modulePath in listOfModulesPaths:
                if self.GetModuleNameFromPath(modulePath) not in modulesList:
                    modulesList.append(self.GetModuleNameFromPath(modulePath))
        return modulesList


class CMakeListAutoModuleIncluder(WinModulesCollector):
    def __init__(self, devKitPath, cmakeFilePath, vcxprojectFolder):
        super().__init__(devKitPath, cmakeFilePath, vcxprojectFolder)

    def ParseCMakeFile(self):
        with open(self.cmakeFilePath) as cmfile:
            for line in cmfile:
                print(line)

    def GetCmakeExistingModules(self):
        pass


def Main(argv):
    parser = argparse.ArgumentParser(description="CMakeList.txt module collector")
    parser.add_argument(
        "-devKitPath", "--devKitPath", help="Path to the Archicad Development Kit"
    )
    parser.add_argument(
        "-cmakeFilePath", "--cmakeFilePath", help="Path to the CMakeLists.txt"
    )
    parser.add_argument(
        "-vcxprojectFolder", "--vcxprojectFolder", help="The path to the AddOn.vcxproj"
    )
    args = parser.parse_args()

    # python AddModules.py -devKitPath "C:\Program Files\GRAPHISOFT\API Development Kit 24.3009" -cmakeFilePath "D:\TEMP\CPP DEVELOPMENT\archicad-addon-cmake" -vcxprojectFolder "D:\TEMP\CPP DEVELOPMENT\archicad-addon-cmake\Build"
    moduleIncluder = CMakeListAutoModuleIncluder(
        devKitPath=args.devKitPath,
        cmakeFilePath=args.cmakeFilePath,
        vcxprojectFolder=args.vcxprojectFolder,
    )
    moduleIncluder.ParseCMakeFile()
    # comp.GetExistingProjectModules()

    return 0


sys.exit(Main(sys.argv))

# if __name__ == '__main__':
#     Main()
