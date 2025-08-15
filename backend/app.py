from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tickchat.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

@app.route('/')
def index():
    return "TickChat Backend is running."

@app.route('/send', methods=['POST'])
def send():
    data = request.get_json()
    msg = Message(username=data['username'], content=data['message'])
    db.session.add(msg)
    db.session.commit()
    return jsonify({'status':'ok'})

@app.route('/messages')
def messages():
    msgs = Message.query.order_by(Message.timestamp.asc()).all()
    output = [{'username': m.username, 'message': m.content} for m in msgs]
    return jsonify(output)

if __name__ == '__main__':
    if not os.path.exists('tickchat.db'):
        db.create_all()
    app.run(host='0.0.0.0', port=5000)
