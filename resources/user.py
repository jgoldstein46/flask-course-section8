import sqlite3
from flask_restful import Resource, reqparse
import argparse
from models.usermodel import UserModel


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, help="this value cannot be null")
    parser.add_argument('password', type=str, required=True, help="this value cannot be null")

    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data["username"]):
            return {"message": "A user with that name already exists"}, 400

        user = UserModel(**data)
        user.save_to_db()

        return {"message": "user created successfully"}, 201

