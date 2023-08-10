function (SetGlobalCompilerDefinitions)

    if (WIN32)
        add_definitions (-DUNICODE -D_UNICODE)
    else ()
        add_definitions (-Dmacintosh=1)
    endif ()
    add_definitions (-DACExtension)

endfunction ()

function (SetCompilerOptions target acVersion)

    if (${acVersion} LESS 27)
        target_compile_features (${target} PUBLIC cxx_std_14)
    else ()
        target_compile_features (${target} PUBLIC cxx_std_17)
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
        if (${acVersion} LESS_EQUAL "24")
            target_compile_options (${target} PUBLIC -Wno-non-c-typedef-for-linkage)
        endif ()
    endif ()
	
endfunction ()

function (DetectACVersion devKitDir acVersion)

    set (ACAPIncFileLocation ${devKitDir}/Inc/ACAPinc.h)
    if (EXISTS ${ACAPIncFileLocation})
        file (READ ${ACAPIncFileLocation} ACAPIncContent)
        string (REGEX MATCHALL "#define[ \t]+ServerMainVers_([0-9][0-9])" VersionList ${ACAPIncContent})
        set (${acVersion} ${CMAKE_MATCH_1} PARENT_SCOPE)
    else ()
        message (FATAL_ERROR "Failed to detect Archicad version, please check the value of the AC_API_DEVKIT_DIR variable.")
    endif ()

endfunction ()

