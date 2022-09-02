cmake_minimum_required (VERSION 3.16)

function (SetCompilerOptions target ac_version)
	if (${ac_version} EQUAL "27")
		target_compile_features (${target} PUBLIC cxx_std_17)
	else ()
		target_compile_features (${target} PUBLIC cxx_std_14)
	endif ()
	target_compile_options (${target} PUBLIC "$<$<CONFIG:Debug>:-DDEBUG>")
	if (WIN32)
		target_compile_options (${target} PUBLIC /W4 /WX
			/Zc:wchar_t-
			/wd4499
			/EHsc
		)
	else ()
		target_compile_options (${target} PUBLIC -Wall -Wextra -Werror
			-fvisibility=hidden
			-Wno-multichar
			-Wno-ctor-dtor-privacy
			-Wno-invalid-offsetof
			-Wno-ignored-qualifiers
			-Wno-reorder
			-Wno-overloaded-virtual
			-Wno-unused-parameter
			-Wno-deprecated)
	endif ()
endfunction ()

set (API_DEVKIT_DIR $ENV{AC_API_DEVKIT_DIR})

if (CONAN_DEVKIT)
	include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
	set (CONAN_DISABLE_CHECK_COMPILER true)
	conan_basic_setup (NO_OUTPUT_DIRS)
	set (API_DEVKIT_DIR ${CONAN_ARCHICAD-APIDEVKIT_ROOT})
endif ()

set_property (GLOBAL PROPERTY USE_FOLDERS ON)

if (WIN32)
	set (CMAKE_GENERATOR_TOOLSET "v142")
endif ()
set (CMAKE_SUPPRESS_REGENERATION 1)
set (CMAKE_CONFIGURATION_TYPES Debug;Release;RelWithDebInfo)
set (AC_API_DEVKIT_DIR ${API_DEVKIT_DIR} CACHE PATH "API DevKit directory.")
set (AC_ADDON_NAME "ExampleAddOn" CACHE STRING "Add-On name.")
set (AC_ADDON_LANGUAGE "INT" CACHE STRING "Add-On language code.")
set (AC_MDID_DEV "1" CACHE STRING "Your Developer ID")
set (AC_MDID_LOC "1" CACHE STRING "Add-On Local ID")

set (ACAPINC_FILE_LOCATION ${AC_API_DEVKIT_DIR}/Inc/ACAPinc.h)
if (EXISTS ${ACAPINC_FILE_LOCATION})
	file (READ ${ACAPINC_FILE_LOCATION} ACAPIncContent)
	string (REGEX MATCHALL "#define[ \t]+ServerMainVers_([0-9][0-9])" VersionList ${ACAPIncContent})
	set (ARCHICAD_VERSION ${CMAKE_MATCH_1})
	message (STATUS "Archicad Version: ${ARCHICAD_VERSION}")
else ()
	message (FATAL_ERROR "Failed to detect Archicad version, please check the value of the AC_API_DEVKIT_DIR variable.")
endif ()

if (WIN32)
	add_definitions (-DUNICODE -D_UNICODE)
else ()
	add_definitions (-Dmacintosh=1)
endif ()
add_definitions (-DACExtension)

project (${AC_ADDON_NAME})

set (AddOnSourcesFolder Sources/AddOn)
set (AddOnResourcesFolder Sources/AddOnResources)

# AddOnResources

set (ResourceObjectsDir ${CMAKE_BINARY_DIR}/ResourceObjects)

configure_file (${AddOnResourcesFolder}/ResourceMDIDIds.hpp.in ${ResourceObjectsDir}/ResourceMDIDIds.hpp)

