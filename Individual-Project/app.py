from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'

#Code goes below here
config = {
  "apiKey": "AIzaSyBdi9Ygj_BXFuKqzBZPQWkSVGfhgiO4pGE",
  "authDomain": "personal-project-crazy-crazy.firebaseapp.com",
  "projectId": "personal-project-crazy-crazy",
  "storageBucket": "personal-project-crazy-crazy.appspot.com",
  "messagingSenderId": "793628397478",
  "appId": "1:793628397478:web:bece2dcff34c9d05190967",
  "measurementId": "G-8EK7YMSC4F", "databaseURL":"https://personal-project-crazy-crazy-default-rtdb.firebaseio.com/"}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()



#Code goes above here

if __name__ == '__main__':
    app.run(debug=True)