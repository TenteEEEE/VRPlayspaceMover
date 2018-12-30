import zmq
import struct
import numpy as np
from threading import Thread

# It relates with your height and camera position, please adjust it
pixel2m = 0.0035

ctx = zmq.Context()

sub_tracker = ctx.socket(zmq.SUB)
sub_tracker.connect('tcp://127.0.0.1:55113')
sub_tracker.setsockopt_string(zmq.SUBSCRIBE,'')

sub_hmd = ctx.socket(zmq.SUB)
sub_hmd.connect('tcp://127.0.0.1:55114')
sub_hmd.setsockopt_string(zmq.SUBSCRIBE,'')

pub_tracker = ctx.socket(zmq.PUB)
pub_tracker.bind('tcp://127.0.0.1:55115')

tracker_index = [0, -6, -5, -2, -1] # nose, lhip, rhip, lankle, rankle

def recv_tracker(sock, tracker_index):
    tracking = sock.recv_pyobj()
    if tracking['result'] != []:
        poses = tracking['result'][0]['keypoints'][tracker_index]
        return poses.numpy()
    else:
        return -1

def recv_hmd(sock):
    msgs = sock.recv_multipart()
    pos = msgs[:3]
    quat = msgs[3:]
    pos = [struct.unpack('f',d)[0] for d in pos]
    quat = [struct.unpack('f',d)[0] for d in quat]
    return pos, quat

def make_msg(poses,quats):
    hip = list((poses[0]+poses[1])/2)
    lankle = list(poses[2]) # LR are fliped in steam VR
    rankle = list(poses[3])
    data = [hip, quats[0], lankle, quats[1], rankle, quats[2]]
    data = [a for d in data for a in d]
    return data
    
poses_update = np.zeros((4,3))
while(1):
    poses = recv_tracker(sub_tracker, tracker_index)
    hmd = recv_hmd(sub_hmd)
    if isinstance(poses,int) is False:
        poses_dif = [np.append((poses[0]-p)*pixel2m,[0]) for p in poses[1:]]
        poses_update = [hmd[0]+p for p in poses_dif]
    quats_update = [hmd[1] for i in range(3)]
    msg = make_msg(poses_update, quats_update)
    pub_tracker.send_json(msg)
