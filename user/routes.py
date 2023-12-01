from flask import Flask
from app import app
from user.models import User, Event
from flask import session
import pymongo
from datetime import datetime

myclient = pymongo.MongoClient("mongodb+srv://team17:TqZI3KaT56q6xwYZ@team17.ufycbtt.mongodb.net/")
mydb = myclient.test


@app.route('/')
def home():
    user_json = session.get('user')
    if user_json:
        user = json.loads(user_json)
        user_data = json.loads(user_json)
        user_email = user_data['email']

        recent_event = list(mydb.events.find({'time': {'$gte': current_datetime}}, {'_id': 1, 'title': 1, 'time': 1}).sort("time", 1).limit(6))
        recent_sale = list(mydb.events.find({'time': {'$gte': current_datetime}}, {'_id': 1, 'title': 1, 'ticket_time': 1}).sort("ticket_time", 1).limit(6))

        return render_template('home.html',
                               user_email=user_email,
                               recent_event=recent_event,
                               recent_sale=recent_sale)
    else:
        recent_event = list(
            mydb.events.find({'time': {'$gte': current_datetime}}, {'_id': 1, 'title': 1, 'time': 1}).sort("time",
                                                                                                           1).limit(6))
        recent_sale = list(
            mydb.events.find({'time': {'$gte': current_datetime}}, {'_id': 1, 'title': 1, 'ticket_time': 1}).sort(
                "ticket_time", 1).limit(6))

        return render_template('home.html',
                               recent_event=recent_event,
                               recent_sale=recent_sale)

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

@app.route("/delete_member/<member_id>", methods = ['GET'])
def delete_member(member_id):
    #print("passed routes.py, reaching for User.get_all_member()")
    return User().delete_member(member_id)

@app.route("/get_member/<member_id>", methods = ['GET'])
def get_member(member_id):
    return User().get_member(member_id)

@app.route("/eventlist", methods = ['GET'])
def get_all_event():
    return Event().get_all_event()

@app.route("/add_event", methods = ['POST'])
def add_event():
    return Event().add_event()

@app.route("/delete_event/<event_id>", methods = ['GET'])
def delete_event(event_id):
    print("routes: delete event")
    return Event().delete_event(event_id)

@app.route("/get_event/<event_id>", methods = ['GET'])
def get_event(event_id):
    return Event().get_event(event_id)

@app.route('/update_event/<event_id>', methods=['POST', 'GET'])
def update_event(event_id):
    print("routes: update event")
    return Event().update_event(event_id)

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
@app.route("/set")
def embedded():
    return Event.embedded()

@app.route("/query")
def query():
    return Event.query()