function (LinkGSLibrariesToProject acVersion devKitDir addOnName)

    if (WIN32)
        if (${acVersion} LESS 27)
            target_link_libraries (${addOnName}
                "$<$<CONFIG:Debug>:${devKitDir}/Lib/Win/ACAP_STATD.lib>"
                "$<$<CONFIG:Release>:${devKitDir}/Lib/Win/ACAP_STAT.lib>"
                "$<$<CONFIG:RelWithDebInfo>:${devKitDir}/Lib/Win/ACAP_STAT.lib>"
            )
        else ()
            target_link_libraries (${addOnName}
                "$<$<CONFIG:Debug>:${devKitDir}/Lib/ACAP_STATD.lib>"
                "$<$<CONFIG:Release>:${devKitDir}/Lib/ACAP_STAT.lib>"
                "$<$<CONFIG:RelWithDebInfo>:${devKitDir}/Lib/ACAP_STAT.lib>"
            )
        endif ()
    else ()
        find_library (CocoaFramework Cocoa)
        if (${acVersion} LESS 27)
            target_link_libraries (${addOnName}
                "${devKitDir}/Lib/Mactel/libACAP_STAT.a"
                ${CocoaFramework}
            )
        else ()
            target_link_libraries (${addOnName}
                "${devKitDir}/Lib/libACAP_STAT.a"
                ${CocoaFramework}
            )
        endif ()
    endif ()

    file (GLOB ModuleFolders ${devKitDir}/Modules/*)
    target_include_directories (${addOnName} PUBLIC ${ModuleFolders})
    if (WIN32)
        file (GLOB LibFilesInFolder ${devKitDir}/Modules/*/*/*.lib)
        target_link_libraries (${addOnName} ${LibFilesInFolder})
    else ()
        file (GLOB FrameworkFilesInFolder ${devKitDir}/Frameworks/*.framework)
        target_link_libraries (${addOnName} ${FrameworkFilesInFolder})
    endif ()

endfunction ()

function (GenerateAddOnProject acVersion devKitDir addOnName addOnFolder addOnLanguage)

    find_package (Python COMPONENTS Interpreter)

    set (AddOnSourcesFolder ${addOnFolder}/Src)
    set (AddOnResourcesFolder ${addOnFolder})

    set (ResourceObjectsDir ${CMAKE_BINARY_DIR}/ResourceObjects)
    set (ResourceStampFile "${ResourceObjectsDir}/AddOnResources.stamp")
    configure_file (${addOnFolder}/Tools/ResourceMDIDIds.hpp.in ${ResourceObjectsDir}/ResourceMDIDIds.hpp)

    file (GLOB AddOnImageFiles CONFIGURE_DEPENDS
        ${AddOnResourcesFolder}/RFIX/Images/*.svg
    )
    if (WIN32)
        file (GLOB AddOnResourceFiles CONFIGURE_DEPENDS
            ${AddOnResourcesFolder}/R${addOnLanguage}/*.grc
            ${AddOnResourcesFolder}/RFIX/*.grc
            ${AddOnResourcesFolder}/RFIX.win/*.rc2
            ${AddOnResourcesFolder}/Tools/*.py
        )
    else ()
        file (GLOB AddOnResourceFiles CONFIGURE_DEPENDS
            ${AddOnResourcesFolder}/R${addOnLanguage}/*.grc
            ${AddOnResourcesFolder}/RFIX/*.grc
            ${AddOnResourcesFolder}/RFIX.mac/*.plist
            ${AddOnResourcesFolder}/Tools/*.py
        )
    endif ()

    get_filename_component (AddOnSourcesFolderAbsolute "${CMAKE_CURRENT_LIST_DIR}/${AddOnSourcesFolder}" ABSOLUTE)
    get_filename_component (AddOnResourcesFolderAbsolute "${CMAKE_CURRENT_LIST_DIR}/${AddOnResourcesFolder}" ABSOLUTE)
    if (WIN32)
        add_custom_command (
            OUTPUT ${ResourceStampFile}
            DEPENDS ${AddOnResourceFiles} ${AddOnImageFiles}
            COMMENT "Compiling resources..."
            COMMAND ${CMAKE_COMMAND} -E make_directory "${ResourceObjectsDir}"
            COMMAND ${Python_EXECUTABLE} "${AddOnResourcesFolderAbsolute}/Tools/CompileResources.py" "${addOnLanguage}" "${devKitDir}" "${AddOnSourcesFolderAbsolute}" "${AddOnResourcesFolderAbsolute}" "${ResourceObjectsDir}" "${ResourceObjectsDir}/${addOnName}.res"
            COMMAND ${CMAKE_COMMAND} -E touch ${ResourceStampFile}
        )
    else ()
        add_custom_command (
            OUTPUT ${ResourceStampFile}
            DEPENDS ${AddOnResourceFiles} ${AddOnImageFiles}
            COMMENT "Compiling resources..."
            COMMAND ${CMAKE_COMMAND} -E make_directory "${ResourceObjectsDir}"
            COMMAND ${Python_EXECUTABLE} "${AddOnResourcesFolderAbsolute}/Tools/CompileResources.py" "${addOnLanguage}" "${devKitDir}" "${AddOnSourcesFolderAbsolute}" "${AddOnResourcesFolderAbsolute}" "${ResourceObjectsDir}" "${CMAKE_BINARY_DIR}/$<CONFIG>/${addOnName}.bundle/Contents/Resources"
            COMMAND ${CMAKE_COMMAND} -E copy "${devKitDir}/Inc/PkgInfo" "${CMAKE_BINARY_DIR}/$<CONFIG>/${addOnName}.bundle/Contents/PkgInfo"
            COMMAND ${CMAKE_COMMAND} -E touch ${ResourceStampFile}
        )
    endif ()

    file (GLOB AddOnHeaderFiles CONFIGURE_DEPENDS
        ${AddOnSourcesFolder}/*.h
        ${AddOnSourcesFolder}/*.hpp
    )
    file (GLOB AddOnSourceFiles CONFIGURE_DEPENDS
        ${AddOnSourcesFolder}/*.c
        ${AddOnSourcesFolder}/*.cpp
    )
    set (
        AddOnFiles
        ${AddOnHeaderFiles}
        ${AddOnSourceFiles}
        ${AddOnImageFiles}
        ${AddOnResourceFiles}
        ${ResourceStampFile}
    )
    
    source_group ("Sources" FILES ${AddOnHeaderFiles} ${AddOnSourceFiles})
    source_group ("Images" FILES ${AddOnImageFiles})
    source_group ("Resources" FILES ${AddOnResourceFiles})
    if (WIN32)
        add_library (${addOnName} SHARED ${AddOnFiles})
    else ()
        add_library (${addOnName} MODULE ${AddOnFiles})
    endif ()

    set_target_properties (${addOnName} PROPERTIES OUTPUT_NAME ${addOnName})
    if (WIN32)
        set_target_properties (${addOnName} PROPERTIES SUFFIX ".apx")
        set_target_properties (${addOnName} PROPERTIES RUNTIME_OUTPUT_DIRECTORY_$<CONFIG> "${CMAKE_BINARY_DIR}/$<CONFIG>")
    else ()
        set_target_properties (${addOnName} PROPERTIES BUNDLE TRUE)
        set_target_properties (${addOnName} PROPERTIES MACOSX_BUNDLE_INFO_PLIST "${CMAKE_CURRENT_LIST_DIR}/${AddOnResourcesFolder}/RFIX.mac/Info.plist")
        set_target_properties (${addOnName} PROPERTIES LIBRARY_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/$<CONFIG>")
    endif ()

    if (WIN32)
        target_link_options (${addOnName} PUBLIC "${ResourceObjectsDir}/${addOnName}.res")
        target_link_options (${addOnName} PUBLIC /export:GetExportedFuncAddrs,@1 /export:SetImportedFuncAddrs,@2)
    endif ()

    target_include_directories (${addOnName} PUBLIC
        ${AddOnSourcesFolder}
        ${devKitDir}/Inc
    )

    LinkGSLibrariesToProject (${acVersion} ${devKitDir} ${addOnName})

    set_source_files_properties (${AddOnSourceFiles} PROPERTIES LANGUAGE CXX)
    SetCompilerOptions (${addOnName} ${acVersion})

endfunction ()
