from flask import Flask, render_template, url_for, request, session, redirect
import json
import pymongo
from functools import wraps
from user.models import User 

app = Flask(__name__)
app.secret_key = b'kushfuii7w4y7ry47ihwiheihf8774sdf4'

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            return redirect('/')
        
    return wrap

#routes
from user import routes


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/user/register')
def user_signup():
    return render_template('register.html')

@app.route('/user/login')
def user_login():
    User().signout()
    return render_template('login.html')

@app.route('/memberprofile/')
@login_required
def dashboard():
    return render_template('memberprofile.html')

@app.route('/user/update_user')
@login_required
def edit():
    user_json = session.get('user')
    if user_json:
        user = json.loads(user_json)
        return render_template('update_user.html', user=user)  # Pass the user variable to the template
    else:
        return redirect('/login')

@app.route('/user/showphoto')
@login_required
def showphoto():
    return render_template('showphoto.html')

@app.route('/showmember')
@login_required
def showmember():
    return render_template('showmember.html')


@app.route('/questions')
def question():
    print("reaching for questions.html")
    return render_template('questions.html', questions = questions)

if __name__ == "__main__":
    app.run(debug=True)