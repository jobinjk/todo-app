from flask import Flask, jsonify, request, json, redirect, url_for, render_template
from flask_login import UserMixin, LoginManager, login_required, login_user, logout_user, current_user
from flask_mongoengine import MongoEngine, DoesNotExist
from werkzeug.security import generate_password_hash, check_password_hash
import datetime,random,string, bcrypt
from bson.objectid import ObjectId

db = MongoEngine()

app = Flask(__name__)   # creating app name

app.config['MONGODB_DB'] = 'testrun'
app.config['SECRET_KEY'] = "secret key is here !!!"
# app.config['MONGODB_HOST'] = ''
# app.config['MONGODB_PORT'] = 12345
db.init_app(app)


login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user):
    return User.objects.get(id=user)



class User(db.Document):
    date_created = db.DateTimeField(default=datetime.datetime.now, required=True)
    username = db.StringField(max_length=50, required=True)
    password = db.StringField(required=True)

    def __unicode__(self):
        return self.id

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def is_authenticated(self):
        return True

    def get_id(self):
        return unicode(self.id)

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def validate_login(password_hash, password):
        return check_password_hash(password_hash, password)

    meta = {
        'allow_inheritance': True,
        'indexes': ['-date_created', 'username'],
        'ordering': ['-date_created']
    }

class Task(db.Document):
    user = db.ReferenceField(User)
    task = db.StringField(max_length=100, required=True)
    description = db.StringField(max_length=1000, required=True)
    date_created = db.DateTimeField(default=datetime.datetime.now, required=True)
    date_completed = db.DateTimeField()
    finished = db.BooleanField(default=False)
    priority = db.StringField(max_length=50, required=True)
    # last_name = db.StringField(max_length=50)

# app.config['DEBUG'] = True
@app.route('/') # setting app route for eg 127.0.0.1:5000/<something>

def api_start(): # creating a function api_root which returns some txt to url
    try:
        if current_user:
            print True
            username = current_user.username
            return render_template('index.html', username=username) 
    except:
        return render_template('index.html', username=None) 



@app.route('/login', methods = ['POST']) # setting another route /messages methods as post

def api_login(): # creating a function api_message which gives a json data when a form is submitted in url
    data= request.get_json()

    try:
        user = User.objects.get(username=data['username'])
        if user.validate_login(user.password, data['password']):
            user_obj = User.objects.get(id=user.id)
            login_user(user_obj)
            return jsonify({'status': True})
    except DoesNotExist:
        return jsonify({'status': False})
    return jsonify({'status': False})


@app.route('/signup', methods = ['POST']) # setting another route /messages methods as post

def api_signup(): # creating a function api_message which gives a json data when a form is submitted in url
    data= request.get_json()

    print data
    try:
        data = User.objects.get(username=data['username'])
        return jsonify({'status': False})
    except DoesNotExist:

        hashed_pass = bcrypt.hashpw(str(data['password']), bcrypt.gensalt())
        user_obj = User(username=data['username'])
        user_obj.set_password(data['password'])
        user_obj.save()
    return jsonify({'status':True})


@app.route("/logout", methods=['GET'])
def api_logout():
    logout_user()
    return redirect(url_for('api_start'))



@app.route('/task') # setting another route /messages methods as post
@login_required
def api_task(): # creating a function api_message which gives a json data when a form is submitted in url
    all_tasks = Task.objects(user = current_user.id).order_by('date_created','-date_created')
    his_tasks = []
    for task in all_tasks:
        his_tasks.append({
            'task':task.task,
            'description':task.description,
            'date_created':task.date_created,
            'date_completed':task.date_completed,
            'priority':task.priority,
            'task_id':str(task.id)
            })

    return render_template('task.html',tasks=his_tasks)  


