
# Bs from flask
#from typing import Text
from flask import Flask, render_template , request , session, jsonify
from flask.helpers import url_for
from werkzeug.utils import redirect

#import firebase shit
import firebase_admin
from firebase_admin import credentials , firestore 

#import pyrebase for auth
import pyrebase

#import 5-line algorithm
from redcheck import check

#for random link
import random
import string

#import bitly depedencies
import bitlyshortener

#import requests 
import requests


app = Flask(__name__, template_folder='static')
app.secret_key = "super secret key"
cred = credentials.Certificate("config.json")
firebase_admin.initialize_app(cred)

config = {
  "apiKey": "AIzaSyCtlD3lnlGYiouoA755Bg2qOHSj_mOvaq8",
  "authDomain": "deez-fed22.firebaseapp.com",
  "databaseURL": "https://deez-fed22-default-rtdb.firebaseio.com",
  "projectId": "deez-fed22",
  "storageBucket": "deez-fed22.appspot.com",
  "messagingSenderId": "737530002329",
  "appId": "1:737530002329:web:6f1f0a8b30fef5cdc5f108"
}


firebase = pyrebase.initialize_app(config)

db = firestore.client()
auth = firebase.auth()





#check username
def getdetails(username):
   pages = db.collection('pages').where('username','==',username).get()

   #exciting variable names...yay!!
   confetti = []
   for i in pages:
      confetti.append(i.to_dict())

   return confetti

#get links from pagename
def getlinks(name):
   links = db.collection('links').where('pagename', '==',name).get()
   
   confets = []
   for i in links:
      confets.append(i.to_dict())

   return confets

#add link to database
def add_link(name,link):
   doa = check(link)
   new_link = db.collection('links').document()


   new_link.set({
      'pagename':name,
      'alive':doa,
      'url':link
   })

def add_page(username, name):
   new_page = db.collection('pages').document()

   new_page.set({
      'pagename': name,
      'description': "",
      'username': username
   })

#remove url form database
def remove(link):
   doc_ref = db.collection('links').where('url','==',link).get()
   #print(doc_ref.id)
   #lin = str(doc_ref.id)
   doc = doc_ref[0]
   id = doc.id

   #lin = "qOp6srAn664CDNsMCN3L"

   #doc = db.collection('links').document(lin).delete()

   db.collection('links').document(id).delete()

def remove_page(name):

   username = session.get('username',None)

   doc = db.collection('pages').where('pagename','==',name).where('username','==',username).get()
 
   if doc[0]:
      doc = doc[0]
      id = doc.id
      db.collection('pages').document(id).delete()
   else:
      pass

#get url for the links page(shortened url)
def get_url(pagename):
   username = session.get('username',None)

   doc = db.collection('pages').where('pagename','==',pagename).where('username','==',username).get()
   confets = []
   for i in doc:
      confets.append(i.to_dict())

   doc = confets[0]
   
   
   return doc['description']
   


'''def geturl(name):
   coll = db.collection('short').where('pagename','==', name).get()
   doc = coll[0]

   short = doc['link']

   return short'''



#get working urls for the shortened site
def get_working_urls(name):
   doc = db.collection('links').where('pagename','==',name).get()

   links = []
   for i in doc:
      links.append(i.to_dict())   
   urls = []
   for i in links:
      if i['alive']:
         urls.append(i['url'])

   return urls

#update url to database for main page, if already exists do nothing
def update_url(name, url):
   doc = db.collection('pages').where('pagename','==',name).get()
   
   doc = doc[0]
   id = doc.id

   data = db.collection('pages').document(id)

   data.update({
      'description': url
   })


#CHECK IF short already exists
def check_short(name):
   doc = db.collection('pages').where('pagename','==',name).get()

   linkss = []

   for i in doc:
      linkss.append(i.to_dict())

   page = linkss[0] 

   if 'short' in page['description']:
      return False
   else:
      return True

   

#check if the shortened url is available elsewhere
def check_avail(link):
   docs = db.collection('pages').get()

   short = []

   for i in docs: 
      dic = i.to_dict()
      short.append(dic['description'])

   if link in short:
      return True

#def check page name from the shortened url
def get_page_name(url):
   docs = db.collection('pages').where('description', '==', url).get()

   short = []

   for i in docs: 
      dic = i.to_dict()
      short.append(dic)
   
   return short[0]['pagename']

#randomizer function
def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
   return ''.join(random.choice(chars) for _ in range(size))


'''def login(username, password):
   try:
      
      return True
   except:
      return False'''

def set_dead(link, route):
   docs = db.collection('links').where('pagename', '==', route).where('url', '==', link).get()

   doc = docs[0]
   id = doc.id

   data = db.collection('links').document(id)

   data.update({
      'alive': False
   })

def bitlyy(url):
   docs = db.collection('bitly').stream()

   short = []

   for i in docs: 
      dic = i.to_dict()
      short.append(dic['token'])

   shortener = bitlyshortener.Shortener(tokens=short, max_cache_size=256)

   urls = [url]

   short = shortener.shorten_urls(urls)

   return short[0]


def antibot(ip):

   payload={}
   files={}
   headers = {}

   url = "https://antibot.pw/api/v2-blockers?ip="+ip+"&apikey=bb0be71d497cd248ec194f6621a4a614&ua=test"


   response = requests.request("GET", url, headers=headers, data=payload, files=files)

   response = response.json()


   #print("Response is")
   #return response.text

   return response['is_bot']

