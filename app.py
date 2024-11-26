from flask import Flask, render_template, Response, jsonify ,session ,url_for , request ,flash,redirect
import gunicorn
from camera import *

app = Flask(__name__)

df1 = music_rec()
df1 = df1.head(15)

users = {'username': 'password'}

@app.route('/VideoFeed')
def index():
    print(df1.to_json(orient='records'))
    return render_template('index.html',  data=df1)


@app.route('/faceDetect')
def face_feed():
    return render_template('index.html')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the user exists and the password is correct
        if username in users and users[username] == password:
            session['username'] = username
            flash('Login successful!')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password!')

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out.')
    return redirect(url_for('index'))


@app.route('/')
def home():
    return render_template('landingpage.html')

def gen(camera):
    while True:
        global df1
        frame, df1 = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/t')
def gen_table():
    return df1.to_json(orient='records')


if __name__ == '__main__':
    app.debug = False
    app.run()
