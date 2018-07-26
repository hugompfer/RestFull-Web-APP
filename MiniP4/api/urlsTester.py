import os
import unittest
import json
from api.maiin import app,db
TEST_DB = 'dbTeste.db'

"""Test login requests /login"""
class TestLoginPage(unittest.TestCase):

    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
                                                os.path.join('../', TEST_DB)
        self.app = app.test_client()

    # executed after each test
    def tearDown(self):
        pass

    def test_redirect_without_login(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertIn('login', str(response.data))

    def test_login(self):
        response = self.app.get('/login', follow_redirects=True)
        self.assertIn('login', str(response.data))

    def test_login(self):
        response = self.app.get('/login', follow_redirects=True)
        self.assertIn('login', str(response.data))

"""Test register requests(api/user/register)"""
class TestRegisterRequests(unittest.TestCase):

    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../'+ TEST_DB
        self.app = app.test_client()

    # executed after each test
    def tearDown(self):
        pass

    def test_register_sucess(self):
        db.drop_all()
        db.create_all()
        response = self.app.post('/api/user/register/',data=json.dumps(dict(username="hugof", password="1", email="hugof@gmail.com",name="hugo ferreira")),content_type='application/json',follow_redirects=True)
        self.assertIn('/login', str(response.data))

    def test_register_emailError(self):
        response = self.app.post('/api/user/register/', data=json.dumps(
            dict(username="hugoo", password="1", email="@gmail.com", name="hugo ferreira")),
                                 content_type='application/json', follow_redirects=True)
        self.assertIn('email', str(response.data))

    def test_register_usernameError(self):
        response = self.app.post('/api/user/register/', data=json.dumps(
            dict(username="hugof", password="1", email="rgdfdfg@gmail.com", name="hugo ferreira")),
                                 content_type='application/json', follow_redirects=True)
        self.assertIn('username', str(response.data))

    def test_register_login(self):
        response = self.app.post('/api/user/login/', data=json.dumps(
            dict(username="hugof", password="1")),
                                 content_type='application/json', follow_redirects=True)
        self.assertIn('/dashboard', str(response.data))


"""Test requests of users (api/user)"""
class TestUserRequests(unittest.TestCase):

    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../'+ TEST_DB
        self.app = app.test_client()

    # executed after each test
    def tearDown(self):
        pass

    def test_user_information(self):
        db.drop_all()
        db.create_all()
        response = self.app.post('/api/user/register/', data=json.dumps(
            dict(username="hugof", password="1", email="rgdfdfg@gmail.com", name="hugo ferreira")),
                                 content_type='application/json', follow_redirects=True)
        response = self.app.post('/api/user/login/', data=json.dumps(
            dict(username="hugof", password="1")),
                                 content_type='application/json', follow_redirects=True)
        response = self.app.get('/api/user/',follow_redirects=True)
        self.assertIn('{"email":"rgdfdfg@gmail.com","name":"hugo ferreira","password":"1","username":"hugof"}', str(response.data))

    def test_user_update(self):
        response = self.app.post('/api/user/login/', data=json.dumps(
            dict(username="hugof", password="1")),
                                 content_type='application/json', follow_redirects=True)
        response = self.app.put('/api/user/', data=json.dumps(
            dict(username="hugof", password="1", email="hugoferreira@gmail.com", name="hugo ferreira")),
                                 content_type='application/json', follow_redirects=True)
        self.assertIn('Informacao alterada',str(response.data))

    def test_user_updateError(self):
        response = self.app.post('/api/user/register/', data=json.dumps(
            dict(username="tiago", password="1", email="tiago@gmail.com", name="Tiago")),
                                 content_type='application/json', follow_redirects=True)

        response = self.app.post('/api/user/login/', data=json.dumps(
            dict(username="hugof", password="1")),
                                 content_type='application/json', follow_redirects=True)
        response = self.app.put('/api/user/', data=json.dumps(
            dict(username="tiago", password="1", email="hugoferreira@gmail.com", name="hugo ferreira")),
                                 content_type='application/json', follow_redirects=True)
        self.assertIn('Username ja utilizado!',str(response.data))


"""Test requests of projects (api/projects..)"""
class TestProjectsRequests(unittest.TestCase):

    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../'+ TEST_DB
        self.app = app.test_client()

        response = self.app.post('/api/user/login/', data=json.dumps(
            dict(username="hugof", password="1")),
                                 content_type='application/json', follow_redirects=True)
        self.assertIn('/dashboard', str(response.data))

    # executed after each test
    def tearDown(self):
        pass

    def test_create_project(self):
        response = self.app.post('/api/projects/', data=json.dumps(
            dict(name="CD")),content_type='application/json', follow_redirects=True)
        self.assertIn('Projeto criado com sucesso!', str(response.data))

    def test_create_projectError(self):
        response = self.app.post('/api/projects/', data=json.dumps(
            dict(name="CD")),content_type='application/json', follow_redirects=True)
        self.assertIn('Ja tem um nome de projeto igual a este!', str(response.data))

    def test_getProjects(self):
        response = self.app.get('/api/projects/', follow_redirects=True)
        self.assertIn('"name":"CD"',
                      str(response.data))

    def test_getProject(self):
        response = self.app.post('/api/projects/', data=json.dumps(
            dict(name="CD")), content_type='application/json', follow_redirects=True)

        response = self.app.get('/api/projects/1/', follow_redirects=True)
        self.assertIn('"name":"CD"', str(response.data))

        response = self.app.get('/api/projects/2/', follow_redirects=True)
        self.assertIn('Projeto nao encontrado', str(response.data))

    def test_update_project(self):
        response = self.app.put('/api/projects/2/', data=json.dumps(
            dict(name="CD2")), content_type='application/json', follow_redirects=True)
        self.assertIn('Projeto nao encontrado', str(response.data))

        response = self.app.put('/api/projects/1/', data=json.dumps(
            dict(name="CD2")), content_type='application/json', follow_redirects=True)
        self.assertIn('Projeto atualizado com sucesso!', str(response.data))

    def test_delete_project(self):

        response = self.app.delete('/api/projects/2/', data=json.dumps(
            dict(name="CD2")), content_type='application/json', follow_redirects=True)
        self.assertIn('Projeto nao encontrado', str(response.data))

        response = self.app.delete('/api/projects/1/', follow_redirects=True)
        self.assertIn('Projeto removido com sucesso!', str(response.data))


"""Test requests of tasks (api/projects/<id>/tasks/..)"""
class TestTasksRequests(unittest.TestCase):

    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../'+ TEST_DB
        self.app = app.test_client()

        response = self.app.post('/api/user/login/', data=json.dumps(
            dict(username="hugof", password="1")),
                                 content_type='application/json', follow_redirects=True)
        self.assertIn('/dashboard', str(response.data))

    # executed after each test
    def tearDown(self):
        pass

    def test_task_project(self):
        response = self.app.post('/api/projects/', data=json.dumps(
            dict(name="CD")), content_type='application/json', follow_redirects=True)
        self.assertIn('Projeto criado com sucesso!', str(response.data))

        response = self.app.post('/api/projects/1/tasks/', data=json.dumps(
            dict(title="Task1", order=1, due_date="2018-09-10", completed=False,project_id=1)),
                                 content_type='application/json', follow_redirects=True)
        self.assertIn('Task adicionada com sucesso!', str(response.data))

        response = self.app.get('/api/projects/1/tasks/', follow_redirects=True)
        self.assertIn('"title":"Task1"', str(response.data))

        response = self.app.get('/api/projects/1/tasks/1', follow_redirects=True)
        self.assertIn('"title":"Task1"', str(response.data))

        response = self.app.get('/api/projects/1/tasks/2', follow_redirects=True)
        self.assertIn('nao encontrada', str(response.data))

        response = self.app.put('/api/projects/1/tasks/1/',data=json.dumps(
            dict(title="Task2", order=2, due_date="2018-09-10", completed=False,project_id=1)),
                                 content_type='application/json', follow_redirects=True)
        self.assertIn('Task atualizada com sucesso!', str(response.data))

        response = self.app.put('/api/projects/1/tasks/2/', data=json.dumps(
            dict(title="Task2", order=2, due_date="2018-09-10", completed=False, project_id=1)),
                                content_type='application/json', follow_redirects=True)
        self.assertIn('nao encontrada', str(response.data))

        response = self.app.put('/api/projects/1/tasks/1/', data=json.dumps(
            dict(title="Task2", order="fsdf", due_date="2018-09-10", completed=False, project_id=1)),
                                content_type='application/json', follow_redirects=True)
        self.assertIn('Existem campos mal preenchidos!', str(response.data))

        response = self.app.delete('/api/projects/1/tasks/2/', follow_redirects=True)
        self.assertIn('nao encontrada', str(response.data))

        response = self.app.delete('/api/projects/1/tasks/1/', follow_redirects=True)
        self.assertIn('Task removida com sucesso!', str(response.data))


if __name__ == "__main__":
    unittest.main()