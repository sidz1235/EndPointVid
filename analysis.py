import tempfile
import cv2
import numpy as np
from moviepy.editor import VideoFileClip
from pydub import AudioSegment
from pydub.silence import detect_silence
import librosa
import re
import speech_recognition as sr
from openai import OpenAI
# from database import insert_data
# from app1 import mapthedata
client = OpenAI(api_key="")

def generate_response(user_input):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": """
                    filler_words = ["Um", "Uh", "Like", "You know", "Well", "So", "Basically", "Actually", "Literally", "Kind of", "Sort of", "I mean", "Anyway", "Right", "OK", "Hmm", "Ah", "Yeah", "I guess", "Just", "Somehow", "Somehow or other", "Really", "Definitely", "Absolutely", "Totally", "Honestly", "Seriously", "Honestly", "Absolutely", "Anyway", "Somehow", "Somehow or other", "Definitely", "Basically", "Like I said", "At the end of the day", "Actually", "Literally", "You see", "I mean", "Right?", "You know what I mean?", "I guess", "I suppose", "Sort of", "Kind of", "Well", "OK", "Fine", "Alright", "You know", "I guess so", "So to speak", "As it were", "In a manner of speaking", "By the way", "Incidentally", "By the by", "By the way", "In any case", "In any event", "Anyway", "Anyhow", "Nevertheless", "Nonetheless", "However", "Still", "Yet", "Moreover", "Furthermore", "Additionally", "Besides", "In addition", "Also", "Too", "As well", "Apart from that", "Apart from this", "To tell the truth", "To be honest", "Frankly", "To be frank", "In fact", "As a matter of fact", "To be precise", "To be exact", "If truth be told", "To tell you the truth", "Believe it or not", "Oddly enough", "Strangely enough", "Funnily enough", "Surprisingly", "Amazingly", "Interestingly", "Curiously", "Fortunately", "Unfortunately", "Regrettably", "Luckily", "Thankfully", "Happily", "Sadly", "Frankly", "Honestly", "To be perfectly honest", "To be perfectly frank", "To be perfectly truthful", "To be perfectly sincere", "If you want my honest opinion", "If you want my honest opinion", "To be brutally honest", "To be quite honest", "If you ask me", "To my mind", "In my opinion", "In my view", "As I see it", "As far as I'm concerned", "If you ask me", "From my point of view", "From where I'm sitting", "Personally", "Speaking for myself", "According to me", "I reckon", "I guess", "I suppose", "I believe", "I think", "I feel", "It seems to me", "It appears to me", "It strikes me", "It seems", "It appears", "It looks", "It sounds", "It feels", "It smells", "It tastes", "I expect", "I imagine", "I assume", "I presume", "I suppose", "I think", "I believe", "I reckon", "I guess", "I dare say", "I would say", "I take it", "I gather", "I understand", "I gather", "I take it", "I understand", "I hear", "I hear tell", "I hear tell that", "Rumour has it that", "I wonder", "I wonder if", "I wonder whether", "I wonder what", "I wonder where", "I wonder why", "I wonder how", "Don't you think", "Do you think", "Do you suppose", "What do you think", "How about you", "What about you", "How do you see", "How do you feel", "How do you think", "How do you believe", "How do you reckon", "How do you guess", "What do you make of", "What's your opinion on", "What's your view on", "What's your take on", "What's your position on", "What do you feel about", "What do you think about", "What do you believe about", "What do you reckon about", "What do you guess about", "Don't you agree", "Do you agree", "Aren't you of the same opinion", "Are you of the same opinion", "Wouldn't you say", "Do you concur", "Do you concur with me", "Do you concur with that", "Would you concur", "Do you concur with my opinion", "Would you agree with me", "Would you agree with that", "Would you agree with my opinion", "I'd say so", "I'd say", "I guess so", "I think so", "I believe so", "I reckon so", "I suppose so", "I'd imagine so", "I'd assume so", "I take it so", "I understand so", "I gather so", "I hear so", "Rumour has it so", "I'd say not", "I guess not", "I think not", "I believe not", "I reckon not", "I suppose not", "I'd imagine not", "I'd assume not", "I take it not", "I understand not", "I gather not", "I hear not", "Rumour has it not", "It seems so to me", "It appears so to me", "It looks so to me", "It sounds so to me", "It feels so to me", "It smells so to me", "It tastes so to me", "It seems not to me", "It appears not to me", "It looks not to me", "It sounds not to me", "It feels not to me", "It smells not to me", "It tastes not to me", "It seems so to you", "It appears so to you", "It looks so to you", "It sounds so to you", "It feels so to you", "It smells so to you", "It tastes so to you", "It seems not to you", "It appears not to you", "It looks not to you", "It sounds not to you", "It feels not to you", "It smells not to you", "It tastes not to you"]

                    from the above list of filler words ,check with below text provided and return integer value of total number of filler words check for spelling mistake in fillers too
                    return only the integer total count of fillers
                """ 
                +user_input
            },

        ],
        temperature=0,
        max_tokens=256,
        top_p=1
    )

    return response.choices[0].message.content




def compute_filler(audio_file):

    try:

        recognizer = sr.Recognizer()
        with sr.AudioFile(audio_file) as source:
            audio_data = recognizer.record(source)
            transcript = recognizer.recognize_google(audio_data)

        nWords = len(transcript.split())
        fillers = generate_response(transcript)

        pattern = r'\d+'
        
        matches = re.findall(pattern, fillers)
        
        nFillers =  int(matches[0])

        return nWords,nFillers
    
    except :
        return False,False


def compute_voice(audio):
    y, sr = librosa.load(audio)

    frame_length = 2048
    hop_length = 512
    energy = librosa.feature.rms(y=y, frame_length=frame_length, hop_length=hop_length)[0]

    mean_energy = np.mean(energy)
    std_energy = np.std(energy)

    soft_threshold = mean_energy - 0.5 * std_energy
    medium_threshold = mean_energy + 0.5 * std_energy

    soft_duration = 0
    medium_duration = 0
    high_duration = 0

    for e in energy:
        if e < soft_threshold:
            soft_duration += hop_length / sr
        elif soft_threshold <= e < medium_threshold:
            medium_duration += hop_length / sr
        else:
            high_duration += hop_length / sr

    total_duration = librosa.get_duration(y=y, sr=sr)

    percentage_soft = (soft_duration / total_duration) * 100
    percentage_medium = (medium_duration / total_duration) * 100
    percentage_high = (high_duration / total_duration) * 100

    voice_duration = (soft_duration,medium_duration,high_duration)
    voice_percentage = (percentage_soft,percentage_medium,percentage_high)

    return voice_duration,voice_percentage

def compute_pauses(audio_file_path, min_silence_duration=1000, silence_threshold=-50):
    audio = AudioSegment.from_wav(audio_file_path)
    silent_chunks = detect_silence(audio, min_silence_len=min_silence_duration, silence_thresh=silence_threshold)
    silent_chunks_filtered = [chunk for chunk in silent_chunks if chunk[1] - chunk[0] >= min_silence_duration]
    
    num_pauses = len(silent_chunks_filtered)
    pause_durations = [((start / 1000), (stop / 1000)) for start, stop in silent_chunks_filtered]
    total_pause_time = sum((stop - start) / 1000 for start, stop in silent_chunks_filtered)
    
    return num_pauses, total_pause_time

def compute_audio(input_video_path, output_audio_path):
    video_clip = VideoFileClip(input_video_path)

    audio_clip = video_clip.audio

    audio_clip.write_audiofile(output_audio_path)

    audio_clip.close()
    video_clip.close()

def video_duration(video_path):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration_seconds = total_frames // fps
    cap.release()
    return duration_seconds



def detect_eye(img):
    face_cascade = cv2.CascadeClassifier("xml/face.xml")
    eye_cascade = cv2.CascadeClassifier("xml/eye.xml")

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    
    eyes = ()
    for (x,y,w,h) in faces:
        img = cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray)
    for (ex,ey,ew,eh) in eyes:
        cv2.rectangle(img,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
    if len(eyes) > 0:
        return True
    else:
        return False

def process_video(video_path):
    frames_to_skip = 10
    cap = cv2.VideoCapture(video_path)

    frame_count = 0
    eye_detected_count = 0
    total_frame_count = 0

    frames_skipped = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        total_frame_count += 1

        frames_skipped += 1
        if frames_skipped < frames_to_skip:
            continue
        frames_skipped = 0

        if detect_eye(frame):
            eye_detected_count += 1

    eye_detection_percentage = (eye_detected_count / (total_frame_count / frames_to_skip)) * 100

    cap.release()
    cv2.destroyAllWindows()

    return eye_detection_percentage

def compute(video_path,filename,country_code,mobile_number):
    # try:
        
        #print(video)
        # print('started')
        with open(video_path, "rb") as video:
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                temp_file.write(video.read())
                file_path = temp_file.name

        audio = "audio.wav"
        compute_audio(file_path, audio)
        words, fillers = compute_filler(audio)
        if words == 0 :
            return {"error": "Check Audio", "traceback": "Audio Segment cannot be Empty and Meaningless"}, 0
        
        eye_contact = process_video(file_path)

        duration_vid = video_duration(file_path)


        num_pauses, total_pause_time = compute_pauses(audio)
        voice_duration, voice_Percentage = compute_voice(audio)
        soft, medium, high = voice_duration
        soft_p, medium_p, high_p = voice_Percentage
        
        if duration_vid >  60 :
            fpm = int((fillers / duration_vid) * 60)
            wpm = int((words / duration_vid) * 60)
        else :
            fpm = fillers
            wpm = words

        avg_words, avg_fillers = 125, 1

        if wpm > avg_words:
            words_feed = "GREAT"
        else:
            words_feed = "SLOW"

        if fpm > avg_fillers:
            fillers_feed = "HIGH"
        else:
            fillers_feed = "GREAT"

        avg_eye = 60
        if eye_contact > avg_eye:
            eye_feed = "GREAT"
        else:
            eye_feed = "LOW"

        avg_pause = 0.5

        if num_pauses > 0:
            pause_time = total_pause_time / num_pauses
        else:
            pause_time = 0

        if pause_time > avg_pause:
            pause_feed = "LONG"
        else:
            pause_feed = "GREAT"

        # print(filename)

        databasedata={
            "Country_Code": int(country_code),
            'Mobile_Number': str(mobile_number),
            "Duration": int(duration_vid),
            "Total_Words": words,
            'Filler_Words_Per_Minute': wpm,
            'Average_Words_Per_Minute': avg_words,
            'Fillers_Per_Minute': fpm,
            'Average_Fillers_Per_Minute': avg_fillers,
            'Eye_Contact_Percentage': round(eye_contact,2),
            'Num_Pauses': num_pauses,
            'Total_Pause_Time': round(total_pause_time, 2),
            'Soft_Voices_Percentage': round(soft_p,2),
            'Medium_Voices_Percentage': round(medium_p,2),
            'High_Voices_Percentage': round(high_p,2),
            'file_name' : filename,
        }
        #print("-------------mapping data to api-----------------")
        #print(databasedata)
       
        # insert_data(databasedata)
        # mapthedata(databasedata)
        
        
        data = {
            "Duration": str(duration_vid)+" s",
            "Words": {
                "Total": str(words)+" words",
                "WPM": str(wpm)+" words per minute",
                "Feed": words_feed,
                "Average": str(avg_words)+" words per minute",
            },
            "Filler Words": {
                "Total": str(fillers)+" words",
                "FPM": str(fpm)+" fillers per minute",
                "Feed": fillers_feed,
                "Average": str(avg_fillers)+" fillers per minute",
            },
            "Eye Contact": {
                "Percentage": str(round(eye_contact,2))+" percent",
                "Feed": eye_feed,
                "Average": str(avg_eye)+" percent",
            },
            "Pauses": str(num_pauses)+" pauses",
            "Pause Time": {
                "Total ": str(round(total_pause_time, 2))+" seconds",
                "Per Pause": str(round(pause_time, 2))+" seconds per pause",
                "Feed" : pause_feed,
                "Average": str(round(avg_pause, 2))+" seconds per pause",
            },
            "Voices": {
                "Soft": str(round(soft, 2))+" seconds",
                "Soft Percentage": str(round(soft_p, 2))+" percent",
                "Medium": str(round(medium, 2))+" seconds",
                "Medium Percentage": str(round(medium_p, 2))+" percent",
                "High": str(round(high, 2))+" seconds",
                "High Percentage": str(round(high_p, 2))+" percent",
            }
        }



        return data,databasedata
    
    # except Exception as e:
    #     print(e)
    #     return {"error": "Check Audio and Video Formats", "traceback": "Video and Audio Cannot be Empty"}, 0
