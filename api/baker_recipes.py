from django.contrib.auth import get_user_model
from model_bakery.recipe import Recipe

from api import models

# Baker recipes
userTemplate = Recipe(
    get_user_model(),
    password='password'
)
restaurantTemplate = Recipe(models.Restaurant)
