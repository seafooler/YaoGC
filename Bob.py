from utils import *
import pickle
import gcot
import cgarble

def recvall(sock):
    BUFF_SIZE = 4096
    data = b''
    while True:
        part = sock.recv(BUFF_SIZE)
        data += part
        if len(part) < BUFF_SIZE:
            break
    return data


def cgarbletestb():
    with listen() as s:
        conn, addr = s.accept()
        with conn:
            a = recvall(conn)
            amsg = pickle.loads(a)

            b_in_raw = [randint(0,1) for i in range(len(amsg["cinfo"]["b_inputs"]))]
            b_ins = [''] * len(b_in_raw)
            conn.sendall(b'ready')
            ci = 0
            while(b_ins[ci] == ""):
                print("attempting ot", ci)
                res = gcot.OT_Receiver(b_in_raw[ci], conn)
                if (not res == -1):
                    b_ins[ci] = res
                print("received secret:", b_ins[ci])
                ci += 1
                if(ci < len(b_in_raw)):
                    conn.sendall(b'continue')
                else:
                    break
            conn.sendall(b"ins-done")
            print("b_ins", b_ins)

            final_inputs = amsg["inputs"] + b_ins
            gc = amsg["gc"]
            cinfo = amsg["cinfo"]
            rmap = amsg["rmap"]

            eval_result = cgarble.gcEval(gc, final_inputs, cinfo, rmap)
            print("RESULT:", eval_result)

            a_raw_inputs = amsg["raw_ins"]
            b_raw_inputs = b_in_raw
            raw_inputs = a_raw_inputs + b_raw_inputs
            print('raw_inputs', raw_inputs)
            expected = not (a_raw_inputs == b_raw_inputs)
            print("correct:", expected == eval_result)



if(__name__ == "__main__"):
    cgarbletestb()