import re
from api.models import Task
from datetime import datetime

"""check if email is valid"""
def validateEmail(email):
    match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', email)
    return not match==None

"""check if task data is valid"""
def validateTask(data,idProject):
    try:
        task = Task(title=data["title"], order=int(data['order']), due_date=datetime.strptime(data['due_date'], '%Y-%m-%d'),
                    completed=data['completed'], creation_date=datetime.now(), project_id=idProject)
        return task
    except:
        return None