def get_short(name):
   doc = db.collection('pages').where('pagename','==',name).get()

   linkss = []

   for i in doc:
      linkss.append(i.to_dict())

   page = linkss[0] 

   return page['description']

@app.route('/')
def start():
   if  session.get('logged_in',None):
      return redirect(url_for('login_submit'))
   else:
      return render_template("html/login.html")


@app.route('/')
def hello_world(text):
   if  session.get('logged_in',None):
      return redirect(url_for('login_submit'))
   else:
      return render_template("html/login.html", text = text)

@app.route('/login', methods=['post','get'])
def login_deez():
   if request.method == 'POST':
      username = {
         "username": request.form['username'],
         "password": request.form['password']
      }

      email = username['username']
      pwd = username['password']


      try: 
         auth.sign_in_with_email_and_password(email, pwd)

         session['logged_in'] = True

         user_name = username['username']

         session['username'] = user_name

         return redirect(url_for('login_submit'))
      except:
         return redirect(url_for('hello_world', text="Wrong credentials"))


@app.route('/logout')
def logout():
   session['logged_in'] = False

   return redirect(url_for('start'))

@app.route('/main')
def login_submit():
   if  session.get('logged_in',None):
      user_name = session.get('username', None)
      
      #initialize current page variable
      session['currentpage'] = "none"
      
      pages = getdetails(user_name)
      return render_template('html/mainpage.html', pages=pages, username = user_name)
   else:
      return render_template("html/login.html", text="Login Again")


#to display
'''@app.route('/lgsubmit')
def main_deez():
   print(pages)
   return render_template("html/mainpage.html")'''


#WHAT WAS THIS FUNCTION EVEN???
#OPen the links page
@app.route('/page', methods=['post','get'])
def links():
   #from the main page
   if request.method == 'POST':
      page = request.form['pgname']

      session['currentpage'] = page

      

      return redirect(url_for('go_links'))
   else:
      #function from create site button
      
      return redirect(url_for('newlinks'))

@app.route('/alllinks')
def go_links():
   page = session.get('currentpage', None)

   many_links = getlinks(page)
   
   if many_links:
      page1 = many_links[0]
      name = page1['pagename']
   else:
      name = page
   try:
      return render_template("html/page.html", many_links = many_links,name = name, url = get_url(name))
   except:
      return redirect(url_for('login_submit'))

@app.route('/newpage')
def newlinks():
   page = session.get('pagename',None)
   many_links = getlinks(page)

   if many_links:
      page1 = many_links[0]
      name = page1['pagename']
   else:
      name = page

   return render_template("html/page.html", many_links = many_links,name = name, url = get_url(name))



#function name ni ufala but it works
# where tf does this redirect to?? 
# #Thus was some function in the templates   
@app.route('/servo_pos', methods= ["POST"])
def servo_pos():
   address = request.form["name"]
   name = request.form["pagename"]
   doa = check(address)
   doa = str(doa)

   add_link(name,address)
   return jsonify(doa)

#to add a page
@app.route('/addpage', methods=["POST"])
def addpage():
   name = request.form["title"]
   #desc = request.form["desc"]
   username = request.form["username"]

   add_page(username,name)

   session['pagename'] = name

   return redirect(url_for('links'))

@app.route('/removepage', methods=["POST"])
def removepage():
   name = request.form['pagename']

   remove_page(name)

   return "done"


#another lost route
@app.route('/remove_link', methods=["POST"])
def remove_link():
   address = request.form["adress"]
   #print(address)
   remove(address)
   return "done"

@app.route('/short/<route>')
def shortened(route):
   from flask import request   
   if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
      ip = request.environ['REMOTE_ADDR']
   else:
      ip = request.environ['HTTP_X_FORWARDED_FOR']

   if session.get('currentpage',None) == "none":
      route = get_page_name('short/'+route)
      session['currentpage'] = route
   else:
      route = session.get('currentpage',None)
   links = get_working_urls(route)

   def get_link():
      rand = random.choice(links)

      if 'http' in rand:
         link = rand
      else:
         link = 'http://' + rand 

      return link
   
   link = get_link()
   while check(link) == False:
      link = get_link()
      set_dead(link,route)

   bot = antibot(ip)

   session['bot'] = bot

   print(ip)

   #print(session.get('bot', None))
   try:
      if session.get('bot', None) == True:
         return redirect("https://youtu.be/dQw4w9WgXcQ")
      elif session.get('bot', None) == False:
         return redirect(link)
   except:
      return session.get('bot', None) 


@app.route('/bitly', methods=['post','get'])
def bitly():
   name = request.form['pagename']

   if check_short(name):
      url = 'short/'

      digits = id_generator()
      shorturl = url + digits
      

      while check_avail(shorturl):  
         digits = id_generator()
         shorturl = url + digits
         update_url(name, shorturl)
      
      link = bitlyy("https://deezshorts.herokuapp.com/"+shorturl)
   else:
      short = get_short(name)
      link = bitlyy("https://deezshorts.herokuapp.com/"+short)


   return link

if __name__ == '__main__':
   app.debug = True
   app.run()
