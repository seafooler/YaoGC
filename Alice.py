import json
from cgarble import *
from random import randint
from utils import *
import pickle
import gcot


def multiintest():
    with open('./equal8.json') as f:
        data = f.read()

    cinfo = json.loads(data) 
    lb = iLabel(cinfo) # assign keys to each wire
    gc, rmap = gGarble(cinfo, lb)

    araw = [randint(0, 1) for i in range(len(cinfo["a_inputs"]))]
    ains = ['' for i in range(len(araw))]
    for i in range(len(araw)):
        ains[i] = lb[cinfo["a_inputs"][i]][araw[i]]
    ginfo = {
        "gc": gc,
        "cinfo": cinfo,
        "inputs": ains,
        "rmap": rmap,
        "raw_ins": araw,
    }    

    s = connect()
    s.sendall(pickle.dumps(ginfo))

    OTDone = False
    innum = 0
    b_secrets = {}
    for _ in cinfo["b_inputs"]:
        b_secrets[innum] = lb[cinfo["b_inputs"][innum]]
        innum += 1
    innum = 0

    print("b_secrets", b_secrets)
    msg = s.recv(256)
    while(not OTDone):
        print("secrets to send:", b_secrets[innum])
        otres = gcot.OT_Sender(b_secrets[innum], s)
        print("ot ended with", otres)
        if(otres == 1):
            innum += 1
        bres = s.recv(256)
        if(bres == b'ins-done'):
            OTDone = True


if (__name__ == "__main__"):
    totalcon = 0.0
    multiintest()
