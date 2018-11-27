#!/bin/sh

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

function Help()
{
    echo "=========================================Package============================================"
    echo "sh package.sh [shared]"
    echo "usage: sh package.sh shared"
    echo "shared: build python client by dynamic boost python and rocketmq library"
    echo "default: build python client by static boost python and rocketmq library"
    echo "=========================================Package============================================"
    echo ""
}

if [ $# -gt 0 ];then
    if [ "$1" != "shared" ];then
        #echo "unsupport para value $1, please see the help"
        Help
        exit 1
    fi
fi

PACKAGE="rocketmq-client-python"
VERSION=$(cat src/PythonWrapper.h | grep PYTHON_CLIENT_VERSION | cut -f2 -d"\"")
CWD_DIR=$(cd "$(dirname "$0")"; pwd)
DEPLOY_BUILD_HOME=${CWD_DIR}/${PACKAGE}

# ##====================================================================
#make
rm -rf ${CWD_DIR}/tmpbuild
mkdir -p ${CWD_DIR}/tmpbuild
cd ${CWD_DIR}/tmpbuild
if [ $1 = "shared" ]; then
    echo "------------Build Client using dynamic library------------"
    cmake ${CWD_DIR} -DBoost_USE_STATIC_LIBS=OFF -DROCKETMQ_USE_STATIC_LIBS=OFF
    RMQ=$(cat CMakeCache.txt | grep ROCKETMQ_LIBRARIES:FILEPATH= | cut -f2 -d "=")
    echo "Rocketmq Library:${RMQ}"
else
    echo "-------------Build Client using static library-------------"
    cmake ${CWD_DIR} -DBoost_USE_STATIC_LIBS=ON -DROCKETMQ_USE_STATIC_LIBS=ON
fi
if [ $? -ne 0 ];then
        exit 1
fi
make
if [ $? -ne 0 ];then
        exit 1
fi
cd ${CWD_DIR}
# ##====================================================================
# # deploy
echo "Package Library...."
rm -rf   ${DEPLOY_BUILD_HOME}
mkdir -p ${DEPLOY_BUILD_HOME}/lib
if [ $1 = "shared" ];then
    echo "Copy librocketmq to package...."
    cp -rf ${RMQ} ${DEPLOY_BUILD_HOME}/lib/
    #cp -rf /usr/local/lib/libboost_python.*.so.* ${DEPLOY_BUILD_HOME}/lib/
fi
cp -rf ${CWD_DIR}/bin/*.so  ${DEPLOY_BUILD_HOME}/lib/
cp -rf ${CWD_DIR}/sample ${DEPLOY_BUILD_HOME}/
cp -rf ${CWD_DIR}/doc 	  ${DEPLOY_BUILD_HOME}/
cp -rf ${CWD_DIR}/changelog  ${DEPLOY_BUILD_HOME}/


cd ${CWD_DIR} && tar -cvzf ./${PACKAGE}-${VERSION}.tar.gz ./${VERSION}  >/dev/null 2>&1
rm -rf ${DEPLOY_BUILD_HOME}
# # ##====================================================================
cd ${CWD_DIR}/tmpbuild
make clean
cd ${CWD_DIR}
rm -rf ${CWD_DIR}/tmpbuild
