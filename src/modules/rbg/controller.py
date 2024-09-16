from flask import Flask, Blueprint, request, jsonify
from werkzeug.utils import secure_filename
import os
from .service import ImageService
from pathlib import Path


rgb_bp = Blueprint('rgb', __name__, url_prefix='/api/v1/rgb')
rgb_service = ImageService(os.path.join(Path(__file__).parent.parent.parent.parent, "./static/rgb_image"))
ALLOWED_EXTENSIONS =  {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Route to upload and store images
@rgb_bp.route('/upload', methods=['POST'])
def upload_images():
    if 'files' not in request.files:
        return jsonify({'error': 'No files part in request'}), 400

    files = request.files.getlist('files')
    saved_files = []
    
    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(Path(__file__).parent.parent.parent.parent, "./static/rgb_image" ,filename)
            file.save(file_path)
            saved_files.append(filename)
    
    return jsonify({'uploaded_files': saved_files}), 200

# Route to generate color histogram
@rgb_bp.route('/image/<filename>/histogram', methods=['GET'])
def color_histogram(filename):
    result = rgb_service.generate_histogram(filename)
    if 'error' in result:
        return jsonify(result), 400
    return jsonify(result), 200

# Route to generate segmentation mask
@rgb_bp.route('/image/<filename>/segmentation', methods=['POST'])
def segmentation_mask(filename):
    params = request.json  # Parameters for segmentation (like thresholds)
    result = rgb_service.generate_segmentation_mask(filename, params)
    if 'error' in result:
        return jsonify(result), 400
    return jsonify(result), 200

# Route for image manipulation (resize, crop, format conversion)
@rgb_bp.route('/image/<filename>/manipulate', methods=['POST'])
def manipulate_image(filename):
    manipulation_params = request.json  # Example: { "action": "resize", "width": 100, "height": 100 }
    result = rgb_service.manipulate_image(filename, manipulation_params)
    if 'error' in result:
        return jsonify(result), 400
    return jsonify(result), 200
