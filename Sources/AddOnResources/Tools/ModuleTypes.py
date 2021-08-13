from pathlib import Path
import re
from typing import overload


class Module(object):
    def __init__(self, target: str, folderName: str, libraryName: str, devKit):
        self.folderName = folderName
        self.libraryName = libraryName
        self.target = target
        self.devKit = devKit
        self.libraryPath = self.GetLibraryFileAbsoluteLocation()
        self.folderAbsolutePath = self.GetModulAbsoluteFolder()

    def IsExcluded(self):
        if self.folderName == "RS" or self.folderName == "VectorImage":
            return True
        return False

    def GetLibraryFileAbsoluteLocation(self):
        libFile = f"Support\\Modules\\{self.folderName}\\Win\\{self.libraryName}"

        path = Path(self.devKit)
        path = path.joinpath(libFile)
        return path

    def GetModulAbsoluteFolder(self):
        modulesFolder = f"Support\\Modules\\{self.folderName}"
        path = Path(self.devKit)
        path = path.joinpath(modulesFolder)
        return path

    def ADDGSModuleString(self) -> str:
        libraryNameStripped = str(self.libraryName)
        libSubRegex = r"(Imp.*[LIB|lib])"
        libraryNameStripped = re.sub(libSubRegex, "", libraryNameStripped)
        return (
            f"AddGSModule ({self.target} { self.folderName } { libraryNameStripped })"
        )

    def __str__(self) -> str:
        return self.ADDGSModuleString()

    def __repr__(self) -> str:
        return self.ADDGSModuleString()

    def __eq__(self, o: object) -> bool:

        return self.ADDGSModuleString() == o.ADDGSModuleString()


class CModule(Module):
    def __init__(
        self,
        target: str,
        folderName: str,
        libraryName: str,
        match: re.Match,
        devKit,
    ):
        super().__init__(target, folderName, libraryName, devKit)
        self.start = match.start()
        self.end = match.end()
