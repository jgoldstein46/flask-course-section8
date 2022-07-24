import os

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from security import identity, authenticate
from resources.user import UserRegister
from resources.item import Item, ItemList
from db import db
from resources.store import Store, StoreList


app = Flask(__name__)
db_url = os.environ.get('DATABASE_URL', "sqlite:///data.db")
if db_url.split(":")[0] == "postgres":
    db_url = "".join(["postgresql"] + db_url.split(":")[1:])
app.config["SQLALCHEMY_DATABASE_URI"] = db_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
api = Api(app)
app.secret_key = 'justin'

jwt = JWT(app, authenticate, identity)

api.add_resource(Store, "/store/<string:name>")
api.add_resource(ItemList, '/items')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(UserRegister, '/register')
api.add_resource(StoreList, "/stores")

if __name__ == "__main__":
    db.init_app(app)
    app.run(port=5000, debug=True)
