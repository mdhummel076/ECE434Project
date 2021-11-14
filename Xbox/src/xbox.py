#!/usr/bin/env python3
# license removed for brevity
import rospy
from std_msgs.msg import Float32MultiArray
from std_msgs.msg import Float32
import time
from xbox360controller import Xbox360Controller
import numpy

import time,threading
import string

val1 = 0
val2 = 0
val3 = 0
val4 = 0
val5 = 0

def parse():
    pub = rospy.Publisher('Commands', Float32MultiArray, queue_size=10)
    gripperPub = rospy.Publisher('armGripper', Float32)
    rospy.init_node('armControl', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    
    try:
        with Xbox360Controller(0, axis_threshold=0.05) as controller: #might need to change the 1 to a 0 depending on the controller
            while not rospy.is_shutdown():
                val1 = controller.axis_l.x*0.2
                val2 = controller.axis_l.y
                val3 = controller.axis_r.y
                val4 = controller.axis_r.x
                val5 = (controller.trigger_l.value - controller.trigger_r.value)*0.1

                gripperCommand = 0
                if controller.button_a.is_pressed:
                    gripperCommand += 1
                elif controller.button_b.is_pressed:
                    gripperCommand -= 1
                gripperMsg = Float32()
                gripperMsg.data = gripperCommand
                gripperPub.publish(gripperMsg)

                rospy.loginfo_throttle(0.25, "1: "+str(val1)+"2: "+str(val2)+"3: "+str(val3)+"4: "+str(val4)+"5: "+str(val5))

                pub.publish(Float32MultiArray(data=[val1,val2,val3,val4,val5]))

                rate.sleep()

    except Exception as e:
        rospy.loginfo_throttle(0.25, "Error: "+str(e))
        pub.publish(Float32MultiArray(data=[0,0,0,0,0]))

try:
        parse()
except rospy.ROSInterruptException:
        pass
