from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, get_jwt, jwt_required
from annotate.extensions import jwt
from werkzeug.security import generate_password_hash
from annotate.models import db, User
from sqlalchemy import func

user_bp = Blueprint('user', __name__)


@user_bp.route('/existence/<string:username>', methods=['GET'])
def checkUserExistence(username):
    exists = db.session.query(User.id).filter_by(username=func.binary(username)).first() is not None
    if exists:
        return jsonify(True)
    return jsonify(False)


@user_bp.route('/register', methods=['POST'])
def register():
    request_data = request.get_json()
    username = request_data.get('username')
    password = request_data.get('password')

    exists = db.session.query(User.id).filter_by(username=func.binary(username)).first() is not None
    if exists:  # username duplicate
        return jsonify(message='UsernameDuplicate'), 400

    user = User(
        username=username,
        password_hash=generate_password_hash(password)
    )
    db.session.add(user)
    db.session.commit()
    return jsonify(message='Success')


@user_bp.route('/login', methods=['POST'])
def login():
    request_data = request.get_json()
    username = request_data.get('username')
    password = request_data.get('password')
    user = User.query.filter_by(username=func.binary(username)).first()
    if user is None:
        return jsonify(message='UserNotExist'), 400

    if not user.verify_password(password):
        return jsonify(message='PasswordIncorrect'), 400
    additional_claims = {'username': user.username}
    access_token = create_access_token(identity=user, additional_claims=additional_claims)
    return jsonify(access_token=access_token, logged_user=user.username)


@user_bp.route('/info', methods=['Get'])
@jwt_required()
def getUserInfo():
    claims = get_jwt()
    return jsonify(claims['username'])


# we can access user by current_user of flask_jwt_extended
@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter_by(id=identity).one_or_none()


@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.id
