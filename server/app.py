from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages')
def all_messages():
    messages = [m.to_dict() for m in Message.query.all()]
    return messages, 200

@app.route('/messages', methods=['POST'])
def post_message():
    new_message = Message(body=request.json['body'], username=request.json['username'])
    db.session.add(new_message)
    db.session.commit()
    return new_message.to_dict(), 201


@app.route('/messages/<int:id>', methods=['PATCH'])
def patch_message(id):
    message_to_update = Message.query.where(Message.id == id).first()
    
    if message_to_update:
        setattr(message_to_update, 'body', request.json['body'])

        db.session.add(message_to_update)
        db.session.commit()
        return message_to_update.to_dict(), 201
    
    return { "error": "Not found"}, 404

@app.route('/messages/<int:id>', methods=['DELETE'])
def delete_message(id):
    message_to_delete = Message.query.where(Message.id == id).first()
    
    if message_to_delete:
        db.session.delete(message_to_delete)
        db.session.commit()
        return {}, 204
    
    return { "error": "Not found"}, 404

if __name__ == '__main__':
    app.run(port=5555)
