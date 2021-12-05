
# GIFT64 IMPLEMENTATION TRY

def perm_bit_calc_gift64(i):
    P_i = 4*(i//16) + 16*(((3*((i%16)//4) + i%4)%4)) + i%4
    return P_i

def calc_rev_sbox(Sbox):
    rev_Sbox=[-1 for _ in range(16)]
    for i in range(16):
        for j in range(16):
            if Sbox[j]==i:
                rev_Sbox[i]=j
                break
    return rev_Sbox

Sbox = [0x1, 0xa, 0x4, 0xc, 0x6, 0xf, 0x3, 0x9, 0x2, 0xd, 0xb, 0x7, 0x5, 0x0, 0x8, 0xe]
rev_Sbox=calc_rev_sbox(Sbox)
Permutation_bits = [perm_bit_calc_gift64(i) for i in range(64)]
#print(Permutation_bits)

def generate_round_keys_from_main_key(main_key):
    round_keys=[]
    round_key=hex_to_bin_str(main_key)
    aa,bb='',''
    for _ in range(28):
        round_keys.append(round_key[-32:])
        a=round_key[-16:]
        b=round_key[-32:-16]
        aa=a[-12:]+a[:-12]
        bb=b[-2:]+b[:-2]
        round_key=bb+aa+round_key[:-32]
    return round_keys

round_constants=[0x01,0x03,0x07,0x0f,0x1f,0x3e,0x3d,0x3b,0x37,0x2f,0x1e,0x3c,0x39,0x33,0x27,0x0e,0x1d,0x3a,0x35,0x2b,0x16,0x2c,0x18,0x30,0x21,0x02,0x05,0x0b]

def sub_cells(text):
    ans=[]
    for i in range(16):
        ans.append(hex(Sbox[int(text[4*i:4*i+4], 2)])[2:])
    for i in range(16):
        ans[i]=hex_to_bin_str(ans[i])
    return ''.join(ans)

def rev_sub_cells(text):
    ans=[]
    for i in range(16):
        ans.append(hex(rev_Sbox[int(text[4*i:4*i+4], 2)])[2:])
    for i in range(16):
        ans[i]=hex_to_bin_str(ans[i])
    return ''.join(ans)

def permutation_bits(text):
    text=text[::-1]
    new_text_permuted=[None]*len(text)
    for i in range(64):
        new_text_permuted[Permutation_bits[i]]=text[i]
    new_text_permuted=''.join(new_text_permuted)
    new_text_permuted=new_text_permuted[::-1]
    return new_text_permuted

def rev_permutation_bits(text):
    text=text[::-1]
    new_text_permuted=[None]*len(text)
    for i in range(64):
        new_text_permuted[i]=text[Permutation_bits[i]]
    new_text_permuted=''.join(new_text_permuted)
    new_text_permuted=new_text_permuted[::-1]
    return new_text_permuted

def hex_to_bin_str(text):
    ans=''
    for c in text:
        z='0000'
        z+=str(bin(int(c, 16)))[2:]
        ans+=z[-4:]
    return ans
#hex_to_bin_str('eea0')

def bin_to_64bit_hex(text):

    ans='0'*16
    t = str(hex(int(text,2)))[2:]
    ans = (ans+t)[-16:]
    return ans

def add_round_key_and_round_constant(round_keys,text_in,round_number):

    round_key=round_keys[round_number]
    u, v = round_key[:16], round_key[16:]
    u=[int(x) for x in u]
    v=[int(x) for x in v]
    text=[int(x) for x in text_in]

    u.reverse()
    v.reverse()
    text.reverse()

    for j in range(16):
        text[4*j+1]^=u[j]
        text[4*j]^=v[j]
    
    round_constant=('00000000'+hex_to_bin_str(hex(round_constants[round_number])[2:]))[-6:]
    round_constant=[int(x) for x in round_constant]
    round_constant.reverse()
    text[63]^=1
    text[3]^=round_constant[0]
    text[7]^=round_constant[1]
    text[11]^=round_constant[2]
    text[15]^=round_constant[3]
    text[19]^=round_constant[4]
    text[23]^=round_constant[5]
    text.reverse()

    return ''.join(map(str, text))

def encrypt_using_gift64(text, main_key):
    round_keys=generate_round_keys_from_main_key(main_key)
    text=hex_to_bin_str(text)
    #states1.append(text)    
    for round_number in range(28):
        text=sub_cells(text)
        #states1.append(text)
        text=permutation_bits(text)
        #states1.append(text)
        text=add_round_key_and_round_constant(round_keys,text,round_number)    
        #states1.append(text)
    return text

def decrypt_using_gift64(text, main_key):
    round_keys=generate_round_keys_from_main_key(main_key)
    text=hex_to_bin_str(text)
    for round_number in range(27,-1,-1):
        #states2.append(text)
        text=add_round_key_and_round_constant(round_keys,text,round_number)
        #states2.append(text)
        text=rev_permutation_bits(text)
        #states2.append(text)    
        text=rev_sub_cells(text)
    #states2.append(text)    
    return text

#plaintext = 'c450c7727a9b8a7d'
#main_key = '00000000000000000000000000000000'

#states1=[]
#states2=[]
#print()
#print(">>> 128 bit key in hex format:", main_key)
#print(">>> 64 bit plaintext in hex format:", plaintext)
#ciphertext = hex(int(encrypt_using_gift64(plaintext, main_key),2))[2:]
#ciphertext = bin_to_64bit_hex(encrypt_using_gift64(plaintext, main_key))
#print(">>> ciphertext calculated using the encrypt method:", ciphertext)
#ciphertext2 = bin_to_64bit_hex(decrypt_using_gift64(ciphertext, main_key))
#print(">>> plaintext decrypted by using decrypt method:", ciphertext2)
#print(">>> decrypted ciphertext = initial plaintext?", ciphertext2==plaintext)

