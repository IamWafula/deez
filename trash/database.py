
# Bs from flask
from flask import Flask, render_template , request , session, jsonify
from flask.helpers import url_for
from werkzeug.utils import redirect

#import firebase shit
import firebase_admin
from firebase_admin import credentials , firestore 
from firebase_admin import auth

#import 5-line algorithm
from redcheck import check

#for random link
import random


app = Flask(__name__, template_folder='static')
app.secret_key = "super secret key"
cred = credentials.Certificate("config.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

docs = db.collection('pages').where('description', '==', 'short/HIJIKINS').get()

short = []

for i in docs: 
    dic = i.to_dict()
    short.append(dic)

print(short[0]['pagename'])