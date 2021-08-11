from ntpath import join
import os
import sys
import platform
import subprocess
import shutil
import codecs
import argparse
from pathlib import Path

import xml.etree.ElementTree as ET
import re


class Module(object):
    def __init__(self, target: str, folderName: Path, libraryName: Path, devKit):
        self.folderName = folderName
        self.libraryName = libraryName
        self.target = target
        self.devKit = devKit
        self.libraryPath = self.GetLibraryFileAbsoluteLocation()
        self.folderAbsolutePath = self.GetModulAbsoluteFolder()

    def GetLibraryFileAbsoluteLocation(self):
        libFile = f"Support\\Modules\\{self.folderName}\\Win\\{self.libraryName}"

        path = Path(self.devKit)
        path = path.joinpath(libFile)
        return path

    def GetModulAbsoluteFolder(self):
        modulesFolder = f"Support\\Modules\\{self.folderName}"
        path = Path(self.devKit)
        path = path.joinpath(modulesFolder)
        print(path)
        return path

    def ADDGSModule(self) -> str:
        libraryNameStripped = str(self.libraryName)
        libSubRegex = r"(Imp.*[LIB|lib])"
        libraryNameStripped = re.sub(libSubRegex, "", libraryNameStripped)
        return f"ADDGSModule({self.target} { self.folderName } { libraryNameStripped })"

    def __str__(self) -> str:
        return self.ADDGSModule()


class WinModulesCollector(object):
    def __init__(self, devKitPath, cmakeFilePath, vcxprojectFolder, archicadVersion):
        self.INCLUDEPATH = os.path.join(devKitPath, "Support\\Modules")

        self.archicadVersion = archicadVersion
        # - The path to the Dev Kit Directory
        self.devKitPath = os.path.join(devKitPath)
        # - The path to the CMakeList.txt CMAKE_CURRENT_LIST_DIR
        self.cmakeFilePath = os.path.join(cmakeFilePath, "CMakeLists.txt")
        # - The path to the AddOn.vcxprojx CMAKE_CURRENT_BINARY_DIR
        self.vcxprojectFilePath = os.path.join(vcxprojectFolder, "AddOn.vcxproj")

        # vcxproj Tree init
        self.root = ET.parse(self.vcxprojectFilePath).getroot()
        self.namespace = self.GetNamespace(self.root)
        # The list of all include folders added from archicad library
        self.additionalIncludeFolders = self.GetIncludedModules(
            f"ItemDefinitionGroup/ClCompile/AdditionalIncludeDirectories"
        )
        self.additionalDependencies = self.GetIncludedModules(
            f"ItemDefinitionGroup/Link/AdditionalDependencies"
        )
        self.existingModules = self.CollectModules()

    def GetNamespace(self, element: ET.Element) -> str:
        m = re.match(r"\{.*\}", element.tag)
        return m.group(0) if m else ""

    def ConvertToPath(self, textPath: str) -> Path:
        return Path(textPath)

    def isDevKitPath(self, path: os.path) -> bool:
        if self.INCLUDEPATH in str(path):
            return True
        else:
            return False

    ## List of modules
    def CollectModules(self) -> list:
        moduleList = []
        includeFolders = self.additionalIncludeFolders
        dependencies = self.additionalDependencies
        while dependencies:
            dep = dependencies.pop()
            depsParent = dep.parent.parent
            head, libraryFolderName = os.path.split(depsParent)
            head, libraryName = os.path.split(dep)
            if depsParent in includeFolders:
                moduleList.append(
                    Module("AddOn", libraryFolderName, libraryName, self.devKitPath)
                )
                includeFolders.remove(depsParent)
        while includeFolders:
            includeFolder = includeFolders.pop()
            path, folderName = os.path.split(includeFolder)
            moduleList.append(Module("AddOn", folderName, folderName, self.devKitPath))
        return moduleList

    def GetIncludedModules(self, xpath: str) -> list:
        namespace = self.GetNamespace(self.root)
        xpathWithNameSpace = ""
        for elem in xpath.split("/"):
            xpathWithNameSpace += namespace + elem + "/"
        xpathWithNameSpace = xpathWithNameSpace[:-1]

        listOfDependencies = []
        tempList = []
        AdditionalDependencies = self.root.findall(xpathWithNameSpace)
        for dependency in AdditionalDependencies:
            dependencyList = (
                dependency.text.replace("\t", "").replace("\n", "").split(";")
            )
            listOfDependencies = list(map(self.ConvertToPath, dependencyList))
            listOfDependencies = list(filter(self.isDevKitPath, listOfDependencies))
            for dep in listOfDependencies:
                if dep not in tempList:
                    tempList.append(dep)
        return tempList


class CMakeListAutoModuleIncluder(WinModulesCollector):
    def __init__(self, devKitPath, cmakeFilePath, vcxprojectFolder, archicadVersion):
        super().__init__(devKitPath, cmakeFilePath, vcxprojectFolder, archicadVersion)
        self.CMAKEMODULES = []

    def GetCmakeExistingModules(self):
        c_string = ""
        with open(self.cmakeFilePath, "r") as cmfile:
            for line in cmfile:
                c_string += line
            cmfile.close()
        extractADDGSFunctionsRegex = r"(AddGSModule.*\(.*\))"
        extractModuleNameRegex = r"\((\w*)\s(\w*)\s(\w*)\)"

        matches = re.finditer(extractADDGSFunctionsRegex, c_string, re.MULTILINE)

        for match in matches:
            modules = re.finditer(extractModuleNameRegex, match.group())
            for module in modules:
                print(module.group())

        # for matchNum, match in enumerate(matches, start=1):
        #     print(
        #         "Match {matchNum} was found at {start}-{end}: {match}".format(
        #             matchNum=matchNum,
        #             start=match.start(),
        #             end=match.end(),
        #             match=match.group(),
        #         )
        #     )

        # for groupNum in range(0, len(match.groups())):
        #     groupNum = groupNum + 1
        #     print(
        #         "Group {groupNum} found at {start}-{end}: {group}".format(
        #             groupNum=groupNum,
        #             start=match.start(groupNum),
        #             end=match.end(groupNum),
        #             group=match.group(groupNum),
        #         )
        #     )


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
    parser.add_argument(
        "-ACVersion", "--ACVersion", help="The path to the AddOn.vcxproj"
    )
    args = parser.parse_args()

    # python AddModules.py -devKitPath "C:\Program Files\GRAPHISOFT\API Development Kit 24.3009" -cmakeFilePath "D:\TEMP\CPP DEVELOPMENT\archicad-addon-cmake" -vcxprojectFolder "D:\TEMP\CPP DEVELOPMENT\archicad-addon-cmake\Build" -ACVersion 24
    moduleIncluder = CMakeListAutoModuleIncluder(
        devKitPath=args.devKitPath,
        cmakeFilePath=args.cmakeFilePath,
        vcxprojectFolder=args.vcxprojectFolder,
        archicadVersion=args.ACVersion,
    )
    # assert os.path.exists(
    #     moduleIncluder.vcxprojectFilePath
    # ), f"Error vcxproj not found: {moduleIncluder.vcxprojectFilePath}"

    for el in moduleIncluder.existingModules:
        print(el)
    return 0


sys.exit(Main(sys.argv))
