import zmq
import struct

ctx = zmq.Context()
sock = ctx.socket(zmq.SUB)
sock.connect('tcp://127.0.0.1:55114')
sock.setsockopt_string(zmq.SUBSCRIBE,'')

while(1):
    msgs = sock.recv_multipart()
    pos = msgs[:3]
    rot = msgs[3:]
    pos = [struct.unpack('f',d)[0] for d in pos]
    rot = [struct.unpack('f',d)[0] for d in rot]
    print("Pos: %f %f %f"%(pos[0],pos[1],pos[2]))
    print("Rot: %f %f %f %f"%(rot[0],rot[1],rot[2],rot[3]))
