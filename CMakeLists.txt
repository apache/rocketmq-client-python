#/*
#* Licensed to the Apache Software Foundation (ASF) under one or more
#* contributor license agreements.  See the NOTICE file distributed with
#* this work for additional information regarding copyright ownership.
#* The ASF licenses this file to You under the Apache License, Version 2.0
#* (the "License"); you may not use this file except in compliance with
#* the License.  You may obtain a copy of the License at
#*
#*     http://www.apache.org/licenses/LICENSE-2.0
#*
#* Unless required by applicable law or agreed to in writing, software
#* distributed under the License is distributed on an "AS IS" BASIS,
#* WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#* See the License for the specific language governing permissions and
#* limitations under the License.
#*/

project(rocketmq-client-python)

cmake_minimum_required(VERSION 2.6)

set(CMAKE_MACOSX_RPATH 1)

# CMake complains if we don't have this.
if (COMMAND cmake_policy)
    cmake_policy(SET CMP0003 NEW)
endif ()

# We're escaping quotes in the Windows version number, because
# for some reason CMake won't do it at config version 2.4.7
# It seems that this restores the newer behaviour where define
# args are not auto-escaped.
if (COMMAND cmake_policy)
    cmake_policy(SET CMP0005 NEW)
endif ()

if (POLICY CMP0048)
    cmake_policy(SET CMP0048 NEW)
endif ()

if (POLICY CMP0064)
    cmake_policy(SET CMP0064 NEW)
endif ()
# First, declare project (important for prerequisite checks).
project(rocketmq-client-python)

set(CMAKE_ALLOW_LOOSE_LOOP_CONSTRUCTS ON)
set(CMAKE_VERBOSE_MAKEFILE 1)
#Path of custom cmake
set(CMAKE_MODULE_PATH ${PROJECT_SOURCE_DIR}/cmake)
# put binaries in a different dir to make them easier to find.
set(EXECUTABLE_OUTPUT_PATH ${PROJECT_SOURCE_DIR}/bin)
set(LIBRARY_OUTPUT_PATH ${PROJECT_SOURCE_DIR}/bin)

# for unix, put debug files in a separate bin "debug" dir.
# release bin files should stay in the root of the bin dir.
# if (CMAKE_GENERATOR STREQUAL "Unix Makefiles")
#     if (CMAKE_BUILD_TYPE STREQUAL Debug)
#         set(EXECUTABLE_OUTPUT_PATH ${PROJECT_SOURCE_DIR}/bin/debug)
#         set(LIBRARY_OUTPUT_PATH ${PROJECT_SOURCE_DIR}/bin/debug)
#     endif()
# endif()

if (NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE "Release")
endif ()

set(CXX_FLAGS
        -std=c++11
        -g
        -Wall
        -Wno-deprecated
        -fPIC
        -fno-strict-aliasing
        -Wno-unused-result
        -Wno-unused-local-typedef
        # -finline-limit=1000
        # -Wextra
        # -pedantic
        # -pedantic-errors
        # -D_FILE_OFFSET_BITS=64
        # -DVALGRIND
        # -DCHECK_PTHREAD_RETURN_VALUE
        # -Werror
        # -Wconversion
        # -Wno-unused-parameter
        # -Wunused-but-set-variable
        # -Wold-style-cast
        # -Woverloaded-virtual
        # -Wpointer-arith
        # -Wshadow
        # -Wwrite-strings
        # -Wdeprecated-declarations
        # -march=native
        # -MMD
        # -rdynamic
        )

if (CMAKE_BUILD_BITS EQUAL 32)
    list(APPEND CXX_FLAGS "-m32")
else () #not-condition
    list(APPEND CXX_FLAGS "-m64")
endif ()

string(REPLACE ";" " " CMAKE_CXX_FLAGS "${CXX_FLAGS}")
# set(CMAKE_CXX_COMPILER "c++")
set(CMAKE_CXX_FLAGS_DEBUG "-O0 -DDEBUG")
set(CMAKE_CXX_FLAGS_RELEASE "-O3 -DNDEBUG")

include("cmake/ConfigureChecks.cmake")

# Declare deplibs, so we can use list in linker later. There's probably
# a more elegant way of doing this; with SCons, when you check for the
# lib, it is automatically passed to the linker.
set(deplibs)

# For some reason, the check_function_exists macro doesn't detect
# the inet_aton on some pure Unix platforms (e.g. sunos5). So we
# need to do a more detailed check and also include some extra deplibs.

