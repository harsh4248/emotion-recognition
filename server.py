
from flask import Flask, render_template, Response, redirect, request, session
import cv2
from emotion_recogintion import preprocess_image
from music_recommend import music_recommend
import json
from googleapiclient.discovery import build
# from spotipy import Spotify
# from spotipy.oauth2 import SpotifyOAuth


app = Flask(__name__)
app.secret_key = "tVPIFII2IJCN1Ce24rCpv4HmQIglTA2A"  # Change this to a secure secret key
app.config['SESSION_COOKIE_NAME'] = 'spotify_login_session'


# SPOTIPY_CLIENT_ID = '7de9aa52b901455ebd5bd1b1e688083f'
# SPOTIPY_CLIENT_SECRET = 'd736533c1f3a474899567c651d54bf67'
# SPOTIPY_REDIRECT_URI = 'http://localhost:5001/callback'
# SPOTIPY_SCOPE = 'user-library-read user-read-playback-state user-modify-playback-state'


# spotify_oauth = SpotifyOAuth(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI, scope=SPOTIPY_SCOPE)


API_KEY = 'AIzaSyC6fQutNFz0vGdQvxEbzSI84gR-hBHa-z0'
youtube = build('youtube', 'v3', developerKey=API_KEY)

camera = cv2.VideoCapture(0)
music_df = None

def gen_frames():  
    while True:
        success, frame = camera.read()  # read the camera frame
        frame = cv2.flip(frame,1)
        if not success:
            break
        else:
            frame, emotion = preprocess_image(frame)
            if(emotion == None):
                ret, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            else:
                music_list = music_recommend(emotion)
                global music_df
                music_df = music_list
                if music_list.empty:
                    pass
                ret, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n') 
@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# @app.route('/login')
# def login():
#     auth_url = spotify_oauth.get_authorize_url()
#     return redirect(auth_url)


# @app.route('/callback')
# def callback():
#     token_info = spotify_oauth.get_access_token(request.args['code'])
#     session['token_info'] = token_info
#     return redirect('/player')


# @app.route('/player')
# def player():
#     token_info = session.get('token_info', None)

#     if not token_info:
#         return redirect('/login')

#     sp = Spotify(auth=token_info['access_token'])

#     # Example: Get user's currently playing track
#     current_track = sp.current_playback()

#     return render_template('player.html', current_track=current_track)


# @app.route('/play')
# def play():
#     token_info = session.get('token_info', None)

#     if not token_info:
#         return redirect('/login')

#     sp = Spotify(auth=token_info['access_token'])

#     # # Example: Start playback of a specific track
#     # sp.start_playback(uris=['spotify:track:5QdEdUkVhJm3Ibo5xgkg1P'])
#     results = sp.search(q='Love Dose', type='track', limit=1)

#     if results and results['tracks']['items']:
#         track_uri = results['tracks']['items'][0]['uri']

#         # Example: Start playback of the searched track
#         sp.start_playback(uris=[track_uri])

#     return redirect('/player')

def search_music(query):
    # Search for music videos
    search_response = youtube.search().list(
        q=query,
        type='video',
        part='id,snippet',
        maxResults=1
    ).execute()

    # Extract video details
    video_id = search_response['items'][0]['id']['videoId']
    video_title = search_response['items'][0]['snippet']['title']

    return video_id, video_title

def get_video_url(video_id):
    # Get video details
    video_response = youtube.videos().list(
        id=video_id,
        part='id,snippet,contentDetails'
    ).execute()

    # Extract video URL
    video_url = f"https://www.youtube.com/embed/{video_id}"

    return video_url

@app.route('/recommend')
def recommend_music():
    
    video_id, video_title = search_music(f'{music_df.at[0, "name"]} by {music_df.at[0, "artist"]} song')
    video_url = get_video_url(video_id)

    return render_template('index.html',video_title=video_title, video_url=video_url)

@app.route('/')
def landing_page():
    return render_template('index.html',video_title=None, video_url=None)

# main driver function
if __name__ == '__main__':
	app.run(debug=True, port=5001)
