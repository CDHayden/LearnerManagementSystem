import base64
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash
from os import environ

from ..models.user_model import User
import database


def create_user_from_cursor(cursor):
    """
    Returns a user object populated with data from a pymongo cursor

    Parameters
    ----------
    cursor : pymongo_cursor
    Database information to load into user object

    Returns
    -------
    User Object on success
    Empty dict on failure
    """

    s = {}
    if cursor:
        s = User(cursor['_id'],
                    cursor['username'],
                    cursor['forename'],
                    cursor['surname'],
                    cursor['profile_about'],
                    cursor['profile_image'],
                    cursor['subjects'])

    return s

def create_student_from_cursor(cursor):
    """
    Returns a dict populated with select data from a pymongo cursor
    A more stripped down version of the method create_user_from_cursor

    Parameters
    ----------
    cursor: pymongo_cursor

    Returns
    -------
    Dict on success
    {'username':username,'forename':forename,
        'surname':surname,'subjects':subjects,
        'profile':link_to_profle}
    Empty dict on failure
    """
    s = {}
    if cursor:
        s.update({'username':cursor['username'],
            'forename':cursor['forename'],
            'surname':cursor['surname'],
            'subjects':cursor['subjects']})

    return s

def get_user_by_id(user_id):
    """
    Returns User object for user of user_id

    Parameters
    ----------
    user_id : str
    Unique ID of user

    Returns
    -------
    Empty dict on error
    Otherwise a user object (see /models/user_model.py)
    """

    try:
        cursor = database.mongo.db.users.find_one({'_id':ObjectId(user_id)})
        return create_user_from_cursor(cursor)
    except:
        return {}

def get_user_by_username(username):
    """
    Returns User object for user of username

    Parameters
    ----------
    username : str
    Unique username of user

    Returns
    -------
    Empty dict on error
    Otherwise a user object (see /models/user_model.py)
    """

    try:
        cursor = database.mongo.db.users.find_one({'username':username})
        return create_user_from_cursor(cursor)
    except:
        return {}

def generate_menu_items(user_id):
    """
    Generates items to display in a menu

    Parameters
    ----------
    user_id : str
    ObjectId str representation

    Returns
    -------
    [{'subject':['course','course']}...]
    """

    pipeline = [{"$match": {"_id":ObjectId(user_id)}}, 
                {"$unwind": "$subjects"},
                {"$group": 
                    {
                        "_id":"$subjects.subject",
                        "courses": {
                            "$addToSet": "$subjects.course"
                                    }
                    }
                } ]

    menu_items = list(database.mongo.db.users.aggregate(pipeline))
    return menu_items


def allowed_file(filename):
    """Checks if the filename provided is permitted 

    Permitted if it contains a '.' and the file extension is listed
    in the ALLOWED_EXTENSIONS in the .env file
    """

    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in \
        environ.get('ALLOWED_EXTENSIONS')


def update_user_profile(user_id,new_profile_data):
    """
    Updates users profile about and image if changed

    Parameters
    ----------
    user_id : str
    Unique ID of user

    profile_data : dict
    { 'profile_about':str, profile_img: }
    """

    user = get_user_by_id(user_id)
    flashed_message = ("There was a problem updating your profile","alert-danger")

    if 'profile_about' in new_profile_data:
        if user.profile_about != new_profile_data['profile_about']:
            user.profile_about = new_profile_data['profile_about']
            flashed_message = ("Profile updated.","alert-success")

    if 'profile_img' in new_profile_data:
        new_image = new_profile_data['profile_img']

        if new_image and allowed_file(new_image.filename):
            encoded_img = base64.b64encode(new_image.read()).decode()
            filetype = new_image.filename.rsplit('.', 1)[1].lower()
            img_data = f'data:image/{filetype};base64,{encoded_img}'
            database.mongo.db.users.update_one({'_id':user._id},
                    {'$set':
                        {
                            'profile_image': img_data
                        }
                    })

            flashed_message = ("Profile updated.", "alert-success")
    return flashed_message

def get_students_of_course(subject, course):
    """
    Get all students who study subject -course

    Parameters
    ----------
    subject: str
    course: str
    """

    students = list(map(create_student_from_cursor,database.mongo.db.users.find(
            {'$and': [
                {'subjects.subject': subject},
                {'subjects.course':course},
                {'is_teacher':False}
                ]}
            )))

    return students 

def get_students_not_of_course(subject, course):
    """
    Get all students who don't study subject - course

    Parameters
    ----------
    subject: str
    course: str

    Returns a list of usernames of studnets not in the course
    [{'username':username},...]
    """
    query = database.mongo.db.users.find(
             {"$and": [
                 {"subjects":{"$not": { "$elemMatch": {'subject': subject,
                     'course':course}}}},{'is_teacher':False}]},{"_id":0,"username":1}
             )

    students = list(query)

    return students

def get_all_students():
    query = database.mongo.db.users.find({'is_teacher':False})
    students = list(map(create_student_from_cursor,query))
    return students

def add_new_user(user_info):
    """ Try and create a user in the database with provided credentials """

    if not user_info['username'] \
    or not user_info['forename'] \
    or not user_info['surname'] \
    or not user_info['password'] \
    or not user_info['confirmPassword']:
        return {'message':'Missing required information',
        'style':'alert-danger'}

    user_does_exist = get_user_by_username(user_info['username'])
    if user_does_exist:
        return {'message':'Username already in use',
        'style':'alert-danger'}

    if user_info['password'] != user_info['confirmPassword']:
        return {'message':'Passwords do not match',
        'style':'alert-danger'}

    hashed_password = generate_password_hash(user_info['password'])

    try:
        database.mongo.db.users.insert_one({
            '_id':ObjectId(),
            'username':user_info['username'].lower(),
            'password':hashed_password,
            'is_teacher':False,
            'forename':user_info['forename'].lower(),
            'surname':user_info['surname'].lower(),
            'profile_about': 'I need to update my profile',
            'profile_image': 'none',
            'subjects':[]
            })
    except:
        return{'message': 'Database error.','style':'alert-danger'}
    return{'message': f'{user_info["username"]} added.','style':'alert-success'}

def delete_user_from_username(username):
    if username:
        try:
            database.mongo.db.users.delete_one({'username':username})
        except:
            return{'message': 'Database error.','style':'alert-danger'}
        return{'message': f'{username} deleted.','style':'alert-success'}
    return{'message': f'Could not find user {username}.','style':'alert-danger'}

def edit_user_from_username(username,data):
    new_values = {key : value for key, value in data.items() if value not in (None,'')}
    if username:
        if new_values['password'] and new_values['confirmPassword']:
            if new_values['password'] == new_values['confirmPassword']:
                new_values['password'] = generate_password_hash(new_values['confirmPassword'])
                del new_values['confirmPassword']

            else:
                return{'message': 'Passwords do not match.','style':'alert-danger'}

        try:
            database.mongo.db.users.update_one({'username':username},
                    {"$set": new_values})
        except:
            return{'message': 'Database error.','style':'alert-danger'}
        return{'message': f'{username} Updated.','style':'alert-success'}
    return{'message': f'Could not find user {username}.','style':'alert-danger'}
