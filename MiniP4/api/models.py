
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from datetime import datetime

db = SQLAlchemy()

"""Deserialize datetime object into string form for JSON processing."""
def dump_datetime(value):
    if value is None:
        return None
    return [value.strftime("%Y-%m-%d"), value.strftime("%H:%M:%S")]


"""This class defines the users table """
class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    username = db.Column(db.String(50))
    password = db.Column(db.String(50))
    projects = db.relationship('Project', backref=db.backref('user', lazy=True))

    def __repr__(self):
        return '<User %r>' % (self.name)

    """ Return object data in dicionary """
    @property
    def serialize(self):
        return {
            'name': self.name,
            'email': self.email,
            'username': self.username,
            'password': self.password
        }

    """ Return user with an username passed """
    @staticmethod
    def get_user(username):
        return User.query.filter_by(username=username).first()

    """ Add a new user """
    @staticmethod
    def add_user(data):
        try:
            new_user = User(username=data["username"], email=data["email"], password=data["password"],
                            name=data["name"])
            db.session.add(new_user)
            db.session.commit()
            return True
        except:
            return False

    """ Update the information of a certain user """
    @staticmethod
    def update_user(userId, data):
        try:
            user = User.query.filter_by(id=userId).first()
            user.name = data['name']
            user.password = data['password']
            user.email = data['email']
            user.username = data['username']
            db.session.commit()
            return True
        except:
            return False


"""This class defines the projects table """
class Project(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    name = db.Column(db.String(100))
    creation_date = db.Column(db.DateTime)
    last_updated = db.Column(db.DateTime)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    tasks = db.relationship('Task', backref=db.backref('project', lazy=True))

    def __repr__(self):
        return '<Project %r>' % (self.name)

    """ Return object data in dicionary """
    @property
    def serialize(self):
        return {
            'id':self.id,
            'name': self.name,
            'creation_date': dump_datetime(self.creation_date),
            'last_updated': dump_datetime(self.last_updated),
            'user_id':self.user_id
        }

    """ Returns all projects order by the last updated of a certain user"""
    @staticmethod
    def getProjects(user_id):
        resp = [i.serialize for i in Project.query.filter_by(user_id=user_id).order_by(Project.last_updated.desc()).all()]
        return resp

    """ Returns the information of the requested project of the certain user, from the project id given"""
    @staticmethod
    def getProject(proj_id,user_id):
        resp = Project.query.filter_by(id=proj_id).filter_by(user_id=user_id).first()
        return resp.serialize if resp!=None  else None

    """ Returns the information of the requested project of the certain user, from the project name given"""
    @staticmethod
    def getProjectByName(name,user_id):
        resp = Project.query.filter_by(name=name).filter_by(user_id=user_id).first()
        return resp.serialize if resp!=None else None

    """ Add a new project to a user """
    @staticmethod
    def add_project(idUser, data):
        try:
            project = Project(name=data['name'], creation_date=datetime.now(), last_updated=datetime.now(),
                              user_id=idUser)
            db.session.add(project)
            db.session.commit()
            return True
        except:
            return False

    """ Update the project of a user """
    @staticmethod
    def update_project(id_project, data):
        try:
            project = Project.query.filter_by(id=id_project).first()
            project.name= data['name']
            project.last_updated = datetime.now()
            db.session.commit()
            return True
        except:
            return False

    """ Delete the project of a user """
    @staticmethod
    def delete_project(project_id):
        try:
            proj = Project.query.filter_by(id=project_id).first()
            tasks = Task.query.filter_by(project_id=project_id).all()
            for task in tasks:
                db.session.delete(task)
            db.session.delete(proj)
            db.session.commit()
            return True
        except:
            return False

"""This class defines the tasks table """
class Task(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    title = db.Column(db.String(40))
    order = db.Column(db.Integer)
    creation_date = db.Column(db.DateTime)
    due_date = db.Column(db.DateTime)
    completed = db.Column(db.Boolean)
    project_id = db.Column(db.Integer,db.ForeignKey(Project.id))

    def __repr__(self):
        return '<Task %r>' % (self.title)

    """ Return object data in dicionary """
    @property
    def serialize(self):
        return {
            'id':self.id,
            'title': self.title,
            'order': self.order,
            'creation_date': dump_datetime(self.creation_date),
            'due_date': dump_datetime(self.due_date),
            'completed': self.completed,
            'project_id':self.project_id
        }

    """ Returns all tasks, order by the order field of a given project from a user"""
    @staticmethod
    def getTasks(project_id):
        resp = [i.serialize for i in Task.query.filter_by(project_id=project_id).order_by(Task.order).all()]
        return resp

    """ Returns the task requested of given project from a user"""
    @staticmethod
    def getTask(id_project,task_id):
        resp = Task.query.filter_by(id=task_id).filter_by(project_id=id_project).first()
        return resp.serialize if resp!=None  else None

    """Add new task to a project of a certain user"""
    @staticmethod
    def add_task(idProject,data):
        try:
            task=Task(title=data["title"],order=data['order'],due_date = datetime.strptime(data['due_date'], '%Y-%m-%d'),
                      completed = data['completed'],creation_date=datetime.now(),project_id=idProject)
            db.session.add(task)
            db.session.commit()
            return True
        except:
            return False

    """Update a given task from a project of a certain user"""
    @staticmethod
    def update_task(id,task,idProject):
        try:
            task_to_update = Task.query.filter_by(id=id).first()
            taskWithSameOder = Task.query.filter_by(order=task['order']).filter_by(project_id=idProject).first()
            if taskWithSameOder:
                taskWithSameOder.order=task_to_update.order

            task_to_update.title = task['title']
            task_to_update.order = task['order']
            task_to_update.due_date = datetime.strptime(task['due_date'], '%Y-%m-%d')
            task_to_update.completed = task['completed']

            project = Project.query.filter_by(id=idProject).first()
            project.last_updated=datetime.now()

            db.session.commit()
            return True
        except:
            return False

    """Delete a given task from a project of a certain user"""
    @staticmethod
    def delete_task(idProject,id):
        try:
            task_to_delete = Task.query.filter_by(id=id,project_id=idProject).first()
            db.session.delete(task_to_delete)
            db.session.commit()
            return True
        except:
            return False

"""Inicialize the admin"""
admin = Admin()
admin.add_view(ModelView(User,db.session))
admin.add_view(ModelView(Project, db.session))
admin.add_view(ModelView(Task, db.session))