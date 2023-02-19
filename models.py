from flask_sqlalchemy import SQLAlchemy

# from app import db 
db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True, unique=True, nullable=False)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    fname = db.Column(db.String)
    lname = db.Column(db.String)
    photo = db.Column(db.String)
    password = db.Column(db.String, nullable=False)
    bio = db.Column(db.String)


class Preference(db.Model):
    __tablename__ = 'preference'
    pid = db.Column(db.Integer, autoincrement=True, primary_key=True, unique=True, nullable=False)
    user_id  = db.Column(db.Integer, db.ForeignKey("user.user_id"), nullable=False,  unique=True)
    region = db.Column(db.String)
    cuisine = db.Column(db.String)
    type = db.Column(db.String)
    price = db.Column(db.String)
    time = db.Column(db.String)


class Restaurant(db.Model):
    __tablename__ = 'zomato'
    restaurant_id = db.Column(db.Integer,  autoincrement=True, nullable=False, primary_key=True)
    name = db.Column(db.String, nullable=False)
    price = db.Column(db.String, nullable=False)
    cuisine = db.Column(db.String, nullable=False)
    timings = db.Column(db.String)
    city = db.Column(db.String, nullable=False)
    region = db.Column(db.String, nullable=False)
    url = db.Column(db.String, nullable=False)
    type = db.Column(db.String, nullable=False)
    rating_type = db.Column(db.String, nullable=False)
    rating = db.Column(db.Numeric, nullable=False)
    votes = db.Column(db.Integer, nullable=False)
    days_open = db.Column(db.String)
    image = db.Column(db.String, nullable=False) 


class Recipe(db.Model):
    __tablename__ = 'recipes'
    recipe_id = db.Column(db.Integer,  autoincrement=True, nullable=False, primary_key=True)
    name = db.Column(db.String, nullable=False)
    prep_time = db.Column(db.Integer, nullable=False)
    cook_time = db.Column(db.Integer, nullable=False)
    ready_time = db.Column(db.Integer, nullable=False)
    ingredients = db.Column(db.String, nullable=False)
    directions = db.Column(db.String)
    url = db.Column(db.String, nullable=False)
    image = db.Column(db.String, nullable=False) 


class Cuisine(db.Model):
    __tablename__ = 'zomato_exploded'
    id = db.Column(db.Integer,  autoincrement=True, nullable=False, primary_key=True, unique=True)
    restaurant_id = db.Column(db.Integer, nullable=True)
    name = db.Column(db.String, nullable=False)
    cuisine = db.Column(db.String, nullable=False)

   
class Board(db.Model):
    __tablename__ = 'board'
    board_id = db.Column(db.Integer, autoincrement=True, primary_key=True, unique=True, nullable=False)
    title = db.Column(db.String, unique=True, nullable=False)
    user_id  = db.Column(db.Integer, db.ForeignKey("user.user_id"), nullable=False)
    description = db.Column(db.String)
    cover = db.Column(db.String)
    is_priv = db.Column(db.Integer, nullable=False)
    rr = db.Column(db.String, nullable=False)


class Restaurant_Pin(db.Model):
    __tablename__ = 'restaurant_pins'
    pin_id = db.Column(db.Integer, autoincrement=True, primary_key=True, unique=True, nullable=False)
    board_id  = db.Column(db.Integer, db.ForeignKey("board.board_id"), nullable=False)
    restaurant_id  = db.Column(db.Integer, db.ForeignKey("zomato.restaurant_id"), nullable=False)


class Recipe_Pin(db.Model):
    __tablename__ = 'recipe_pins'
    pin_id = db.Column(db.Integer, autoincrement=True, primary_key=True, unique=True, nullable=False)
    board_id  = db.Column(db.Integer, db.ForeignKey("board.board_id"), nullable=False)
    recipe_id  = db.Column(db.Integer,  db.ForeignKey("recipes.recipe_id"), nullable=False)