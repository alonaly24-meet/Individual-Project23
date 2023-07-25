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

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        full_name = request.form["full_name"]
        user = { 'email': email,'password': password,'full_name': full_name}
        try:
            login_session['user']=auth.create_user_with_email_and_password(email, password)
            user_uid = login_session['user']['localId']
            db.child("Users").child(user_uid).set(user)
            return redirect(url_for('personal_page'))
        except:
            return redirect(url_for("signup"))
    else:
        return render_template('signup.html')
        
@app.route('/personal_page', methods=["GET","POST"])
def personal_page():
    return render_template("personal_page.html")


@app.route('/', methods=['GET', 'POST'])
def signin():
    if request.method=="POST":
        email = request.form['email']
        password = request.form['password']
        try:
            login_session['user']=auth.sign_in_with_email_and_password(email, password)
            return redirect(url_for('personal_page'))
        except:
            return redirect(url_for("signin"))
    else:
        return render_template("signin.html")



#Code goes above here

if __name__ == '__main__':
    app.run(debug=True)