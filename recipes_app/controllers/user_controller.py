from flask import render_template, request, redirect, session, flash
from recipes_app import app
from flask_bcrypt import Bcrypt  
from recipes_app.models.user_model import User
from recipes_app.models.recipe_model import Recipe


bcrypt = Bcrypt(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/register/user', methods=['POST'])
def register():
    if not User.validate_user(request.form):
        return redirect("/")
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password" : bcrypt.generate_password_hash(request.form['password'])
    }
    id = User.save(data)
    session['user_id'] = id
    return redirect("/")


@app.route('/login', methods=['POST'])
def login():
    data = {
        "email": request.form["email"],
        "password": request.form["password"]
    }
    user = User.get_by_email(data)
    if not user:
        flash("Invalid Email!", "login")
        return redirect("/")
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid Password!", "login"), 
        return redirect('/')
    session['user_id'] = user.id
    return redirect("/recipes")

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')