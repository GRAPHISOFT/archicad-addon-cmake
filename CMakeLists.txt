cmake_minimum_required (VERSION 3.17)

include (Tools/CMakeCommon.cmake)

set (API_DEVKIT_DIR $ENV{AC_API_DEVKIT_DIR})

set_property (GLOBAL PROPERTY USE_FOLDERS ON)

set (CMAKE_CONFIGURATION_TYPES Debug;Release;RelWithDebInfo)
set (AC_API_DEVKIT_DIR ${API_DEVKIT_DIR} CACHE PATH "API DevKit directory.")
set (AC_ADDON_NAME "ExampleAddOn" CACHE STRING "Add-On name.")
set (AC_ADDON_LANGUAGE "INT" CACHE STRING "Add-On language code.")

if (NOT DEFINED AC_VERSION)
    message (FATAL_ERROR "AC_VERSION is not set!")
endif ()

message (STATUS "Archicad Version: ${AC_VERSION}")
SetGlobalCompilerDefinitions (${AC_VERSION})

project (${AC_ADDON_NAME}-${AC_VERSION})

set (AddOnSourcesFolder Src)
set (AddOnResourcesFolder .)
GenerateAddOnProject (CMakeTarget ${AC_VERSION} ${AC_API_DEVKIT_DIR} ${AC_ADDON_NAME} ${AddOnSourcesFolder} ${AddOnResourcesFolder} ${AC_ADDON_LANGUAGE})
