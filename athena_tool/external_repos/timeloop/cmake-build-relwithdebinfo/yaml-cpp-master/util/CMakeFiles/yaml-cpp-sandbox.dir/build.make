# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.16

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:


#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:


# Remove some rules from gmake that .SUFFIXES does not remove.
SUFFIXES =

.SUFFIXES: .hpux_make_needs_suffix_list


# Suppress display of executed commands.
$(VERBOSE).SILENT:


# A target that is always out of date.
cmake_force:

.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/bin/cmake

# The command to remove a file.
RM = /usr/bin/cmake -E remove -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /mnt/e/dev/athena/athena_tool/external_repos/timeloop

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /mnt/e/dev/athena/athena_tool/external_repos/timeloop/cmake-build-relwithdebinfo

# Include any dependencies generated for this target.
include yaml-cpp-master/util/CMakeFiles/yaml-cpp-sandbox.dir/depend.make

# Include the progress variables for this target.
include yaml-cpp-master/util/CMakeFiles/yaml-cpp-sandbox.dir/progress.make

# Include the compile flags for this target's objects.
include yaml-cpp-master/util/CMakeFiles/yaml-cpp-sandbox.dir/flags.make

yaml-cpp-master/util/CMakeFiles/yaml-cpp-sandbox.dir/sandbox.cpp.o: yaml-cpp-master/util/CMakeFiles/yaml-cpp-sandbox.dir/flags.make
yaml-cpp-master/util/CMakeFiles/yaml-cpp-sandbox.dir/sandbox.cpp.o: ../yaml-cpp-master/util/sandbox.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/mnt/e/dev/athena/athena_tool/external_repos/timeloop/cmake-build-relwithdebinfo/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object yaml-cpp-master/util/CMakeFiles/yaml-cpp-sandbox.dir/sandbox.cpp.o"
	cd /mnt/e/dev/athena/athena_tool/external_repos/timeloop/cmake-build-relwithdebinfo/yaml-cpp-master/util && /usr/bin/g++  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/yaml-cpp-sandbox.dir/sandbox.cpp.o -c /mnt/e/dev/athena/athena_tool/external_repos/timeloop/yaml-cpp-master/util/sandbox.cpp

yaml-cpp-master/util/CMakeFiles/yaml-cpp-sandbox.dir/sandbox.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/yaml-cpp-sandbox.dir/sandbox.cpp.i"
	cd /mnt/e/dev/athena/athena_tool/external_repos/timeloop/cmake-build-relwithdebinfo/yaml-cpp-master/util && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /mnt/e/dev/athena/athena_tool/external_repos/timeloop/yaml-cpp-master/util/sandbox.cpp > CMakeFiles/yaml-cpp-sandbox.dir/sandbox.cpp.i

yaml-cpp-master/util/CMakeFiles/yaml-cpp-sandbox.dir/sandbox.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/yaml-cpp-sandbox.dir/sandbox.cpp.s"
	cd /mnt/e/dev/athena/athena_tool/external_repos/timeloop/cmake-build-relwithdebinfo/yaml-cpp-master/util && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /mnt/e/dev/athena/athena_tool/external_repos/timeloop/yaml-cpp-master/util/sandbox.cpp -o CMakeFiles/yaml-cpp-sandbox.dir/sandbox.cpp.s

# Object files for target yaml-cpp-sandbox
yaml__cpp__sandbox_OBJECTS = \
"CMakeFiles/yaml-cpp-sandbox.dir/sandbox.cpp.o"

# External object files for target yaml-cpp-sandbox
yaml__cpp__sandbox_EXTERNAL_OBJECTS =

yaml-cpp-master/util/sandbox: yaml-cpp-master/util/CMakeFiles/yaml-cpp-sandbox.dir/sandbox.cpp.o
yaml-cpp-master/util/sandbox: yaml-cpp-master/util/CMakeFiles/yaml-cpp-sandbox.dir/build.make
yaml-cpp-master/util/sandbox: yaml-cpp-master/libyaml-cpp.a
yaml-cpp-master/util/sandbox: yaml-cpp-master/util/CMakeFiles/yaml-cpp-sandbox.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/mnt/e/dev/athena/athena_tool/external_repos/timeloop/cmake-build-relwithdebinfo/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX executable sandbox"
	cd /mnt/e/dev/athena/athena_tool/external_repos/timeloop/cmake-build-relwithdebinfo/yaml-cpp-master/util && $(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/yaml-cpp-sandbox.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
yaml-cpp-master/util/CMakeFiles/yaml-cpp-sandbox.dir/build: yaml-cpp-master/util/sandbox

.PHONY : yaml-cpp-master/util/CMakeFiles/yaml-cpp-sandbox.dir/build

yaml-cpp-master/util/CMakeFiles/yaml-cpp-sandbox.dir/clean:
	cd /mnt/e/dev/athena/athena_tool/external_repos/timeloop/cmake-build-relwithdebinfo/yaml-cpp-master/util && $(CMAKE_COMMAND) -P CMakeFiles/yaml-cpp-sandbox.dir/cmake_clean.cmake
.PHONY : yaml-cpp-master/util/CMakeFiles/yaml-cpp-sandbox.dir/clean

yaml-cpp-master/util/CMakeFiles/yaml-cpp-sandbox.dir/depend:
	cd /mnt/e/dev/athena/athena_tool/external_repos/timeloop/cmake-build-relwithdebinfo && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /mnt/e/dev/athena/athena_tool/external_repos/timeloop /mnt/e/dev/athena/athena_tool/external_repos/timeloop/yaml-cpp-master/util /mnt/e/dev/athena/athena_tool/external_repos/timeloop/cmake-build-relwithdebinfo /mnt/e/dev/athena/athena_tool/external_repos/timeloop/cmake-build-relwithdebinfo/yaml-cpp-master/util /mnt/e/dev/athena/athena_tool/external_repos/timeloop/cmake-build-relwithdebinfo/yaml-cpp-master/util/CMakeFiles/yaml-cpp-sandbox.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : yaml-cpp-master/util/CMakeFiles/yaml-cpp-sandbox.dir/depend

