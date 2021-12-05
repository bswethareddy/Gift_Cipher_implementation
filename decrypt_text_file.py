
from gift_cipher_try1 import encrypt_using_gift64, bin_to_64bit_hex, decrypt_using_gift64

def text_to_hex(text):
    z=''.join((hex(ord(c))[2:] for c in text))
    return z

def hex_to_text(text):
    ans=''
    for i in range(0,len(text),2):
        ans+=chr(int(text[i:i+2], 16))       
    return ans 

def break_into_64bit_parts(text):
    padding_val = (16 - len(text)%16)%16
    text = text+'0'*padding_val
    final_arr = [text[i:i+16] for i in range(0,len(text),16)]
    return final_arr

def decrypt_text_with_gift64(text, main_key):
    parts_64bit = break_into_64bit_parts(text)
    decrypted_text = ''
    for text in parts_64bit:
        d = decrypt_using_gift64(text, main_key)
        decrypted_text+=(bin_to_64bit_hex(d))
    final_text=''
    for i in range(0,len(decrypted_text),2):
        final_text+=chr(int(decrypted_text[i:i+2], 16))
    return final_text

main_key = '00000000000000000000000000000000'

with open('encrypted_text.txt', 'r') as file:
    encrypted_lines = [line.strip() for line in file]
decrypted_lines = []
for text in encrypted_lines:
    d = decrypt_text_with_gift64(text, main_key)
    d = d.rstrip('\x00')
    decrypted_lines.append(d)
with open('decrypted_text.txt', 'w') as file:
    for line in decrypted_lines:
        file.write(line+'\n')

