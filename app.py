from flask import Flask
from flask import render_template
from flask import request
from flask import redirect, url_for
from models import Preference, Recipe, User, Restaurant, Recipe, Cuisine, Board, Restaurant_Pin, Recipe_Pin,Preference,db


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///MeaLitdb.sqlite3"
# db = SQLAlchemy()
db.init_app(app)
app.app_context().push()


@app.route("/", methods=["GET", "POST"])
def mealit():
    return render_template("landing.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        storeduser = User.query.filter_by(username=username).first()
        if storeduser is not None:
            users = User.query.all()
            flag = True
            for s in users:
                if s.username == username:
                    flag = False
                    if s.password == password:
                        sid = s.user_id
                        print("login sucessful redirecting to dashboard")
                        return redirect(url_for('home', user_id = sid))
                    else:
                        print(1)
                        return (redirect('/'))
            print(2)
            return (redirect('/'))
        else:
            print(3)
            return (redirect('/'))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html", message="")
    elif request.method == "POST":
        flag = False
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        email = request.form['email']
        storedusername = User.query.filter_by(username=username).first()
        if storedusername is not None:
            flag = True
            message="Username unavailable!"
        storedemail = User.query.filter_by(email=email).first()
        if storedemail is not None:
            flag = True
            message="Email already registered!"
        if (password != confirm_password):
            flag = True
            message="Passwords do not match!"
        print(flag)
        if flag:
            return render_template("register.html", message=message)
            # return render_template("error.html")
        else:
            user = User(username = username, password = password, email = email)
            db.session.add(user)
            db.session.commit()
            uid = user.user_id
            print('User successfully registered')
            return redirect(url_for('quiz', user_id = uid))

def convertor(s):
    r1 = s.replace("'","")
    r2 = r1.replace(",","")
    r3 = r2.replace("[","")
    r4 = r3.replace("]","")
    s_new =r4.split(" ")
    return s_new

@app.route("/MeaLit/<user_id>", methods=["GET", "POST"])
def home(user_id):
    if request.method == "GET":
        restaurant_list = []
        restaurants = Restaurant.query.all()
        recipes = Recipe.query.all()
        p = Preference.query.filter_by(user_id=user_id).first()
        regions = convertor(p.region)
        cuisines = convertor(p.cuisine)
        types = convertor(p.type)
        prices = convertor(p.price)
        for restaurant in restaurants:
            if restaurant not in restaurant_list:
                if restaurant.region in regions:
                    restaurant_list.append(restaurant)
                elif restaurant.cuisine in cuisines:
                    restaurant_list.append(restaurant)
                elif restaurant.type in types:
                    restaurant_list.append(restaurant)           
        return render_template("dashboard.html", restaurants=restaurant_list, recipes=recipes, user_id=user_id, p=0)
    elif request.method == "POST":
        search = request.form['name']
        search = search.title()
        f = Restaurant.query.filter_by(name=search).all()
        if len(f) != 0:
            return render_template("search.html", search=search, restaurants = f, user_id = user_id)
        else:
            f = Cuisine.query.filter_by(cuisine=search).all()
            p = Preference.query.filter_by(user_id=user_id).first()
            cuisines = convertor(p.cuisine)
            if search not in cuisines:
                cuisines.append(search)
                try:
                    p.cuisine = str(cuisines)
                except:
                    db.session.rollback()
                else:
                    db.session.commit()
                    print("getting commited")
            return render_template("search.html", search = search, restaurants = f, user_id = user_id)
    else:
        print("f")

@app.route("/MeaLit/<user_id>/popular", methods=["GET", "POST"])
def popular(user_id):
    if request.method == "GET":
        u = User.query.get(user_id)
        username = u.username
        r = Restaurant.query.all()
        recipes = Recipe.query.all()
        return render_template("dashboard.html", name=username, restaurants=r, recipes=recipes, user_id=user_id, p=1)
    elif request.method == "POST":
        search = request.form['name']
        f = Restaurant.query.filter_by(name=search).all()
        if len(f) != 0:
            return render_template("search.html", search=search, restaurants = f, user_id = user_id)
        else:
            f = Cuisine.query.filter_by(cuisine=search).all()
            return render_template("search.html", search = search, restaurants = f, user_id = user_id)
    else:
        print("f")

@app.route("/MeaLit/<user_id>/quiz",  methods=["GET", "POST"])
def quiz(user_id):
    if request.method == "GET":
        regions = []
        restaurants = Restaurant.query.all()
        for r in restaurants:
            if r.region not in regions:
                regions.append(r.region)
        return render_template("quiz.html", user_id = user_id, regions = regions)
    elif request.method == "POST":
        fname = request.form['fname']
        lname = request.form['lname']
        bio = request.form['bio']
        photo = request.form['photo']
        region = str(request.form.getlist('region'))
        cuisine = str(request.form.getlist('cuisine'))
        type = str(request.form.getlist('type'))
        price = str(request.form.getlist('price'))
        time = str(request.form.getlist('time'))
        p = Preference(user_id = user_id, region = region, cuisine = cuisine, type = type, price = price, time = time)
        try:
            user = db.session.query(User).get(user_id)
            user.fname = fname
            user.lname = lname
            user.bio = bio
            user.photo = photo
            db.session.add(p)
        except:
            db.session.rollback()
        else:
            db.session.commit()
            print("getting commited")
        return redirect(url_for('home', user_id = user_id))
    else:
        print("F")

@app.route("/MeaLit/<user_id>/restaurant/<restaurant_id>", methods=["GET", "POST"])
def view_pin_restaurant(restaurant_id,user_id):
    if request.method == "GET":
        restaurants = Restaurant.query.get(restaurant_id)
        board_list = Board.query.filter_by(user_id=user_id, rr="restaurant").all()
        return render_template("view_pin_restaurant.html", restaurants = restaurants, user_id=user_id, boards = board_list)
    elif request.method == "POST":
        print("inside restaurant save")
        board_id = request.form['board']
        pin = Restaurant_Pin(board_id=board_id, restaurant_id=restaurant_id)
        db.session.add(pin)
        db.session.commit()
        print('Pin added to the board')
        return redirect(url_for('home', user_id=user_id))


@app.route("/MeaLit/<user_id>/recipe/<recipe_id>", methods=["GET", "POST"])
def view_pin_recipe(recipe_id,user_id):
    if request.method == "GET":
        recipes = Recipe.query.get(recipe_id)
        board_list = Board.query.filter_by(user_id=user_id, rr="recipe").all()
        return render_template("view_pin_recipe.html", recipes = recipes, user_id=user_id, boards = board_list)
    elif request.method == "POST":
        board_id = request.form['board']
        pin = Recipe_Pin(board_id=board_id, recipe_id=recipe_id)
        db.session.add(pin)
        db.session.commit()
        db.session.close()
        print('Pin added to the board')
        return redirect(url_for('home', user_id=user_id))


@app.route('/MeaLit/<user_id>/restaurant/<restaurant_id>/delete/<pin_id>', methods=["GET", "POST"])
def delete_pin(user_id, restaurant_id, pin_id):
    print('in restaurant delete pin')
    p = Restaurant_Pin.query.filter_by(pin_id = pin_id).first()
    print(p)
    board_id = p.board_id
    db.session.delete(p)
    db.session.commit()
    return redirect(url_for('view_board', user_id=user_id, board_id=board_id, restaurant_id=restaurant_id, pin_id=pin_id))

@app.route('/MeaLit/<user_id>/recipe/<recipe_id>/delete/<pin_id>', methods=["GET", "POST"])
def delete_pin_recipe(user_id, recipe_id, pin_id):
    print('in recipe delete pin')
    p = Recipe_Pin.query.get(pin_id)
    Recipe_Pin.query.filter_by(pin_id = pin_id).delete()
    db.session.commit()
    board_id = p.board_id
    return redirect(url_for('view_board', user_id=user_id, board_id=board_id, recipe_id=recipe_id, pin_id=pin_id))


@app.route("/MeaLit/<user_id>/profile", methods=["GET", "POST"])
def profile(user_id):
    u = User.query.get(user_id)
    fname = u.fname
    lname = u.lname
    bio = u.bio
    b = Board.query.filter_by(user_id=user_id).all()
    return render_template("profile.html", user = u, fname=fname, lname=lname, bio=bio, user_id=user_id, boards=b)


@app.route("/MeaLit/profile/edit/<user_id>", methods=["GET", "POST"])
def edit_profile(user_id):
    if request.method == "GET":
        u = User.query.get(user_id)
        fname = u.fname
        lname = u.lname
        bio = u.bio
        return render_template("edit_profile.html", user=u, fname=fname, lname=lname, user_id=user_id)
    elif request.method == "POST":
        fname = request.form['fname']
        lname = request.form['lname']
        bio = request.form['bio']
        photo = request.form['photo']
        try:
            user = db.session.query(User).get(user_id)
            user.fname = fname
            user.lname = lname
            user.bio = bio
            user.photo = photo
            print(user.fname, user.bio)
        except:
            db.session.rollback()
        else:
            db.session.commit()
            print("getting commited")
            return redirect(url_for('profile', user_id = user_id))
    else:
        print("F")


@app.route("/MeaLit/profile/<user_id>/createboard", methods=["GET", "POST"])
def create_board(user_id):
    if request.method == "GET":
        return render_template("create_board.html", user_id=user_id)
    elif request.method == "POST":
        title = request.form['title']
        description = request.form['description']
        cover = request.form['cover']
        try:  
            is_priv = request.form['is_priv']
        except:
            is_priv = "0"
        try:  
            rr = request.form['rr']
        except:
            rr = "restaurant"

        board = Board(user_id=user_id, title=title, description=description, cover=cover, is_priv=is_priv, rr=rr)
        db.session.add(board)
        db.session.commit()
        print('Board Created')
        return redirect(url_for('profile', user_id=user_id))


@app.route("/MeaLit/profile/<user_id>/boards/<board_id>", methods=["GET", "POST"])
def view_board(user_id, board_id):
    if request.method == "GET":
        board = Board.query.get(board_id)
        pin_id_list=[]
        restaurant_list=[]
        recipe_list=[]
        if board.rr == "restaurant":
            p = Restaurant_Pin.query.filter_by(board_id=board_id).all()
            for i in p:
                pin_id_list.append(i.pin_id)
                restaurant_list.append(Restaurant.query.get(i.restaurant_id))
        if board.rr == "recipe":        
            q = Recipe_Pin.query.filter_by(board_id = board_id).all()
            for i in q:
                pin_id_list.append(i.pin_id)
                recipe_list.append(Recipe.query.get(i.recipe_id))
        return render_template("view_board.html", restaurants = restaurant_list, recipes = recipe_list, user_id=user_id, board=board, pins = pin_id_list)
    elif request.method == "POST":
        title = request.form['title']
        description = request.form['description']
        cover = request.form['cover']
        is_priv = request.form['is_priv']
        try:
            board = db.session.query(Board).get(board_id)
            board.title = title
            board.description = description
            board.cover = cover
            board.is_priv = is_priv
        except:
            db.session.rollback()
        else:
            db.session.commit()
            print("getting commited")
            return redirect(url_for('view_board', user_id = user_id, board_id=board_id))
    else:
        print('k')    


@app.route("/MeaLit/profile/<user_id>/boards/<board_id>/update", methods=["GET", "POST"])
def edit_board(user_id, board_id):
    if request.method == "GET":
        print("j")
        b = Board.query.get(board_id)
        return render_template("edit_board.html", board=b, user_id=user_id, board_id=board_id)
    elif request.method == "POST":
        title = request.form['title']
        description = request.form['description']
        cover = request.form['cover']
        try:  
            is_priv = request.form['is_priv']
        except:
            is_priv = "0"

        try:
            board = db.session.query(Board).get(board_id)
            board.title = title
            board.description = description
            board.cover = cover
            board.is_priv = is_priv
        except:
            db.session.rollback()
        else:
            db.session.commit()
            print("getting commited")
            return redirect(url_for('view_board', user_id = user_id, board_id=board_id))
    else:
        print('k')   
        

@app.route('/MeaLit/profile/<user_id>/boards/<board_id>/delete', methods=["GET", "POST"])
def delete_board(user_id, board_id):
    print('in delete')
    board = Board.query.filter_by(board_id=board_id).one()
    pins = Restaurant_Pin.query.filter_by(board_id = board_id).all()
    rpins = Recipe_Pin.query.filter_by(board_id = board_id).all()
    for pin in pins:
        db.session.delete(pin)
    for pin in rpins:
        db.session.delete(pin)

    db.session.delete(board)
    db.session.commit()
    return redirect(url_for('profile', user_id=user_id))




if __name__ == '__main__':
    app.run( debug= True, port= 8000 )




# UNUSED

@app.route("/MeaLit/<user_id>/restaurant/<restaurant_id>/save", methods=["GET", "POST"])   
def save_pin(user_id, restaurant_id):
    if request.method == "GET":
        b = Board.query.filter_by(user_id=user_id).all()
        r = Restaurant.query.get(restaurant_id)
        return render_template("save_pin.html", boards = b, restaurant=r, user_id=user_id, restaurant_id=restaurant_id)
    elif request.method == "POST":
        board_id = request.form['board']
        pin = Restaurant_Pin(board_id=board_id, restaurant_id=restaurant_id)
        db.session.add(pin)
        db.session.commit()
        print('Pin added to the board')
        return redirect(url_for('home', user_id=user_id))
    else:
        print("F")


@app.route("/MeaLit/<user_id>/recipe/<recipe_id>/save", methods=["GET", "POST"])   
def save_pin_recipe(user_id, recipe_id):
    if request.method == "GET":
        b = Board.query.filter_by(user_id=user_id).all()
        r = Recipe.query.get(recipe_id)
        return render_template("save_pin.html", boards = b, recipe=r, user_id=user_id, recipe_id=recipe_id)
    elif request.method == "POST":
        board_id = request.form['board']
        pin = Restaurant_Pin(board_id=board_id, recipe_id=recipe_id)
        db.session.add(pin)
        db.session.commit()
        print('Pin added to the board')
        return redirect(url_for('home', user_id=user_id))
    else:
        print("F")

