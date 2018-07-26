/**
 * REST Client
 *
 */

window.onload = function () {
    getProjects();
}
projects = new Projects();
tasks = new Tasks();

document.getElementById("logout").onclick = function () {
    var req = new XMLHttpRequest();
    req.open("GET", "/api/user/logout/");
    req.addEventListener("load", function () {
        var response = JSON.parse(this.responseText);
        window.location.href = response["redirect"];
    });
    req.send();

}

document.getElementById("profile").onclick = function () {
    closeForms();
    document.getElementById("list").style.display = "none";
    document.getElementById("profileModal").style.display = "block";
    var form = document.getElementById("profileForm");
    clearAlerts();
    var req = new XMLHttpRequest();
    req.open("GET", "/api/user/");
    req.addEventListener("load", function () {
        var user = JSON.parse(this.responseText);
        form.username.value = user.username;
        form.nameProfile.value = user.name;
        form.password.value = user.password;
        form.email.value = user.email;
    });
    req.send();
}

document.getElementById("saveProfile").onclick = function () {
    clearAlerts();
    var req = new XMLHttpRequest();
    req.open("PUT", "/api/user/");
    req.setRequestHeader("Content-type", "application/json");
    req.addEventListener("load", function () {
        var response = JSON.parse(this.responseText);
        if (response["username"]) {
            showWarningMessage(response["username"]);
        }else if (response["email"]) {
            showWarningMessage(response["email"]);
        } else {
            closeForms();
            checkAlert(response);
        }
    });
    req.send(getFormProfileInformation());
}

function getProjects() {
    clearAlerts();
    var req = new XMLHttpRequest();
    req.open("GET", "/api/projects/");
    req.addEventListener("load", function () {
        var projs = JSON.parse(this.responseText);
        if (projs["project"]) {
            showWarningMessage(projs["project"]);
        } else {
            var ul = document.getElementById('projects');
            ul.innerHTML = '';
            projects.projects = [];
            document.getElementById("tasks-ul").innerHTML = "";
            document.getElementById("btns").innerHTML = "";
            document.getElementById("project-title").textContent = "Dashboard";

            for (var p in projs) {
                projects.addProject(new Project(projs[p].id, projs[p].name));
                var li = document.createElement('li');
                li.innerHTML = "<a href='#' class='project' onclick='getTasks(" + projs[p].id + ",this)'>" + projs[p].name + "</a>";
                ul.appendChild(li);
            }
            var title = document.getElementById("project-title");
            title.innerHTML += " <button class='btn btn-success' id='addProject' onclick='addProjectForm()'><i class='material-icons'>&#xE147;</i><span>Add Project</span></button>";
            closeForms();
            document.getElementById("formProject").style.marginTop = "100px";
        }
    });
    req.send();
}

function addColor(element) {
    if (element !== undefined) {
        clear();
        element.style.backgroundColor = "#3CB0EB";
        element.style.color = "white";
    }
}

function clear() {
    projetcs = document.getElementsByClassName("project");
    for (var i = 0; i < projetcs.length; i++) {
        projetcs[i].style.backgroundColor = "#f5f5f5";
        projetcs[i].style.color = "black";
    }
}

function getTasks(id, element) {
    addColor(element);
    clearAlerts();
    document.getElementById("mainZone").style.display = "block";
    document.getElementById("list").style.display = "block";
    document.getElementById("profileModal").style.display = "none";

    var req = new XMLHttpRequest();
    req.open("GET", "/api/projects/" + id + "/tasks/");
    req.addEventListener("load", function () {
        var jsonTasks = JSON.parse(this.responseText);
        if (jsonTasks["task"]) {
            showWarningMessage(response["task"]);
        } else {
            var ul = document.getElementById('tasks-ul');
            ul.innerHTML = '';
            var task;
            tasks.tasks = [];
            for (var t in jsonTasks) {
                task = new Task(jsonTasks[t].id, jsonTasks[t].title, jsonTasks[t].order, jsonTasks[t].due_date, jsonTasks[t].completed);
                tasks.addTask(task);
                var li = document.createElement('li');
                li.className = "list-group-item";
                li.appendChild(document.createTextNode(jsonTasks[t].title + ' - ' + jsonTasks[t].order));
                li.innerHTML += " <a class='edit' onclick='updateTaskForm(" + task.id + "," + id + ")'><i class='material-icons' data-toggle='tooltip' title='Edit'>&#xE254;</i></a>";
                li.innerHTML += " <a class='delete' onclick='deleteTask(" + task.id + "," + id + ")'><i class='material-icons' data-toggle='tooltip' title='Edit'>&#xE872;</i></a>";
                if (jsonTasks[t].completed || Date.parse(jsonTasks[t].due_date[0]) < Date.now()) {
                    li.innerHTML += "<span class='glyphicon glyphicon-ok'></span>";
                } else {
                    li.innerHTML += "<span class='glyphicon glyphicon-remove'></span>";
                }
                ul.appendChild(li);
            }
        }
        ul.style.display = "block";
        closeForms();
        addBtns(id);
    });
    req.send();
}

