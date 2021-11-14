from flask import Flask, render_template , request
from flask.helpers import url_for
from werkzeug.utils import redirect
from firebase_admin import firestore
from firebase_admin import credentials

app = Flask(__name__, template_folder='static')
#app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///deez.db'
#db = SQLAlchemy(app)


@app.route('/')
def hello_world():
   return render_template("html/login.html")

@app.route('/login')
def login_deez():
   return render_template("html/login.html")

@app.route('/signup')
def signup_deez():
   return render_template("html/signup.html")


@app.route('/main', methods=['post','get'])
def main_deez():
   return render_template("html/mainpage.html")

@app.route('/page', methods=['post','get'])
def links():
   return render_template("html/page.html")
      


if __name__ == '__main__':
   db.create_all()
   app.debug = True
   app.run()