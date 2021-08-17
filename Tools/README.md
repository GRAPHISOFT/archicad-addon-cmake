# Archicad AddOn CMake template  

## What is this?  

This is a small script which automatically adds or removes the GRAPHISOFT Modules used in the Visual Studio project to the CMakeLists.txt  

## How It Works?  

It is pretty simple:  
    1. After the project is made with CMake it will add a .bat file to the :root/Tools folder. After the bat file is opened it will run the Python script with the required arguments(The arguments are base on the arguments were given at the make process).  
    2. The script reads the AddOn.vcxproj as an XML file and searches the Debug Configuration for dependencies  
    3. Reads all "AddGSModule(target folder libFile)" commands in the CMakeLists.txt.  
    4. Compares the 2 lists and then modifies the CMakeLists.txt

+ If the AddOn Solution has more dependencies than adds them to the CMakeLists.txt
+ If the AddOn Solution has less dependencies than removes them from CMakeLists.txt
  
## What's next  

+ macOS compatibility.  

+ Including all types of folders, not only the GRAPHISOFT modules.
