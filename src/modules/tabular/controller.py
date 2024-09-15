from flask import Blueprint, request, jsonify
from .service import DatasetService

dataset_bp = Blueprint('tabular', __name__, url_prefix='/api/v1/tabular')
dataset_service = DatasetService()

# Upload dataset
@dataset_bp.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
        # file.filename
    dataset_name = file.filename if file.filename else "none_named"
    response = dataset_service.upload_dataset(file, dataset_name)
    return jsonify(response), 200 if 'error' not in response else 400

# Preview dataset
@dataset_bp.route('/<dataset_id>/preview', methods=['GET'])
def preview_data(dataset_id):
    response = dataset_service.preview_dataset(dataset_id)
    return jsonify(response), 200 if 'error' not in response else 404

# CRUD operations
@dataset_bp.route('/<dataset_id>/data', methods=['GET', 'POST', 'PUT', 'DELETE'])
def manage_data(dataset_id):
    if request.method == 'GET':
        response = dataset_service.get_dataset(dataset_id)
    elif request.method == 'POST':
        new_data = request.json
        response = dataset_service.add_row(dataset_id, new_data)
    elif request.method == 'PUT':
        row_id = request.json.get('id')
        updated_data = request.json
        response = dataset_service.update_row(dataset_id, row_id, updated_data)
    elif request.method == 'DELETE':
        row_id = request.json.get('id')
        response = dataset_service.delete_row(dataset_id, row_id)

    return jsonify(response), 200 if 'error' not in response else 400

# Compute statistics
@dataset_bp.route('/<dataset_id>/stats', methods=['POST'])
def advanced_stats(dataset_id):
    column = request.json.get('column')
    response = dataset_service.compute_stats(dataset_id, column)
    return jsonify(response), 200 if 'error' not in response else 404

# Visualize data
@dataset_bp.route('/<dataset_id>/visualize', methods=['POST'])
def visualize_data(dataset_id):
    chart_params = request.json
    response = dataset_service.visualize_data(dataset_id, chart_params)
    return response
    # return jsonify(response), 200 if 'error' not in response else 400

# List all datasets
@dataset_bp.route('/', methods=['GET'])
def get_datasets():
    response = dataset_service.list_datasets()
    return jsonify(response), 200

# Delete dataset
@dataset_bp.route('/<dataset_id>', methods=['DELETE'])
def delete_dataset(dataset_id):
    response = dataset_service.delete_dataset(dataset_id)
    return jsonify(response), 200 if 'error' not in response else 404
