#!/bin/bash

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

VERSION=1.8.1
PACKAGENAME=release-${VERSION}
GTEST=googletest-release-${VERSION}
release-1.8.1.tar.gz

if [ ! -d ${HOME}/${GTEST} ]; then
    if [ -e ${HOME}/${GTEST}.tar.gz ]; then
        echo "Find Packge ${HOME}/${GTEST}.tar.gz......."
    else    
        wget -O ${HOME}/${GTEST}.tar.gz https://github.com/abseil/googletest/archive/${PACKAGENAME}.tar.gz
    fi
    if [ $? -ne 0 ];then
        exit 1
    fi
    tar -xzf ${HOME}/${GTEST}.tar.gz -C ${HOME}
    if [ $? -ne 0 ];then
        exit 1
    fi
else
    echo "Find GTest Source:${HOME}/${GTEST}, Build and install....."
fi

cd ${HOME}/${GTEST}

mkdir build; cd build
echo "Start build google test"
    cmake .. -DCMAKE_CXX_FLAGS=-fPIC -DBUILD_STATIC_LIBS=ON -DBUILD_SHARED_LIBS=OFF
    if [ $? -ne 0 ];then
        exit 1
    fi
    make
    if [ $? -ne 0 ];then
        exit 1
    fi
    make install

    if [ ! -f /usr/local/lib/libgtest.a ]
    then
        echo "#######Error: Install gtest failed.#########"
        exit 1
    fi

echo "Finish build gtest library."
