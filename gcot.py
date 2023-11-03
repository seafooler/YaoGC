from utils import *
import Crypto
from Crypto.Util.number import *
BigPrime = 4776913109852041418248056622882488319

def OT_Enc(g, p, pk, s):
    print("s", s)
    r = randint(1, p-1)
    tmp = n2b(pow(g, r, p))
    # tmp2 = n2b(int.from_bytes(hash(n2b(pow(pk, r, p))), 'big') ^ int.from_bytes(s, 'big'))
    print('pow(pk, r, p):', pow(pk, r, p))
    print('hash(n2b(pow(pk, r, p))):', hash(n2b(pow(pk, r, p))))
    print('int.from_bytes(hash(n2b(pow(pk, r, p)), big', int.from_bytes(hash(n2b(pow(pk, r, p))), 'big'))
    # print('hash(pow(pk, r, p)):', hash(pow(pk, r, p)))

    tmp3 = n2b(int.from_bytes(hash(n2b(pow(pk, r, p))), 'big') ^ int.from_bytes(s, 'big'))

    print('tmp3:', tmp3)

    tmp2 = n2b(bytes_to_long(hash(n2b(pow(pk, r, p)))) ^ bytes_to_long(s))

    print('tmp2:', tmp2)

    return tmp+b'-'+tmp3

def OT_Sender(message, receiver):
    try:
        receiver.send(b'n132-OT2')
        data = receiver.recv(1024)
        p, g = data.split(b'-')
        p = int(p)
        g = int(g)
        c = randint(1, p-1)
        receiver.send(n2b(c))
        data = receiver.recv(1024)
        pks = data.split(b'-')
        pks[0] = int(pks[0])
        pks[1] = int(pks[1])
        assert(c == (pks[0] * pks[1]) % p)
        sec = message
        data = b''
        data += OT_Enc(g, p, pks[0], sec[0])
        data += b'-'
        data += OT_Enc(g, p, pks[1], sec[1])
        receiver.send(data)
        return 1
    except:
        return 0
    

def OT_Receiver(choice, sender):
    m = sender.recv(8)
    if(m==b'n132-OT2'):
        GC = CyclicGroup(BigPrime)
        g = GC.generator
        data = n2b(BigPrime)+b"-"+n2b(g)
        sender.send(data)
        c = int(sender.recv(1024))
        k = GC.rand_int()
        pks = [0, 0]
        b = choice
        pks[b] = GC.pow(g, k)
        pks[1-b] = GC.div(c, pks[b])

        sender.send(pack(pks))
        data = sender.recv(1024).split(b'-')
        b = b*2
        u = int(data[b])
        v = int(data[b+1])

        print('before hash pow')
        tmp1 = hash(n2b(pow(u, k, int(BigPrime))))
        print('int.from_bytes(tmp1, big):', int.from_bytes(tmp1, 'big'))
        print('bytes_to_long(tmp1):', bytes_to_long(tmp1))
        # res = n2b(int.from_bytes(tmp1, 'big') ^ v)
        # res = long_to_bytes( bytes_to_long(tmp1) ^ v )
        print('long_to_bytes:', long_to_bytes( int.from_bytes(tmp1, 'big') ^ v))
        # print('n2b:', int.to_bytes( int.from_bytes(tmp1, 'big') ^ v, 8, 'big'))
        res =  long_to_bytes( int.from_bytes(tmp1, 'big') ^ v)
        return res
    else:
        return -1