function addBtns(idProject) {
    var title = document.getElementById("project-title");
    title.childNodes[0].textContent = projects.getProject(idProject).name;
    for (var i = 2; i < title.childNodes.length; i++) {
        title.removeChild(title.childNodes[i--]);
    }

    var btns = document.getElementById("btns");
    for (var i = 0; i < btns.childNodes.length; i++) {
        btns.removeChild(btns.childNodes[i--]);
    }

    title.innerHTML += " <button class='btn btn-danger' id='removeProject' onclick='removeProject(" + idProject + ")'><i class='material-icons'>&#xE15C;</i> <span>Delete Project</span></button>";
    title.innerHTML += " <button class='btn btn-warning' id='editProject' onclick='editProjectForm(" + idProject + ")'><i class='material-icons' data-toggle='tooltip' title='Edit'>&#xE254;</i> <span>Edit Project</span></button>";
    document.getElementById("btns").innerHTML += " <button  class='btn btn-success' id='addTask' onclick='addTaskForm(" + idProject + ")'><i class='material-icons'>&#xE147;</i><span>Add task</span></button>";
    document.getElementById("formTask").style.display = "none";
}

function createBtn() {
    var btnCreate = document.createElement("button");
    btnCreate.className = "add";
    return btnCreate;
}

function closeForms() {
    document.getElementById("formTask").style.display = "none";
    document.getElementById("formProject").style.display = "none";
    document.getElementById("profileModal").style.display = "none";
    clearForms();
}

function clearForms() {
    document.getElementById("taskForm").reset();
    document.getElementById("projectForm").reset();;
    document.getElementById("profileForm").reset();;
}

function addTaskForm(projectId) {
    closeForms();
    document.getElementById("formTask").style.display = "block";
    document.getElementById("legendTask").textContent = "Adicionar Task";
    var saveBtn = document.getElementById("saveTask");
    var elClone = saveBtn.cloneNode(true);
    elClone.addEventListener("click", function () { addTask(projectId) });
    saveBtn.parentNode.replaceChild(elClone, saveBtn);
    document.getElementById("cancelTask").addEventListener("click", function () { getTasks(currentProject); });
}

function updateTaskForm(taskId, currentProject) {
    closeForms();
    object = tasks.getTask(taskId);
    document.getElementById("legendTask").textContent = "Update Task";
    document.getElementById("formTask").style.display = "block";
    var form = document.getElementById("taskForm");
    form.title.value = object.title;
    form.order.value = object.order;
    form.due_date.value = object.due_date[0];
    form.completed.selectedIndex = object.completed ? 0 : 1;

    var saveBtn = document.getElementById("saveTask");
    var elClone = saveBtn.cloneNode(true);
    elClone.addEventListener("click", function () { updateTask(currentProject, object.id) });
    saveBtn.parentNode.replaceChild(elClone, saveBtn);

    document.getElementById("cancelTask").addEventListener("click", function () { getTasks(currentProject); });
}

function getFormProfileInformation() {
    var form = document.getElementById("profileForm");
    var username = form.username.value;
    var name = form.nameProfile.value;
    var password = form.password.value;
    var email = form.email.value
    return JSON.stringify({ 'username': username, 'name': name, 'password': password, 'email': email });
}

function getFormTaskInformation() {
    var form = document.getElementById("taskForm");
    var title = form.title.value
    var order = form.order.value;
    var due_date = form.due_date.value;
    var completed = form.completed.selectedIndex === 0 ? true : false;
    return JSON.stringify({ 'title': title, 'order': order, 'due_date': due_date, 'completed': completed });
}

function getFormProjectInformation() {
    var form = document.getElementById("projectForm");
    var name = form.name.value
    return JSON.stringify({ 'name': name });
}

function checkAlert(response) {
    if (response["result"]) {
        showSuccessMessage(response["result"]);
    } else if (response["error"]) {
        showDangerMessage(response["error"]);
    } else if (response["account"]) {
        showWarningMessage(response["account"]);
    }
}

