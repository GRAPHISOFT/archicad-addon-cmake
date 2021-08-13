import os
import sys
import platform
import subprocess
import shutil
import codecs
import argparse
from pathlib import Path

from ModuleTypes import CModule, Module
import xml.etree.ElementTree as ET
import re


class WinModulesCollector(object):
    def __init__(
        self, devKitPath, cmakeFilePath, vcxprojectFolder, configuration="Debug|x64"
    ):
        self.INCLUDEPATH = Path(os.path.join(devKitPath, "Support\\Modules"))
        self.configuration = configuration
        # - The path to the Dev Kit Directory
        self.devKitPath = Path(os.path.join(devKitPath))
        # - The path to the CMakeList.txt CMAKE_CURRENT_LIST_DIR
        self.cmakeFilePath = Path(os.path.join(cmakeFilePath, "CMakeLists.txt"))
        # - The path to the AddOn.vcxprojx CMAKE_CURRENT_BINARY_DIR
        self.vcxprojectFilePath = Path(os.path.join(vcxprojectFolder, "AddOn.vcxproj"))

        # vcxproj Tree init
        self.root = ET.parse(self.vcxprojectFilePath).getroot()
        self.namespace = self.GetNamespace(self.root)
        # The list of all include folders added from archicad library
        self.additionalIncludeFolders = self.GetIncludedModules(
            f"ClCompile/AdditionalIncludeDirectories"
        )
        self.additionalDependencies = self.GetIncludedModules(
            f"Link/AdditionalDependencies"
        )
        self.PROJECTMODULES = self.GenerateModules()

    def GetNamespace(self, element: ET.Element) -> str:
        m = re.match(r"\{.*\}", element.tag)
        return m.group(0) if m else ""

    @staticmethod
    def Intersection(lst1, lst2):
        tempList = []
        for el in lst1:
            if el not in lst2:
                tempList.append(el)
        return tempList

    def ConvertToPath(self, textPath: str) -> Path:
        return Path(textPath)

    def isDevKitPath(self, path: Path) -> bool:
        return self.INCLUDEPATH in list(path.parents)

    ## List of modules
    def GenerateModules(self) -> list:
        """creates an array of modules collected from the vcxproj file"""
        moduleList = []
        includeFolders = self.additionalIncludeFolders
        dependencies = self.additionalDependencies
        while dependencies:
            dep = dependencies.pop()
            depsParent = dep.parent.parent
            head, libraryFolder = os.path.split(depsParent)
            head, libraryName = os.path.split(dep)
            tempModule = Module("AddOn", libraryFolder, libraryName, self.devKitPath)
            if tempModule.IsExcluded():
                continue
            if depsParent in includeFolders:
                moduleList.append(tempModule)
                includeFolders.remove(depsParent)
        while includeFolders:
            includeFolder = includeFolders.pop()
            path, folderName = os.path.split(includeFolder)
            tempModule = Module("AddOn", folderName, folderName, self.devKitPath)
            if tempModule.IsExcluded():
                continue
            moduleList.append(tempModule)
        return moduleList

    def FilterItemDefinitionGroupsByConfiguration(self, elements: list):
        """A function that filters the Definition groups from .vcxproj file by the given parameter
        Default: Debux|x64 or as it says inside the function the self.configuration"""
        tempList = []
        if type(elements) is list:
            for element in elements:
                if self.configuration in str(element.attrib["Condition"]):
                    tempList.append(element)
        return tempList

    def GetIncludedModules(self, xpath: str) -> list:
        """Reads from vcxproj file the dependencies specified in the xpath"""
        namespace = self.GetNamespace(self.root)
        xpathWithNameSpace = ""
        for elem in xpath.split("/"):
            xpathWithNameSpace += namespace + elem + "/"
        xpathWithNameSpace = xpathWithNameSpace[:-1]

        listOfDependencies = []
        tempList = []
        ItemDefinitionGroups = self.root.findall(namespace + "ItemDefinitionGroup")
        ItemDefinitionGroups = self.FilterItemDefinitionGroupsByConfiguration(
            ItemDefinitionGroups
        )
        for group in ItemDefinitionGroups:
            for dependency in group.findall(xpathWithNameSpace):
                dependencyList = (
                    dependency.text.replace("\t", "").replace("\n", "").split(";")
                )
                # Convert the splitted paths to actual Path
                listOfDependencies = list(map(self.ConvertToPath, dependencyList))
                # Filter only the GS Dependencies not the user added
                listOfDependencies = list(filter(self.isDevKitPath, listOfDependencies))
                for dep in listOfDependencies:
                    if dep not in tempList:
                        tempList.append(dep)
        return tempList


