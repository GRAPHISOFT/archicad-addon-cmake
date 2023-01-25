from conan import ConanFile


class Recipe(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "CMakeToolchain", "CMakeDeps", "VirtualBuildEnv", "cmake_paths"

    def layout(self):
        self.folders.generators = "conan"

    def requirements(self):
        self.requires("archicad-apidevkit/26")
