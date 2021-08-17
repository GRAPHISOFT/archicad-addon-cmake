import os
import sys
import argparse
import re
from pathlib import Path

import xml.etree.ElementTree as ET


class Module(object):
    def __init__(self, target: str, folderPath: Path, libraryFilePath: Path):
        self.folderPath = folderPath
        self.libraryFilePath = libraryFilePath
        self.target = target

    def GetLibraryName(self):
        if self.libraryFilePath.is_file():
            libSubRegex = r"(Imp.*[LIB|lib])"
            libraryFileNameStripped = re.sub(
                libSubRegex, "", self.libraryFilePath.parts[-1]
            )
            return libraryFileNameStripped
        else:
            return self.folderPath.parts[-1]

    def GetFolderName(self):
        return self.folderPath.parts[-1]

    def IsExcluded(self):
        if self.GetFolderName() == "RS" or self.GetFolderName() == "VectorImage":
            return True
        return False

    def __repr__(self) -> str:
        return f"AddGSModule ({self.target} { self.GetFolderName() } { self.GetLibraryName() })"

    def __str__(self) -> str:
        return f"AddGSModule ({self.target} { self.GetFolderName() } { self.GetLibraryName() })"

    def __eq__(self, o: object) -> bool:
        return str(self) == str(o)


class CModule(Module):
    def __init__(
        self,
        target: str,
        folderPath: Path,
        libraryFilePath: Path,
        match: re.Match,
    ):
        super().__init__(target, folderPath, libraryFilePath)
        self.start = match.start()
        self.end = match.end()


class CMakeListsAutoModuleIncluder:
    def __init__(
        self,
        devKitPath: Path,
        cMakeFilePath: Path,
        vcxprojFilePath: Path,
        configuration="Debug|x64",
        target="AddOn",
    ):
        self.devKitPath = devKitPath
        self.cMakeFilePath = cMakeFilePath.joinpath("CMakeLists.txt")
        self.vcxprojFilePath = vcxprojFilePath.joinpath(f"{target}.vcxproj")
        self.configuration = configuration
        self.DEVKITMODULESPATH = self.devKitPath.joinpath("Support", "Modules")
        self.CMAKELIST_STRING = self.ReadCMakeFile()
        self.CMAKEMODULES = self.GetCmakeExistingModules()

    def ReadCMakeFile(self):
        """Reads the existing CMakeFile.txt and stores it."""

        cmakestring = ""
        with open(self.cMakeFilePath, "r") as cmfile:
            for line in cmfile:
                cmakestring += line
            cmfile.close()
        return cmakestring

    def AddModule(self, module: Module):
        """Adds the specified Module a.k.a AddGSFunction() line to cmakelist.txt"""
        self.CMAKELIST_STRING += f"{str(module)}\n"
        print(f"Added: {module} module to CMakeList.txt")
        self.CMAKEMODULES = self.GetCmakeExistingModules()

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

    def SaveToCMakeFile(self):
        """Write to the existing CMakeList.txt and save changes"""
        cmakeFile = open(self.cMakeFilePath, "w")
        cmakeFile.write(self.CMAKELIST_STRING)
        cmakeFile.close()

    def GetCmakeExistingModules(self):
        """Collects the existing AddGSModule(___ ___ ___) functions, and puts them into an array"""
        tempCmakeModules = []
        extractADDGSFunctionsRegex = r"AddGSModule[\W*]\([\w\s]*\)"
        extractModuleNameRegex = r"\((\w*)\s(\w*)\s(\w*)\)"

        matches = re.finditer(
            extractADDGSFunctionsRegex, self.CMAKELIST_STRING, re.MULTILINE
        )
        for match in matches:
            modules = re.finditer(extractModuleNameRegex, match.group())
            for module in modules:
                target = module.group(1)  # The target
                folder = Path(self.DEVKITMODULESPATH, module.group(2))  # Folder name
                dependency = Path(
                    folder, "Win", f"{module.group(3)}Imp.LIB"
                )  # Library file
                tempModule = CModule(target, folder, dependency, match)
                if (
                    tempModule.IsExcluded()
                ):  # The excluded modules are inside if statements
                    continue
                tempCmakeModules.append(tempModule)
        return tempCmakeModules

    def PrintDifferences(self, listOfModules):
        if len(self.PROJECTMODULES) > len(self.CMAKEMODULES):
            print(f"{self.cMakeFilePath.parts[-1]} has less modules included:")
        elif len(self.PROJECTMODULES) < len(self.CMAKEMODULES):
            print(f"{self.cMakeFilePath.parts[-1]} has more modules included:")
        for dependecy in listOfModules:
            print(dependecy)

    def UpdateCMakeLists(self):
        if sys.platform != "win32":
            print(" NOT SUPPORTED PLATFORM EXITING PROGRAM")
            return

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


