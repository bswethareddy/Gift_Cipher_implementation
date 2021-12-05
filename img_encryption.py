
import base64
from encrypt_text_file import *

main_key = '00000000000000000000000000000000'

with open('input_image.jpg', 'rb') as img:
    s = base64.b64encode(img.read())

z = str(s, 'utf-8')
q = encrypt_text_with_gift64(z, main_key)

with open('img_encrypted.txt', 'w') as newfile:
    newfile.write(q)

