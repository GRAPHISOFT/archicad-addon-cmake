cmake_minimum_required (VERSION 3.17)

include (Tools/CMakeCommon.cmake)

set (API_DEVKIT_DIR $ENV{AC_API_DEVKIT_DIR})

if (GITHUB_BUILD)
    include(${CMAKE_BINARY_DIR}/conan_paths.cmake)
    set (API_DEVKIT_DIR ${CONAN_ARCHICAD-APIDEVKIT_ROOT}/bin)
endif ()

set_property (GLOBAL PROPERTY USE_FOLDERS ON)

set (CMAKE_CONFIGURATION_TYPES Debug;Release;RelWithDebInfo)
set (AC_API_DEVKIT_DIR ${API_DEVKIT_DIR} CACHE PATH "API DevKit directory.")
set (AC_ADDON_NAME "ExampleAddOn" CACHE STRING "Add-On name.")
set (AC_ADDON_LANGUAGE "INT" CACHE STRING "Add-On language code.")

project (${AC_ADDON_NAME})

DetectACVersion (${AC_API_DEVKIT_DIR} ACVersion)
message (STATUS "Archicad Version: ${ACVersion}")

set (AddOnFolder .)
SetGlobalCompilerDefinitions ()
GenerateAddOnProject (${ACVersion} ${AC_API_DEVKIT_DIR} ${AC_ADDON_NAME} ${AddOnFolder} ${AC_ADDON_LANGUAGE})
