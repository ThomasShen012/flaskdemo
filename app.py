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
    user_json = session.get('user')
    if user_json:
        user = json.loads(user_json)
        user_data = json.loads(user_json)
        user_email = user_data['email']
        return render_template('home.html', user_email=user_email)
    else:
        return render_template('home.html')

@app.route('/user/register')
def user_signup():
    return render_template('register.html')

@app.route('/user/login')
def user_login():
    User().signout()
    return render_template('login.html')

@app.route('/memberprofile')
@login_required
def memberprofile():
    user_json = session.get('user')
    if user_json:
        user = json.loads(user_json)
        user_data = json.loads(user_json)
        user_email = user_data['email']
        return render_template('memberprofile.html', user_email=user_email)
    else:
        print("user_json is NOT a thing")
        return redirect('/user/login')

@app.route('/user/update_user')
@login_required
def edit():
    user_json = session.get('user')
    if user_json:
        user = json.loads(user_json)
        return render_template('update_user.html', user=user)  # Pass the user variable to the template
    else:
        return redirect('/user/login')

@app.route('/user/showphoto')
@login_required
def showphoto():
    return render_template('showphoto.html')

@app.route('/admin')
@login_required
def admin():
    return render_template('admin.html')

@app.route("/add_event")
def admin_add_event():
    return render_template('add_event.html')

# testing, ignore this
@app.route('/test')
def test_admin():
    return render_template('test.html')

@app.route('/test_error')
def test_admin_error():
    return render_template('test_error.html')
# testing, ignore this


if __name__ == "__main__":
    app.run(debug=True)