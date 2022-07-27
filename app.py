import os

from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from resources.user import UserRegister, User, UserLogin, UserLogout, TokenRefresh
from resources.item import Item, ItemList
from db import db
from resources.store import Store, StoreList
from blacklist import BLACKLIST


app = Flask(__name__)
db_url = os.environ.get('DATABASE_URL', "sqlite:///data.db")
if db_url.split(":")[0] == "postgres":
    db_url = ":".join(["postgresql"] + db_url.split(":")[1:])
app.config["SQLALCHEMY_DATABASE_URI"] = db_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_BLOCKLIST_ENABLED'] = True
app.config["JWT_BLOCKLIST_TOKEN_CHECKS"] = ['access', 'refresh']
api = Api(app)
app.secret_key = 'justin'

jwt = JWTManager(app)


@jwt.additional_claims_loader
def add_claims_to_jwt(identity):
    if identity == 1:
        return {"is_admin": True}
    return {"is_admin": False}


@jwt.token_in_blocklist_loader
def check_if_token_in_blocklist(jwt_header, jwt_payload):
    # print(jwt_payload, jwt_header)
    return jwt_payload['jti'] in BLACKLIST


@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return jsonify({
        "description": "The token has expired.",
        "error": "token_expired"
    }), 401


@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({
        "description": "Signiture verification failed",
        "error": "invalid_token"
    }), 401


@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({
        "description": "Request does not contain an access token.",
        'error': 'authorization_required'
    }), 401


@jwt.needs_fresh_token_loader
def token_not_fresh_callback(jwt_header, jwt_payload):
    return jsonify({
        "description": "The token is not fresh.",
        'error': 'fresh_token_required'
    }), 401


@jwt.revoked_token_loader
def revoked_token_callback(jwt_header, jwt_payload):
    return jsonify({
        "description": "The token has been revoked.",
        'error': 'token_revoked'
    }), 401


api.add_resource(Store, "/store/<string:name>")
api.add_resource(ItemList, '/items')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(UserRegister, '/register')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(StoreList, "/stores")
api.add_resource(UserLogin, "/login")
api.add_resource(TokenRefresh, '/refresh')
api.add_resource(UserLogout, '/logout')

if __name__ == "__main__":
    db.init_app(app)
    app.run(port=5000, debug=True)