# pthread is used on both Linux and Mac
check_library_exists("pthread" pthread_create "" HAVE_PTHREAD)
if (HAVE_PTHREAD)
    list(APPEND deplibs pthread)
else ()
    message(FATAL_ERROR "Missing library: pthread")
endif ()

check_library_exists(dl dlopen "" HAVE_LIBDL)
if (HAVE_LIBDL)
    list(APPEND deplibs dl)
else () #not-HAVE_LIBDL
    message(FATAL_ERROR "Missing library: dl")
endif ()

check_library_exists(z compress "" HAVE_LIBZ)
if (HAVE_LIBZ)
    list(APPEND deplibs z)
else () #not-HAVE_LIBZ
    message(FATAL_ERROR "Missing library: z")
endif ()


if (WIN32)
    find_package(PythonLibs 2.7)
elseif (APPLE)
    find_package(PythonLibs 2.7)
else ()
    find_package(PythonLibs 2.7)
endif (WIN32)

if (PYTHONLIBS_FOUND)
    message(STATUS "** Python Include dir: ${PYTHON_INCLUDE_DIRS}")
    message(STATUS "** Python Libraries dir: ${PYTHON_LIBRARY_DIRS}")
    message(STATUS "** Python Libraries: ${PYTHON_LIBRARIES}")
    include_directories(${PYTHON_INCLUDE_DIRS})
else ()
    message(FATAL_ERROR "Missing library: python-devel ")
endif ()

option(Boost_USE_STATIC_LIBS "only find boost static libs" OFF) # find boost libs
if (WIN32)
    find_package(Boost REQUIRED COMPONENTS python)
elseif (APPLE)
    find_package(Boost REQUIRED COMPONENTS python)
else ()
    find_package(Boost REQUIRED COMPONENTS python)
endif (WIN32)

if (Boost_FOUND)
    message(STATUS "** Boost Include dir: ${Boost_INCLUDE_DIR}")
    message(STATUS "** Boost Libraries dir: ${Boost_LIBRARY_DIRS}")
    message(STATUS "** Boost Libraries: ${Boost_LIBRARIES}")
    include_directories(${Boost_INCLUDE_DIRS})
else ()
    message(FATAL_ERROR "Missing library: boost_python")
endif ()

option(ROCKETMQ_USE_STATIC_LIBS "only find rocketmq static libs" ON) #find rocketmq libs

find_package(rocketmq)

if (ROCKETMQ_FOUND)
    message(STATUS "** Rocketmq Include dir: ${ROCKETMQ_INCLUDE_DIRS}")
    message(STATUS "** Rocketmq Libraries dir: ${ROCKETMQ_LIBRARY_DIRS}")
    message(STATUS "** Rocketmq Libraries: ${ROCKETMQ_LIBRARIES}")
    include_directories(${ROCKETMQ_INCLUDE_DIRS})
else ()
    message(FATAL_ERROR "Missing library: rocketmq")
endif ()
# add include dir for bsd (posix uses /usr/include/)
set(CMAKE_INCLUDE_PATH "${CMAKE_INCLUDE_PATH}:/usr/include")

# For config.h, set some static values; it may be a good idea to make
# these values dynamic for non-standard UNIX compilers.
set(ACCEPT_TYPE_ARG3 socklen_t)
set(HAVE_CXX_BOOL 1)
set(HAVE_CXX_CASTS 1)
set(HAVE_CXX_EXCEPTIONS 1)
set(HAVE_CXX_MUTABLE 1)
set(HAVE_CXX_STDLIB 1)
set(HAVE_PTHREAD_SIGNAL 1)
set(SELECT_TYPE_ARG1 int)
set(SELECT_TYPE_ARG234 "(fd_set *)")
set(SELECT_TYPE_ARG5 "(struct timeval *)")
set(STDC_HEADERS 1)
set(TIME_WITH_SYS_TIME 1)
set(HAVE_SOCKLEN_T 1)

option(TEST "Build test cases" OFF)
if (TEST)
    enable_testing()
    option(gtest_build_tests OFF)
    #add_subdirectory(third_party/googletest/googletest)
    include_directories(SYSTEM ${gtest_SOURCE_DIR}/include ${gtest_SOURCE_DIR})
    add_subdirectory(unitests)
endif ()

add_subdirectory(project)