file (GLOB AddOnImageFiles
	${AddOnResourcesFolder}/RFIX/Images/*.svg
)
if (WIN32)
	file (GLOB AddOnResourceFiles
		${AddOnResourcesFolder}/R${AC_ADDON_LANGUAGE}/*.grc
		${AddOnResourcesFolder}/RFIX/*.grc
		${AddOnResourcesFolder}/RFIX/*.grc
		${AddOnResourcesFolder}/RFIX.win/*.rc2
		${AddOnResourcesFolder}/Tools/*.py
	)
else ()
	file (GLOB AddOnResourceFiles
		${AddOnResourcesFolder}/R${AC_ADDON_LANGUAGE}/*.grc
		${AddOnResourcesFolder}/RFIX/*.grc
		${AddOnResourcesFolder}/RFIX.mac/*.plist
		${AddOnResourcesFolder}/Tools/*.py
	)
endif ()

source_group ("Images" FILES ${AddOnImageFiles})
source_group ("Resources" FILES ${AddOnResourceFiles})
add_custom_target (
	AddOnResources ALL
	DEPENDS "${ResourceObjectsDir}/AddOnResources.stamp"
	SOURCES ${AddOnResourceFiles} ${AddOnImageFiles}
)

get_filename_component (AddOnSourcesFolderAbsolute "${CMAKE_CURRENT_LIST_DIR}/${AddOnSourcesFolder}" ABSOLUTE)
get_filename_component (AddOnResourcesFolderAbsolute "${CMAKE_CURRENT_LIST_DIR}/${AddOnResourcesFolder}" ABSOLUTE)
if (WIN32)
	add_custom_command (
		OUTPUT "${ResourceObjectsDir}/AddOnResources.stamp"
		DEPENDS ${AddOnResourceFiles} ${AddOnImageFiles}
		COMMENT "Compiling resources..."
		COMMAND ${CMAKE_COMMAND} -E make_directory "${ResourceObjectsDir}"
		COMMAND python "${AddOnResourcesFolderAbsolute}/Tools/CompileResources.py" "${AC_ADDON_LANGUAGE}" "${AC_API_DEVKIT_DIR}" "${AddOnSourcesFolderAbsolute}" "${AddOnResourcesFolderAbsolute}" "${ResourceObjectsDir}" "${ResourceObjectsDir}/${AC_ADDON_NAME}.res"
		COMMAND ${CMAKE_COMMAND} -E touch "${ResourceObjectsDir}/AddOnResources.stamp"
	)
else ()
	add_custom_command (
		OUTPUT "${ResourceObjectsDir}/AddOnResources.stamp"
		DEPENDS ${AddOnResourceFiles} ${AddOnImageFiles}
		COMMENT "Compiling resources..."
		COMMAND ${CMAKE_COMMAND} -E make_directory "${ResourceObjectsDir}"
		COMMAND python "${AddOnResourcesFolderAbsolute}/Tools/CompileResources.py" "${AC_ADDON_LANGUAGE}" "${AC_API_DEVKIT_DIR}" "${AddOnSourcesFolderAbsolute}" "${AddOnResourcesFolderAbsolute}" "${ResourceObjectsDir}" "${CMAKE_BINARY_DIR}/$<CONFIG>/${AC_ADDON_NAME}.bundle/Contents/Resources"
		COMMAND ${CMAKE_COMMAND} -E copy "${AC_API_DEVKIT_DIR}/Inc/PkgInfo" "${CMAKE_BINARY_DIR}/$<CONFIG>/${AC_ADDON_NAME}.bundle/Contents/PkgInfo"
		COMMAND ${CMAKE_COMMAND} -E touch "${ResourceObjectsDir}/AddOnResources.stamp"
	)
endif ()

# AddOn

file (GLOB AddOnHeaderFiles
	${AddOnSourcesFolder}/*.h
	${AddOnSourcesFolder}/*.hpp
)
file (GLOB AddOnSourceFiles
	${AddOnSourcesFolder}/*.c
	${AddOnSourcesFolder}/*.cpp
)
set (
	AddOnFiles
	${AddOnHeaderFiles}
	${AddOnSourceFiles}
)
source_group ("Sources" FILES ${AddOnFiles})
if (WIN32)
	add_library (AddOn SHARED ${AddOnFiles})
else ()
	add_library (AddOn MODULE ${AddOnFiles})
endif ()

set_target_properties (AddOn PROPERTIES OUTPUT_NAME ${AC_ADDON_NAME})
if (WIN32)
	set_target_properties (AddOn PROPERTIES SUFFIX ".apx")
	set_target_properties (AddOn PROPERTIES RUNTIME_OUTPUT_DIRECTORY_$<CONFIG> "${CMAKE_BINARY_DIR}/$<CONFIG>")
else ()
	set_target_properties (AddOn PROPERTIES BUNDLE TRUE)
	set_target_properties (AddOn PROPERTIES MACOSX_BUNDLE_INFO_PLIST "${CMAKE_CURRENT_LIST_DIR}/${AddOnResourcesFolder}/RFIX.mac/Info.plist")
	set_target_properties (AddOn PROPERTIES LIBRARY_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/$<CONFIG>")
endif ()

if (WIN32)
	target_link_options (AddOn PUBLIC "${ResourceObjectsDir}/${AC_ADDON_NAME}.res")
	target_link_options (AddOn PUBLIC /export:GetExportedFuncAddrs,@1 /export:SetImportedFuncAddrs,@2)
endif ()

target_include_directories (AddOn PUBLIC
	${AddOnSourcesFolder}
	${AC_API_DEVKIT_DIR}/Inc
)

if (WIN32)
	target_link_libraries (AddOn
		"$<$<CONFIG:Debug>:${AC_API_DEVKIT_DIR}/Lib/Win/ACAP_STATD.lib>"
		"$<$<CONFIG:Release>:${AC_API_DEVKIT_DIR}/Lib/Win/ACAP_STAT.lib>"
		"$<$<CONFIG:RelWithDebInfo>:${AC_API_DEVKIT_DIR}/Lib/Win/ACAP_STAT.lib>"
	)
else ()
	find_library (CocoaFramework Cocoa)
	target_link_libraries (AddOn
		"${AC_API_DEVKIT_DIR}/Lib/Mactel/libACAP_STAT.a"
		${CocoaFramework}
	)
endif ()

SetCompilerOptions (AddOn ARCHICAD_VERSION)
set_source_files_properties (${AddOnSourceFiles} PROPERTIES LANGUAGE CXX)

file (GLOB ModuleFolders ${AC_API_DEVKIT_DIR}/Modules/*)
target_include_directories (AddOn PUBLIC ${ModuleFolders})
if (WIN32)
	file (GLOB LibFilesInFolder ${AC_API_DEVKIT_DIR}/Modules/*/*/*.lib)
	target_link_libraries (AddOn ${LibFilesInFolder})
else ()
	file (GLOB FrameworkFilesInFolder ${AC_API_DEVKIT_DIR}/Frameworks/*.framework)
	target_link_libraries (AddOn ${FrameworkFilesInFolder})
endif ()
add_dependencies (AddOn AddOnResources)
