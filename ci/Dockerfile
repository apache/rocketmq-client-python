#
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
FROM quay.io/pypa/manylinux1_x86_64:latest

RUN yum install -y wget curl gcc libtool unzip automake autoconf bzip2-devel && ln -s `which cmake28` /usr/bin/cmake

# Install zlib
RUN curl -sqL https://zlib.net/zlib-1.2.11.tar.gz | tar -xz -C /tmp && \
  cd /tmp/zlib-1.2.11/ && \
  ./configure --prefix=/usr && \
  make && \
  make install && \
  cd -  && \
  rm -rf /tmp/zlib-1.2.11

# Build rocketmq-client-cpp
RUN git clone --depth=1 --branch=master https://github.com/apache/rocketmq-client-cpp.git /tmp/rocketmq-client-cpp && \
  mkdir -p /tmp/rocketmq-client-cpp/tmp_down_dir && \
  curl -sqL -o /tmp/rocketmq-client-cpp/tmp_down_dir/libevent-release-2.1.8-stable.zip https://github.com/libevent/libevent/archive/release-2.1.8-stable.zip  && \
  curl -sqL -o /tmp/rocketmq-client-cpp/tmp_down_dir/jsoncpp-0.10.7.zip https://github.com/open-source-parsers/jsoncpp/archive/0.10.7.zip && \
  curl -sqL -o /tmp/rocketmq-client-cpp/tmp_down_dir/boost_1_58_0.tar.gz http://sourceforge.net/projects/boost/files/boost/1.58.0/boost_1_58_0.tar.gz && \
  cd /tmp/rocketmq-client-cpp && bash build.sh && cd - && \
  cp /tmp/rocketmq-client-cpp/bin/librocketmq.so /usr/local/lib/librocketmq.so && \
  rm -rf /tmp/rocketmq-client-cpp
