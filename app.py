import os
from flask import render_template, redirect, request, url_for, flash, abort
from flask_login import login_user, logout_user, login_required, current_user
from init import app, db
from models import User
from forms import LoginForm, RegistrationForm
from flask_socketio import SocketIO
from flask import Flask, render_template, Response
import cv2


socketio = SocketIO(app)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user.check_password(form.password.data) and user is not None:
            login_user(user)
            flash("您已經成功的登入系統")
            next = request.args.get('next')
            if next == None or not next[0]=='/':
                next = url_for('welcome_user')
                return redirect(next)
    return render_template('login.html',form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("您已經登出系統")
    return redirect(url_for('home'))


@app.route('/register',methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
        username=form.username.data, password=form.password.data)
        
        try:
            db.session.add(user)
            db.session.commit()
            flash("感謝註冊本系統成為會員")
            return redirect(url_for('login'))

        except Exception as e:
            flash("您已註冊過本系統", "error")
        
    return render_template('register.html',form=form)


@app.route('/welcome', methods=['GET', 'POST'])
@login_required
def welcome_user():
    return render_template('welcome_user.html',user=current_user)

    
@socketio.on('send')
def chat(message):
    socketio.emit('get', { "message": message, "name": current_user.username})

@socketio.on('text')
def test():
    socketio.send("test")

@app.route('/live')
def live():
    return render_template('live.html')

@app.route('/video')
def video():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


def gen_frames():  
    while True:
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result



if __name__ == '__main__':
    camera = cv2.VideoCapture(1)
    with app.app_context():
        db.create_all()
    socketio.run(app, use_reloader=False) # , debug=True)
    # app.run(debug=True)