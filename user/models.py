from flask import Flask, jsonify, request, render_template, session, redirect, Response, url_for
import re
from datetime import datetime
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

    def delete_member(self, member_id):
        try:
            mydb.users.delete_one({"_id": ObjectId(member_id)})
            return redirect('/memberlist')
        except Exception as e:
            print("Error deleting member:", str(e))
            return {'error': str(e)}

    #個別會員的資料
    def get_member(self, member_id):
        try:
            members = mydb.users.find({},{"name":1, "email":1})
    
            try:
                member_info = mydb.users.find_one({"_id":ObjectId(member_id)}, {"password":0})
                #test_member_json = json_util.dumps(test_member)
                print(member_info)
                return render_template('memberlist.html', members = members, member_info = member_info)

            except Exception as e:
                print("Error (inside) get member info: ", str(e))
                return json_util.dumps({'error' : str(e)})

        except Exception as e:
            print("Error (outside) get all member: ", str(e))
            return json_util.dumps({'error' : str(e)})

    def search(self):
        if request.method == 'POST':
            keyword = request.form['keyword']
            # 使用正则表达式进行模糊搜索，查询多个字段
            regex = re.compile(f'.*{keyword}.*', re.IGNORECASE)

            # 使用 $or 运算符来构建查询条件，以同时搜索 "name" 和 "email" 字段
            query = {
                "$or": [
                    {"title": regex},  # 搜索 "name" 字段
                    {"description": regex}  # 搜索 "email" 字段
                ]
            }

            results = list(mydb.events.find(query))  # 将结果转换为列表
            return render_template('search.html', results=results)

    def event_details(self, event_id):
        # 使用 event_id 检索事件的详细信息，然后将详细信息传递给模板
        event = mydb.events.find_one({"_id": ObjectId(event_id)})  # 假设您的事件具有唯一的 _id
        return render_template('event.html', event=event)


    def all_event():
        all_events = list(mydb.events.find({}, {'_id': 1, 'title': 1}))
        chinese_events = list(mydb.events.find({'category': '1'}, {'_id': 1, 'title': 1}))
        korean_events = list(mydb.events.find({'category': '2'}, {'_id': 1, 'title': 1}))
        japanese_events = list(mydb.events.find({'category': '3'}, {'_id': 1, 'title': 1}))
        western_events = list(mydb.events.find({'category': '4'}, {'_id': 1, 'title': 1}))

        return render_template('all_event.html',
                               all_events=all_events,
                               chinese_events=chinese_events,
                               korean_events=korean_events,
                               japanese_events=japanese_events,
                               western_events=western_events)

# end class User