class WinModuleCollector(CMakeListsAutoModuleIncluder):
    def __init__(
        self,
        devKitPath: Path,
        cMakeFilePath: Path,
        vcxprojFilePath: Path,
        configuration: str,
    ):
        super().__init__(devKitPath, cMakeFilePath, vcxprojFilePath, configuration)
        # self.root = Et.parse()
        self.root = ET.parse(self.vcxprojFilePath).getroot()
        self.namespace = self.GetNamespace(self.root)
        self.additionalIncludeFolders = self.GetIncludedModules(
            f"ClCompile/AdditionalIncludeDirectories"
        )
        self.additionalDependencies = self.GetIncludedModules(
            f"Link/AdditionalDependencies"
        )
        self.PROJECTMODULES = self.GenerateModules()

    @staticmethod
    def Intersection(lst1, lst2):
        tempList = []
        for el in lst1:
            if el not in lst2:
                tempList.append(el)
        return tempList

    def GetNamespace(self, element: ET.Element) -> str:
        """Returns the namespace of the given element"""
        m = re.match(r"\{.*\}", element.tag)
        return m.group(0) if m else ""

    def GenerateModules(self) -> list:
        """creates an array of modules collected from the vcxproj file"""
        moduleList = []
        includeFolders = self.additionalIncludeFolders
        dependencies = self.additionalDependencies
        while dependencies:
            dep = dependencies.pop()
            depsParent = dep.parent.parent
            tempModule = Module("AddOn", depsParent, dep)
            if tempModule.IsExcluded():
                continue
            if depsParent in includeFolders:
                moduleList.append(tempModule)
                includeFolders.remove(depsParent)
        while includeFolders:
            includeFolder = includeFolders.pop()
            tempModule = Module("AddOn", includeFolder, includeFolder)
            if tempModule.IsExcluded():
                continue
            moduleList.append(tempModule)
        return moduleList

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
        ItemDefinitionGroups = list(
            filter(
                lambda el: (self.configuration in str(el.attrib["Condition"])),
                ItemDefinitionGroups,
            )
        )
        for group in ItemDefinitionGroups:
            for dependency in group.findall(xpathWithNameSpace):
                dependencyList = (
                    dependency.text.replace("\t", "").replace("\n", "").split(";")
                )
                # Convert the splitted paths to actual Path
                listOfDependencies = list(map(Path, dependencyList))
                # Filter only the GS Dependencies not the user added
                listOfDependencies = list(
                    filter(
                        lambda path: (self.DEVKITMODULESPATH in list(path.parents)),
                        listOfDependencies,
                    )
                )
                for dep in listOfDependencies:
                    if dep not in tempList:
                        tempList.append(dep)
        return tempList


def Main(argv):
    parser = argparse.ArgumentParser(description="CMakeList.txt module collector")
    parser.add_argument(
        "-devKitPath", "--devKitPath", help="Path to the Archicad Development Kit"
    )
    parser.add_argument(
        "-cMakeFilePath", "--cMakeFilePath", help="Path to the CMakeList.txt"
    )
    parser.add_argument(
        "-vcxprojectFolder", "--vcxprojectFolder", help="The path to the AddOn.vcxproj"
    )
    parser.add_argument(
        "-configuration",
        "--configuration",
        nargs="?",
        default="Debug|x64",
        help="What config this script should look into Debug|x64 or Release|x64",
    )
    args = parser.parse_args()

    assert os.path.exists(
        args.devKitPath
    ), "Check if you entered correctly the Archicad Development Path"
    assert os.path.exists(
        f"{args.cMakeFilePath}\\CMakeLists.txt"
    ), "Check if you entered correctly the CMakeLists.txt folder location"
    assert os.path.isfile(
        f"{args.vcxprojectFolder}\\AddOn.vcxproj"
    ), "Check if you entered correctly the AddOn.vcxproj folder location or the project was built before"

    moduleIncluder = WinModuleCollector(
        devKitPath=Path(args.devKitPath),
        cMakeFilePath=Path(args.cMakeFilePath),
        vcxprojFilePath=Path(args.vcxprojectFolder),
        configuration=args.configuration,
    )

    moduleIncluder.UpdateCMakeLists()
    # moduleIncluder.SaveToCMakeFile()
    return 0


# python AddModules.py -devKitPath "C:\Program Files\GRAPHISOFT\API Development Kit 24.3009" -cMakeFilePath "D:\TEMP\CPP DEVELOPMENT\archicad-addon-cmake" -vcxprojectFolder "D:\TEMP\CPP DEVELOPMENT\archicad-addon-cmake\build"

sys.exit(Main(sys.argv))