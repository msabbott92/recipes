from recipes_app import app
from recipes_app.controllers import user_controller, recipe_controller
from recipes_app.models.user_model import User
from recipes_app.models.recipe_model import Recipe



if __name__ == "__main__":
    app.run(debug=True)