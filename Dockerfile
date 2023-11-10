FROM nvidia/cuda:11.7.1-cudnn8-devel-ubuntu20.04

#get deps
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update && \
        apt-get install -y --no-install-recommends \
        python3-dev python3-pip git g++ wget make libprotobuf-dev protobuf-compiler libopencv-dev \
        libgoogle-glog-dev libboost-all-dev caffe-cpu libhdf5-dev libatlas-base-dev \
        python3-setuptools vim libgtk2.0-dev libgtk-3-dev locales lsb-release unzip nano iputils-ping

RUN dpkg-reconfigure locales


#for python api
RUN pip3 install --upgrade pip
RUN pip3 install numpy opencv-python
#google drive downloader
RUN pip3 install gdown

#replace cmake as old version has CUDA variable bugs
RUN wget https://github.com/Kitware/CMake/releases/download/v3.16.0/cmake-3.16.0-Linux-x86_64.tar.gz && \
tar xzf cmake-3.16.0-Linux-x86_64.tar.gz -C /opt && \
rm cmake-3.16.0-Linux-x86_64.tar.gz
ENV PATH="/opt/cmake-3.16.0-Linux-x86_64/bin:${PATH}"

#install ROS noetic
WORKDIR /ROS
RUN sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list'
RUN apt-key adv --keyserver 'hkp://keyserver.ubuntu.com:80' --recv-key C1CF6E31E6BADE8868B172B4F42ED6FBAB17C654
RUN apt-get update \
 && apt-get install -y --no-install-recommends ros-noetic-desktop-full
RUN apt-get install -y --no-install-recommends python3-rosdep
RUN rosdep init \
 && rosdep fix-permissions \
 && rosdep update
RUN echo "source /opt/ros/noetic/setup.bash" >> ~/.bashrc



#get openpose
WORKDIR /openpose
RUN git clone https://github.com/CMU-Perceptual-Computing-Lab/openpose.git .
#get models from alternative source since official server was down
WORKDIR /deleteme
RUN gdown 1QCSxJZpnWvM00hx49CJ2zky7PWGzpcEh
RUN unzip models.zip
RUN cp -r /deleteme/models /openpose
RUN rm -r /deleteme/models
#add ros openpose script
COPY /src /openpose/examples/tutorial_api_python



#build openpose
WORKDIR /openpose/build
RUN cmake -DBUILD_PYTHON=ON .. && make -j `nproc`
WORKDIR /openpose
