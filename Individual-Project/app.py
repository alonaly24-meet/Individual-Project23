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

def get_checked_items(user_uid):
    user_data = db.child("Users").child(user_uid).get()
    return user_data.val() or {}

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



@app.route('/', methods=["GET","POST"])
def signin():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        try:
            login_session['user'] = auth.sign_in_with_email_and_password(email, password)

            # Retrieve the user's checklist data from the database and store it in checked_items
            user_uid = login_session['user']['localId']
            user_data = db.child("Users").child(user_uid).get()
            login_session['checked_items'] = user_data.val() or {}

            return redirect(url_for('personal_page'))

        except:
            login_session.pop('checked_items', None)
            return redirect(url_for("signin"))
    else:
        return render_template("signin.html")

@app.route('/personal_page', methods=["GET", "POST"])
def personal_page():
    if 'user' in login_session:
        user_uid = login_session['user']['localId']
        checked_items = get_checked_items(user_uid)
    else:
        checked_items = {}

    if request.method == 'POST':
        item1 = request.form.get("item1")
        item2 = request.form.get("item2")
        item3 = request.form.get("item3")
        item4 = request.form.get("item4")
        item5 = request.form.get("item5")
        item6 = request.form.get("item6")
        item7 = request.form.get("item7")

        if user_uid:
            user_checklist = {
                "item1": item1,
                "item2": item2,
                "item3": item3,
                "item4": item4,
                "item5": item5,
                "item6": item6,
                "item7": item7
            }
        db.child("Users").child(user_uid).set(user_checklist)

        return redirect(url_for("survey"))
    
    return render_template("personal_page.html", checked_items=checked_items)

@app.route("/survey",methods=["GET","POST"])
def survey():
    if request.method == 'POST':
        return render_template("tips.html")
    else:
        return render_template("tips.html")

@app.route('/signout')
def signout():
    login_session['user'] = None
    auth.current_user = None
    return redirect(url_for('signin'))

#Code goes above here

if __name__ == '__main__':
    app.run(debug=True)