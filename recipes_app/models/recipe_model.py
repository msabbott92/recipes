from recipes_app.config.mysqlconnection import connectToMySQL
from flask import flash
from recipes_app.models.user_model import User

class Recipe:
    db = "recipes_schema"
    def __init__(self, data):
        self.id = data["id"]
        self.name = data["name"]
        self.description = data["description"]
        self.instructions = data["instructions"]
        self.under_30 = data["under_30"]
        self.date_made = data["date_made"]
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data["user_id"]
        self.creator = None

    @classmethod
    def save(cls, data):
        query = "INSERT INTO recipes (name, description, instructions, under_30, date_made, created_at, updated_at, user_id) VALUES (%(name)s, %(description)s, %(instructions)s, %(under_30)s, %(date_made)s, NOW(), NOW(), %(user_id)s);"
        results = connectToMySQL(cls.db).query_db(query,data)
        return results
    
    @staticmethod
    def validate_recipe(data):
        is_valid = True

        if len(data['name']) < 2:
            flash("Name must be at least 3 characters long")
            is_valid = False
        if len(data['description']) < 2:
            flash("Please give a valid description")
            is_valid = False
        if len(data['instructions']) < 2:
            flash("Please provide valid instructions")
        if "under_30" not in data:
            flash("Please select a cook time")
            is_valid = False
        if data["date_made"] == "":
            flash("Please select when meal was created")
            is_valid = False
        return is_valid
    
    @classmethod
    def get_all_recipes(cls):
        query = "SELECT * FROM recipes JOIN users on recipes.user_id = users.id"
        results = connectToMySQL(cls.db).query_db(query)
        all_recipes = []
        for row in results:
            recipe_by_user = cls(row)
            user_info = {
                "id":row["users.id"],
                "first_name": row["first_name"],
                "last_name": row["last_name"],
            }
            recipe_by_user.creator = user_info
            all_recipes.append(recipe_by_user)
        return all_recipes
    
    @classmethod
    def get_recipe_by_id(cls, data):
        print(data)
        query = "SELECT * FROM recipes JOIN users on recipes.user_id = users.id WHERE recipes.id = %(id)s"
        results = connectToMySQL(cls.db).query_db(query, data)
        return cls(results[0])

    @classmethod
    def update_recipe(cls, data):
        query = " UPDATE recipes SET name = %(name)s, description = %(description)s, instructions = %(instructions)s, under_30 = %(under_30)s, date_made = %(date_made)s WHERE id = %(id)s"
        return connectToMySQL(cls.db).query_db(query, data)
    
    @classmethod
    def delete_recipe(cls, data):
        query = "DELETE FROM recipes WHERE id = %(id)s"
        return connectToMySQL(cls.db).query_db(query, data)

    