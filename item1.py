import sqlite3
from flask import Flask, request
from flask_restful import Resource,reqparse, Api
from security1 import authenticate,identity
from flask_jwt import JWT, jwt_required, current_identity

app = Flask(__name__)
app.secret_key = "secret123"
api = Api(app)

jwt = JWT(app, authenticate, identity)
