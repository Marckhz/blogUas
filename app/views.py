
from flask import Blueprint
from flask import render_template, request, flash, session, redirect,url_for
from flask import request, jsonify


from . import mongo

import os

import pprint

from flask_login import login_required, login_user

from . import login_manager


from .forms import LoginForm

from .model import User

import base64

page = Blueprint('page', __name__)


@login_manager.user_loader
def load_user(user_id):
  mongo_user = mongo.db.users.find_one({"email":user_id })
  return User(user_id)


@page.route('/', methods =['GET', 'POST'])
def index():

  #form = LoginForm()

  #query = mongo.db.problems.find({})

  return render_template('home.html')


@page.route('/login', methods = ['GET', 'POST'])
def login():

  form = LoginForm(request.form)
  find_user = None

  if request.method == 'POST':
    find_user = mongo.db.users.find_one({"username":form.username.data,
                                        "password":form.password.data})
    if find_user is not None:
      instance_user = User(find_user['email'])
      if instance_user.email == find_user['email']:
        login_user(instance_user)
        session['username'] = instance_user.email
        print(instance_user.email)
        flash('Hemos enviado un link para su inicio de sesion', 'success') 

    if find_user is None:
      mongo.db.users.insert_one({"username":form.email.data})
      flash('Lo estamos redireccionando para completar su registro', 'primary')
      return redirect(url_for('page.register'))

  return render_template('layout.html', title= 'Login', form = form)


@page.route('/add_a_problem', methods = ['GET', 'POST'])
def add_problem():

  problemForm = ProblemForm(request.form )
  form = LoginForm()
  if request.method == 'POST':  
    file = request.files['file']
    file_to_b64 = base64.b64encode(file.read() )

    #falta un campo de descripcion
    find_user = mongo.db.problems.insert({"email":session['username'],
                    "problemName":problemForm.problem_description.data,
                    "industry":problemForm.industry.data,
                    "stage":problemForm.stage.data,
                    "company":problemForm.company.data,
                    "company_tagline":problemForm.company_tagline.data,
                    "image":file_to_b64.decode("utf-8")
              
              })
    print(file_to_b64)
  return render_template('add_problem.html', title='add problem', form=form, problemForm= problemForm)


@page.route('/admin/carousel/', methods= ['GET', 'POST'])
def upload_carousel():

  if request.method =='POST':
    file_one = request.file['file_one']
    file_one_to_b64 = base64.b64encode(file_one.read() )

    file_two = request.file['file_two']
    file_two_to_b64 = base64.b64encode(file_two.read() )
    
    file_three = request.file['file_three']
    file_three_to_b64 = base64.b64encode(file_three.read() )


    find_user = mongo.db.carousel.find_one_and_update({"username":session['username']},
                                                      {"$set":{"image_one":file_one_to_b64.decode("utf-8"),
                                                              "image_two":file_two_to_b64.decode("utf-8"),
                                                              "image_three":file_three_to_b64.decode("utf-8")
                                                            
                                                            }
                                                            })


  return render_template('admin/dashboard.html')


@page.route('/problem_description/<problem>')
def get_problem(problem):

  for index in mongo.db.users.find({}):
    email = index['email']
    for item in index['added_problems']:
      problem = item['problemName']
      industry = item['industry']
      stage = item['stage']

  return render_template('show.html', problem=problem, email = email, industry=industry, stage=stage, title='show')




