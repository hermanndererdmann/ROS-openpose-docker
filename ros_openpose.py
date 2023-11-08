#!/usr/bin/env python3

import rospy
import cv2
import argparse
import os
import sys
import time
from sys import platform
from sensor_msgs.msg import Image
from cv_bridge import CvBridge




try:
    # Import Openpose (Windows/Ubuntu/OSX)
    dir_path = os.path.dirname(os.path.realpath(__file__))
    try:
        # Windows Import
        if platform == "win32":
            # Change these variables to point to the correct folder (Release/x64 etc.)
            sys.path.append(dir_path + '/../../python/openpose/Release');
            os.environ['PATH']  = os.environ['PATH'] + ';' + dir_path + '/../../x64/Release;' +  dir_path + '/../../bin;'
            import pyopenpose as op
        else:
            # Change these variables to point to the correct folder (Release/x64 etc.)
            sys.path.append('../../python');
            # If you run `make install` (default path is `/usr/local/python` for Ubuntu), you can also access the OpenPose/python module from there. This will install OpenPose and the python library at your desired installation path. Ensure that this is in your python path in order to use it.
            # sys.path.append('/usr/local/python')
            from openpose import pyopenpose as op
    except ImportError as e:
        print('Error: OpenPose library could not be found. Did you enable `BUILD_PYTHON` in CMake and have this Python script in the right folder?')
        raise e


    pub = None
    opWrapper = None
    


    def main():
        global pub
        global opWrapper
        rospy.init_node("openpose_node")
        image_topic = rospy.get_param("~image_topic", "/openpose/keypoints")


        rospy.Subscriber('camera/rgb/image_color', Image, openpose_callback)

        pub = rospy.Publisher('image_topic', Image, queue_size=10)
        
        # Custom Params
        params = dict()
        params["model_folder"] = "../../../models/"


        # Starting OpenPose
        opWrapper = op.WrapperPython()
        opWrapper.configure(params)
        opWrapper.start()


        rospy.spin()


    def openpose_callback(data):
        global pub
        global opWrapper
        image_out = Image()
        bridge_out = CvBridge()
        bridge_in = CvBridge()



        
        imageToProcess = bridge_in.imgmsg_to_cv2(data, desired_encoding = "passthrough")
        

        # Process Image
        datum = op.Datum()
        datum.cvInputData = imageToProcess
        opWrapper.emplaceAndPop(op.VectorDatum([datum]))

        
        
        cv2.imshow("OpenPose 1.7.0 - Tutorial Python API", datum.cvOutputData)
        cv2.waitKey(1)


        

        #img output prep
        image_out = bridge_out.cv2_to_imgmsg(datum.cvOutputData, encoding = "passthrough")
    

        #Publish the image with keypoints
        pub.publish(image_out)







        

    if __name__ == '__main__':
        main()
        
except Exception as e:
    print(e)
    sys.exit(-1)

