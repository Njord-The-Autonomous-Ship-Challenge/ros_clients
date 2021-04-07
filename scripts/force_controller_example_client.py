#!/usr/bin/env python2

import rospy
from std_msgs.msg import String

import grpc

from force_control import force_control_pb2
from force_control import force_control_pb2_grpc

from ros_clients.msg import GeneralizedForce

force_control_channel = 0
force_control_stub = 0

def callback(force):

    grpc_force = force_control_pb2.GeneralizedForce(
        x = force.x,
        y = force.y,
        z = force.z,
        k = force.k,
        m = force.m,
        n = force.n,
    )
        
    success = force_control_stub.ApplyForce(
            force_control_pb2.ForceRequest(vesselId = "Milliampere", 
            generalizedForce = grpc_force
    ))



def listener():

    rospy.Subscriber("force_control", GeneralizedForce, callback)

    rospy.spin()



if __name__ == '__main__':
    rospy.init_node('listener', anonymous=True)
    server_params = rospy.get_param('~')
    server_ip = server_params["server_ip"]
    server_port = server_params["server_port"]
    
    force_control_channel = grpc.insecure_channel(server_ip + ':' + str(server_port))
    force_control_stub = force_control_pb2_grpc.ForceControlStub(force_control_channel)
        
    listener()
    
