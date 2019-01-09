# /*
# * Licensed to the Apache Software Foundation (ASF) under one or more
# * contributor license agreements.  See the NOTICE file distributed with
# * this work for additional information regarding copyright ownership.
# * The ASF licenses this file to You under the Apache License, Version 2.0
# * (the "License"); you may not use this file except in compliance with
# * the License.  You may obtain a copy of the License at
# *
# *     http://www.apache.org/licenses/LICENSE-2.0
# *
# * Unless required by applicable law or agreed to in writing, software
# * distributed under the License is distributed on an "AS IS" BASIS,
# * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# * See the License for the specific language governing permissions and
# * limitations under the License.
# */

from distutils.core import Extension

from setuptools import setup

BOOST_INCLUDE_PATH = "/usr/local/include/boost"
PYTHON_INCLUDE_PATH = "/usr/include/python2.7"
ROCKETMQ_INCLUDE_PATH = "/usr/local/include/rocketmq"
PYTHON_LIB_DIR = "/usr/lib64"
BOOST_LIB_DIR = "/usr/local/lib"
ROCKETMQ_LIB_DIR = "/usr/local/lib"
NAME = 'librocketmqclientpython'
setup(name=NAME,
      version='1.2.0',
      url="https://github.com/apache/rocketmq-client-python",
      description="RocketMQ Python client",
      long_description="RocketMQ Python client is developed on top of rocketmq-client-cpp, which has been proven "
                       "robust and widely adopted within Alibaba Group by many business units for more than three "
                       "years.",
      license="Apache License, Version 2.0",
      platforms=["linux"],
      packages=["src"],
      ext_modules=[Extension(name=NAME
                             , sources=['src/PythonWrapper.cpp']
                             , extra_compile_args=[]
                             , extra_link_args=["-lboost_python", "-lrocketmq"]
                             , include_dirs=[BOOST_INCLUDE_PATH, ROCKETMQ_INCLUDE_PATH]
                             , library_dirs=[PYTHON_LIB_DIR, ROCKETMQ_LIB_DIR, BOOST_LIB_DIR]
                             ), ],
      )
