# Archicad Add-On CMake Template

This repository contains a CMake template for Archicad Add-On Development.

## Prerequisites

- [Archicad Development Kit](https://archicadapi.graphisoft.com/downloads/api-development-kit) (that matches your Archicad version).
- [CMake](https://cmake.org) (3.16 minimum version is needed).
- [Python](https://www.python.org) for resource compilation (version 2.7+ or 3.8+).

### Clone this repository

This repository uses [archicad-addon-cmake-tools](https://github.com/GRAPHISOFT/archicad-addon-cmake-tools) as a submodule, so in order to use this repository you need to be sure that all submodules are cloned properly.

To clone the repository with submodules, use the following command.
```
git clone --recurse-submodules
```

To get the latest changes together with submodule changes, use the following command.
```
git pull --recurse-submodules
```

## Build with downloaded Archicad API Development Kit

- Clone this repository as it's described in the previous section.
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

This template is tested with all Archicad versions starting from Archicad 23 using the downloaded Archicad API Development Kit.

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
