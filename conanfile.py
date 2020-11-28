from conans import ConanFile, CMake, tools

_ppconsul_boost_orig = '''if (NOT ${USE_BOOST_REGEX})
    find_package(Boost ${BOOST_MIN_VERSION} REQUIRED)
else ()
    find_package(Boost ${BOOST_MIN_VERSION} REQUIRED COMPONENTS regex)
    add_definitions(-DPPCONSUL_USE_BOOST_REGEX)
endif ()'''

_ppconsul_boost_new= '''
set(Boost_FOUND ON)
set(Boost_LIBRARIES "${CONAN_LIBS_BOOST}")
set(Boost_INCLUDE_DIRS "${CONAN_INCLUDE_DIRS_BOOST}")'''

_ppconsul_curl_orig = "find_package(CURL REQUIRED)"

_ppconsul_curl_new = '''
set(CURL_FOUND ON)
set(CURL_LIBRARIES "${CONAN_LIBS_LIBCURL}")
set(CURL_INCLUDE_DIR "${CONAN_INCLUDE_DIRS_LIBCURL}")'''

class PpconsulConan(ConanFile):
    name = "Ppconsul"
    version = "0.2.1"
    license = "BSL"
    url = "https://github.com/oliora/ppconsul"
    settings = "os", "compiler", "build_type", "arch"
    requires = (
        "boost/1.73.0",
        "libcurl/7.73.0"
    )
    generators = "cmake", "cmake_find_package_multi"

    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.definitions['CMAKE_POSITION_INDEPENDENT_CODE'] = True
        cmake.configure(source_folder="ppconsul")
        return cmake

    def configure(self):
        if self.settings.os == "Windows" and self.settings.compiler == "Visual Studio":
            del self.options.fPIC
            compiler_version = tools.Version(self.settings.compiler.version)
            if compiler_version < 14:
                raise ConanInvalidConfiguration("gRPC can only be built with Visual Studio 2015 or higher.")
        self.options["libcurl"].shared = True

    def source(self):
        self.run("git clone {}.git".format(self.url))
        tools.replace_in_file("ppconsul/CMakeLists.txt",
            "include(./conan_paths.cmake OPTIONAL)",
            "include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)\nconan_basic_setup()")
        tools.replace_in_file("ppconsul/CMakeLists.txt",
            _ppconsul_boost_orig, _ppconsul_boost_new)
        tools.replace_in_file("ppconsul/CMakeLists.txt",
            _ppconsul_curl_orig, _ppconsul_curl_new)

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        self.copy(pattern="LICENSE", dst="licenses", keep_path=False)
        cmake = self._configure_cmake()
        cmake.install()

    def package_info(self):
        self.cpp_info.names["cmake_find_package"] = self.name
        self.cpp_info.names["cmake_find_package_multi"] = self.name
        self.cpp_info.libs = ["Ppconsul"]
