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
CMAKE_BINARY_DIR = /mnt/e/dev/athena/athena_tool/external_repos/timeloop/cmake-build-release

# Utility rule file for NightlySubmit.

# Include the progress variables for this target.
include yaml-cpp-master/CMakeFiles/NightlySubmit.dir/progress.make

yaml-cpp-master/CMakeFiles/NightlySubmit:
	cd /mnt/e/dev/athena/athena_tool/external_repos/timeloop/cmake-build-release/yaml-cpp-master && /usr/bin/ctest -D NightlySubmit

NightlySubmit: yaml-cpp-master/CMakeFiles/NightlySubmit
NightlySubmit: yaml-cpp-master/CMakeFiles/NightlySubmit.dir/build.make

.PHONY : NightlySubmit

# Rule to build all files generated by this target.
yaml-cpp-master/CMakeFiles/NightlySubmit.dir/build: NightlySubmit

.PHONY : yaml-cpp-master/CMakeFiles/NightlySubmit.dir/build

yaml-cpp-master/CMakeFiles/NightlySubmit.dir/clean:
	cd /mnt/e/dev/athena/athena_tool/external_repos/timeloop/cmake-build-release/yaml-cpp-master && $(CMAKE_COMMAND) -P CMakeFiles/NightlySubmit.dir/cmake_clean.cmake
.PHONY : yaml-cpp-master/CMakeFiles/NightlySubmit.dir/clean

yaml-cpp-master/CMakeFiles/NightlySubmit.dir/depend:
	cd /mnt/e/dev/athena/athena_tool/external_repos/timeloop/cmake-build-release && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /mnt/e/dev/athena/athena_tool/external_repos/timeloop /mnt/e/dev/athena/athena_tool/external_repos/timeloop/yaml-cpp-master /mnt/e/dev/athena/athena_tool/external_repos/timeloop/cmake-build-release /mnt/e/dev/athena/athena_tool/external_repos/timeloop/cmake-build-release/yaml-cpp-master /mnt/e/dev/athena/athena_tool/external_repos/timeloop/cmake-build-release/yaml-cpp-master/CMakeFiles/NightlySubmit.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : yaml-cpp-master/CMakeFiles/NightlySubmit.dir/depend

