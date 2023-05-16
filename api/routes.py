from flask import Flask, jsonify, Blueprint, request
from flask_swagger import swagger
from .model.text import TextModel
from logger import get_logger

logger = get_logger(__name__)

app = Flask(__name__)

api = Blueprint("api",__name__,url_prefix="/api")

@api.route('/summarize', methods=['POST'])
def summarize():
    """
    Summarize Text API
    ---
    parameters:
      - name: text
        in: body
        type: string
        required: true
        description: The text to be summarized
    responses:
      200:
        description: The summarized text
        schema:
          type: object
          properties:
            summarized_text:
              type: string
              description: The summarized text
    """
    logger.info('IVai proceessar')

    data = request.get_json()
    text = data['text']
    # num_sentences = data['num_sentences']
    logger.info('Initializing with text: %s', text)

    text_object = TextModel(text)
   
    summarized_text = text_object.summarize_text()
    
    return jsonify({'summarized_text': summarized_text}), 200
