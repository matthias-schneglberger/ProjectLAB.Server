import json
import mysql.connector
from flask import Flask
from flask import request


# region classes

class Project:
    def __init__(self, project_id, title, desc, state):
        self.project_id = project_id
        self.title = title
        self.desc = desc
        self.state = state

    def toJson(self):
        jsonData = {'Id': self.project_id, 'ProjectTitle': self.title, 'ProjectDesc': self.desc, 'State': self.state}

        jsonString = json.dumps(jsonData)
        return jsonString

    def fromROW(self, dataRow):
        project_id = dataRow[0]
        title = dataRow[1]
        desc = dataRow[2]
        state = dataRow[3]
        return Project(project_id=project_id, title=title, desc=desc, state=state)

    def fromJson(self, jsonString):
        jsondata = json.load(jsonString)
        return Project(project_id=jsondata['Id'], title=jsondata['Title'], desc=jsondata['Desc'],
                       state=jsondata['State'])


class Task:
    def __init__(self, task_Id, project_Id, taskTitle, taskDesc, taskState):
        self.task_Id = task_Id
        self.project_Id = project_Id
        self.taskTitle = taskTitle
        self.taskDesc = taskDesc
        self.taskSate = taskState

    def toJson(self):
        jsonData = {'Id': self.task_Id, 'ProjectID': self.project_Id, 'TaskTitle': self.taskTitle, 'TaskDesc': self.taskDesc, 'TaskState': self.taskSate}

        jsonString = json.dumps(jsonData)
        return jsonString

    def fromROW(self, dataRow):
        task_Id = dataRow[0]
        project_Id = dataRow[1]
        taskTitle = dataRow[2]
        taskDesc = dataRow[3]
        taskState = dataRow[4]

        return Task(task_Id=task_Id, project_Id=project_Id, taskTitle=taskTitle, taskDesc=taskDesc, taskState=taskState)

    def fromJson(self, jsonString):
        jsondata = json.load(jsonString)
        return Task(task_Id=jsondata['Id'], project_Id=jsondata['ProjectID'], taskTitle=jsondata['TaskTitle'], taskDesc=jsondata['TaskDesc'], taskState=jsondata['TaskState'])


# endregion classes

mydb = mysql.connector.connect(
    port=3333,
    host="srv-schneg",
    user="root",
    password="schneglberger",
    db="projectLAB"
)

app = Flask(__name__)
root = "/projectLAB"


@app.route('/')
def Index():
    return "<a href='" + root + "'>Project LAB<a>"


@app.route(root + '/')
def projectIndex():
    return "<h3>  ProjectLAB - Matthias Schneglberger</h3><a href='" + root + "/project/list'>Alle Projekte</a><br/><a href='" + root + "/task/list'>Alle Tasks</a><br/>"


# region projectCRUD
@app.route(root + '/project/<id>', methods=["GET"])
def getProjectById(id):
    sqlserver = mydb.cursor()
    sqlserver.execute(("SELECT * FROM project WHERE ID='" + id + "'"))
    row = sqlserver.fetchone()
    pro1 = Project(
        project_id=row[0],
        title=row[1],
        desc=row[2],
        state=row[3]
    )
    print(pro1.toJson())
    mydb.commit()
    sqlserver.close()
    return pro1.toJson()


@app.route(root + '/project/<id>', methods=["DELETE"])
def deleteProjectById(id):
    sqlserver = mydb.cursor()
    sqlserver.execute(("DELETE FROM project WHERE Id='{}'".format(id)))
    mydb.commit()
    sqlserver.close()
    return "succesfully deleted project with ID=" + id


@app.route(root + '/project/<id>', methods=["PUT"])
def updateProjectById(id):
    return "update " + id


@app.route(root + '/project', methods=["POST"])
def postProject():
    projJsonString = request.get_json()
    jsondata = json.loads(json.dumps(projJsonString))

    sqlserver = mydb.cursor()
    sqlserver.execute(("INSERT INTO project VALUES ('{}','{}','{}',{})".format(jsondata["Id"], jsondata["ProjectTitle"],
                                                                               jsondata["ProjectDesc"],
                                                                               jsondata["State"], )))
    mydb.commit()
    sqlserver.close()

    return "inserted succefully!"


@app.route(root + '/project/list', methods=["GET"])
def getProjectList():
    sqlserver = mydb.cursor()
    sqlserver.execute("SELECT * FROM project")
    jsonstring = "["
    for row in sqlserver.fetchall():
        pro1 = Project(
            project_id=row[0],
            title=row[1],
            desc=row[2],
            state=row[3]
        )

        jsonstring += pro1.toJson() + ","
    jsonstring = jsonstring[:-1]
    jsonstring += "]"
    mydb.commit()
    sqlserver.close()
    return jsonstring


# endregion projectCRUD



#region taskCRUD

@app.route(root + '/task/<id>', methods=["GET"])
def getTaskById(id):
    sqlserver = mydb.cursor()
    sqlserver.execute(("SELECT * FROM task WHERE ID='" + id + "'"))
    row = sqlserver.fetchone()
    pro1 = Task(
        task_Id=row[0],
        project_Id=row[1],
        taskTitle=row[2],
        taskDesc=row[3],
        taskState=row[4]
    )
    print(pro1.toJson())
    mydb.commit()
    sqlserver.close()
    return pro1.toJson()


@app.route(root + '/task/<id>', methods=["DELETE"])
def deleteTaskById(id):
    sqlserver = mydb.cursor()
    sqlserver.execute(("DELETE FROM task WHERE Id='{}'".format(id)))
    mydb.commit()
    sqlserver.close()
    return "succesfully deleted Task with ID=" + id


@app.route(root + '/task/<id>', methods=["PUT"])
def updateTaskById(id):
    return "update task " + id


@app.route(root + '/task', methods=["POST"])
def postTask():
    projJsonString = request.get_json()
    jsondata = json.loads(json.dumps(projJsonString))

    sqlserver = mydb.cursor()
    sqlserver.execute(("INSERT INTO task VALUES ('{}','{}','{}','{}', {})".format(jsondata["Id"], jsondata["ProjectID"],
                                                                               jsondata["TaskTitle"],
                                                                               jsondata["TaskDesc"],jsondata["TaskState"])))
    mydb.commit()
    sqlserver.close()

    return "inserted succefully!"


@app.route(root + '/task/list', methods=["GET"])
def getTaskList():
    sqlserver = mydb.cursor()
    sqlserver.execute("SELECT * FROM task")
    jsonstring = "["
    for row in sqlserver.fetchall():
        pro1 = Task(
            task_Id=row[0],
            project_Id=row[1],
            taskTitle=row[2],
            taskDesc=row[3],
            taskState=row[4]
        )

        jsonstring += pro1.toJson() + ","
    jsonstring = jsonstring[:-1]

    jsonstring += "]"
    mydb.commit()
    sqlserver.close()
    return jsonstring


#endregoin taskCRUD



if __name__ == '__main__':
    app.run(debug=True)