@app.route('/newtask', methods = ['POST']) # setting another route /messages methods as post
@login_required
def api_newtask(): # creating a function api_message which gives a json data when a form is submitted in url
    data= request.get_json()

    try:
        task_obj = Task()
        task_obj.user = User.objects.get(id=current_user.id)
        task_obj.task = data['task']
        task_obj.description = data['description']
        task_obj.date_completed = data['date_completed']
        task_obj.priority = data['priority']
        task_obj.save()

        # Now get all task for this user and return it
        all_tasks = Task.objects(user = current_user.id).order_by('date_created','-date_created')
        his_tasks = []
        for task in all_tasks:
            his_tasks.append({
                'task':task.task,
                'description':task.description,
                'date_created':task.date_created,
                'date_completed':task.date_completed,
                'priority':task.priority,
                'task_id':str(task.id)
                })
        return jsonify({'status':True,'tasks':his_tasks})
    except Exception as e:
        raise e
        return jsonify({'status':False})


@app.route('/delete',methods=['POST'])
@login_required
def api_delete():
    data = request.get_json()
    # Delete the particular task
    print data
    try:
        Task.objects.get(user = current_user.id, id = ObjectId(data['task_id'])).delete()

        # Now get all task for this user and return it
        all_tasks = Task.objects(user = current_user.id).order_by('date_created','-date_created')
        his_tasks = []
        for task in all_tasks:
            his_tasks.append({
                'task':task.task,
                'description':task.description,
                'date_created':task.date_created,
                'date_completed':task.date_completed,
                'priority':task.priority,
                'task_id':str(task.id)
                })
        return jsonify({'status':True,'tasks':his_tasks})
    except DoesNotExist as e:

        return jsonify({'status':False})



@app.route("/getTasks", methods=['GET'])
@login_required
def get_tasks():
    # Return all the tasks created by the <user>
    filter_ = request.args.get('filter')
    print filter_

    try:
        if filter_ == 'completed':
            tasks = Task.objects(finished=True, user=current_user.id)
        elif filter_ == 'uncompleted':
            tasks = Task.objects(finished=False, user=current_user.id)
        else:
            tasks = Task.objects(user=current_user.id)

        his_tasks = []
        for task in tasks:
            his_tasks.append({
                'task':task.task,
                'description':task.description,
                'date_created':task.date_created,
                'date_completed':task.date_completed,
                'priority':task.priority,
                'task_id':str(task.id)
                })
        return jsonify({'status':True,'tasks':his_tasks})
    except:
        return jsonify({'status':False})
                

    # try:
    #     all_tasks = Task.objects(user = current_user.id).order_by('date_created','-date_created')
    #     his_tasks = []

    #     return jsonify({'status':True,'tasks':his_tasks})
    # except Exception as e:

    return jsonify({'status':False})

@app.route('/markAsFinished',methods=['POST'])
@login_required
def markAsFinished():
    data = request.get_json()
    print data

    try:
        task_obj = Task.objects.get(user=current_user.id, id=ObjectId(data['task_id']))
        task_obj.finished = True
        task_obj.date_completed = datetime.datetime.utcnow()
        task_obj.save()

        # Now get all task for this user and return it
        all_tasks = Task.objects(user = current_user.id).order_by('date_created','-date_created')
        his_tasks = []
        for task in all_tasks:
            his_tasks.append({
                'task':task.task,
                'description':task.description,
                'date_created':task.date_created,
                'date_completed':task.date_completed,
                'priority':task.priority,
                'task_id':str(task.id)
                })
        return jsonify({'status':True,'tasks':his_tasks})
    except Exception as e:
        raise e
        return jsonify({'status':False})





@app.route('/edit', methods = ['POST']) # setting another route /messages methods as post
@login_required
def api_edittask(): # creating a function api_message which gives a json data when a form is submitted in url
    data = request.get_json()['task']
    print data

    current_task = Task.objects.get(id=ObjectId(data['task_id']), user=current_user.id)

    current_task.task = data['task']
    current_task.description = data['description']
    current_task.date_created = data['date_created']
    current_task.priority = data['priority']
    current_task.save()

    all_tasks = Task.objects(user = current_user.id).order_by('date_created','-date_created')
    his_tasks = []
    for task in all_tasks:
        his_tasks.append({
            'task':task.task,
            'description':task.description,
            'date_created':task.date_created,
            'date_completed':task.date_completed,
            'priority':task.priority,
            'task_id':str(task.id)
            })
    return jsonify({'status':True,'tasks':his_tasks})

if __name__ == '__main__':
    app.run()