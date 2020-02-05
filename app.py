from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
app.secret_key = 'secure'
api = Api(app)


tasks = []


class Task(Resource):
    def get(self, name,):
        task = next(filter(lambda x: x['Task'] == name, tasks), None)
        for n in tasks:
            return task, 200 if task else 404

    def post(self, name):
        if next(filter(lambda x: x['Task'] == name, tasks), None):
            return {'message': "Task: '{}' already exists.".format(name)}

        data = request.get_json()
        task = {
            'Task': name,
            'Status': data['status']}
        tasks.append(task)
        return task, 201

    def delete(self, name):
        global tasks
        tasks = list(filter(lambda x: x['task'] != name, tasks))
        return {'message': 'Task sucessfully deleted'}


    def put(self, name):
        data = request.get_json()
        for task in tasks:
            if task['Task'] == name:
                task['Status'] = data['status']
        return {'message': 'Task Status changed successfully'}


class Tasks(Resource):
    def get(self):
        return {'Tasks': tasks}


api.add_resource(Task, '/task/<string:name>')
api.add_resource(Tasks, '/tasks')

app.run(port=5000, debug=True)
