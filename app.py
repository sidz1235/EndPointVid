from flask import Flask, render_template, request, jsonify
import os
from analysis import compute
import base64
from test import *
from flask_cors import CORS
from database import fetch_data_by_mobile_number,insert_data

app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = 'videos'
UPLOAD_FOLDER = 'videos/'


@app.route('/analyse', methods=['POST'])
def analyse():

    mobile_number = str(request.form['mobile_number'])
    country_code = request.form['country_code']
    print(mobile_number, country_code,sep="and")
    uploaded_file = request.files['file']

    
    filename = uploaded_file.filename
    file_path = 'temp_video.mp4'
    uploaded_file.save(file_path)

    results = compute(file_path,filename,country_code,mobile_number)
    return results



@app.route('/user-data')
def get_data():

    mobile_number = request.args.get('mobile_number')
    country_code = request.args.get('country_code')
    # print(mobile_number, country_code,sep="and")
    data = fetch_data_by_mobile_number(mobile_number,country_code)
    return jsonify(data)



@app.route('/videos')
def get_video_names():
    video_names = []
    for root, dirs, files in os.walk('videos'):
        for file in files:
            if file.endswith('.mp4'):
                video_names.append(os.path.splitext(file)[0])
    return jsonify(video_names)



@app.route('/sendvideo')
def send_video():
    video_name = request.args.get('video_name')
    video_file_path = os.path.join('videos', video_name, f"{video_name}.mp4")

    if os.path.exists(video_file_path):
        with open(video_file_path, 'rb') as f:
            video_data = f.read()

        base64_encoded_video = base64.b64encode(video_data).decode('utf-8')

        video_info = {
            'file_data': base64_encoded_video
        }

        return jsonify(video_info)
    else:
        return jsonify({'error': 'Video not found'})
    

    
@app.route('/sendtext')
def send_text():
    text_name = request.args.get('text_name')
    text_file_path = os.path.join('videos', text_name, f"{text_name}.txt")

    if os.path.exists(text_file_path):
        with open(text_file_path, 'r') as f:
            text_data = f.read()

    text_info = {
        'text_data': text_data
    }

    return jsonify(text_info)



if __name__ == '__main__':
    app.run(debug=False)



