
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
from .forms import TeamForm

from .model import User

import base64

page = Blueprint('page', __name__)



@login_manager.user_loader
def load_user(username):
  mongo_user = mongo.db.users.find_one({"username":username})
  return User(mongo_user['username'])


@page.route('/', methods =['GET'])
def index():

  posts = mongo.db.posts.find({})

  carrusel = mongo.db.caraousel.find({})

  return render_template('home.html',posts=posts, carrusel=carrusel)


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
        return redirect('/admin/dashboard/')
    
    if super_user is None or bcrypt.check_password_hash(super_user['password'], form.password.data) != form.password.data:
      flash("are you really super user?", "danger")


  return render_template('admin/login.html', title= 'Login', form = form)

@page.route('/admin/logout/', methods =['GET', 'POST'])
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
  teamForm = TeamForm()


  posts = mongo.db.posts.find({})

  personal = mongo.db.team.find({})

  return render_template('admin/dashboard.html', form=form, posts = posts, personal = personal,  teamForm = TeamForm() )


@page.route('/admin/dashboard/post/', methods = ['GET', 'POST'])
@login_required
def new_post():
  
  form = NewPost(request.form )
  teamForm = TeamForm()
  error = None
  
  if request.method == 'POST':  
    file = request.files['file']
    file_to_b64 = base64.b64encode(file.read() )
    find_user = mongo.db.posts.insert({"email":session['username'],
                                          "title":form.title.data,
                                          "body":form.body.data,
                                          "posted_date":datetime.today(),
                                          "categoria":form.category.data,
                                          "image":file_to_b64.decode("utf-8")
              
                                          })
    flash('Nuevo Post', 'success')
    error = True
    return redirect('admin/dashboard/')


  if error is None:
    flash('error', 'danger')
    
    flash('upps...hay un problema', 'danger')
  return render_template('admin/dashboard.html', title='add problem', form=form, teamForm = teamForm)
  

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


@page.route('/admin/dashboard/uploadTeam/', methods =['GET', 'POST'])
@login_required
def teamUpload():

  teamForm = TeamForm(request.form)
  form = NewPost()


  if request.method == 'POST':
    file = request.files['file']
    file_to_b64 = base64.b64encode(file.read() )
    mongo.db.team.insert({"name":teamForm.name.data,
                          "departament":teamForm.departament.data,
                          "charge":teamForm.charge.data,
                          "phone":teamForm.phone.data,
                          "email":teamForm.email.data,
                          "image":file_to_b64.decode('utf-8') })

    flash('Personal Agregado', 'success')
    return redirect(url_for('.dashboard'))

  return render_template('admin/dashboard.html', teamForm = teamForm, form= form)



@page.route('/show/<post_id>/', methods=['GET'])
def get_post(post_id):

  post = mongo.db.posts.find_one_or_404({"title":post_id})
  return render_template('show.html', post=post)

@page.route('/plan_curricular/', methods = ['GET'])
def plan_curricular():

  return render_template('plan_curricular.html')

@page.route('/home/calendario/', methods=['GET'])
def calendario():
  return render_template('calendario.html')


@page.route('/home/programas/', methods = ['GET'])
def programas():

  return render_template('programas.html')

@page.route('/home/mision/', methods = ['GET'])
def mision():

  return render_template('mision.html')

@page.route('/home/organigrama/', methods = ['GET'])
def organigrama():
  return render_template('organigrama.html')



@page.route('/home/directorio/', methods = ['GET'])
def directorio():

  team_query = mongo.db.team.find({})

  return render_template('directorio.html', team_query = team_query)

@page.route('/home/directorio/show/<position_id>/', methods=['GET'])
def get_team(position_id):

  personal = mongo.db.team.find_one_or_404({"departament":position_id})
  return render_template('show_personal.html', personal = personal)


@page.route('/home/noticias/categoria/<category_id>/', methods = ['GET'])
def get_by_category(category_id):


  query =  mongo.db.posts.find({"category":category_id})
  in_section = category_id
   
  
  return render_template('show_category.html', query = query, in_section = in_section)


@page.route('/admin/dashboard/<post_id>/', methods = ['GET', 'POST'])
@login_required
def delete_post(post_id):

  post = mongo.db.posts.find_one_and_delete({'title':post_id})

  flash('Publicacion eliminada', 'warning')

  return redirect(url_for('.dashboard', post = post) )

@page.route('/admin/dashboard/edit/<team_id>/', methods =['GET', 'POST'])
@login_required
def update_team(team_id):

  teamForm = TeamForm(request.form)
  form = NewPost()
  if request.method == 'POST':
    file = request.files['file']
    file_to_b64 = base64.b64encode(file.read() )
    mongo.db.team.find_one_and_update({"name":team_id},
                                              {"$set":{
                                                    "name":teamForm.name.data,
                                                    "departament":teamForm.departament.data,
                                                    "charge":teamForm.charge.data,
                                                    "phone":teamForm.phone.data,
                                                    "email":teamForm.email.data,
                                                    "image":file_to_b64.decode("utf-8")
                                              } 
                                            })
    flash('Personal Actualizado', 'success')
    return redirect(url_for('.dashboard'))


  return redirect('.dashboard')



