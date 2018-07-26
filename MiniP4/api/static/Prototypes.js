/**
 * REST Client
 *
 */

function User(name,email,password,username){
    this.name=name;
    this.email=email;
    this.password=password;
    this.username=username;
}

function Project(id,name){
    this.id=id;
    this.name=name;
}

Project.prototype.editProject=function(name){
    this.name=name;
};

function Projects(){
    this.projects=[];
}

Projects.prototype.addProject=function(project){
    this.projects.push(project);
};

Projects.prototype.getProject=function(id){
    for(var i=0;i<this.projects.length;i++){
        if(this.projects[i].id===id){
            return this.projects[i];
        }
    }
    return null;
};

function Task(id,title,order,due_date,completed){
    this.id=id;
    this.title=title;
    this.order=order;
    this.due_date=due_date;
    this.completed=completed;
}

Task.prototype.editTask=function(title,order,due_date,completed){
    this.id=id;
    this.title=title;
    this.order=order;
    this.due_date=due_date;
    this.completed=completed;
};

function Tasks(){
    this.tasks=[];
}

Tasks.prototype.addTask=function(task){
    this.tasks.push(task);
};

Tasks.prototype.getTask=function(id){
    for(var i=0;i<this.tasks.length;i++){
        if(this.tasks[i].id===id){
            return this.tasks[i];
        }
    }
    return null;
};

