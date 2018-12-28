import time
import zmq
# import numpy as np #for random data generator
import json

ctx = zmq.Context()
sock = ctx.socket(zmq.PUB)

sock.bind('tcp://127.0.0.1:55115')

hip_pos = [0.1,0.1,0.1]
hip_rot = [0.2,0.2,0.2,0.2]
lleg_pos = [0.3,0.3,0.3]
lleg_rot = [0.4,0.4,0.4,0.4]
rleg_pos = [0.5,0.5,0.5]
rleg_rot = [0.6,0.6,0.6,0.6]
data = [hip_pos, hip_rot, lleg_pos, lleg_rot, rleg_pos, rleg_rot]
data = [d for sbj in data for d in sbj]

while(1):
    time.sleep(1.0)
    # data = np.random.rand(21)
    sock.send_json(list(data))
