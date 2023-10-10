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

@app.route('/memberprofile')
@login_required
def memberprofile():
    print(session)

    user_json = session.get('user')
    if user_json:
        user = json.loads(user_json)
        user_data = json.loads(user_json)
        user_name = user_data['name']

        if user_name == 'Administrator':
            print("user_name is admin")
            #is_admin == True
            return render_template('memberprofile.html', user_name=user_name)
        else:
            print("user_name is NOT admin")
            #is_admin == False
            return render_template('memberprofile.html', user_name=user_name)
    else:
        print("user_json is NOT a thing")
        return redirect('/login')

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

@app.route('/admin')
def admin():
    #print("reaching for admin.html")
    return render_template('admin.html', members = members)

@app.route('/test')
def test_admin():
    print("reaching for test.html")
    return render_template('test.html', members = members)

if __name__ == "__main__":
    app.run(debug=True)