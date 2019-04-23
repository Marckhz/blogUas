
from flask import Blueprint
from flask import render_template, request, flash, session, redirect,url_for
from flask import request, jsonify


from . import mongo
from . import bcrypt
from datetime import datetime


import os

import pprint

from flask_login import login_required, login_user

from . import login_manager


from .forms import LoginForm
from .forms import NewPost

from .model import User

import base64

page = Blueprint('page', __name__)


@login_manager.user_loader
def load_user(username):
  mongo_user = mongo.db.users.find_one({"username":username})
  return User(mongo_user['username'])


@page.route('/', methods =['GET', 'POST'])
def index():

  posts = mongo.db.posts.find({})


  return render_template('home.html',posts=posts )


@page.route('/admin/login/', methods = ['GET', 'POST'])
def login():

  form = LoginForm(request.form)
  super_user = None

  if request.method == 'POST':
    super_user = mongo.db.superusers.find_one({"username":form.username.data})

    if super_user is not None:
      if bcrypt.check_password_hash(super_user['password'], form.password.data):
        user_obj = User(super_user['username'])
        user_obj.is_authenticated = True
        login_user(user_obj)
        print(user_obj.username)
        session['username'] = user_obj.username
        flash('Login sucessful', 'success')
        return render_template('home.html')
    
    if super_user is None or bcrypt.check_password_hash(super_user['password'], form.password.data) != form.password.data:
      flash("are you really super user?", "danger")


  return render_template('admin/login.html', title= 'Login', form = form)

@page.route('/admin/logout', methods =['GET', 'POST'])
@login_required
def logout():

  user_obj = current_user
  user_obj.is_authenticated = False
  logout_user()

  return render_template('admin/login.html')



@page.route('/admin/dashboard/', methods=['GET', 'POST'])
@login_required
def dashboard():

  form = NewPost()

  return render_template('admin/dashboard.html', form=form)


@page.route('/admin/dashboard/post/', methods = ['GET', 'POST'])
@login_required
def new_post():
  
  form = NewPost(request.form )
  error = None
  
  if request.method == 'POST':  
    file = request.files['file']
    file_to_b64 = base64.b64encode(file.read() )
    find_user = mongo.db.posts.insert({"email":session['username'],
                                          "title":form.title.data,
                                          "body":form.body.data,
                                          "posted_date":datetime.now(),
                                          "image":file_to_b64.decode("utf-8")
              
                                          })
    flash('Nuevo Post', 'success')
    error = True
    return redirect('admin/dashboard/')


  if error is None:
    flash('error', 'danger')
    
    flash('upps...hay un problema', 'danger')
  return render_template('admin/dashboard.html', title='add problem', form=form,)
  



@page.route('/admin/dashboard/caraousel/', methods= ['GET', 'POST'])
@login_required
def upload_carousel():

  error = None

  if request.method =='POST':
    file_one = request.files['file_one']
    file_one_to_b64 = base64.b64encode(file_one.read() )

    file_two = request.files['file_two']
    file_two_to_b64 = base64.b64encode(file_two.read() )
    
    file_three = request.files['file_three']
    file_three_to_b64 = base64.b64encode(file_three.read() )

    if mongo.db.caraousel.find_one({"username":session['username']}):
      mongo.db.caraousel.find_one_and_update({"username":session['username']},
                                                        {"$set":{"image_one":file_one_to_b64.decode("utf-8"),
                                                                "image_two":file_two_to_b64.decode("utf-8"),
                                                                "image_three":file_three_to_b64.decode("utf-8")
                                                              
                                                              }
                                                              })
      flash('Nuevo carrusel', 'success')
      error = True
      return redirect('admin/dashboard/')
    else:
      mongo.db.caraousel.insert({"username":session['username'],
                              "image_one":file_one_to_b64.decode("utf-8"),
                              "image_two":file_two_to_b64.decode("utf-8"),
                              "image_three":file_three_to_b64.decode("utf-8")
                              })
    if error is None:
      flash('algo salio mal', 'danger')

  return render_template('admin/dashboard.html')


@page.route('/blog/posts/int:<_id>')
def get_problem(problem):

  for index in mongo.db.users.find({}):
    email = index['email']
    for item in index['added_problems']:
      problem = item['problemName']
      industry = item['industry']
      stage = item['stage']

  return render_template('show.html', problem=problem, email = email, industry=industry, stage=stage, title='show')



