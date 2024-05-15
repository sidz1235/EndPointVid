import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, request, jsonify
import os
from analysis import compute  # Assuming `compute` is a function in `analysis` module
import base64
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Set up logging
log_file_path = 'app.log'
handler = RotatingFileHandler(log_file_path, maxBytes=10000, backupCount=3)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger = logging.getLogger(__name__)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

# Function to log the client's IP address
def log_request_info(route):
    client_ip = request.remote_addr
    logger.info(f"Request to {route} from IP: {client_ip}")

# Route to handle video analysis
@app.route('/analyse', methods=['POST'])
def analyse():
    try:
        log_request_info('/analyse')
        mobile_number = str(request.form['mobile_number'])
        country_code = request.form['country_code']
        uploaded_file = request.files['file']
        filename = uploaded_file.filename
        file_path = 'temp_video.mp4'
        uploaded_file.save(file_path)
        results, analysisdata = compute(file_path, filename, country_code, mobile_number)
        api_url = "http://localhost:8081/stats"
        vdanalyse = {
            "CountryCode": analysisdata["Country_Code"],
            "MobileNumber": analysisdata["Mobile_Number"],
            "Duration": analysisdata["Duration"],
            "Total_Words": analysisdata["Total_Words"],
            "Filler_Words_Per_Minute": analysisdata["Filler_Words_Per_Minute"],
            "Average_Words_Per_Minute": analysisdata["Average_Words_Per_Minute"],
            "Fillers_Per_Minute": analysisdata["Fillers_Per_Minute"],
            "Average_Fillers_Per_Minute": analysisdata["Average_Fillers_Per_Minute"],
            "Eye_Contact_Percentage": analysisdata["Eye_Contact_Percentage"],
            "Num_Pauses": analysisdata["Num_Pauses"],
            "Total_Pause_Time": analysisdata["Total_Pause_Time"],
            "Soft_Voices_Percentage": analysisdata["Soft_Voices_Percentage"],
            "Medium_Voices_Percentage": analysisdata["Medium_Voices_Percentage"],
            "High_Voices_Percentage": analysisdata["High_Voices_Percentage"],
            "file_name": analysisdata["file_name"]
        }
        response = requests.post(api_url, data=vdanalyse)
        logger.info(f"Sent analysis data to {api_url}, received status code {response.status_code}")
        return results
    except Exception as e:
        logger.error(f"Error in /analyse route: {e}")
        return jsonify({"error": str(e)}), 500

# Route to get user data
@app.route('/user-data')
def get_data():
    try:
        log_request_info('/user-data')
        mobile_number = request.args.get('mobile_number')
        country_code = request.args.get('country_code')
        api_url = "http://localhost:8081/getstats"
        vdanalyse = { "CountryCode": country_code, "MobileNumber": mobile_number }
        response = requests.post(api_url, data=vdanalyse)
        data = response.json()
        logger.info(f"Retrieved user data for {mobile_number} from {api_url}")
        return jsonify(data)
    except Exception as e:
        logger.error(f"Error in /user-data route: {e}")
        return jsonify({"error": str(e)}), 500

# Route to get the list of available videos
@app.route('/videos')
def get_video_names():
    try:
        log_request_info('/videos')
        video_names = []
        for root, dirs, files in os.walk('videos'):
            for file in files:
                if file.endswith('.mp4'):
                    video_names.append(os.path.splitext(file)[0])
        logger.info(f"Retrieved list of video names: {video_names}")
        return jsonify(video_names)
    except Exception as e:
        logger.error(f"Error in /videos route: {e}")
        return jsonify({"error": str(e)}), 500

# Route to send video file
@app.route('/sendvideo')
def send_video():
    try:
        log_request_info('/sendvideo')
        video_name = request.args.get('video_name')
        video_file_path = os.path.join('videos', video_name, f"{video_name}.mp4")
        if os.path.exists(video_file_path):
            with open(video_file_path, 'rb') as f:
                video_data = f.read()
            base64_encoded_video = base64.b64encode(video_data).decode('utf-8')
            video_info = {
                'file_data': base64_encoded_video
            }
            logger.info(f"Sent video file {video_name}.mp4")
            return jsonify(video_info)
        else:
            logger.warning(f"Video file {video_name}.mp4 not found")
            return jsonify({'error': 'Video not found'}), 404
    except Exception as e:
        logger.error(f"Error in /sendvideo route: {e}")
        return jsonify({"error": str(e)}), 500

# Route to send text file
@app.route('/sendtext')
def send_text():
    try:
        log_request_info('/sendtext')
        text_name = request.args.get('text_name')
        text_file_path = os.path.join('videos', text_name, f"{text_name}.txt")
        if os.path.exists(text_file_path):
            with open(text_file_path, 'r') as f:
                text_data = f.read()
            text_info = {
                'text_data': text_data
            }
            logger.info(f"Sent text file {text_name}.txt")
            return jsonify(text_info)
        else:
            logger.warning(f"Text file {text_name}.txt not found")
            return jsonify({'error': 'Text file not found'}), 404
    except Exception as e:
        logger.error(f"Error in /sendtext route: {e}")
        return jsonify({"error": str(e)}), 500

# if __name__ == '__main__':
#     app.run(debug=False)
