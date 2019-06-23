from flask import render_template, flash, redirect, url_for
from backend import app
from backend.forms import LoginForm

# login
from flask_login import current_user, login_user, logout_user, login_required
from backend.models import User

# redirect to "next" page
from flask import request
from werkzeug.urls import url_parse

# user registration
from backend import db
from backend.forms import RegistrationForm

# recommendation
from backend.forms import FoodTypeForm

@app.route('/')
@app.route('/index')
@login_required
def index():
    user = {'username': 'Miguel'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title='Home', posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/recommend', methods=['GET', 'POST'])
def recommend():
    # method for accessing data (duplicate)
    def access_new_json(path):
        import os
        import json

        path = os.path.join(os.getcwd(), path)
        with open(path, 'r') as file:
            content = file.read()
        data = json.loads(content.encode('utf-8'))
        return data


    # method for sub-obtimal recommendation
    def recommend_by_nutrient(base, data, num, n_type):
        if num == 0: 
            return list(), base
#
        from random import shuffle
#   
        random_list = access_new_json("api_code/new_foods_ratings.json")
        #sorted_list = sorted(random_list, key = lambda k:k[n_type])
        shuffle(random_list)

        base_div = [base['fat'] / num, base['proteins'] / num, base['carbohydrates'] / num]    

        result = list()
        for i in range(len(random_list)):
            entry = dict()
            entry['name']      = random_list[i]['name']
            entry['nutrients'] = data[entry['name']]

            if data[entry['name']][n_type] < 1e-9:
                continue

            entry['serving']   = min([base_div[0]*0.66 / (data[entry['name']]['fat'] + 0.01),
                                      base_div[1]*0.66 / (data[entry['name']]['proteins'] + 0.01),
                                      base_div[2]*0.66 / (data[entry['name']]['carbohydrates'] + 0.01)])

            entry['serving']   = min([500, entry['serving']])
            entry['serving']   = max([0, entry['serving']])

            # modify base value again
            base['fat']             = base['fat']           - entry['serving'] * data[entry['name']]['fat'] 
            base['proteins']        = base['proteins']      - entry['serving'] * data[entry['name']]['proteins'] 
            base['carbohydrates']   = base['carbohydrates'] - entry['serving'] * data[entry['name']]['carbohydrates']

            result.append(entry)
            if (len(result) == num):
                break
        return result, base

    number_of_people = 1
    fat_rec = list()
    pro_rec = list()
    carb_rec = list()

    form = FoodTypeForm()
    if form.validate_on_submit():
        base = access_new_json("api_code/categories.json")[0] # dict()
        data = access_new_json("api_code/new_foods.json")  # dict(dict())

        number_of_people = int(form.estimated_number.data)
        fat_num = int(form.fat_num.data)
        pro_num = int(form.pro_num.data)
        carb_num = int(form.carb_num.data)

        loss    = 1e19
        
        for ite in range(1000):
            base_temp = base.copy()
            # fat
            fat_rec_temp, base_temp = recommend_by_nutrient(base_temp, data, fat_num, 'fat')
            # proteins
            pro_rec_temp, base_temp = recommend_by_nutrient(base_temp, data, pro_num, 'proteins')
            # carbs
            carb_rec_temp, base_temp = recommend_by_nutrient(base_temp, data, carb_num, 'carbohydrates')
            
            # calculate loss
            cur_loss = base_temp['fat'] + base_temp['proteins'] + base_temp['carbohydrates']
            if cur_loss < loss:
                loss = cur_loss
                fat_rec = fat_rec_temp.copy()
                pro_rec = pro_rec_temp.copy()
                carb_rec = carb_rec_temp.copy()

        for i1 in range(fat_num):
            fat_rec[i1]['serving'] = fat_rec[i1]['serving'] * number_of_people
        for i2 in range(pro_num):
            pro_rec[i2]['serving'] = pro_rec[i2]['serving'] * number_of_people
        for i3 in range(carb_num):
            carb_rec[i3]['serving'] = carb_rec[i3]['serving'] * number_of_people

    return render_template('recommend.html', title='Recommendation', form=form, fat_rec=fat_rec, pro_rec=pro_rec, carb_rec=carb_rec)


@app.route('/api/test')
def get_data():
    return {'test': 'test1',
            'testa': 'testa1'}
