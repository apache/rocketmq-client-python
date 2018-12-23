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
VERSION=1.58.0
BOOST=boost_1_58_0

if [ ! -d ${HOME}/${BOOST} ]; then
    if [ -e ${HOME}/${BOOST}.tar.gz ]; then
        echo "Find Packge ${HOME}/${BOOST}.tar.gz......."
    else    
        wget -O ${HOME}/${BOOST}.tar.gz http://sourceforge.net/projects/boost/files/boost/${VERSION}/${BOOST}.tar.gz
    fi
    if [ $? -ne 0 ];then
        exit 1
    fi
    tar -xzf ${HOME}/${BOOST}.tar.gz -C ${HOME}
    if [ $? -ne 0 ];then
        exit 1
    fi
else
    echo "Find Boost Source:${HOME}/${BOOST}, Build and install....."
fi

cd ${HOME}/${BOOST}

./bootstrap.sh --prefix=/usr/local --with-libraries=python
if [ $? -ne 0 ];then
    exit 1
fi
echo "Install boost static library...."
sudo   ./b2 cflags="-fPIC" cxxflags="-fPIC -Wno-unused-local-typedefs -Wno-strict-aliasing" link=static \
       runtime-link=static --with-python  \
       -a install 
if [ $? -ne 0 ];then
    exit 1
fi
echo "Install boost dynamic library....."
sudo   ./b2 cflags="-fPIC" cxxflags="-fPIC -Wno-unused-local-typedefs -Wno-strict-aliasing" link=shared \
       runtime-link=shared --with-python \
       -a install
if [ $? -ne 0 ];then
    exit 1
fi
echo "Finish build boost library."
