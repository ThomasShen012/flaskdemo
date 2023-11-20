from flask import Flask
from app import app
from user.models import User, Event


@app.route('/user/signup', methods=['POST'])
def signup():
    return User().signup()

@app.route('/user/signout')
def signout():
    return User().signout()

@app.route('/user/login', methods=['POST'])
def login():
    return User().login()

@app.route('/user/update_user', methods=['POST'])
def update_user():
    return User().update_user()
'''
@app.route('/user/update_user', methods=['POST'])
def update_user_route():
    user_obj = User()
    return user_obj.update_user()
'''
@app.route("/memberlist", methods = ['GET'])
def get_all_member():
    return User().get_all_member()

@app.route("/delete_member/<string:email>", methods = ['GET'])
def delete_member(email):
    #print("passed routes.py, reaching for User.get_all_member()")
    return User().delete_member(email)

@app.route("/get_member/<string:email>", methods = ['GET'])
def get_member(email):
    return User().get_member(email)

### testing
'''
@app.route("/test", methods = ['GET'])
def test_get_all_member():
    return User().test_get_all_member()
'''
### end testing

@app.route("/eventlist", methods = ['GET'])
def get_all_event():
    return Event().get_all_event()

@app.route("/add_event", methods = ['POST'])
def add_event():
    return Event().add_event()

@app.route("/delete_event/<string:title>", methods = ['GET'])
def delete_event(title):
    print("routes: delete event")
    return Event().delete_event(title)

@app.route("/get_event/<string:title>", methods = ['GET'])
def get_event(title):
    return Event().get_event(title)

@app.route('/update_event/<string:title>', methods=['POST', 'GET'])
def update_event(title):
    print("routes: update event")
    return Event().update_event(title)

@app.route('/search', methods=['POST'])
def search():
    return User().search()

@app.route('/event/<event_id>')
def event_details(event_id):
    return User().event_details(event_id)

@app.route("/all_event", methods = ['GET'])
def all_event():
    return User.all_event()


#embedded
@app.route("/embedded")
def embedded():
    return Event.embedded()

@app.route("/query")
def query():
    return Event.query()
