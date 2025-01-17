from flask import Blueprint, jsonify

from applications.models.model_example import Message

routes = Blueprint('routes', __name__)


@routes.route('/api/hello', methods=['GET'])
def hello():
    # Fetch a message from the database
    message = Message.query.first()
    return jsonify({"message": message.text if message else "Hello, World!"})
