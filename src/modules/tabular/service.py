import pandas as pd
import plotly.express as px
from .model import DatasetModel
from ...core.helpers import detect_outliers
import json
import os
import uuid
from pathlib import Path

class DatasetService:
    def __init__(self):
        from ...core.db import db  # Import MongoDB client from app
        self.dataset_model = DatasetModel(db)
        self.chart_dir = Path(__file__).parent.parent.parent.parent
        os.makedirs(self.chart_dir, exist_ok=True)

    def upload_dataset(self, file, dataset_name):
        try:
            data = pd.read_csv(file)
            dataset_id = self.dataset_model.save_dataset(data, dataset_name)
            return {"message": "Dataset uploaded", "dataset_id": str(dataset_id)}
        except Exception as e:
            return {"error": str(e)}

    def preview_dataset(self, dataset_id):
        data = self.dataset_model.get_dataset(dataset_id)
        if data is not None:
            return json.loads(data.head().to_json(orient='records'))
        return {"error": "Dataset not found"}

    def compute_stats(self, dataset_id, column):
        data = self.dataset_model.get_dataset(dataset_id)
        if data is None:
            return {"error": "Dataset not found"}
        
        try:
            stats = {
                'mean': data[column].mean(),
                'median': data[column].median(),
                'mode': data[column].mode().tolist(),
                'quartiles': data[column].quantile([0.25, 0.5, 0.75]).tolist(),
                'outliers': detect_outliers(data[column])
            }
            return stats
        except Exception as e:
            return {"error": str(e)}

    def visualize_data(self, dataset_id, chart_params):
        data = self.dataset_model.get_dataset(dataset_id)
        if data is None:
            return {"error": "Dataset not found"}

        try:
            chart_type = chart_params.get('type')
            x_col = chart_params.get('x')
            y_col = chart_params.get('y')

            if chart_type == 'scatter':
                fig = px.scatter(data, x=x_col, y=y_col)
            elif chart_type == 'bar':
                fig = px.bar(data, x=x_col, y=y_col)
            else:
                return {"error": "Invalid chart type"}
            
            chart_id = str(uuid.uuid4())
            chart_path = os.path.join(self.chart_dir, "./static/charts" f'{chart_id}.html')
            fig.write_html(chart_path, include_plotlyjs='cdn')

            chart_url = f'/static/charts/{chart_id}.html'
            return {"chart_url": chart_url}
        except Exception as e:
            return {"error": str(e)}

    def list_datasets(self):
        return self.dataset_model.list_datasets()

    def delete_dataset(self, dataset_id):
        result = self.dataset_model.delete_dataset(dataset_id)
        if result.deleted_count:
            return {"message": "Dataset deleted successfully"}
        return {"error": "Dataset not found"}

    # Add Row, Update Row, Delete Row methods here
