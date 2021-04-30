from flask import Flask, send_file
from flask_restful import Api, Resource, reqparse
import json
from flask_autoindex import AutoIndex
import werkzeug


app = Flask(__name__)
api = Api(app)

def save_data(array):
    with open("files/data.txt", 'w') as file:
        file.write(json.dumps(array))

def get_data():
    with open("files/data.txt", 'r') as file:
        return json.loads(file.read())



class User(Resource):
    def get(self, name):
        users = get_data()
        if (name == 'all'):
            return users, 200
        for user in users:
            if (name == user["name"]):
                return user, 200
        return "User not found", 404


    def post(self, name):
        parser = reqparse.RequestParser()
        parser.add_argument("age")
        parser.add_argument("occupation")
        args = parser.parse_args()


        users = get_data()
        for user in users:
            if (name == user["name"]):
                return "User with name {} already exists".format(name), 400

        user = {
            "name": name,
            "age": args["age"],
            "occpation": args["occupation"]
        }

        users.append(user)
        save_data(users)
        return user, 201

    def put(self, name):
        parser = reqparse.RequestParser()
        parser.add_argument("age")
        parser.add_argument("occupation")
        args = parser.parse_args()

        users = get_data()
        for user in users:
            if(name == user["name"]):
                user["age"] = args["age"]
                user["occupation"] = args["occupation"]
                return user, 200

        user = {
            "name": name,
            "age": args["age"],
            "occpation": args["occupation"]
        }

        users.append(user)
        save_data(users)
        return user, 201


    def delete(self, name):
        users = get_data()
        users = [user for user in users if user["name"] != name]
        save_data(users)
        return "{} is deleted".format(name), 200


class Download(Resource):
    def get(self, name):
        try:
            return send_file(name, as_attachment=True)
        except:
            return "File does not exist", 404

class Upload(Resource):
    def post(self):
        parse = reqparse.RequestParser()
        parse.add_argument('file', type=werkzeug.datastructures.FileStorage, location='files')
        args = parse.parse_args()
        image_file = args['file']
        image_file.save("files/name.jpg")

    def get(self):
        return "FUCK YOU", 200

    def delete(self):
        return "FUCK YOU", 200

    def put(self):
        return "FUCK YOU", 200


api.add_resource(User, "/api/user/<string:name>")
api.add_resource(Download, "/api/download/<string:name>")
api.add_resource(Upload, '/api/upload/')
AutoIndex(app)
app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)