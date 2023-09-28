# Archicad Add-On CMake Template

This repository contains a CMake template for Archicad Add-On Development.

[![Build](https://github.com/GRAPHISOFT/archicad-addon-cmake/actions/workflows/build.yml/badge.svg)](https://github.com/GRAPHISOFT/archicad-addon-cmake/actions/workflows/build.yml)

## Cloning the repository

https://github.com/GRAPHISOFT/archicad-addon-cmake-tools is included as a submodule.

- Clone the repository using
  ```
  git pull --recurse-submodules
  ```
  **OR**
  
  Run this command after the **first time** you clone the repository:
  ```
  git submodule update --init --recursive
  ```


- To update the submodule, use the following command:
  ```
  git submodule update --recursive --remote
  ```
  (Note: for older git versions, the <em> --remote </em> flag may not be neccesary)

## Prerequisites

- [Archicad Development Kit](https://archicadapi.graphisoft.com/downloads/api-development-kit) (that matches your Archicad version).
- [CMake](https://cmake.org) (3.16 minimum version is needed).
- [Python](https://www.python.org) for resource compilation (version 2.7+ or 3.8+).
- [Conan](https://conan.io) (version 1.x, optional).

## Build with downloaded Archicad API Development Kit

- [Download the CMake Template from here](https://github.com/GRAPHISOFT/archicad-addon-cmake/archive/master.zip).
- [Download the Archicad Add-On Development Kit from here](https://archicadapi.graphisoft.com/downloads/api-development-kit).
- Generate the IDE project with CMake, and set the following variables:
  - `AC_API_DEVKIT_DIR`: The Support folder of the installed Archicad Add-On Development Kit. You can also set an environment variable with the same name so you don't have to provide this value during project generation.
  - `AC_ADDON_NAME`: (optional) The name of the project file and the result binary Add-On file (default is "ExampleAddOn").
  - `AC_ADDON_LANGUAGE`: (optional) The language code of the Add-On (default is "INT").
- To release your Add-On you need to provide valid MDIDs, you can generate them on the [Archicad API site](https://archicadapi.graphisoft.com/profile/add-ons).

### Visual Studio (Windows)

Run these command from the command line to generate the Visual Studio project. Replace `<DevKitSupportDir>` with the path of the Support folder in your downloaded Development Kit. See the list below for the matching Visual Studio versions for different Archicad versions.

| Archicad | Visual Studio | Platform toolset |
|---|---|---|
| Archicad 27 | Visual Studio 2019 | v142 |
| Archicad 26 | Visual Studio 2019 | v142 |
| Archicad 25 | Visual Studio 2019 | v142 |
| Archicad 24 | Visual Studio 2017 | v141 |
| Archicad 23 | Visual Studio 2017 | v141 |

Please note that you can always use the latest Visual Studio, but make sure you provide the correct platform toolset.

Example for using Visual Studio 2022 with platform toolset 142:
```
cmake -B Build -G "Visual Studio 17 2022" -A x64 -T v142 -DAC_API_DEVKIT_DIR=<DevKitSupportDir> .
```

### XCode (MacOS)

Run this command from the command line to generate the XCode project:

```
cmake -B Build -G "Xcode" -DAC_API_DEVKIT_DIR=<DevKitSupportDir> .
```

### Visual Studio Code (Platform Independent)

- Install the "CMake Tools" extension for Visual Studio Code.
- Set the "AC_API_DEVKIT_DIR" environment variable to the installed Development Kit Support folder.
- Open the root folder in Visual Studio Code, configure and build the solution.

## Build using the Conan Package Manager

You can use the Conan package manager to get the Development Kit. This method works only for Archicad 25 and later versions.

### Preparation

[Install the Conan package manager](https://conan.io/downloads.html). Please not that you need to **install version 1.x**.

```
pip install conan==1.59.0
```

#### Windows

Create the default profile, set the compiler version and install dependencies by using the following commands:

```
conan profile new default --detect
conan profile update settings.compiler.version=16 default
conan install . -pr:b=default --install-folder=Build/
conan\conanbuild.bat
```

#### MacOS

Create the default profile, set the compiler version and install dependencies by using the following commands:

```
conan profile new default --detect
conan profile update settings.compiler.version=13 default
conan install . -pr:b=default --install-folder=Build/
source conan/conanbuild.sh
```

### Visual Studio (Windows)

Run this command from the command line:

```
cmake -B Build -G "Visual Studio 17 2022" .
```

### XCode (MacOS)

Run this command from the command line:

```
cmake -B Build -G "Xcode" .
```

### Visual Studio Code (Platform Independent)

- Install the "CMake Tools" extension for Visual Studio Code.
- Open the root folder in Visual Studio Code, configure and build the solution.

## Archicad Compatibility

This template is tested with all Archicad versions starting from Archicad 23 using the downloaded Archicad API Development Kit and starting from Archicad 25 using Conan.

## Use in Archicad

To use the Add-On in Archicad, you have to add your compiled .apx or .bundle file in Add-On Manager. The example Add-On registers a new command into the Options menu. Please note that the example Add-On works only in the demo version of Archicad.

You can start Archicad in demo mode by the following command line commands:
- Windows: `ARCHICAD.exe -DEMO`
- MacOS: `ARCHICAD\ 26.app/Contents/MacOS/ARCHICAD -demo`

## Modifications

If you use the same source structure as the template, you probably won't have to modify anything in the project generation process.

## Possible Improvements

- Multilingual support (provide example for another localized version).
- The generated XCode source structure could be improved.
