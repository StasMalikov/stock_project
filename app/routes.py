import os
from app import app
from flask import render_template, flash, redirect, url_for, request
from app.db_utils import DbUtils
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from app.utils import Utils


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html',)

@app.route('/test')
def test():
    return render_template('test.html',)

@app.route('/sign_in', methods = ['GET','POST'])
def sign_in():
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']
        p_hash = DbUtils.get_user_password(login)
        if p_hash is not None:
            if check_password_hash(DbUtils.get_user_password(login), password):
                users = DbUtils.select_users()
                return render_template('manage_users.html', users = users, len=len(users))
            else:
                return render_template('index.html', messege = "Неправильный логин или пароль")
        else:
           return render_template('index.html' , messege = "Неправильный логин или пароль") 
    else:
        return redirect(url_for('index.html'))
    users = DbUtils.select_users()
    return render_template('manage_users.html', users = users, len=len(users))

@app.route('/manage_products', methods = ['GET','POST'])
def manage_products():
    if request.method == 'POST':
        action = request.form['submit']
        if action == "Редактировать":
            prod = Utils.get_product_id(request.form['id'])
            factories = Utils.clear_select(prod.factory, DbUtils.select_factories_names()) 
            types = Utils.clear_select(prod.product_type, DbUtils.select_product_types_names()) 
            ingredients = Utils.clear_select(prod.ingridients, DbUtils.select_ingredients_name()) 
            return render_template('edit_product.html', product = prod, factories = factories, types = types, ingredients = ingredients)        

        elif action == "Удалить":
            DbUtils.delete_product(request.form['id'])

    products = Utils.get_products()
    return render_template('manage_products.html', products = products, len_p = len(products))

@app.route('/edit_product', methods = ['GET','POST'])
def edit_product():
    if request.method == 'POST':
        expiration_size = request.form['expitation_size']

        if expiration_size == "час":
            expiration  = int(request.form['expitation_value'])

        elif expiration_size == "день":
            expiration = 24*int(request.form['expitation_value'])

        elif expiration_size == "месяц":
            expiration = 730*int(request.form['expitation_value'])

        elif expiration_size == "год":
            expiration = 8760*int(request.form['expitation_value'])
        file = request.files['picture']
        if file.filename=="":
            DbUtils.update_product(request.form['id'], request.form['prod_name'],\
                                         DbUtils.select_factories_id(request.form['factory'])[0][0], \
                                         DbUtils.select_product_types_id(request.form['type'])[0][0], \
                                         request.form['calorie_content'],\
                                         expiration,\
                                         request.form['dimension'],\
                                         request.form['weight'])
        else:
            file.save(app.config['UPLOAD_FOLDER'] + file.filename)
            DbUtils.update_product_pic(request.form['id'], request.form['prod_name'], DbUtils.select_factories_id(request.form['factory'])[0][0], DbUtils.select_product_types_id(request.form['type'])[0][0],request.form['calorie_content'],expiration,request.form['dimension'],request.form['weight'],file.filename)

        DbUtils.delete_product_ingredient(request.form['id'])
        DbUtils.insert_product_ingredients(request.form['id'], request.form.getlist('ingredient[]'))

        products = Utils.get_products()
        return render_template('manage_products.html', products = products, len_p = len(products))
        
    factories = DbUtils.select_factories_names()
    types = DbUtils.select_product_types_names()
    ingredients = DbUtils.select_ingredients()
    return render_template('add_product.html', factories = factories, len_f = len(factories), types = types, len_t = len(types), ingredients = ingredients, len_i = len(ingredients))


@app.route('/add_product', methods = ['GET','POST'])
def add_product():
    if request.method == 'POST':
        if 'picture' not in request.files:
            print("error !!!!")
        file = request.files['picture']

        if file.filename == '':
            return render_template('add_product.html')
        file.save(app.config['UPLOAD_FOLDER'] + file.filename)

        expiration_size = request.form['expitation_size']

        if expiration_size == "час":
            expiration  = int(request.form['expitation_value'])

        elif expiration_size == "день":
            expiration = 24*int(request.form['expitation_value'])

        elif expiration_size == "месяц":
            expiration = 730*int(request.form['expitation_value'])

        elif expiration_size == "год":
            expiration = 8760*int(request.form['expitation_value'])

        prod_id = DbUtils.insert_product( request.form['prod_name'],\
                                         DbUtils.select_factories_id(request.form['factory'])[0][0], \
                                         DbUtils.select_product_types_id(request.form['type'])[0][0], \
                                         request.form['calorie_content'],\
                                         expiration,\
                                         request.form['dimension'],\
                                         request.form['weight'],\
                                         file.filename)

        DbUtils.insert_product_ingredients(prod_id, request.form.getlist('ingredient[]'))
        products = Utils.get_products()
        return render_template('manage_products.html', products = products, len_p = len(products))
        
    factories = DbUtils.select_factories_names()
    types = DbUtils.select_product_types_names()
    ingredients = DbUtils.select_ingredients()
    return render_template('add_product.html', factories = factories, len_f = len(factories), types = types, len_t = len(types), ingredients = ingredients, len_i = len(ingredients))


