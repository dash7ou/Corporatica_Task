#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask
from flask_restful import Api
from pymongo import MongoClient
from .modules.tabular import controller as dataset_controller
from .core.settings import settings


app = Flask(__name__)

api = Api(app)

# app.config["APPLICATION_ROOT"] = "/"

@app.route('/healthcheck')
def healthcheck():
    return 'OK'

# Register blueprints
app.register_blueprint(dataset_controller.dataset_bp)


if __name__ == '__main__':
    # TODO: Add swagger integration
    app.run(debug=True)  # important to mention debug=True
