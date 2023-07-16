from flask import render_template, request, redirect, session, flash
from recipes_app import app
from flask_bcrypt import Bcrypt  
from recipes_app.models.user_model import User
from recipes_app.models.recipe_model import Recipe

@app.route("/create_recipe", methods=['POST'])
def create_new_recipe():
    if 'user_id' not in session:
        return redirect("/")
    if not Recipe.validate_recipe(request.form):
        return redirect("/recipes/new")
    data = {
        "name" : request.form["name"],
        "description": request.form["description"],
        "instructions": request.form["instructions"],
        "under_30": request.form["under_30"],
        "date_made": request.form["date_made"],
        "user_id": session["user_id"]
    }

    Recipe.save(data)
    return redirect('/recipes')

@app.route("/recipes/new")
def new_recipe():
    if 'user_id' not in session:
        return redirect("/")
    return render_template("new_recipe.html")

@app.route("/recipe/edit/<int:id>")
def edit_recipe(id):
    if 'user_id' not in session:
        return redirect("/recipes")
    recipe = Recipe.get_recipe_by_id({"id":id})
    return render_template("edit_recipe.html", recipe = recipe)

@app.route("/recipes")
def recipes_home():
    data = {
        "id": session["user_id"]
    }
    recipes = Recipe.get_all_recipes()

    return render_template("recipes.html", user = User.get_one_by_id(data), recipes = recipes)

@app.route("/update_recipe/<int:id>", methods = ['POST'])
def update_recipe(id):
    if 'user_id' not in session:
        return redirect("/")
    if not Recipe.validate_recipe(request.form):
        return redirect(f"/recipes/edit/{id}")
    data = {
        "id": id,
        "name" : request.form["name"],
        "description": request.form["description"],
        "instructions": request.form["instructions"],
        "under_30": request.form["under_30"],
        "date_made": request.form["date_made"],
    }
    Recipe.update_recipe(data)
    return redirect("/recipes")

@app.route("/recipes/<int:id>")
def view_recipe(id):
    if 'user_id' not in session:
        return redirect("/recipes")
    data = {
        "id": session["user_id"]
    }
    return render_template("view_recipe.html", user = User.get_one_by_id(data), recipe = Recipe.get_recipe_by_id({"id":id}))

@app.route("/recipe/delete/<int:id>")
def delete_recipe(id):
    if 'user_id' not in session:
        return redirect('/')
    Recipe.delete_recipe({'id':id})
    return redirect("/recipes")




    