@app.route('/manage_ingredients', methods = ['GET','POST'])
def manage_ingredients():
    if request.method == 'POST':
        action = request.form['submit']
        if action == "Добавить":
            DbUtils.insert_ingredients(request.form['ing_name'], request.form['dimension'])
        elif action == "Сохранить изменения":
            DbUtils.update_ingredients(request.form['id'], request.form['ing_name'], request.form['dimension'])
        elif action == "Удалить":
            DbUtils.delete_ingredients(request.form['id'])

    ingredients = DbUtils.select_ingredients()
    return render_template('manage_ingredients.html', ingredients = ingredients, len = len(ingredients))

@app.route('/manage_product_type', methods = ['GET','POST'])
def manage_product_type():
    if request.method == 'POST':
        action = request.form['submit']
        if action == "Добавить":
            DbUtils.insert_product_types(request.form['prod_type_name'])
        elif action == "Сохранить изменения":
            DbUtils.update_product_types(request.form['id'], request.form['prod_type_name'])
        elif action == "Удалить":
            DbUtils.delete_product_types(request.form['id'])

    pr_types = DbUtils.select_product_types()
    return render_template('manage_product_type.html', product_types = pr_types, len = len(pr_types))

# -------------------------FACTORIES------------------METHODS----------------

@app.route('/edit_factory', methods = ['GET','POST'])
def edit_factory():
    if request.method == 'POST':
        action = request.form['submit']
        if action == "Изменить":
            manufacturers = DbUtils.select_manufacturers_name()
            formated_man = []
            for i in manufacturers:
                formated_man.append(i[0]) 
            return render_template('edit_factory.html', manufacturers = formated_man, id =request.form['id'], location = request.form['location'], fact_name = request.form['fact_name'], manuf_name =  request.form['manuf_name'])
        elif action == "Удалить":
            DbUtils.delete_factory(request.form['id'])
            factories = DbUtils.select_factories()
            return render_template('manage_factories.html', factories = factories, len = len(factories))
    return render_template('edit_factory.html')

@app.route('/add_factory', methods = ['GET','POST'])
def add_factory():
    if request.method == 'POST':
        DbUtils.insert_factory(request.form['location'], request.form['fact_name'], request.form['manuf_name'])
        factories = DbUtils.select_factories()
        return render_template('manage_factories.html', factories = factories, len = len(factories))
    else:     
        manufacturers = DbUtils.select_manufacturers_name()
        formated_man = []
        for i in manufacturers:
            formated_man.append(i[0]) 
        return render_template('add_factory.html', manufacturers = formated_man )

@app.route('/update_factory', methods = ['GET','POST'])
def update_factory():
    if request.method == 'POST':
        DbUtils.update_factory(request.form['id'], request.form['location'], request.form['fact_name'], request.form['manuf_name'])
    factories = DbUtils.select_factories()
    return render_template('manage_factories.html', factories = factories, len = len(factories))

@app.route('/manage_factories', methods = ['GET','POST'])
def manage_factories():
    factories = DbUtils.select_factories()
    return render_template('manage_factories.html', factories = factories, len = len(factories))

@app.route('/manage_manufacturers', methods = ['GET','POST'])
def manage_manufacturers():
    if request.method == 'POST':
        action = request.form['submit']
        if action == "Добавить":
            DbUtils.insert_manufacturer(request.form['email'], request.form['comp_name'])
        elif action == "Сохранить изменения":
            DbUtils.update_manufacturer(request.form['id'], request.form['email'], request.form['comp_name'])
        elif action == "Удалить":
            DbUtils.delete_manufacturer(request.form['id'])

    manufacturers = DbUtils.select_manufacturers()
    return render_template('manage_manufacturers.html', manufacturers = manufacturers, len=len(manufacturers))


# ----------------USERS---METHODS------------------------------------------------------------------
@app.route('/manage_users')
def manage_users():
    users = DbUtils.select_users()
    return render_template('manage_users.html', users = users, len=len(users))

@app.route('/add_user', methods = ['GET','POST'])
def add_user():
    if request.method == 'POST':
        DbUtils.insert_user(request.form['login'],request.form['password'], request.form['email'], request.form['user_type'], request.form['full_name'])
        users = DbUtils.select_users()
        return render_template('manage_users.html', users = users, len=len(users))
    return render_template('add_user.html')
    
@app.route('/update_user', methods = ['GET','POST'])
def update_user():
    if request.method == 'POST':
        password = request.form['password']
        password_hash = ""
        if password == "":
            password_hash = ""
        else:
            password_hash = generate_password_hash(request.form['password'])
        
        DbUtils.update_user(request.form['id'], request.form['login'], password_hash, request.form['email'], request.form['user_type'], request.form['full_name'])
        users = DbUtils.select_users()
        return render_template('manage_users.html', users = users, len=len(users))
    users = DbUtils.select_users()
    return render_template('manage_users.html', users = users, len=len(users))


@app.route('/edit_user', methods = ['GET','POST'])
def edit_user():
    if request.method == 'POST':
        action_type = request.form['submit']
        if action_type == "Удалить":
            DbUtils.delete_user(request.form['id'])

            users = DbUtils.select_users()
            return render_template("manage_users.html", users = users, len=len(users))
        elif action_type == "Изменить":
           return render_template('edit_user.html', id = request.form['id'],  login = request.form['login'], email= request.form['email'], full_name= request.form['full_name'], user_type= request.form['user_type'] )

    return render_template('edit_user.html')
    