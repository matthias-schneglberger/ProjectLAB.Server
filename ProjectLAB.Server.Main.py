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
        jsonData = {}
        jsonData['Id'] = self.project_id
        jsonData['ProjectTitle'] = self.title
        jsonData['ProjectDesc'] = self.desc
        jsonData['State'] = self.state

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


@app.route(root + '/')
def index():
    return "ProjectLAB by Matthias Schneglberger"


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
    # pro1 = Project(project_id=jsondata["Id"], title=jsondata["ProjectTitle"], desc=jsondata["ProjectDesc"], state=jsondata["State"])

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
    jsonstring = "\"Projects\": ["
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


if __name__ == '__main__':
    app.run(debug=True)
