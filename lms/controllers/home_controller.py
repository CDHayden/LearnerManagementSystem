from werkzeug.security import generate_password_hash, check_password_hash
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

def register_user(username, password, confirmPassword):
    """ Try and create a user in the database with provided credentials """
    if not username or not password or not confirmPassword:
        return no_details_error

    if get_user_from_username(username) is not None:
        return user_already_exists_error

    if password != confirmPassword:
        return password_not_match_arrow 

    hashed_password = generate_password_hash(password)

    try:
        mongo.db.users.insert_one({'username':username.lower(),'password':hashed_password})
    except:
        return db_error
    return successful_registration_message
