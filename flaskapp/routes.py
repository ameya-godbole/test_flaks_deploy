from flaskapp import app ,db ,bcrypt , api
from flask import request
from  flaskapp.models import User
from flask_login import login_user , current_user , logout_user , login_required
from flask_jsonpify import jsonify
from flask_restful import Resource 


@app.route("/")
def index():
    return jsonify({'text':'Home Page'}) 


@app.route("/register",methods=['GET','POST'])
def register():


    data = request.get_json()

    print(data)
    if request.method == 'POST':

        if current_user.is_authenticated:
            return jsonify({'status':'fail','massage':'user is already logged in'})

        # if "username" not in data['username'] or email not in data['email'] :
        #     return jsonify({'status':'fail','massage':'user name and email is requried'})

        username = data['username']
        email = data['email']
        password = data['password']
        confirm_password = data['confirm_password']


        if password != confirm_password:
            return jsonify({'status':'fail','massage':'password doesn\'t match'})

        
        user = User.query.filter_by(username=username).first()

        if user:
            return jsonify({'status': 'fail', 'message': 'User already registered.'})
        
        user = User.query.filter_by(email=email).first()

        if user:
            return jsonify({'status': 'fail', 'message': 'User already registered.'})


        hashed_passwd = bcrypt.generate_password_hash(password).decode('utf-8')

        user = User(username=username,email=email,password=hashed_passwd)
        db.session.add(user)
        db.session.commit()

        massage = f"User {username} successfully added "

        return jsonify({'status': 'success', 'message': massage})

    return jsonify({'data':'something'})


@app.route("/login",methods=['GET','POST'])
def login():
    

    data = request.get_json()

    if current_user.is_authenticated:
            return jsonify({'status':'fail','massage':'user is already logged in'})
    
    email = data['email']
    password = data['password']
    remember = data['remember']

    user = User.query.filter_by(email=form.email.data).first()
    
    if user and bcrypt.check_password_hash(user.password,password):
        login_user(user,remember=remember)
        massage = f"User {username} logged in "
        return jsonify({'status':'success','massage':massage})
    else:
        return jsonify({'status':'fail','massage':'something went wrong'})

    return jsonify({'data':'something'})

@app.route("/logout",methods=['GET','POST'])
def logout():
    logout_user()
    return  jsonify({'status':'success','massage':'logged out'})
