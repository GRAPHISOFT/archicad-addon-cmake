cmake_minimum_required (VERSION 3.17)

include (Tools/CMakeCommon.cmake)

set (API_DEVKIT_DIR $ENV{AC_API_DEVKIT_DIR})

set_property (GLOBAL PROPERTY USE_FOLDERS ON)

set (CMAKE_CONFIGURATION_TYPES Debug;Release;RelWithDebInfo)
set (AC_API_DEVKIT_DIR ${API_DEVKIT_DIR} CACHE PATH "API DevKit directory.")
set (AC_ADDON_LANGUAGE "INT" CACHE STRING "Add-On language code.")

DetectACVersion (${AC_API_DEVKIT_DIR} ACVersion)
message (STATUS "Archicad Version: ${ACVersion}")

SetGlobalCompilerDefinitions (${ACVersion})

project (${AC_ADDON_NAME})

set (AddOnSourcesFolder Src)
set (AddOnResourcesFolder .)
GenerateAddOnProject (${ACVersion} ${AC_API_DEVKIT_DIR} ${AC_ADDON_NAME} ${AddOnSourcesFolder} ${AddOnResourcesFolder} ${AC_ADDON_LANGUAGE})
