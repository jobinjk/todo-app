# todo-app

Make a TODO-API using Python-Flask


create a virtual environment using code:- `virtualenv <name>`

activate virtual environment by using code:- `source virtualenv<name>/bin/activate`

enter into virtualenv using `cd virtualenv<name>`

install flask using:- `sudo pip install flask`

install rest api using:- `pip install flask-restful`

install flask-mongoengine using:- `pip install flask-mongoengine`

install `mongodb`

now lets start coding

create a python app `<name>.py`

import `flask, url_for, request, jsonify, json, redirect` you will get the required information from this url

import `UserMixin, LoginManager, login_required, login_user, logout_user, current_user` from flask_login

import `MongoEngine, DoesNotExist` from flask_mongoengine

import `generate_password_hash, check_password_hash from werkzeug.security`

import `datetime,random,string, bcrypt`

install `gunicorn` for testing pip install gunicorn

install `insomnia` for testing server client relation

run the python file in terminal using `python <name>.py`


ENDPOINT

/login; method="POST"; #to login

/signup; method="POST" #to create a new login

/logout; method="GET" #to logout from the current user

/newtask; method="POST" #to start a newtask

/delete; method="POST" #to delete a task

/getTasks; method="GET" #to get/analyse the given task

/markAsFinished; method="POST" #to mark the completed task

/edit; method="POST" #to edit an existing task
