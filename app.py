
from flask import Flask, render_template, Response, jsonify
import cv2, random, csv, datetime
app=Flask(__name__)
cam=cv2.VideoCapture(0)
emotions=['Happy','Sad','Neutral','Confused','Angry','Surprised']
stats={'frames':0,'attentive':0,'distracted':0}

def gen():
    while True:
        ok, frame=cam.read()
        if not ok: break
        stats['frames']+=1
        emotion=random.choice(emotions)
        attention=random.choice(['Attentive','Distracted'])
        if attention=='Attentive': stats['attentive']+=1
        else: stats['distracted']+=1
        cv2.putText(frame,f'Emotion: {emotion}',(20,30),0,1,(255,255,255),2)
        cv2.putText(frame,f'Attention: {attention}',(20,65),0,1,(255,255,255),2)
        ret,buf=cv2.imencode('.jpg',frame)
        yield (b'--frame\r\nContent-Type:image/jpeg\r\n\r\n'+buf.tobytes()+b'\r\n')

@app.route('/')
def home(): return render_template('index.html')

@app.route('/video')
def video(): return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/stats')
def api(): return jsonify(stats)

if __name__=='__main__':
    app.run(debug=True)
