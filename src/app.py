#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask
from flask_restful import Api
from pymongo import MongoClient
from .modules.tabular import controller as dataset_controller
from .modules.text import controller as text_controller
from .modules.rbg import controller as rgb_controller
from .core.settings import settings
import os


# app = Flask(__name__)
static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'static')

app = Flask(__name__, static_folder=static_dir)

# app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static', 'images')
# app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}

api = Api(app)

# app.config["APPLICATION_ROOT"] = "/"

@app.route('/healthcheck')
def healthcheck():
    return 'OK'

# Register blueprints
app.register_blueprint(dataset_controller.dataset_bp)
app.register_blueprint(rgb_controller.rgb_bp)
app.register_blueprint(text_controller.text_bp)



if __name__ == '__main__':
    # TODO: Add swagger integration
    app.run(debug=True)  # important to mention debug=True
