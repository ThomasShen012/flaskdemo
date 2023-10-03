from flask import Flask
from app import app
from user.models import User


@app.route('/user/signup', methods=['POST'])
def signup():
    return User().signup()

@app.route('/user/signout')
def signout():
    return User().signout()

@app.route('/user/login', methods=['POST'])
def login():
    return User().login()
'''
@app.route('/user/update_user', methods=['POST'])
def update_user():
    return User().update_user()
'''
@app.route('/user/update_user', methods=['POST'])
def update_user_route():
    user_obj = User()
    return user_obj.update_user()

@app.route('/showmember', methods=['GET'])
def show_member():
    return User().show_member()


@app.route("/questions", methods = ['GET'])
def questions():
    print("passed routes.py, reaching for User.question")
    return User().question()
    