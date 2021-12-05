def dec_to_binary(num):
    res = [int(i) for i in bin(num)[2:]]
    return res

sbox=[]
for i in range(0,16):
    b = dec_to_binary(i)
    b[3] = b[3] ^ (b[0] and b[2])
    temp = b[0]^ (b[1] and b[3])
    b[2] = b[2]^ (temp and b[1])
    b[1] = b[1]^ b[0]
    b[1] = not(b[0])
    b[2] = b[2]^ (temp and b[1])
    b[3] = temp
    print(b)
