# Archicad Add-On CMake Template

This repository contains a CMake template for Archicad Add-On Development. You can use it to generate native Visual Studio or XCode project or to develop an Add-On directly in Visual Studio Code without using any other environments.

## Prerequisites

- [CMake](https://cmake.org) (3.16 minimum version is needed).
- On Windows:
  - [Python](https://www.python.org) for resource compilation (version 2.7+ or 3.5+).
- On MacOS:
  - [Perl](https://www.perl.org) for resource compilation.

## Usage

- [Download the CMake Template from here](https://github.com/GRAPHISOFT/archicad-addon-cmake/archive/master.zip).
- [Download the Archicad Add-On Development Kit from here](http://archicadapi.graphisoft.com).
- Generate the IDE project with CMake:
  - Use a directory named "Build" as target so gitignore will ignore these files.
  - Set the API_DEVKIT_DIR variable to the installed development kit directory (e.g. "C:\Program Files\GRAPHISOFT\API Development Kit 24.3009"). You can set it as an environment variable or you can pass it to CMake like in the examples below.
- If you want to release your Add-On you have to modify the MDID in the "AddOnResources/RFIX/AddOnFix.grc" file.

## Usage Examples

### Visual Studio (Windows)

Run these commands from the command line.

```
mkdir Build
cd Build
cmake -G "Visual Studio 15 2017" -A "x64" -DAPI_DEVKIT_DIR="C:\API Development Kit 24.3009" ..
cd ..
```

### XCode (MacOS)

Run these commands from the command line.

```
mkdir Build
cd Build
cmake -G "Xcode" -DAPI_DEVKIT_DIR=/Applications/GRAPHISOFT\ ARCHICAD\ API\ DevKit\ 24.3009 ..
cd ..
```

### Visual Studio Code (Platform Independent)

- Install the "CMake Tools" extension for Visual Studio Code.
- Set the "API_DEVKIT_DIR" environment variable to the installed Development Kit folder.
- Open the root folder in Visual Studio Code, configure and build the solution.

## Modifications

If you use the same source structure as the template, you probably won't have to modify anything in the project generation process.

One exception is the module dependency list. The template uses only the minimum required number of Archicad modules. If you want to add more modules, you have to modify the module list at the end of the `CMakeLists.txt` file.

## Compatibility

This template is tested with the Archicad versions below. It doesn't contain any version dependent code so in theory it should work with other Archicad versions as well.
- Archicad 23
- Archicad 24

## Possible Improvements

- Multilanguage support (now it supports only INT localization).
- Use Python for resource compilation on both platforms.
- The generated XCode source structure could be improved.