class CMakeListAutoModuleIncluder(WinModulesCollector):
    def __init__(self, devKitPath, cmakeFilePath, vcxprojectFolder, configuration):
        super().__init__(devKitPath, cmakeFilePath, vcxprojectFolder, configuration)
        self.CMAKELIST_STRING = self.ReadCMakeFile()
        self.CMAKEMODULES = self.GetCmakeExistingModules()

    def ReadCMakeFile(self):
        """Reads the existing CMakeFile.txt and stores it."""
        cmakestring = ""
        with open(self.cmakeFilePath, "r") as cmfile:
            for line in cmfile:
                cmakestring += line
            cmfile.close()
        return cmakestring

    def RemoveModuleFromCMakeFile(self, module: Module):
        """Removes the specified CModule a.k.a AddGSFunction() line from cmakelist.txt"""
        if type(module) is CModule:
            if len(self.CMAKELIST_STRING) > module.end:
                self.CMAKELIST_STRING = (
                    self.CMAKELIST_STRING[0 : module.start :]
                    + self.CMAKELIST_STRING[module.end + 1 : :]
                )
        elif type(module) is Module:
            cMod = self.CMAKEMODULES[self.CMAKEMODULES.index(module)]
            if len(self.CMAKELIST_STRING) > cMod.end:
                self.CMAKELIST_STRING = (
                    self.CMAKELIST_STRING[0 : cMod.start :]
                    + self.CMAKELIST_STRING[cMod.end + 1 : :]
                )
            print(f"Just removed {module} of type {type(module)}")

        self.CMAKEMODULES = self.GetCmakeExistingModules()

    def AddModule(self, module: Module):
        """Adds the specified Module a.k.a AddGSFunction() line to cmakelist.txt"""
        self.CMAKELIST_STRING += f"{str(module)}\n"
        print(f"Added: {module} module to CMakeList.txt")
        self.CMAKEMODULES = self.GetCmakeExistingModules()
        pass

    def Save(self):
        """Write to the existing CMakeList.txt and save changes"""
        cmakeFile = open(self.cmakeFilePath, "w")
        cmakeFile.write(self.CMAKELIST_STRING)
        cmakeFile.close()
        pass

    def PrintDifferences(self, listOfModules):
        print("These dependencies are different")
        for dependecy in listOfModules:
            print(f"${dependecy.folderName} ${dependecy.libraryName}")
        pass

    def GetCmakeExistingModules(self):
        """Collects the existing AddGSModule(___ ___ ___) functions, and puts them into an array"""
        tempCmakeModules = []
        extractADDGSFunctionsRegex = r"(AddGSModule.*\(.*\))"
        extractModuleNameRegex = r"\((\w*)\s(\w*)\s(\w*)\)"

        matches = re.finditer(
            extractADDGSFunctionsRegex, self.CMAKELIST_STRING, re.MULTILINE
        )
        for match in matches:
            modules = re.finditer(extractModuleNameRegex, match.group())
            for module in modules:
                target = module.group(1)  # The target
                folder = module.group(2)  # Folder name
                dependency = module.group(3)  # Library file
                tempModule = CModule(target, folder, dependency, match, self.devKitPath)
                if (
                    tempModule.IsExcluded()
                ):  # The excluded modules are inside if statements
                    continue
                tempCmakeModules.append(tempModule)
        return tempCmakeModules

    def UpdateCMakeLists(self):
        if len(self.PROJECTMODULES) == len(self.CMAKEMODULES):
            print("MODULES ARE UP TO DATE, EXITING PROGRAM")
            return
        if len(self.PROJECTMODULES) > len(self.CMAKEMODULES):
            print(
                f"DETECTED MORE MODULES IN PROJECT THAN IN CMAKELIST, ADDING MISSING MODULES TO CMakeList.txt"
            )
            intersection = self.Intersection(self.PROJECTMODULES, self.CMAKEMODULES)
            self.PrintDifferences(intersection)
            while intersection:
                module = intersection.pop()
                self.AddModule(module)
            return
        elif len(self.PROJECTMODULES) < len(self.CMAKEMODULES):

            print(
                f"DETECTED LESS MODULES IN PROJECT THAN IN CMAKELIST, REMOVING EXTRA MODULES FROM CMakeList.txt"
            )
            intersection = self.Intersection(self.CMAKEMODULES, self.PROJECTMODULES)
            self.PrintDifferences(intersection)
            while intersection:
                module = intersection.pop()
                self.RemoveModuleFromCMakeFile(module)
            return


def Main(argv):
    parser = argparse.ArgumentParser(description="CMakeList.txt module collector")
    parser.add_argument(
        "-devKitPath", "--devKitPath", help="Path to the Archicad Development Kit"
    )
    parser.add_argument(
        "-cmakeFilePath", "--cmakeFilePath", help="Path to the CMakeList.txt"
    )
    parser.add_argument(
        "-vcxprojectFolder", "--vcxprojectFolder", help="The path to the AddOn.vcxproj"
    )
    parser.add_argument(
        "-configuration",
        "--configuration",
        nargs="?",
        default="Debug|x64",
        help="The path to the AddOn.vcxproj",
    )
    args = parser.parse_args()

    assert os.path.exists(
        args.devKitPath
    ), "Check if you entered correctly the Archicad Development Path"
    assert os.path.exists(
        f"{args.cmakeFilePath}\\CMakeLists.txt"
    ), "Check if you entered correctly the CMakeLists.txt folder location"
    assert os.path.isfile(
        f"{args.vcxprojectFolder}\\AddOn.vcxproj"
    ), "Check if you entered correctly the AddOn.vcxproj folder location or the project was built before"

    moduleIncluder = CMakeListAutoModuleIncluder(
        devKitPath=args.devKitPath,
        cmakeFilePath=args.cmakeFilePath,
        vcxprojectFolder=args.vcxprojectFolder,
        configuration=args.configuration,
    )

    moduleIncluder.UpdateCMakeLists()
    moduleIncluder.Save()
    return 0


sys.exit(Main(sys.argv))
