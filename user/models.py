from flask import Flask, jsonify, request, render_template, session, redirect, Response, url_for

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

import pymongo
import json
from bson import json_util
from passlib.hash import pbkdf2_sha256
from bson.objectid import ObjectId

myclient = pymongo.MongoClient("mongodb+srv://team17:TqZI3KaT56q6xwYZ@team17.ufycbtt.mongodb.net/")
mydb = myclient.test

class User:

    def start_session(self, user):
        del user['password']
        user_json = json_util.dumps(user)
        session['logged_in'] = True
        session['user'] = user_json
        return user_json

    def signup(self):

        if request.form.get('password') != request.form.get('password_confirm'):
            return jsonify({ "error": "Confirm Password must match"}), 401

        user = {
            "name": request.form.get('name'),
            "email": request.form.get('email'),
            "password": request.form.get('password'),
            "phone": request.form.get('phone'),
            "address": request.form.get('address'),
            "gender": request.form.get('gender'),
            "birthday": request.form.get('birthday')
        }
        user['password'] = pbkdf2_sha256.encrypt(user['password'])

        user_json = json_util.dumps(user)

        if not mydb.users.find_one({ "email": user['email'] }):
            mydb.users.insert_one(user)
            return self.start_session(user)

        elif mydb.users.find_one({ "email": user['email']}): 
            return jsonify({ "error": "email address already exist"}), 400

        else:
            return jsonify({ "error": "something's wrong..."}), 400

    def signout(self):
        session.clear()
        return redirect('/')
    
    def login(self):
        user = mydb.users.find_one({
            "email": request.form.get('email')
        })

        if not user:
            return jsonify({ "error": "email not found"}), 401

        elif not pbkdf2_sha256.verify(request.form.get('password'), user['password']):
            return jsonify({ "error": "password incorrect"}), 401

        elif user and pbkdf2_sha256.verify(request.form.get('password'), user['password']):
            return self.start_session(user)
        
        return jsonify({ "error": "Something's wrong..." }), 401
        #return jsonify({ "error": "Invalid" }), 401
       
    def update_user(self):
        user_json = session.get('user')  # Get user JSON from session
        user_data = json.loads(user_json)  # Parse JSON to dictionary
        user_email = user_data['email']
        
        if not user_email:
            return jsonify({"error": "Email not found in session"}), 400
        
        update_data = {
            "name": request.form.get('name'),
            "password": pbkdf2_sha256.encrypt(request.form.get('password')),
            "phone": request.form.get('phone'),
            "address": request.form.get('address'),
            "gender": request.form.get('gender'),
            "birthday": request.form.get('birthday')
        }

        for field in ['name', 'phone', 'address', 'gender', 'birthday']:
            new_value = request.form.get(field)
            if new_value:
                update_data[field] = new_value

        # Handle password separately to hash it before updating
        new_password = request.form.get('password')
        if new_password:
            update_data['password'] = pbkdf2_sha256.encrypt(new_password)
        
        if not update_data:
            return jsonify({"error": "No fields to update"}), 400

        # Update the user information
        result = mydb.users.update_one(
            {"email": user_email},
            {"$set": update_data}            
        )

        if result.modified_count > 0:
            # Fetch and return the updated user
            updated_user = mydb.users.find_one({"email": user_email})
            del updated_user['password']
            
            # Update the session with the new user data
            session['user'] = json_util.dumps(updated_user)
            
            return json_util.dumps(updated_user)
        
        return jsonify({"error": "Update failed"}), 400
    
    def get_all_member(self):
        try:
            members = mydb.users.find({},{"name":1, "email":1})
            #print("passed models.py, reaching for db")
            return render_template('memberlist.html', members = members)
        except Exception as e:
            print("Error getting all member")
            return json_util.dumps({'error' : str(e)})

    def delete_member(self, email):
        try:
            mydb.users.delete_one({"email": email})
            return redirect('/memberlist')
        except Exception as e:
            print("Error deleting member:", str(e))
            return {'error': str(e)}

    #個別會員的資料
    def get_member(self, email):
        try:
            members = mydb.users.find({},{"name":1, "email":1})
    
            try:
                member_info = mydb.users.find_one({"email":email}, {"_id":0, "password":0})
                #test_member_json = json_util.dumps(test_member)
                print(member_info)
                return render_template('memberlist.html', members = members, member_info = member_info)

            except Exception as e:
                print("Error (inside) get member info: ", str(e))
                return json_util.dumps({'error' : str(e)})

        except Exception as e:
            print("Error (outside) get all member: ", str(e))
            return json_util.dumps({'error' : str(e)})

    ### testing    
    def is_admin(self):
        try:
            user_json = session.get('user')
            if user_json:
                user_data = json.laods(user_json)
                if user_data['email'] == 'ncumis.team17@gmail.com':
                    return render_template('test.html')
                else:
                    return render_template('test.html')
            else:
                print("user_json is null")
                return render_template("/test_error")

        except Exception as e:
            print("error")
            return json_util.dumps({'error' : str(e)})
    ### end testing

