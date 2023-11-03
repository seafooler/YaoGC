from cryptography.fernet import Fernet


SWITCH = {
    "AND": lambda x, y: x and y,
    "OR": lambda x, y: x or y,
    "XOR": lambda x, y: x ^ y,
    "NOT": lambda x: not x,
    "NAND": lambda x, y: not (x and y),
    "NOR": lambda x, y: not (x or y),
    "XNOR": lambda x, y: not (x ^ y),
}

def encrypt(key, data):
    return Fernet(key).encrypt(data)

def decrypt(key, data):
    return Fernet(key).decrypt(data)

def genkey():
    return Fernet.generate_key()

def iLabel(cinfo):
    gates = cinfo["gates"]
    a_inputs = cinfo["a_inputs"]
    b_inputs = cinfo["b_inputs"]
    total_num = len(gates) + len(a_inputs) + len(b_inputs)
    res = []

    for _ in range(total_num):
        res.append({0: genkey(), 1: genkey()})
    return res

def gGarble(cinfo, labels):
    gates = cinfo["gates"]
    gc = []

    for g in gates:
        gate = {}
        res = []
        logic = SWITCH[g["type"]]
        if(g["type"] == "NOT"):
            for i in range(2):
                g_out = logic(i)
                assert(g_out == 0 or g_out == 1)
                raw_label = labels[g["output"][0]][g_out]
                k0 = labels[g["input"][0]][i]

                tmp = encrypt(k0, raw_label)
                res.append(tmp)
        else:
            for i in range(2):
                for j in range(2):
                    g_out = logic(i, j)
                    assert(g_out == 0 or g_out == 1)
                    raw_label = labels[g["output"][0]][g_out]
                    k0 = labels[g["input"][0]][i]
                    k1 = labels[g["input"][1]][j]

                    tmp = encrypt(k1, encrypt(k0, raw_label))
                    res.append(tmp)
        gate["id"] = g["id"]
        gate["garbledResult"] = res
        gc.append(gate)
    
    rmap = {
        0: labels[cinfo["output"][0]][0],
        1: labels[cinfo["output"][0]][1]
    }

    return gc, rmap

def ggEval(w1, w2, table):
    for v in table:
        try:
            if(w2):
                res = decrypt(w1, decrypt(w2, v))
                if(res):
                    return res
            else:
                res = decrypt(w1, v)
                if(res):
                    return res
        except Exception:
            pass

    print("gate eval failure")
    exit(1)

def gcEval(gc, inputs, cinfo, rmap):
    assert(len(inputs) == len(cinfo["a_inputs"])+len(cinfo["b_inputs"]))
    inputs += [0] * (cinfo["output"][0]-len(inputs)+1)

    for g in gc:
        gateInfo = cinfo["gates"][g["id"]]
        gatetype = gateInfo["type"]

        wire1 = inputs[gateInfo["input"][0]]
        if (gatetype == "NOT"):
            wire2 = None
        else:
            wire2 = inputs[gateInfo["input"][1]]

        output_idx = gateInfo["output"][0]
        res =ggEval(wire1, wire2, g["garbledResult"])
        inputs[output_idx] = res
    
    if(rmap[0] == inputs[cinfo["output"][0]]):
        return 0
    else:
        return 1