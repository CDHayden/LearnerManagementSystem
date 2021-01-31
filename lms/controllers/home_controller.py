from werkzeug.security import check_password_hash
from bson.objectid import ObjectId
import database

def get_returnable_user(user):
    """ Returns a cursor with ObjectID to hex string and no password"""
    user['id'] = str(user['_id'])
    del user['_id']
    del user['password']
    return user

def get_user_from_username(username):
    return database.mongo.db.users.find_one(
            {'username':username.lower()})

def get_user_from_id(_id):
    return database.mongo.db.users.find_one({'_id':ObjectId(_id)})

def log_user_in(username, password):
    """ check to see if user credentials match a db record, if so return
    user object otherwise False

    Parameters
    ----------
    username : str
    password : str 
    """

    if not username or not password:
        return False

    user = get_user_from_username(username) 
    if not user:
        return False

    if not check_password_hash(user['password'], password):
        return False

    return get_returnable_user(user)
