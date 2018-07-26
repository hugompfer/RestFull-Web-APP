
from flask_restful import Resource
from flask import request, jsonify, make_response
from api.models import User
from api.models import Project
from api.models import Task
from api.maiin import app
from flask_login import LoginManager
from flask_login import login_user, current_user,login_required,logout_user
from flask_restful import Api
from api.validators import *

login_manager = LoginManager()
login_manager.app=app
login_manager.init_app(app)
login_manager.login_view = 'login'

"""define the user_loader method"""
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


"""Class to handle the / requests, its possible use GET methods"""
class Initial(Resource):
    @login_required
    def get(self):
        return app.send_static_file('dashboard.html')


"""Class to handle the /login/ requests, its possible use GET methods"""
class Login(Resource):
    def get(self):
        return app.send_static_file('login.html')


"""Class to handle the /dashboard/ requests, its possible use GET methods"""
class Dashboard(Resource):
    @login_required
    def get(self):
        return app.send_static_file('dashboard.html')


"""Class to handle the /api/user/login/ requests, its possible use POST methods"""
class LoginAPI(Resource):
    def post(self):
        data = request.get_json()
        user = User.get_user(data["username"])
        if user:
            if user.password == data["password"]:
                login_user(user, remember=True)
                return make_response(jsonify({'redirect':'/dashboard'}),200)
        return make_response(jsonify({'credentials': 'Credenciais erradas'}),404)


"""Class to handle the /api/user/logout/ requests, its possible use GET methods"""
class Logout(Resource):
    @login_required
    def get(self):
        logout_user()
        return make_response(jsonify({'redirect':'/login'}),200)


"""Class to handle the /api/user/ requests,its possible use PUT/GET methods"""
class UserAPI(Resource):
    @login_required
    def get(self):
        user = load_user(current_user.id)
        return make_response(jsonify(user.serialize))

    @login_required
    def put(self):
        data = request.get_json()
        user = User.get_user(data["username"])
        if user == None or user.id==current_user.id:
            if user.id==current_user.id:
                if not validateEmail(data["email"]):
                    return make_response(jsonify({'email': 'Email inválido!'}), 400)
                result=User.update_user(current_user.id,data)
                if result:
                    return make_response(jsonify({'result': 'Informacao alterada'}),200)
                return make_response(jsonify({'error': 'Ocorreu um erro! Tente de outra vez!'}), 500)
            return make_response(jsonify({'account': 'Não tem acesso a esta conta'}), 403)
        return make_response(jsonify({'username': 'Username ja utilizado!'}), 400)


"""Class to handle the /api/user/register requests, its possible use POST methods"""
class RegisterAPI(Resource):
    def post(self):
        data = request.get_json()
        user = User.get_user(data["username"])
        if user==None:
            if not validateEmail(data["email"]):
                return make_response(jsonify({'email': 'Email inválido!'}), 400)
            else:
                result = User.add_user(data)
                if result :
                    return make_response(jsonify({'redirect': '/login'}), 200)
                return make_response(jsonify({'error': 'Ocorreu um erro no registo. Tente outra vez.'}), 500)
        return make_response(jsonify({'username': 'Username já utilizado!'}), 400)


"""Class to handle the /api/projects/ requests, its possible use POST/GET methods"""
class ProjectsAPI(Resource):
    @login_required
    def get(self):
        projects=Project.getProjects(current_user.id)
        return make_response(jsonify(projects), 200)

    @login_required
    def post(self):
        data = request.get_json()
        project = Project.getProjectByName(data["name"],current_user.id)
        id=current_user.id
        if project == None:
            result = Project.add_project(current_user.id, data)
            if result:
                return make_response(jsonify({'result': 'Projeto criado com sucesso!'}), 201)
            return make_response(jsonify({'error': 'Ocorreu um erro! Tente outra vez!'}), 200)
        return make_response(jsonify({'name': 'Ja tem um nome de projeto igual a este!'}), 400)


