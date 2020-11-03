from flask import Flask, jsonify, request
from flask_restful import Api, Resource, reqparse
from flasgger import Swagger
from flasgger.utils import swag_from
import qsgw_host.api as QSGW_HOST_SERVICE
#from werkzeug.security import generate_password_hash, check_password_hash
#from flask_sqlalchemy import SQLAlchemy

import sys,os

app = Flask(__name__)
app.config['SWAGGER'] = {
    "swagger_version": "2.0",
    "title": "Storage Gateway Midware",
    "headers": [
        ('Access-Control-Allow-Origin', '*'),
        ('Access-Control-Allow-Methods', "GET, POST, PUT, DELETE, OPTIONS"),
        ('Access-Control-Allow-Credentials', "true"),
    ],
    "specs": [
        {
            "endpoint": "qsgw_v1",
            "route": "/qsgw/v1/json",
            "title": "QSGW API v1",
            "description": "QCS Storage Gateway API v1"
        },
    ],
    "securityDefinitions": {
        "token_auth": {
            "type": "apiKey",
            "name": "X-Auth-Token",
            "in": "header"
        }
    },
    "security": ['token_auth'],
    "swagger_ui": True,
    "specs_route": "/qsgw/v1/api/",
    "description": "QCS Storage Gateway Midware API",
    "version": "1.0.0",
    "contact": {
        "email": "jimhsia@qnap.com",
        "url": "www.qnap.com"
    },
    "host":'10.19.5.212'+":"+str(5000),
    "schemes": ["http"],
    "termsOfService":"www.qnap.com"
}
#app.config['SECRET_KEY'] = "ryanhuang"
#app.config['SQLALCHEMY_DATABAS_URI'] = "/home/ryanhuang/ryanhuang_github/python/web/todo.db"
#db = SQLAlchemy(app)


swag = Swagger(app)
api = Api(app)

QSGW_HOST_SERVICE.init_api(api)

## main service
if __name__ == '__main__':
    #db.create_all()
    app.run(host='10.19.5.212', port='5000', debug=True)
