# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Find RocketMQ Libary
#
# Find the rocketmq includes and library
#
# if you need to add a custom library search path, do it via CMAKE_PREFIX_PATH
#
# -*- cmake -*-
# - Find Rocketmq
# Find the Rocketmq includes and library
# This module defines
#  ROCKETMQ_INCLUDE_DIRS, where to find CCommon.h, CMessage.h, etc.#include "CCommon.h"
#  ROCKETMQ_LIBRARIES, the libraries needed to use Rocketmq.
#  ROCKETMQ_FOUND, If false, do not try to use Rocketmq.
#  also defined, but not for general use are
#  ROCKETMQ_LIBRARIES, where to find the rocketmq library.

# Support preference of static libs by adjusting CMAKE_FIND_LIBRARY_SUFFIXES
if (ROCKETMQ_USE_STATIC_LIBS)
    set(_rocketmq_ORIG_CMAKE_FIND_LIBRARY_SUFFIXES :${CMAKE_FIND_LIBRARY_SUFFIXES})
    if (WIN32)
        list(INSERT CMAKE_FIND_LIBRARY_SUFFIXES 0 .lib .a)
    else ()
        set(CMAKE_FIND_LIBRARY_SUFFIXES .a)
    endif ()
else ()
    set(_rocketmq_ORIG_CMAKE_FIND_LIBRARY_SUFFIXES :${CMAKE_FIND_LIBRARY_SUFFIXES})
    if (WIN32)
        list(INSERT CMAKE_FIND_LIBRARY_SUFFIXES 0 .dll)
    elseif (APPLE)
        set(CMAKE_FIND_LIBRARY_SUFFIXES .dylib)
    else ()
        set(CMAKE_FIND_LIBRARY_SUFFIXES .so)
    endif (WIN32)
endif (ROCKETMQ_USE_STATIC_LIBS)
if (ROCKETMQ_USE_SHARED_LIBS)
    set(_rocketmq_ORIG_CMAKE_FIND_LIBRARY_SUFFIXES :${CMAKE_FIND_LIBRARY_SUFFIXES})
    if (WIN32)
        list(INSERT CMAKE_FIND_LIBRARY_SUFFIXES 0 .dll)
    elseif (APPLE)
        set(CMAKE_FIND_LIBRARY_SUFFIXES .dylib)
    else ()
        set(CMAKE_FIND_LIBRARY_SUFFIXES .so)
    endif ()
endif (ROCKETMQ_USE_SHARED_LIBS)

FIND_PATH(ROCKETMQ_INCLUDE_DIRS
        NAMES
        CCommon.h
        PATHS
        /usr/include
        /usr/local/include
        C:/rocketmq/include
        ${CMAKE_SOURCE_DIR}/win32-deps/include
        ${ROCKETMQ_LIBRARY_DIRS}
        PATH_SUFFIXES rocketmq
        )
message(status**** "rocketmq include path: ${ROCKETMQ_INCLUDE_DIRS}")

find_library(ROCKETMQ_LIBRARIES
        NAMES rocketmq
        PATHS
        /usr/lib
        /usr/local/lib
        C:/rocketmq/lib
        ${CMAKE_SOURCE_DIR}/win32-deps/lib
        ${ROCKETMQ_LIBRARY_DIRS}
        )
message(status**** "rocketmq libaray: ${ROCKETMQ_LIBRARIES}")

IF (ROCKETMQ_LIBRARIES AND ROCKETMQ_INCLUDE_DIRS)
    SET(ROCKETMQ_LIBRARIES ${ROCKETMQ_LIBRARIES})
    SET(ROCKETMQ_FOUND "YES")
    message(status "Find library: rocketmq")
ELSE (ROCKETMQ_LIBRARIES AND ROCKETMQ_INCLUDE_DIRS)
    SET(ROCKETMQ_FOUND "NO")
    message(FATAL_ERROR "Missing library: rocketmq")
ENDIF (ROCKETMQ_LIBRARIES AND ROCKETMQ_INCLUDE_DIRS)


IF (ROCKETMQ_FOUND)
    IF (NOT ROCKETMQ_FIND_QUIETLY)
        MESSAGE(STATUS "Found Rocketmq: ${ROCKETMQ_LIBRARIES}")
    ENDIF (NOT ROCKETMQ_FIND_QUIETLY)
ELSE (ROCKETMQ_FOUND)
    IF (ROCKETMQ_FIND_REQUIRED)
        MESSAGE(FATAL_ERROR "Could not find ROCKETMQ library include: ${ROCKETMQ_INCLUDE_DIRS}, lib: ${ROCKETMQ_LIBRARIES}")
    ENDIF (ROCKETMQ_FIND_REQUIRED)
ENDIF (ROCKETMQ_FOUND)

MARK_AS_ADVANCED(
        ROCKETMQ_LIBRARIES
        ROCKETMQ_INCLUDE_DIRS
)

# Restore the original find library ordering
if (ROCKETMQ_USE_STATIC_LIBS)
    set(CMAKE_FIND_LIBRARY_SUFFIXES ${_rocketmq_ORIG_CMAKE_FIND_LIBRARY_SUFFIXES})
else ()
    set(CMAKE_FIND_LIBRARY_SUFFIXES ${_rocketmq_ORIG_CMAKE_FIND_LIBRARY_SUFFIXES})
endif ()