"""Class to handle the /api/project/<id> requests, its possible use PUT/GET/DELETE methods"""
class ProjectAPI(Resource):
    @login_required
    def get(self,idProject):
        project = Project.getProject(idProject,current_user.id)
        if project != None :
            return make_response(jsonify(project), 200)
        return make_response(jsonify({'project': 'Projeto nao encontrado!'}), 404)#meter no site

    @login_required
    def put(self,idProject):
        data = request.get_json()
        project = Project.getProject(idProject,current_user.id)
        if project != None :
            result = Project.update_project(idProject, data)
            if result :
                return make_response(jsonify({'result': 'Projeto atualizado com sucesso!'}), 200)
            return make_response(jsonify({'error': 'Ocorreu um erro! Tente outra vez!'}), 500)
        return make_response(jsonify({'project': 'Projeto nao encontrado!'}), 404)

    @login_required
    def delete(self,idProject):
        project = Project.getProject(idProject,current_user.id)
        if project != None :
            result =Project.delete_project(idProject)
            if result:
                return make_response(jsonify({'result': 'Projeto removido com sucesso!'}), 200)
            return make_response(jsonify({'error': 'Ocorreu um erro! Tente outra vez!'}), 500)
        return make_response(jsonify({'project': 'Projeto nao encontrado!'}), 404)


"""Class to handle the /api/project/<id>/tasks/ requests, its possible use POST/GET methods"""
class TasksAPI(Resource):
    @login_required
    def get(self,idProject):
        project = Project.getProject(idProject,current_user.id)
        if (project != None):
            tasks=Task.getTasks(idProject)
            return make_response(jsonify(tasks), 200)
        return make_response(jsonify({'task': 'Task nao encontrada!'}), 404)

    def post(self,idProject):
        data = request.get_json()
        task=validateTask(data,idProject)
        if task==None:
            return make_response(jsonify({'fields': 'Existem campos mal preenchidos!'}), 400)
        else:
            result = Task.add_task(idProject,data)
            if result:
                return make_response(jsonify({'result': 'Task adicionada com sucesso!'}), 200)
            return make_response(jsonify({'error': 'Ocorreu um erro! Tente de outra vez!'}), 500)


"""Class to handle the /api/project/<id>/tasks/<id> requests, its possible use PUT/GET/DELETE methods"""
class TaskAPI(Resource):
    @login_required
    def get(self,idProject,idTask):
        project = Project.getProject(idProject,current_user.id)
        task = Task.getTask(idProject, idTask)
        if project != None and task!=None:
            return make_response(jsonify(task), 200)
        return make_response(jsonify({'task': 'Task nao encontrada!'}), 403)

    @login_required
    def put(self,idProject,idTask):
        project = Project.getProject(idProject,current_user.id)
        if project != None :
            data = request.get_json()
            task = validateTask(data, idProject)
            if task == None:
                return make_response(jsonify({'fields': 'Existem campos mal preenchidos!'}), 400)
            else:
                task = Task.getTask(idProject, idTask)
                if task != None:
                    result=Task.update_task(idTask,data,idProject)
                    if result:
                        return make_response(jsonify({'result': 'Task atualizada com sucesso!'}), 200)
                    return make_response(jsonify({'error': 'Ocorreu um erro! Tente de outra vez!'}), 500)
        return make_response(jsonify({'task': 'Task nao encontrada!'}), 404)

    @login_required
    def delete(self,idProject,idTask):
        project = Project.getProject(idProject,current_user.id)
        if project != None :
            task = Task.getTask(idProject, idTask)
            if task != None:
                result = Task.delete_task(idProject,idTask)
                if result:
                    return make_response(jsonify({'result': 'Task removida com sucesso!'}), 200)
                return make_response(jsonify({'error': 'Ocorreu um erro! Tente de outra vez!'}), 500)
        return make_response(jsonify({'task': 'Task nao encontrada!'}), 404)


"""Define the routes"""
api = Api(app)
api.add_resource(Initial, '/', endpoint = 'initial')
api.add_resource(Login, '/login', endpoint = 'login')
api.add_resource(Dashboard, '/dashboard', endpoint = 'dashboard')
api.add_resource(UserAPI, '/api/user/', endpoint = 'user')
api.add_resource(LoginAPI, '/api/user/login/', endpoint = 'loginapi')
api.add_resource(Logout, '/api/user/logout/', endpoint = 'logout')
api.add_resource(RegisterAPI, '/api/user/register/', endpoint = 'register')
api.add_resource(ProjectsAPI, '/api/projects/', endpoint = 'projects')
api.add_resource(ProjectAPI, '/api/projects/<idProject>/', endpoint = 'project')
api.add_resource(TasksAPI, '/api/projects/<idProject>/tasks/', endpoint = 'tasks')
api.add_resource(TaskAPI, '/api/projects/<idProject>/tasks/<idTask>/', endpoint = 'task')