function addTask(idProject) {
    clearAlerts();
    var req = new XMLHttpRequest();
    req.open("POST", "/api/projects/" + idProject + "/tasks/");
    req.setRequestHeader("Content-type", "application/json");
    req.addEventListener("load", function () {
        var response = JSON.parse(this.responseText);
        if (response["fields"]) {
            showWarningMessage(response["fields"]);
        } else {
            getTasks(idProject);
            checkAlert(response);
        }
    });
    req.send(getFormTaskInformation());
}

function updateTask(currentProject, id) {
    clearAlerts();
    var req = new XMLHttpRequest();
    req.open("PUT", "/api/projects/" + currentProject + "/tasks/" + id + "/");
    req.setRequestHeader("Content-type", "application/json");
    req.addEventListener("load", function () {
        var response = JSON.parse(this.responseText);
        if (response["fields"]) {
            showWarningMessage(response["fields"]);
        } else if (response["task"]) {
            showWarningMessage(response["task"]);
        } else {
            getTasks(currentProject);
            checkAlert(response);
        }
    });
    req.send(getFormTaskInformation());
}

function deleteTask(id, currentProject) {
    var r = confirm("Tem a certeza que pretende eliminar esta tarefa?");
    if (r == true) {
        clearAlerts();
        var req = new XMLHttpRequest();
        req.open("DELETE", "/api/projects/" + currentProject + "/tasks/" + id + "/");
        req.addEventListener("load", function () {
            var response = JSON.parse(this.responseText);
            getTasks(currentProject);
            if (response["task"]) {
                showWarningMessage(response["task"]);
            }else{
                checkAlert(response);
            }
        });
        req.send();
    }
}

function addProject() {
    clearAlerts();
    var req = new XMLHttpRequest();
    req.open("POST", "/api/projects/");
    req.setRequestHeader("Content-type", "application/json")
    req.addEventListener("load", function () {
        var response = JSON.parse(this.responseText);
        getProjects();
        if (response["name"]) {
            showWarningMessage(response["name"]);
        } else {
            checkAlert(response);
        }
    });
    req.send(getFormProjectInformation());
}

function editProject(idProject) {
    clearAlerts();
    var req = new XMLHttpRequest();
    req.open("PUT", "/api/projects/" + idProject + "/");
    req.setRequestHeader("Content-type", "application/json")
    req.addEventListener("load", function () {
        var response = JSON.parse(this.responseText);
        getProjects();
        if (response["project"]) {
            showWarningMessage(response["project"]);
        } else {
            checkAlert(response);
        }
    });
    req.send(getFormProjectInformation());
}

function removeProject(idProject) {
    var r = confirm("Tem a certeza que pretende eliminar este projeto?");
    if (r == true) {
        clearAlerts();
        var req = new XMLHttpRequest();
        req.open("DELETE", "/api/projects/" + idProject + "/");
        req.setRequestHeader("Content-type", "application/json")
        req.addEventListener("load", function () {
            var response = JSON.parse(this.responseText);
            getProjects();
            if (response["project"]) {
                showWarningMessage(response["project"]);
            } else {
                checkAlert(response);
            }
        });
        req.send(getFormProjectInformation());
    }
}

function addProjectForm() {
    closeForms();
    document.getElementById("formProject").style.display = "block";
    document.getElementById("legendProject").textContent = "Add Project";
    var saveBtn = document.getElementById("saveProject");
    var elClone = saveBtn.cloneNode(true);
    elClone.addEventListener("click", function () { addProject() });
    saveBtn.parentNode.replaceChild(elClone, saveBtn);
    document.getElementById("cancelTask").addEventListener("click", function () { getProjects(); });
}

function editProjectForm(idProject) {
    closeForms();
    document.getElementById("formProject").style.display = "block";
    document.getElementById("legendProject").textContent = "Edit Project";
    var saveBtn = document.getElementById("saveProject");
    var elClone = saveBtn.cloneNode(true);
    elClone.addEventListener("click", function () { editProject(idProject) });
    saveBtn.parentNode.replaceChild(elClone, saveBtn);
    document.getElementById("cancelTask").addEventListener("click", function () { getProjects(); });
    var form = document.getElementById("projectForm");
    form.name.value = projects.getProject(idProject).name;
}

function cancel(){
    document.getElementById("cancelTask").style.display="none";
    document.getElementById("cancelProject").style.display="none";
}