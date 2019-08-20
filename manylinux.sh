#!/bin/bash

yum install -y wget curl gcc libtool unzip automake autoconf bzip2-devel

ln -s `which cmake28` /usr/bin/cmake

# Install zlib
curl -sqL https://zlib.net/zlib-1.2.11.tar.gz | tar -xz -C /tmp
cd /tmp/zlib-1.2.11/ && ./configure --prefix=/usr && make && make install && cd -

# Build rocketmq-client-cpp
git clone --depth=1 --branch=rocketmq-python-0.4.0 https://github.com/messense/rocketmq-client-cpp.git /tmp/rocketmq-client-cpp
mkdir -p /tmp/rocketmq-client-cpp/tmp_down_dir
curl -sqL -o /tmp/rocketmq-client-cpp/tmp_down_dir/libevent-release-2.1.8-stable.zip https://github.com/libevent/libevent/archive/release-2.1.8-stable.zip
curl -sqL -o /tmp/rocketmq-client-cpp/tmp_down_dir/jsoncpp-0.10.7.zip https://github.com/open-source-parsers/jsoncpp/archive/0.10.7.zip
curl -sqL -o /tmp/rocketmq-client-cpp/tmp_down_dir/boost_1_58_0.tar.gz http://sourceforge.net/projects/boost/files/boost/1.58.0/boost_1_58_0.tar.gz
cd /tmp/rocketmq-client-cpp && bash build.sh && cd -
cp /tmp/rocketmq-client-cpp/bin/librocketmq.so /io/rocketmq/librocketmq.so

# Build wheels
which linux32 && LINUX32=linux32
$LINUX32 /opt/python/cp27-cp27mu/bin/python setup.py bdist_wheel

# Audit wheels
for wheel in dist/*-linux_*.whl; do
  auditwheel repair $wheel -w dist/
  rm $wheel
done
