# Archicad AddOn CMake template  

## What is this?  

This is a small script which automatically adds the GRAPHISOFT Modules used in the project to the CMakeLists.txt  

## Why I made this script?  

During development, I am using more than 2 PCs on Windows and one macOS to make an AddOn. Many times I had the issue that I forgot some dependency or I had to put all the dependencies in the other build configurations (which is tedious and time-consuming sometimes).

## How It Works?  

It is pretty simple:  
    1. After the project is successfully Built it runs AddModules.py  
    2. Reads AddOn.vcxproj as an XML file and searches the Debug Configuration for dependencies  
    3. Reads all "AddGSModule(target folder libFile)" commands in it.  
    4. Compares the 2 lists and then:  

+ If AddOn Solution has more dependencies than adds them to the CMakeLists.txt
+ If AddOn Solution has less dependencies than searches in the CMakeLists.txt and removes them  
  
## What's next  

+ macOS compatibility.  

+ Including all types of folders, not only the GRAPHISOFT modules.
