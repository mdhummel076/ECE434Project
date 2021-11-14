#!/usr/bin/env python3

import Adafruit_BBIO.PWM as PWM
import time
import rospy
from std_msgs.msg import Float32MultiArray

pin1="P9_14"
pin2="P9_21"

PWM.start(pin1, 50)
PWM.start(pin2, 50)

rospy.loginfo("Started")

def callback(cmd):
	if len(cmd.data) > 0:
		PWM.set_duty_cycle(pin1, cmd.data[0]*50+50)
		PWM.set_duty_cycle(pin2, cmd.data[1]*50+50)
		rospy.loginfo("Speed 1: "+str(cmd.data[0]*50+50)+" Speed 2: "+str(cmd.data[1]*50+50))
	else:
		PWM.set_duty_cycle(pin1, 50)
		PWM.set_duty_cycle(pin2, 50)

rospy.init_node("Motors", anonymous=True)

rospy.Subscriber("Commands", Float32MultiArray, callback)

try:
	while not rospy.is_shutdown():
		time.sleep(0.01)

except KeyboardInterrupt:
	rospy.loginfo("Shutting Down")
	PWM.cleanup()
PWM.cleanup()


