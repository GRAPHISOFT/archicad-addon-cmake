# Archicad Add-On CMake Template

This repository contains a CMake template for Archicad Add-On Development.

## Prerequisites

- Development environment:
  - Windows: [Visual Studio](https://visualstudio.microsoft.com/downloads/)
  - MacOS: [Xcode](https://developer.apple.com/xcode/resources/)
- [CMake](https://cmake.org) (3.19 minimum version is needed).
- [Python](https://www.python.org) for resource compilation and build script usage (3.10+).

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

- `addOnName`: name of the Add-On.
- `description`: description of the Add-On.
- `defaultLanguage`: a single language for which the Add-On is built when localization is not enabled. Must be one of the languages specified in `languages`.
- `languages`: list of languages, for which localization can be done / for which the .grc files are present in their respective directories.
- `version`: version of the Add-On. Must have 1, 2 or 3 numeric components (`123`, `1.23` or `1.2.3` respectively) all of which must be in the `0-65535` range.
- `copyright`: an object with fields `name` and `year`. These will be used to embed a copyright notice in the Add-On.
- `additionalCMakeParams` (optional): a list of additional Add-On specific CMake parameters as JSON key-value pairs. The build script will forward it to CMake.

See the example [config.json](https://github.com/GRAPHISOFT/archicad-addon-cmake/blob/master/config.json).

### Definitions in C++ code

The following macro definitions are set to string literals (they expand to `"a C string"`) with values based on the above:

- `ADDON_NAME`: This is the `addOnName` field as is.
- `ADDON_DESCRIPTION`: This is the `description` field as is.
- `ADDON_VERSION`: This is the 3 component version number derived from `version`.
  - Example: this macro definition expands to `"123.0.0"` if the value of `version` is `"123"`.

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

### Fill in metadata in `config.json`

The version number `0.0.0` (or `0.0` or `0` according to the rules above) is recognized as a placeholder and using it will result in a warning.
This template contains a `version` value with this placeholder value that should be changed.

You may also want to change the `addOnName`, `description` and `copyright` values.
You may use the `%Y` placeholder in the `copyright.year` field to always refer to the current year.

### Build with downloaded Archicad API Development Kit

- Clone this repository as it's described in the previous section.
- Review and modify the config file as described in the previous section.
- [Download the Archicad Add-On Development Kit from here](https://archicadapi.graphisoft.com/downloads/api-development-kit) or from [here](https://github.com/GRAPHISOFT/archicad-api-devkit/releases).
- Generate the IDE project with CMake, and set the following variables (see example [below](#visual-studio-windows)):
  - `AC_VERSION`: The version number of Archicad that the Add-On is built for.
  - `AC_API_DEVKIT_DIR`: The Support folder of the installed Archicad Add-On Development Kit. You can also set an environment variable with the same name so you don't have to provide this value during project generation.
  - `AC_ADDON_LANGUAGE`: (optional) The language code of the Add-On (default is "INT").
- To release your Add-On you need to provide valid MDIDs, you can generate them on the [Archicad API site](https://archicadapi.graphisoft.com/profile/add-ons).

#### Visual Studio (Windows)

See the list below for the matching Visual Studio and platform toolset versions for different Archicad versions.

| Archicad | Visual Studio | Platform toolset |
|---|---|---|
| Archicad 29 | Visual Studio 2019 | v143 |
| Archicad 28 | Visual Studio 2019 | v142 |
| Archicad 27 | Visual Studio 2019 | v142 |
| Archicad 26 | Visual Studio 2019 | v142 |
| Archicad 25 | Visual Studio 2019 | v142 |
| Archicad 24 | Visual Studio 2017 | v141 |
| Archicad 23 | Visual Studio 2017 | v141 |

Please note that you can always use the latest Visual Studio, but make sure you provide the correct platform toolset.

Example for using Visual Studio 2022 with platform toolset 142:
```
cmake -B Build -G "Visual Studio 17 2022" -A x64 -T v142 -DAC_API_DEVKIT_DIR=<DevKitSupportDir> -DAC_VERSION=28
```

#### XCode (MacOS)

See the list below for the matching deployment targets for different Archicad versions.

| Archicad | Deployment target |
|---|---|
| Archicad 29 | 11.0 |
| Archicad 28 | 11.0 |
| Archicad 27 | 10.15 |
| Archicad 26 | 10.15 |
| Archicad 25 | 10.15 |
| Archicad 24 | 10.13 |
| Archicad 23 | 10.12 |

Run this command from the command line to generate the XCode project:

```
cmake -B Build -G Xcode -DAC_API_DEVKIT_DIR=<DevKitSupportDir> -DAC_VERSION=29
```

#### Visual Studio Code (Platform Independent)

- Install the `CMake Tools` extension for Visual Studio Code.
- Set the `AC_API_DEVKIT_DIR` environment variable to the installed Development Kit Support folder.
- Open the root folder in Visual Studio Code, configure and build the solution.

### Marking a build suitable for distribution

The `AC_ADDON_FOR_DISTRIBUTION` CMake variable controls whether the result of a build has metadata embedded in it that marks it as a private build.
When the variable is set to a false value (such as `OFF`), then the add-on is marked private.

Please make sure you have a release workflow setup separate from a developer workflow where this variable is set to a true value (such as `ON`).
The add-on produced by this release workflow is what should be used for distribution.

## Archicad Compatibility

This template is tested with all Archicad versions starting from Archicad 25.

## Use in Archicad

To use the Add-On in Archicad, you have to add your compiled .apx or .bundle file in Add-On Manager. The example Add-On registers a new command into the Options menu. Please note that the example Add-On works only in the demo version of Archicad.

You can start Archicad in demo mode by the following command line commands:
- Windows: `Archicad.exe -DEMO`
- MacOS: `open Archicad\ 29.app --args -demo`