# end class User

class Event:
    def delete_event(self, title):
        try:
            mydb.events.delete_one({"title": title})
            return redirect('/eventlist')
        except Exception as e:
            print("Error deleting event:", str(e))
            return {'error': str(e)}
    
    def add_event(self):

        event = {
            "title": request.form.get('title'),
            "category": request.form.get('category'),
            "time": request.form.get('time'),
            "ticket_time": request.form.get('ticket_time'),
            "ticket_price": request.form.get('ticket_price'),
            "ticket_amount": request.form.get('ticket_amount'),
            "description": request.form.get('description'),
            "notices": request.form.get('notices')
        }

        event_json = json_util.dumps(event)
        if not mydb.events.find_one({"title":event['title']}):
            mydb.events.insert_one(event)
            return jsonify({ "success": "event added!"}), 200
            #return "<p> event added! </p>"
        else:
            return jsonify({ "error": "title already exist"}), 400
    
    def get_all_event(self):
        try:
            events = mydb.events.find({},{"_id":0, "title":1, "time":1, "category":1})
            return render_template('eventlist.html', events = events)
        except Exception as e:
            print("Error getting all event")
            return json_util.dumps({'error' : str(e)})

    #個別活動的資料
    def get_event(self, title):
        try:
            events = mydb.events.find({},{"_id":0, "title":1, "time":1, "category":1})
    
            try:
                event_info = mydb.events.find_one({"title":title}, {"_id":0})
                print(event_info)
                return render_template('eventlist.html', events = events, event_info = event_info)

            except Exception as e:
                print("Error (inside) get event info: ", str(e))
                return json_util.dumps({'error' : str(e)})

        except Exception as e:
            print("Error (outside) get all event: ", str(e))
            return json_util.dumps({'error' : str(e)})

    def update_event(self, title):
        print("modals: update event")
        event = mydb.events.find_one({"title":title}, {"_id":0})

        if request.method == 'POST':

            new_data = {
            "category": request.form.get('category'),
            "time": request.form.get('time'),
            "ticket_time": request.form.get('ticket_time'),
            "ticket_price": request.form.get('ticket_price'),
            "ticket_amount": request.form.get('ticket_amount'),
            "description": request.form.get('description'),
            "notices": request.form.get('notices')
            }

            '''
            for field in ['title', 'category', 'time', 'ticket_time', 'ticket_price', 'ticket_amount', 'description', 'notices']:
                new_value = request.form.get(field)
                if new_value:
                    new_data[field] = new_value
            '''

            print(new_data)

            if not new_data:
                return jsonify({"error": "Can't get new data"}), 400
            
            # Update the event information
            result = mydb.events.update_one(
                {"title": title},
                {"$set": new_data}            
            )

            return jsonify({"success": "models: event updated"}), 200
        
            print(result.modified_count)
            if result.modified_count > 0:
                # Fetch and return the updated user
                updated_event = mydb.events.find_one({"title":title}, {"_id":0})

                return get_event(self, title)  #回到eventlist和event_info
        
            #return jsonify({"error": "Update failed"}), 400

        return render_template('update_event.html', event = event)

        
        
        