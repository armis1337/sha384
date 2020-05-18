import sys
import math

# SHA 256

h = [None] * 8
h = [0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a, 0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19]

k = [None] * 64
k = [0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
   0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
   0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
   0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
   0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
   0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
   0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
   0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2]

a = ""
b = ""
c = ""
d = ""
e = ""
f = ""
g = ""
hh = ""

def main():
    if len(sys.argv) == 1:
        print('Iveskite failo pavadinima')
        return
    message = read(sys.argv[1])
    x = pad(message)
    x = parse(x)
    x = hash(x)
    print(x)

def read(file = 'test.txt'):
    f = open(file, 'rb')
    return f.read()

def pad(message):    
    newmsg = ""
    k = 0
    if type(message) is bytes:
        # 0000 0000 - formato pakeitimas i bitus
        for byte in message:
            newmsg += '{0:08b}'.format(byte)
        return pad(newmsg)
    else:
        newmsg = message
        k = math.ceil(len(newmsg) / 512)
        lastblocksize = len(newmsg) - 512 * (k - 1)
        l = '{0:064b}'.format(int(len(newmsg)))
        if lastblocksize < 448:
            newmsg += '1'
            for i in range(447 - lastblocksize):
                newmsg += '0'
            newmsg += l
        else:
            newmsg += '1'
            for i in range((k+1) * 512 - len(newmsg) - 64):
                newmsg += '0'
            newmsg += l
        return newmsg

def parse(message):
    if len(message)%512 != 0:
        return

    m = [None] * int(len(message) / 512)
    for i in range(int(len(message) / 512)):
        block = message[i*512: (i+1)*512]
        m[i] = [None] * 16
        for j in range(16):
            m[i][j] = block[j*32: (j+1)*32]
    return m

def ch(x, y, z):
    return (x & y) ^ (~x & z)

def maj(x, y, z):
    return (x & y) ^ (x & z) ^ (y & z)

def rotR(x, n):
    mask = int('11111111111111111111111111111111', 2) # not x = x^mask
    return (x >> n) | ((x << (32 - n)) & mask)

def complement(x):
    x =  str(x)
    res = ""
    for i in x:
        if i == '0':
            res += '1'
        else:
            res += '0'
    return int(res, 2)

def sum0(x):
    return rotR(x, 2) ^ rotR(x, 13) ^ rotR(x, 22)

def sum1(x):
    return rotR(x, 6) ^ rotR(x, 11) ^ rotR(x, 25)

def sigma0(x):
    return rotR(x, 7) ^ rotR(x, 18) ^ (x >> 3)

def sigma1(x):
    return rotR(x, 17) ^ rotR(x, 19) ^ (x >> 10)

def addMod32(x, y):
    if (x + y > 4294967296): # 2^32
        return(addMod32(x - 4294967296, y))
    else:
        return x + y
    return (x+y) % int(math.pow(2, 32))

def hash(message):
    for i in range(len(message)):
        w = [None] * 64
        for j in range(64):
            if j < 16:
                w[j] = int(message[i][j], 2)
            else:
                w[j] = addMod32(
                    addMod32(sigma1(w[j-2]), w[j-7]), 
                    addMod32(sigma0(w[j-15]), w[j-16])
                    )
        a = h[0]
        b = h[1]
        c = h[2]
        d = h[3]
        e = h[4]
        f = h[5]
        g = h[6]
        hh = h[7]
        
        for t in range(64):
            T1 = addMod32(
                addMod32(
                addMod32(hh, sum1(e)), 
                addMod32(ch(e, f, g), k[t])
                ), w[t])
            T1 = (hh + sum1(e) + ch(e, f, g) + k[t] + w[t]) % int(math.pow(2, 32))
            T2 = (sum0(a) + maj(a, b, c)) % int(math.pow(2, 32))
            hh = g
            g = f
            f = e
            e = addMod32(d, T1)
            d = c
            c = b
            b = a
            a = addMod32(T1, T2)

        h[0] = addMod32(a, h[0])
        h[1] = addMod32(b, h[1])
        h[2] = addMod32(c, h[2])
        h[3] = addMod32(d, h[3])
        h[4] = addMod32(e, h[4])
        h[5] = addMod32(f, h[5])
        h[6] = addMod32(g, h[6])
        h[7] = addMod32(hh, h[7])

    rez = '0x'
    for i in h:
        rez += hex(i)[2:]
    return rez
    
    
if __name__ == "__main__":
    main()