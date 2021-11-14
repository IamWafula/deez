from flask import Flask, render_template, redirect , request, jsonify
from flask.helpers import url_for
from flask.wrappers import Request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder='static')
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///deez.db'

db = SQLAlchemy(app)


class Users(db.Model):
  name = db.Column(db.String, primary_key = True)
  passw = db.Column(db.String(100), nullable=False)

user1 = Users(name = "demouser", passw = "demouserpassword")

use = []

@app.route('/')
def hello_world():
  return render_template('form.html')

@app.route('/submit', methods=['post','get'])
def userss():
  if request.method == 'POST':
    user = Users(name = request.form['name'], passw = request.form['passw'])

    use.append(user.name)

  db.session.add(user)
  db.session.commit()

  return redirect(url_for('list'))
  

@app.route('/users')
def list():
  
  return jsonify(use)

if __name__ == '__main__':
    app.debug = True
    db.create_all()
    #app.run(host='0.0.0.0')
    app.run()