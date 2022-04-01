from crypt import methods
import json
from flask import Flask, jsonify, request
from flask_cors import cross_origin, CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app=Flask(__name__)
cors = CORS(app)

app.config['CORS_HEADERS'] = 'Content-Type'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db=SQLAlchemy(app)

class Todo(db.Model):
    id =db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(200), nullable=False)
    priority=db.Column(db.Integer, default=0)
    date_created=db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Task{self.id}>' 

@app.route('/')
@cross_origin()
def index():
    return 'Hello World!'

@app.route('/addTask', methods=["POST"])
@cross_origin()
def addTask():
    data=request.get_json()
    newTask= Todo(name=data['taskContent'])

    try:
        db.session.add(newTask)
        db.session.commit()
        return jsonify(data)
    except:
        return 'There was some error' 

@app.route('/listTask')
@cross_origin()
def listTask():
    datas=Todo.query.all()
    info=[]
    for data in datas:
        status=False
        if data.priority==1:
            status=True

        obj={
            'id':data.id,
            'taskContent': data.name,
            'priority': status,
            'date': data.date_created
        }
        info.append(obj)

    return jsonify({'info': info})

@app.route('/delete/<int:id>', methods= ["DELETE"])
@cross_origin()
def deleteTask(id):
    task_to_delete=Todo.query.get_or_404(id)
    
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return 'Deleted task'
    except:
        return 'There was some error' 

@app.route('/update/<int:id>', methods= ["PUT"])
@cross_origin()
def updateTask(id):
    task_to_update=Todo.query.get_or_404(id)
    if task_to_update.priority==False:
        task_to_update.priority=True
    else: task_to_update.priority=False

    try:
        db.session.commit()
        return 'Updated task'
    except:
        return 'There was some error' 

if __name__ == "__main__":
    app.run(debug=True)