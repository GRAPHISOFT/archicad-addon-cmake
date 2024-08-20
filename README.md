# Archicad Add-On CMake Template

This repository contains a CMake template for Archicad Add-On Development.

## Prerequisites

- Development environment:
  - Windows: [Visual Studio](https://visualstudio.microsoft.com/downloads/)
  - MacOS: [Xcode](https://developer.apple.com/xcode/resources/)
- [CMake](https://cmake.org) (3.16 minimum version is needed).
- [Python](https://www.python.org) for resource compilation and build script usage (3.8+).

## Quick setup

The easiest way to generate projects and build the Add-On is to use the provided build script. The project and the binaries will be created in the `Build` folder.

1. Open a command prompt.
2. Clone this repository:
```
git clone https://github.com/GRAPHISOFT/archicad-addon-cmake.git --recurse-submodules
```
3. Run the build script from the root of the repository:
```
python Tools/BuildAddOn.py --configFile config.json
```

## Config file

The build script reads the config.json file for required build parameters:

- addOnName: name of the Add-On.
- defaultLanguage: a single language for which the Add-On is built when localization is not enabled.
- languages: list of languages, for which localization can be done / for which the .grc files are present in their respective directories.
- additionalCMakeParams (optional): a list of additional Add-On specific CMake parameters as JSON key-value pairs. The build script will forward it to CMake.

See the example [config.json](https://github.com/GRAPHISOFT/archicad-addon-cmake/blob/master/config.json).

## Detailed instructions

If the provided build script doesn't work for you, you can set up your environment manually.

### Clone this repository

This repository uses [archicad-addon-cmake-tools](https://github.com/GRAPHISOFT/archicad-addon-cmake-tools) as a submodule, so in order to use this repository you need to be sure that all submodules are cloned properly.

To clone the repository with submodules, use the following command.
```
git clone https://github.com/GRAPHISOFT/archicad-addon-cmake.git --recurse-submodules
```

To get the latest changes together with submodule changes, use the following command.
```
git pull --recurse-submodules
```

To update only the submodules, use the following command.
```
git submodule update --remote
```

### Build with downloaded Archicad API Development Kit

- Clone this repository as it's described in the previous section.
- [Download the Archicad Add-On Development Kit from here](https://archicadapi.graphisoft.com/downloads/api-development-kit) or from [here](https://github.com/GRAPHISOFT/archicad-api-devkit/releases).
- Generate the IDE project with CMake, and set the following variables (see example [below](#visual-studio-windows)):
  - `AC_VERSION`: The version number of Archicad that the Add-On is built for.
  - `AC_API_DEVKIT_DIR`: The Support folder of the installed Archicad Add-On Development Kit. You can also set an environment variable with the same name so you don't have to provide this value during project generation.
  - `AC_ADDON_NAME`: (optional) The name of the project file and the result binary Add-On file (default is "ExampleAddOn").
  - `AC_ADDON_LANGUAGE`: (optional) The language code of the Add-On (default is "INT").
- To release your Add-On you need to provide valid MDIDs, you can generate them on the [Archicad API site](https://archicadapi.graphisoft.com/profile/add-ons).

#### Visual Studio (Windows)

See the list below for the matching Visual Studio and platform toolset versions for different Archicad versions.

| Archicad | Visual Studio | Platform toolset |
|---|---|---|
| Archicad 28 | Visual Studio 2019 | v142 |
| Archicad 27 | Visual Studio 2019 | v142 |
| Archicad 26 | Visual Studio 2019 | v142 |
| Archicad 25 | Visual Studio 2019 | v142 |
| Archicad 24 | Visual Studio 2017 | v141 |
| Archicad 23 | Visual Studio 2017 | v141 |

Please note that you can always use the latest Visual Studio, but make sure you provide the correct platform toolset.

Example for using Visual Studio 2022 with platform toolset 142:
```
cmake -B Build -G "Visual Studio 17 2022" -A x64 -T v142 -DAC_API_DEVKIT_DIR=<DevKitSupportDir> -DAC_VERSION=28 .
```

#### XCode (MacOS)

See the list below for the matching deployment targets for different Archicad versions.

| Archicad | Deployment target |
|---|---|
| Archicad 28 | 11.0 |
| Archicad 27 | 10.15 |
| Archicad 26 | 10.15 |
| Archicad 25 | 10.15 |
| Archicad 24 | 10.13 |
| Archicad 23 | 10.12 |

Run this command from the command line to generate the XCode project:

```
cmake -B Build -G "Xcode" -DAC_API_DEVKIT_DIR=<DevKitSupportDir> -DAC_VERSION=28 .
```

#### Visual Studio Code (Platform Independent)

- Install the "CMake Tools" extension for Visual Studio Code.
- Set the "AC_API_DEVKIT_DIR" environment variable to the installed Development Kit Support folder.
- Open the root folder in Visual Studio Code, configure and build the solution.

## Archicad Compatibility

This template is tested with all Archicad versions starting from Archicad 25.

## Use in Archicad

To use the Add-On in Archicad, you have to add your compiled .apx or .bundle file in Add-On Manager. The example Add-On registers a new command into the Options menu. Please note that the example Add-On works only in the demo version of Archicad.

You can start Archicad in demo mode by the following command line commands:
- Windows: `ARCHICAD.exe -DEMO`
- MacOS: `ARCHICAD\ 26.app/Contents/MacOS/ARCHICAD -demo`
