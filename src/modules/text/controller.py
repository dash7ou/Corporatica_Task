from flask import Flask, Blueprint, request, jsonify
import os
from .service import TextAnalysisService
from pathlib import Path


text_bp = Blueprint('text', __name__, url_prefix='/api/v1/text')
VISUALIZATION_FOLDER = os.path.join(Path(__file__).parent.parent.parent.parent, "./static/visualizations")

text_service = TextAnalysisService(VISUALIZATION_FOLDER)

@text_bp.route('/summarize', methods=['POST'])
def summarize_text():
    data = request.json
    text = data.get('text')
    if not text:
        return jsonify({'error': 'No text provided'}), 400
    summary = text_service.summarize(text)
    return jsonify({'summary': summary}), 200

@text_bp.route('/keywords', methods=['POST'])
def extract_keywords():
    data = request.json
    text = data.get('text')
    if not text:
        return jsonify({'error': 'No text provided'}), 400
    keywords = text_service.extract_keywords(text)
    return jsonify({'keywords': keywords}), 200

@text_bp.route('/sentiment', methods=['POST'])
def analyze_sentiment():
    data = request.json
    text = data.get('text')
    if not text:
        return jsonify({'error': 'No text provided'}), 400
    sentiment = text_service.analyze_sentiment(text)
    return jsonify({'sentiment': sentiment}), 200

@text_bp.route('/process', methods=['POST'])
def process_text():
    data = request.json
    text = data.get('text')
    search_query = data.get('search_query')
    category = data.get('category')
    custom_query = data.get('custom_query')
    
    result = text_service.process_text(text, search_query, category, custom_query)
    return jsonify(result), 200