from recipes_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    db = "recipes_schema"
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW());"
        return connectToMySQL(cls.db).query_db(query, data)
        

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users"
        results = connectToMySQL(cls.db).query_db(query)
        users = []
        for u in results:
            users.append(cls(u))
        return users
    
    @staticmethod
    def validate_user(user): 
        is_valid = True

        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid email address!", "register")
            is_valid = False
        elif User.get_by_email(user):
            flash("Email already taken", "register")
            is_valid = False
        if len(user['first_name']) < 2:
            flash("First name is reqired", "register")
            is_valid = False
        if len(user['last_name']) < 2:
            flash("Last name is required", "register")
            is_valid = False
        if len(user['email']) < 2:
            flash("Email is required", "register")
            is_valid = False
        if user['password'] != user['confirm_password']:
            flash("Passwords don't match","register")
            is_valid = False
        return is_valid
    
    @classmethod
    def get_by_email(cls,data):
        print(data, "method")
        query = 'SELECT * FROM users WHERE email = %(email)s;'
        result = connectToMySQL(cls.db).query_db(query,data)
        return cls(result[0])
    
    @classmethod
    def get_one_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        result = connectToMySQL(cls.db).query_db(query,data)
        return cls(result[0])