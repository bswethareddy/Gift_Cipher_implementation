import json
from flask import send_file,Flask, render_template, request, jsonify
from encrypt_text_file import *
from decrypt_text_file import *
import base64
import wave
import os
# imported the requests library
import requests

# def download_file_from_google_drive(id, destination):
#     URL = "https://docs.google.com/uc?export=download"

#     session = requests.Session()

#     response = session.get(URL, params = { 'id' : id }, stream = True)
#     token = get_confirm_token(response)

#     if token:
#         params = { 'id' : id, 'confirm' : token }
#         response = session.get(URL, params = params, stream = True)

#     save_response_content(response, destination)    

# def get_confirm_token(response):
#     for key, value in response.cookies.items():
#         if key.startswith('download_warning'):
#             return value

#     return None

# def save_response_content(response, destination):
#     CHUNK_SIZE = 32768

#     with open(destination, "wb") as f:
#         for chunk in response.iter_content(CHUNK_SIZE):
#             if chunk: # filter out keep-alive new chunks
#                 f.write(chunk)

#from converstion import app2
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("InputOutput.html")

@app.route('/problem1')
def problem1():
    return render_template("P1.html")
@app.route('/problem2')
def problem2():
    return render_template("P2.html")


@app.route("/submitJSON2", methods=["POST"])
def processJSON2():
    jsonStr = request.get_json()
    #print(jsonStr)
    jsonObj = json.loads(jsonStr)
    response = ""
    temp1=jsonObj['temp1']
    response+="<b> HI<b>"+str(temp1)+"</b><br>"
    return response
    #return jsonStr
@app.route("/submitJSON1_", methods=["POST"])
def processJSON1_():
    jsonObj = request.get_json()
    main_key = jsonObj['secret_key']

    # file_id = jsonObj["audio_"].split('/')[-2]
    # destination = 'my_file.wav'
    # download_file_from_google_drive(file_id, destination)
    e_path = os.getcwd()
    audio_path = os.path.join(e_path, jsonObj['audio_'].split('\\')[-1])


    with wave.open(audio_path, 'rb') as file:
        arr=file.getparams()
        f=file.readframes(100000)
    
    e=base64.b64encode(f)
    e=str(e, 'utf-8')
    e=encrypt_text_with_gift64(e, main_key)
    with open('encrypted_text.txt', 'w') as file:
        file.write(e)
    with open('parameters_audio.txt', 'w') as f:
        for p in arr:
            if p=='NONE':
                f.write(str(-1)+'\n')
            elif p=='not compressed':
                f.write(str(-2)+'\n')
            else:
                f.write(str(p)+'\n')
    
    return "ok"
    
@app.route("/get_file", methods=["GET"])
def get_file():
    response = 'encrypted_text.txt'
    return send_file(response, 
         mimetype="txt", 
         as_attachment=True, 
         attachment_filename="encrypted_text.txt")

@app.route("/get_par_file", methods=["GET"])
def get_par_file():
    response = 'parameters_audio.txt'
    return send_file(response, 
         mimetype="txt", 
         as_attachment=True, 
         attachment_filename="parameters_audio.txt")

@app.route("/submitJSON2_", methods=["POST"])
def processJSON2_():
    jsonObj = request.get_json()
    main_key = jsonObj['secret_key'] 
    e_path = os.getcwd()
    encrypt_path = os.path.join(e_path, jsonObj['encrypted_text'].split('\\')[-1])
    with open(encrypt_path, 'r') as file:
        encrypted_line = file.read()
    d = decrypt_text_with_gift64(encrypted_line, main_key)
    d = bytes(d, 'utf-8')
    d = base64.b64decode(d)
    pars=[]
    p_path = os.getcwd()
    par_path = os.path.join(p_path, jsonObj['par_text'].split('\\')[-1])
    with open(par_path, 'r') as f:
        for line in f:
            if int(line)==-1:
                pars.append('NONE')
            elif int(line)==-2:
                pars.append('not compressed')
            else:
                pars.append(int(line))
    with wave.open('output_audio.wav', 'wb') as f:
        f.setparams(pars)
        f.writeframes(d)

    return "ok"

@app.route("/get_audio_file", methods=["GET"])
def get_audio_file():
    response = 'output_audio.wav'
    return send_file(response, 
         mimetype="txt", 
         as_attachment=True, 
         attachment_filename="Decrypted_audio.wav")


if __name__ == "__main__":
    app.run(debug=True)
    #app.run(host='0.0.0.0', port=port, debug=True)
