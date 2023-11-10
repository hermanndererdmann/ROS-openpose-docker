# ROS-openpose-docker
![Docker Pulls](https://img.shields.io/docker/pulls/hermanndererdmann/ros-openpose-docker)

containerized person recognition with openpose in ROS.

## Requirements
- Docker
- NVIDIA GPU
- ≈ 20GB of free space

## Getting started
This image can be pulled from DockerHub but it also can be build locally.
### Build Docker Image
This step can be skipped if the image is downloaded.

Navigate to the cloned repository and run

```
docker build -t ros-openpose-docker .
```
after this the image is build and saved on the drive.

### Run Docker Image
```
xhost +local:root; docker run -ti --rm  --gpus all --net=host -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix:rw ros-openpose-docker
```

With each start of the container, the hostname & IP of the ROS slave have to be added to the ects/hosts file with `nano`. Both IP addresses should be static.

In my example this is:
```
10.0.106.30 rosberry
```
After this we can start the `roscore`.


### Starting Openpose
To start Openpose or other services in the container we need to open a new terminal. To get into the running Docker Container use:
```
docker exec -it <YOUR-BUILT-CONTAINER-NAME> bash
```

Navigate to `/openpose/build/examples/tutorial_api_python` and start `ros_openpose.py`



