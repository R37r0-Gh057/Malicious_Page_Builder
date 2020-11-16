# This script is just for debugging process
# You can use this script to test a module

from flask import Flask, render_template, request, Response
from base64 import b64decode
import json, pyaudio

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('audio.html')

@app.route('/saveaudio',methods=['GET','POST'])
def saveaudio():
    if request.method == 'POST':
        print('incoming')
        with open('test_audio.wav','wb') as f:
            f.write(b64decode(request.get_json()))
            print('success')
            return 'OK','200'
    else:
        print('just got get')
        return 'OK','200'
app.run(host="0.0.0.0",debug=True)

'''
var xhr = new XMLHttpRequest();
                xhr.onload=function(e) {
                    if(this.readyState === 4) {
                        console.log('server returned: ', e.target.responseText);
                    }
                var fd = new FormData()
                console.log('sending blob')
                fd.append('audio_data',blob,'test.wav')
                xhr.open('POST','/saveaudio',true)
                xhr.send(fd)
                console.log('blob sent')'''
