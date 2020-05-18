import sys
import math

# SHA 384

h = [None] * 8
h = [0xcbbb9d5dc1059ed8, 0x629a292a367cd507, 0x9159015a3070dd17, 0x152fecd8f70e5939, 
    0x67332667ffc00b31, 0x8eb44a8768581511, 0xdb0c2e0d64f98fa7, 0x47b5481dbefa4fa4]

k = [None] * 80
k = [0x428a2f98d728ae22, 0x7137449123ef65cd, 0xb5c0fbcfec4d3b2f, 0xe9b5dba58189dbbc, 0x3956c25bf348b538, 
    0x59f111f1b605d019, 0x923f82a4af194f9b, 0xab1c5ed5da6d8118, 0xd807aa98a3030242, 0x12835b0145706fbe, 
    0x243185be4ee4b28c, 0x550c7dc3d5ffb4e2, 0x72be5d74f27b896f, 0x80deb1fe3b1696b1, 0x9bdc06a725c71235, 
    0xc19bf174cf692694, 0xe49b69c19ef14ad2, 0xefbe4786384f25e3, 0x0fc19dc68b8cd5b5, 0x240ca1cc77ac9c65, 
    0x2de92c6f592b0275, 0x4a7484aa6ea6e483, 0x5cb0a9dcbd41fbd4, 0x76f988da831153b5, 0x983e5152ee66dfab, 
    0xa831c66d2db43210, 0xb00327c898fb213f, 0xbf597fc7beef0ee4, 0xc6e00bf33da88fc2, 0xd5a79147930aa725, 
    0x06ca6351e003826f, 0x142929670a0e6e70, 0x27b70a8546d22ffc, 0x2e1b21385c26c926, 0x4d2c6dfc5ac42aed, 
    0x53380d139d95b3df, 0x650a73548baf63de, 0x766a0abb3c77b2a8, 0x81c2c92e47edaee6, 0x92722c851482353b, 
    0xa2bfe8a14cf10364, 0xa81a664bbc423001, 0xc24b8b70d0f89791, 0xc76c51a30654be30, 0xd192e819d6ef5218, 
    0xd69906245565a910, 0xf40e35855771202a, 0x106aa07032bbd1b8, 0x19a4c116b8d2d0c8, 0x1e376c085141ab53, 
    0x2748774cdf8eeb99, 0x34b0bcb5e19b48a8, 0x391c0cb3c5c95a63, 0x4ed8aa4ae3418acb, 0x5b9cca4f7763e373, 
    0x682e6ff3d6b2b8a3, 0x748f82ee5defb2fc, 0x78a5636f43172f60, 0x84c87814a1f0ab72, 0x8cc702081a6439ec, 
    0x90befffa23631e28, 0xa4506cebde82bde9, 0xbef9a3f7b2c67915, 0xc67178f2e372532b, 0xca273eceea26619c, 
    0xd186b8c721c0c207, 0xeada7dd6cde0eb1e, 0xf57d4f7fee6ed178, 0x06f067aa72176fba, 0x0a637dc5a2c898a6, 
    0x113f9804bef90dae, 0x1b710b35131c471b, 0x28db77f523047d84, 0x32caab7b40c72493, 0x3c9ebe0a15c9bebc, 
    0x431d67c49c100d4c, 0x4cc5d4becb3e42b6, 0x597f299cfc657e2a, 0x5fcb6fab3ad6faec, 0x6c44198c4a475817]

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
    x = read(sys.argv[1])
    x = pad(x)
    x = parse(x)
    x = hash(x)
    print(x)

# failo atidarymas skaitymui baitais
# funkcija priima failo pavadinima, grazina failo turini baitu formatu
def read(file = 'test.txt'):
    f = open(file, 'rb')
    return f.read()

# zinutes pavertimas bitais bei ilgio padarymas i toki, kad len(msg) % 1024 = 0
# funkcija priima zinute baitais, grazina 1024*n bitu seka
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
        k = math.ceil(len(newmsg) / 1024)
        lastblocksize = len(newmsg) - 1024 * (k - 1)
        l = '{0:0128b}'.format(int(len(newmsg)))
        if lastblocksize < 896:
            newmsg += '1'
            for i in range(895 - lastblocksize):
                newmsg += '0'
            newmsg += l
        else:
            newmsg += '1'
            for i in range((k+1) * 1024 - len(newmsg) - 128):
                newmsg += '0'
            newmsg += l
        return newmsg

# 1024*n bitu sekos suskaldymas i n bloku, susidedanciu is 1024 bitu
# funkcija priima zinute bitu sekos pavidalu, grazina n bloku
# 1 blokas sudarytas is 16 bloku, kuriuose yra po 64 zinutes bitus (m[n][16])
def parse(message):
    if len(message)%1024 != 0:
        return

    m = [None] * int(len(message) / 1024)
    for i in range(int(len(message) / 1024)):
        block = message[i*1024: (i+1)*1024]
        m[i] = [None] * 16
        for j in range(16):
            m[i][j] = block[j*64: (j+1)*64]
    return m

def ch(x, y, z):
    return (x & y) ^ (~x & z)

def maj(x, y, z):
    return (x & y) ^ (x & z) ^ (y & z)

def rotR(x, n):
    mask = int('1111111111111111111111111111111111111111111111111111111111111111', 2)
    return (x >> n) | ((x << (64 - n)) & mask)

def sum0(x):
    return rotR(x, 28) ^ rotR(x, 34) ^ rotR(x, 39)

def sum1(x):
    return rotR(x, 14) ^ rotR(x, 18) ^ rotR(x, 41)

def sigma0(x):
    return rotR(x, 1) ^ rotR(x, 8) ^ (x >> 7)

def sigma1(x):
    return rotR(x, 19) ^ rotR(x, 61) ^ (x >> 6)

def mod64(x):
    return x % int(math.pow(2, 64))

# zinutes uzkodavimas
# funkcija priima zinute pavidalu m[n][16]
def hash(message):
    for i in range(len(message)):
        w = [None] * 80
        for j in range(80):
            if j < 16:
                w[j] = int(message[i][j], 2)
            else:
                w[j] = mod64(sigma1(w[j-2]) + w[j-7] + sigma0(w[j-15]) + w[j-16])
        a = h[0]
        b = h[1]
        c = h[2]
        d = h[3]
        e = h[4]
        f = h[5]
        g = h[6]
        hh = h[7]
        
        for t in range(80):
            T1 = mod64(hh + sum1(e) + ch(e, f, g) + k[t] + w[t])
            T2 = mod64(sum0(a) + maj(a, b, c))
            hh = g
            g = f
            f = e
            e = mod64(d + T1)
            d = c
            c = b
            b = a
            a = mod64(T1 + T2)

        h[0] = mod64(a + h[0])
        h[1] = mod64(b + h[1])
        h[2] = mod64(c + h[2])
        h[3] = mod64(d + h[3])
        h[4] = mod64(e + h[4])
        h[5] = mod64(f + h[5])
        h[6] = mod64(g + h[6])
        h[7] = mod64(hh + h[7])

    rez = '0x'
    for i in range(len(h) - 2):
        rez += format(h[i], '016x')
    return rez

if __name__ == "__main__":
    main()