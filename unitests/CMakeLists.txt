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
project(UnitTest)
if (WIN32)
    find_package(gtest)
elseif (APPLE)
    find_package(gtest)
else ()
    set(GTEST_INCLUDE_DIRS /usr/local/include)
    set(GTEST_LIBRARY_DIRS /usr/local/lib)
    set(GTEST_LIBRARIES /usr/local/lib/libgtest.a)
    set(GTEST_FOUND true)
endif (WIN32)

if (GTEST_FOUND)
    message(STATUS "** GTEST Include dir: ${GTEST_INCLUDE_DIRS}")
    message(STATUS "** GTEST Libraries dir: ${GTEST_LIBRARY_DIRS}")
    message(STATUS "** GTEST Libraries: ${GTEST_LIBRARIES}")
    include_directories(${GTEST_INCLUDE_DIRS})
else ()
    message(FATAL_ERROR "Missing library: gtest ")
endif ()
file(GLOB_RECURSE SRC_FILES ${CMAKE_SOURCE_DIR}/src/*.cpp)
file(GLOB_RECURSE TEST_SRC_FILES ${CMAKE_SOURCE_DIR}/unitests/*.cpp)

# subdirs
SET(SUB_DIRS)
file(GLOB children ${CMAKE_SOURCE_DIR}/src/*.h)
FOREACH (child ${children})
    IF (IS_DIRECTORY ${child})
        LIST(APPEND SUB_DIRS ${child})
    ENDIF ()
ENDFOREACH ()
LIST(APPEND SUB_DIRS ${CMAKE_SOURCE_DIR}/src)
include_directories(${CMAKE_SOURCE_DIR}/include)
include_directories(${SUB_DIRS})

message(STATUS "All Source File" ${SRC_FILES})
message(STATUS "All Test Source File" ${TEST_SRC_FILES})
#message(STATUS "All Head File Dir" ${SUB_DIRS})
add_executable(runUnitTests
        ${TEST_SRC_FILES}
        ${SRC_FILES}
        )

target_link_libraries(runUnitTests
        dl
        ${ROCKETMQ_LIBRARIES}
        ${Boost_LIBRARIES}
        ${PYTHON_LIBRARIES}
        ${GTEST_LIBRARIES})

if (UNIX AND NOT APPLE)
    target_link_libraries(runUnitTests rt)
endif ()

set_target_properties(runUnitTests PROPERTIES
        RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR})
add_test(runUnitTests ${CMAKE_BINARY_DIR}/runUnitTests)
