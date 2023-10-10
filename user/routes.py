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

@app.route("/admin", methods = ['GET'])
def get_all_member():
    return User().get_all_member()

### testing
@app.route("/test", methods = ['GET'])
def test_get_all_member():
    return User().test_get_all_member()
### end testing