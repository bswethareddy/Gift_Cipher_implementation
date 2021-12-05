
import base64
from decrypt_text_file import *

main_key = '00000000000000000000000000000000'

with open('img_encrypted.txt', 'r') as f:
    e=f.read()

d = decrypt_text_with_gift64(e, main_key)
d = bytes(d, 'utf-8')
d = base64.b64decode(d)

with open('output_image.jpg', 'wb') as newfile:
    newfile.write(d)

