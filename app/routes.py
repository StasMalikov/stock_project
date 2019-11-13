from app import app
from flask import render_template, flash, redirect, url_for, request
from app.forms import LoginForm
from app.db_utils import DbUtils
from werkzeug.security import check_password_hash

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html',)

@app.route('/sign_in', methods = ['GET','POST'])
def sign_in():
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']
        p_hash = DbUtils.get_user_password(login)
        if p_hash is not None:
            if check_password_hash(DbUtils.get_user_password(login), password):
                return render_template('users.html')
            else:
                return render_template('index.html', messege = "Неправильный логин или пароль")
        else:
           return render_template('index.html' , messege = "Неправильный логин или пароль") 
    else:
        return redirect(url_for('index.html'))
    return render_template('users.html')


@app.route('/admin_main')
def admin_main():
    return render_template('admin_main.html')
    
@app.route('/users')
def users():
    #DbUtils.insert_user("stas", "malikov", "stas@gmail.com", "admin", "stas malikov")
    return render_template('users.html')
    
@app.route('/users_select')
def users_select():
    users = DbUtils.select_users()
    return render_template('users_select.html', users = users)

@app.route('/users_insert')
def users_insert():
    pass

@app.route('/users_delete')
def users_delete():
    pass

@app.route('/users_update')
def users_update():
    pass