class Event:

    def delete_event(self, event_id):
        try:
            mydb.events.delete_one({"_id": ObjectId(event_id)})
            return redirect('/eventlist')
        except Exception as e:
            print("Error deleting event:", str(e))
            return {'error': str(e)}
    
    def add_event(self):

        '''
        event = {
            "title": request.form.get('title'),
            "category": request.form.get('category'),
            "time": datetime.strptime(request.form.get('time'), '%Y-%m-%dT%H:%M'),
            "ticket_time": datetime.strptime(request.form.get('ticket_time'), '%Y-%m-%dT%H:%M'),
            "description": request.form.get('description'),
            "notices": request.form.get('notices'),
            "ticket": [{
                'name': request.form.get('ticket-type-name'),
                'price': int(request.form.get('ticket-type-price')),
                'amount': int(request.form.get('ticket-type-amount'))
            }]
        }
        '''

        title = request.form.get('title')
        category = request.form.get('category')
        time = datetime.strptime(request.form.get('time'), '%Y-%m-%dT%H:%M')
        ticket_time = datetime.strptime(request.form.get('ticket_time'), '%Y-%m-%dT%H:%M')
        description = request.form.get('description')
        notices = request.form.get('notices')
        
        ticket_types = request.form.getlist('ticket-type-name')
        ticket_prices = request.form.getlist('ticket-type-price')
        ticket_amounts = request.form.getlist('ticket-type-amount')

        print("Ticket types:", ticket_types)
        print("Ticket prices:", ticket_prices)
        print("Ticket amounts:", ticket_amounts)

        tickets = []
        for i in range(len(ticket_types)):
            ticket = {
                "name": ticket_types[i],
                "price": ticket_prices[i],
                "amount": ticket_amounts[i]
            }
            tickets.append(ticket)

        event = {
            "title": title,
            "category": category,
            "time": time,
            "ticket_time": ticket_time,
            "description": description,
            "notices": notices,
            "ticket": tickets
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
            events = mydb.events.find({},{"title":1, "time":1, "category":1})

            '''
            print(events)
            for result in events:
                print(result["title"])
                print(result["category"])
                if result["category"] == '1':
                    result["category"] = "華語"
                elif result["category"] == '2':
                    result["category"] = "韓國"
                elif result["category"] == '3':
                    result["category"] = "日本"
                elif result["category"] == '4':
                    result["category"] = "西洋"
                print(result["category"])
            print(events)
            '''

            return render_template('eventlist.html', events = events)
        except Exception as e:
            print("Error getting all event")
            return json_util.dumps({'error' : str(e)})

    #個別活動的資料
    def get_event(self, event_id):
        try:
            events = mydb.events.find({},{"title":1, "time":1, "category":1})
    
            try:
                event_info = mydb.events.find_one({"_id": ObjectId(event_id)})
                print(event_info)

                #print(event_info["category"])
                if event_info["category"] == '1':
                    event_info["category"] = "華語"
                elif event_info["category"] == '2':
                    event_info["category"] = "韓國"
                elif event_info["category"] == '3':
                    event_info["category"] = "日本"
                elif event_info["category"] == '4':
                    event_info["category"] = "西洋"
                #print(event_info["category"])

                return render_template('eventlist.html', events = events, event_info = event_info)

            except Exception as e:
                print("Error (inside) get event info: ", str(e))
                return json_util.dumps({'error' : str(e)})

        except Exception as e:
            print("Error (outside) get all event: ", str(e))
            return json_util.dumps({'error' : str(e)})

    def update_event(self, event_id):
        print("modals: update event")
        event = mydb.events.find_one({"_id": ObjectId(event_id)})

        if request.method == 'POST':
            title = request.form.get('category')
            category = request.form.get('category')
            time = datetime.strptime(request.form.get('time'), '%Y-%m-%dT%H:%M')
            ticket_time = datetime.strptime(request.form.get('ticket_time'), '%Y-%m-%dT%H:%M')
            description = request.form.get('description')
            notices = request.form.get('notices')
        
            ticket_types = request.form.getlist('ticket-type-name')
            ticket_prices = request.form.getlist('ticket-type-price')
            ticket_amounts = request.form.getlist('ticket-type-amount')

            print("Ticket types:", ticket_types)
            print("Ticket prices:", ticket_prices)
            print("Ticket amounts:", ticket_amounts)

            tickets = []
            for i in range(len(ticket_types)):
                ticket = {
                    "name": ticket_types[i],
                    "price": ticket_prices[i],
                    "amount": ticket_amounts[i]
                }
                tickets.append(ticket)

            new_data = {
                "title": title,
                "category": category,
                "time": time,
                "ticket_time": ticket_time,
                "description": description,
                "notices": notices,
                "ticket": tickets
            }

            #print(new_data)

            if not new_data:
                return jsonify({"error": "Can't get new data"}), 400

            # Update the event information
            result = mydb.events.update_one(
                {"_id": ObjectId(event_id)},
                {"$set": new_data}            
            )

            return Event.get_event(self, event_id)  #回到eventlist和event_info
            #return jsonify({"success": "models: event updated"}), 200
        
            #return jsonify({"error": "Update failed"}), 400

        return render_template('update_event.html', event = event)

        
    #embedded
    def embedded():
        if mydb.events.find({'title': "123"}):
            mydb.events.update_one({'title': "胖虎aka孩子王之世界巡迴"}, {'$unset': { 'ticket_price': "", 'ticket_amount': "" }})
            mydb.events.update_one({'title': "123"}, {'$unset': { 'ticket_price': "", 'ticket_amount': "" }})
            mydb.events.update_one({'title': "123"}, 
                {'$set': { 'ticket': [
                    {'name': "搖滾區", 'price': 3000, 'amount': 200},
                    {'name': "A區", 'price': 2100, 'amount': 200},
                    {'name': "B區", 'price': 100, 'amount': 100},
                    {'name': "C區", 'price': 2100, 'amount': 60},
                ] }})
                
            return "set"
        else:
            return "cannot find 123"

    def query():
        if mydb.events.find({'title': "Coldplay"}):
            result = mydb.events.find_one({'title': "Coldplay"})

            #print(result["category"])
            if result["category"] == '1':
                result["category"] = "華語"
            elif result["category"] == '2':
                result["category"] = "韓國"
            elif result["category"] == '3':
                result["category"] = "日本"
            elif result["category"] == '4':
                result["category"] = "西洋"
            #print(result["category"])

            print("length of ticket list: " + str(len(result["ticket"])))
            
            return render_template('query.html', result = result)
        else:
            return "cannot find 123"

    def event_ticket(self, event_id):
        # 使用 event_id 检索事件的详细信息，然后将详细信息传递给模板
        event = mydb.events.find_one({"_id": ObjectId(event_id)})  # 假设您的事件具有唯一的 _id
        return render_template('event_ticket.html', event=event)

    def create_seat(self):
        seats_data = {
            'event_id': 'your_event_id',  # 替换为活动的 event_id
            'title': '胖虎aka孩子王之世界巡迴',  # 活动标题
            'tickets': [
                {
                    'name': '空地前排站票',  # 票种名称
                    'seats': [
                        {'seat_num': i, 'status': '未售出', 'member': 'none'} for i in range(1, 11)  # 座位数量为 10
                    ]
                },
                {
                    'name': '座位前區',
                    'seats': [
                        {'seat_num': i, 'status': '未售出', 'member': 'none'} for i in range(1, 26)  # 座位数量为 25
                    ]
                },
                {
                    'name': '座位後區',
                    'seats': [
                        {'seat_num': i, 'status': '已售出', 'member': 'none'} for i in range(1, 16)  # 座位数量为 15
                    ]
                }
            ]
        }
        # 插入数据到 seat 表
        mydb.seat.insert_one(seats_data)
        return "create_seat"

    def check_ticket_availability(self):
        event_id = request.args.get('event_id')
        ticket_name = request.args.get('ticket_name')

        # 查询对应活动的对应票种是否有未售出的票
        result = mydb.seat.aggregate([
            {
                "$match": {
                    "tickets.name": ticket_name
                }
            },
            {
                "$unwind": "$tickets"
            },
            {
                "$match": {
                    "tickets.name": ticket_name,
                    "tickets.seats.status": "未售出"  # 检查座位状态不是"未售出"的情况
                }
            },
            {
                "$group": {
                    "_id": "$_id",
                    "count": {"$sum": 1}  # 统计符合条件的文档数量
                }
            },
            {
                "$project": {
                    "count": 1
                }
            }
        ])

        remaining_tickets = sum(doc['count'] for doc in result)

        # 检查是否所有票都已售罄
        is_all_sold = remaining_tickets == 0

        print(f"尚未售出的票數：{remaining_tickets}")
        return jsonify({'available': not is_all_sold})

    def checkout(self, event_id):
        # 檢查是否有現有的訂單
        user_json = session.get('user')
        user_data = json.loads(user_json)
        existing_order = mydb.orders.find_one({
            'user_name': user_data['name'],
            'order_status': 1,
            'order_expired_at': {'$gt': datetime.utcnow()}  # 訂單過期時間必須大於現在的時間
        })

        if existing_order:
            # 如果有現有訂單，檢查是否超過十分鐘
            order_expired_at = existing_order['order_expired_at']
            current_time = datetime.utcnow()
            remaining = order_expired_at - current_time
            remaining_time = max(remaining, timedelta(0))

            if remaining_time > timedelta(0):
                # 如果還在有效期內，顯示訂單資訊和剩餘時間
                return render_template('checkout.html', order_data=existing_order, remaining_time=remaining_time,
                                       name=user_data['name'], email=user_data['email'], phone=user_data['phone'])
            else:
                # 如果已超過有效期，取消訂單
                mydb.orders.update_one({'order_id': existing_order['order_id']}, {'$set': {'order_status': 0}})

                # 返回模板，顯示相應的信息
                return render_template('all_event.html')

        else:
            # 如果沒有現有訂單，創建一個新訂單
            order_id = ''.join(random.choices(string.digits, k=8))
            event = mydb.events.find_one({"_id": ObjectId(event_id)})
            area = "A區"
            seat = "1排1號"
            ticket_price = 5800
            num_tickets = 1
            total_amount = ticket_price * num_tickets

            order_created_at = datetime.utcnow()
            order_expired_at = order_created_at + timedelta(minutes=10)
            order_status = 1

            order_data = {
                "user_name": user_data['name'],
                "order_id": order_id,
                "event": event,
                "area": area,
                "seat": seat,
                "ticket_price": ticket_price,
                "num_tickets": num_tickets,
                "total_amount": total_amount,
                "order_created_at": order_created_at,
                "order_expired_at": order_expired_at,
                "order_status": order_status
            }

            mydb.orders.insert_one(order_data)

            current_time = datetime.utcnow()
            remaining = order_expired_at - current_time
            remaining_time = max(remaining, timedelta(0))

            return render_template('checkout.html', order_data=order_data, remaining_time=remaining_time,
                                   name=user_data['name'], email=user_data['email'], phone=user_data['phone'])


    def cancel_order(self):
        order_id = request.form.get('orderId')

        result = mydb.orders.update_one(
            {'order_id': order_id},
            {'$set': {'order_status': 0}}
        )

        if result.modified_count > 0:
            # 取消成功，返回成功的消息
            return jsonify({"message": "訂單已取消"})
        else:
            # 找不到相應的訂單或取消失敗，返回錯誤的消息
            return jsonify({"message": "取消訂單失敗，請檢查訂單是否存在"})

    def confirm_verification(self):
        # 在這裡添加更新訂單狀態的邏輯
        # 你可能需要從前端的請求中獲取一些數據，例如訂單編號

        # 假設你有一個叫做 order_id 的變數，代表訂單編號
        order_id = request.form.get('order_id')

        # 在這裡添加更新訂單狀態的邏輯
        # 這是一個示例，你需要根據你的實際情況進行修改
        result = mydb.orders.update_one(
            {'order_id': order_id},
            {'$set': {'order_status': 2}}  # 將訂單狀態更改為 2，表示已確認驗證
        )

        if result.modified_count > 0:
            # 更新成功，返回成功的消息
            data = {"message": "Success"}
            return render_template('recognition_correct.html', data=data)
        else:
            # 更新失敗，返回錯誤的消息
            return jsonify({"message": "訂單狀態更新失敗，請檢查訂單是否存在"})

    def generate_order_id():
        return ''.join(random.choices(string.digits, k=8))  # 生成8位數字的訂單編號

    def update_order_status():
        data = request.json
        order_id = data.get('order_id')
        new_status = data.get('new_status')

        # 在這裡根據 order_id 更新資料庫中的訂單狀態為 new_status

        # 假設使用 Flask-MongoEngine
        order = mydb.orders.objects(order_id=order_id).first()
        if order:
            order.status = new_status
            order.save()
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'error': 'Order not found'}), 404
    