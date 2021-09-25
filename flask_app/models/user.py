
from flask_app.config.mysqlconnection import MySQLConnection
from flask import flash, session, jsonify, request
from flask_app.models.image import Image
from flask_app.models.recipe import Recipe
import os
import bcrypt
import re


class User():
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.phone = data['phone']
        self.password = data['password'] #will come from the database hashed
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.menu_id = data['menu_id']
        self.shopping_list_id = data['shopping_list_id']
        self.profile_image_id = data['profile_image_id']
        self.profile_image = Image.getProfileImage(data['profile_image_id'])
        self.favorites = Recipe.getFavoriteRecipes(data['id'])
        

    def __str__(self):
        return f" id: {self.id}, \n first_name: '{self.first_name}', \n last_name: '{self.last_name}', \n email: '{self.email}', \n phone: '{self.phone}', \n password: '{self.password}', \n created_at: {self.created_at}, \n upated_at: {self.updated_at}, \n menu_id: {self.menu_id}, \n shopping_list_id: {self.shopping_list_id}, \n profile_image_id: {self.profile_image_id}, \n  profile_image: {self.profile_image} favorites: {self.favorites}"
    
    @classmethod
    def validateLogin(cls, data):
        print("Data Recieved from Login: ", data)

        user = cls.getUserByEmail(data['email'])

        if user:
            password = cls.checkMatchPW(data['password'], user.password)
            if password:
                session['user_id'] = user.id
                return user
        return False

    @classmethod
    def registerUser(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password, phone, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, %(phone)s, NOW(), NOW())"

        #Adds User Data to session to keep data fields if registration fails: 
        session['first_name'] = data['first_name']
        session['last_name'] = data['last_name']
        if 'email' in data:
            session['email'] = data['email']
        if 'phone' in data:
            session['phone'] = data['phone']
        if 'country_code' in data:
            session['country_code'] = data['country_code']

        #Checks for valid registration and throws flash messages. Returns False if errors are found
        is_valid = cls.validateRegistration(data)

        if is_valid: 
            #hash Password before adding to database: 
            data["password"] = cls.hashPW(data['password'])
            data['phone'] = f"{data['country_code']}{data['phone']}"

            id = MySQLConnection().query_db(query, data)
            print("New user created with the id : ", id)
            session['user_id'] = id
            
            return id
        else: 
            return False


#Gets user from database returns an Instance of User
    @classmethod
    def getUserById(cls, id):
        
        query = f"SELECT * FROM users LEFT JOIN images ON profile_image_id = images.id WHERE users.id = {id}"

        user_fromDB = MySQLConnection().query_db(query)

        if user_fromDB:
            user = cls(user_fromDB[0])
            print("RETRIEVING USER: ", user)
            return user
        else:
            print("Could not find user from database!")
            return False

    @staticmethod
    def hashPW(password):
        hashed = bcrypt.hashpw(bytes(password, "utf8"), bcrypt.gensalt(14))
        print(f'Password: {password}, hashed into: {hashed}')
        return hashed

    @staticmethod
    def checkMatchPW(password, hashed_pw):

        pw_check = bcrypt.checkpw(bytes(password, "utf8"), bytes(hashed_pw, 'utf8'))
        print("hashed pw check: ", pw_check )

        if not pw_check:
            flash('Incorrect Password', 'login')
        
        return pw_check 

    @classmethod
    def getUserByEmail(cls, email):
        query = f'SELECT * FROM users WHERE email = "{email}"'

        user = MySQLConnection().query_db(query)

        if user:
            return cls(user[0])
        else:
            return False

    @classmethod
    def validateRegistration(cls, data):
        is_valid = True
        if cls.validateName(data) == False:
            is_valid = False
        
        if cls.validateEmail(data) == False:
            is_valid = False
        
        if cls.validatePassword(data) == False:
            is_valid = False

        # if cls.validate_phone(data['phone'], data['country_code'])
        
        return is_valid

    @staticmethod
    def validate_phone(num, country_code): #Code not operational
        is_valid = True
        #Calling API from NumVerify
        query = f"http://apilayer.net/api/validate?access_key={os.environ.get('numverify_access_code')}&number={num}&country_code={country_code}"

        # r = request.get(query)

        # print( jsonify( r.json() ) )
        
        #  if(phone_valid['success'] == False ):
        #     flash("Invalid Phone Number", 'phone')
        #     print('Phone Validation error: ', phone_valid['error']['info'] )
        #     is_valid = False

        return is_valid

    @staticmethod
    def validateName(data):
        is_valid = True
        if len(data['first_name']) < 3:
            flash('First Name needs more than two characters', 'first_name')
            is_valid = False
        if len(data['last_name']) < 3:
            flash('Last name needs more than two characters', 'last_name')
            is_valid = False
        return is_valid

    @staticmethod
    def validateEmail(data):
        is_valid = True
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
        if( not EMAIL_REGEX.match(data['email'])):
            flash("Must enter valid email", 'email')
            is_valid = False
        return is_valid
    
    @staticmethod
    def validatePassword(data):
        is_valid = True
        if(len(data['password']) < 8):
            flash("Password must be at least 8 characters", 'password')
            is_valid = False
        if(len(data['password']) > 25):
            flash("Password must be shorter than 26 characters", 'password')
            is_valid = False
        if(data['password'] != data['confirm_password']):
            flash("Passwords do not match!", 'password')
            is_valid = False
        numberandchar = re.compile(r'^.*[0-9].*')
        if(not numberandchar.match(data['confirm_password'])):
            flash("Password must contain at least 1 number", 'password')
            is_valid = False
        return is_valid
    
    @staticmethod
    def validateProfilePhoto(data):
        is_valid = True
        if len(data['profile_picture']) > 100000:
            flash('Profile Image too large', 'profile_picture')
            is_valid = False
        return is_valid
    
    @classmethod
    def validateUser(cls, data):
        is_valid = True
        if cls.validateName(data) == False:
            is_valid = False
        
        if cls.validateEmail(data) == False:
            is_valid = False
        
        # if cls.validate_phone(data['phone'], data['country_code'])

        # if cls.validateProfilePhoto(data) == False: 
        #     is_valid = False
        
        return is_valid
        

    @classmethod
    def updateUser(cls, data):
        query = "UPDATE users SET first_name = %(first_name)s, last_name = %(last_name)s, email = %(email)s, updated_at = NOW(), profile_image_id = %(profile_image_id)s WHERE id = %(id)s"

        #checks for validation
        is_valid = cls.validateUser(data)

        data['profile_image_id'] = Image.insertImageToDB(data)

        #Update user in database
        MySQLConnection().query_db(query, data)

        return is_valid

