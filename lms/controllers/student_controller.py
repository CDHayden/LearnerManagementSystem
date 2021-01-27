import base64
from bson.objectid import ObjectId
from os import environ

from ..models.student_model import Student
import database


def create_student_from_cursor(cursor):
    """
    Returns a student object populated with data from a pymongo cursor

    Parameters
    ----------
    cursor : pymongo_cursor
    Database information to load into student object

    Returns
    -------
    Student Object on success
    Empty dict on failure
    """

    s = {}
    if cursor:
        s = Student(cursor['_id'],
                    cursor['forename'],
                    cursor['surname'],
                    cursor['profile_about'],
                    cursor['profile_image'],
                    cursor['subjects'])

    return s


#Accepts get_student_by_name("Bob Loblaw") and get_student_by_name("Bob", "Loblaw")
def get_student_by_name(name, surname=None):
    #If name is one variable seperated by space
    #Split it and store those values in name and surname
    if surname is None:
        names = name.split(" ")
        if(len(names) != 2):
            raise TypeError(f"Expected two names found {name}")
        else:
            name = names[0]
            surname = names[1]

    if database.mongo.db.users.count_documents({'forename': name,
                                       'surname': surname}) > 0:

        return list(map(create_student_from_cursor,
                        database.mongo.db.users.find({'forename': name,
                                                 'surname': surname})
                        ))

    else:
        raise NameError(f"Student {name} {surname} could not be found.")


def get_student_by_id(student_id):
    """
    Returns Student object for student of student_id

    Parameters
    ----------
    student_id : str
    Unique ID of student

    Returns
    -------
    Empty dict on error
    Otherwise a student object (see /models/student_model.py)
    """

    try:
        cursor = database.mongo.db.users.find_one({'_id':ObjectId(student_id)})
        return create_student_from_cursor(cursor)
    except:
        return {}


def get_subject_content(student_id, subject_name):
    """
    Returns an overview of a subject for a student

    Parameters
    ----------
    student_id : str
    ID of the student to use
    subject_name : str
    Name of the subject we want to overview of

    Return
    ------
    Empty dictionary on error.
    On success: {'avg_grade':float, 'num_courses': int}
    """
    total = 0
    student = get_student_by_id(student_id)
    if student and subject_name in student.subjects:
        subject = student.subjects[subject_name]
        for course in subject:
            total = total + subject[course]['grade']
        avg_grade = round(total / len(subject),2)
        return {'num_courses':len(subject), 'avg_grade': avg_grade }
    else:
        return {}


def allowed_file(filename):
    """Checks if the filename provided is permitted 

    Permitted if it contains a '.' and the file extension is listed
    in the ALLOWED_EXTENSIONS in the .env file
    """

    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in \
        environ.get('ALLOWED_EXTENSIONS')


def update_student_profile(student_id,new_profile_data):
    """
    Updates students profile about and image if changed

    Parameters
    ----------
    student_id : str
    Unique ID of student

    profile_data : dict
    { 'profile_about':str, profile_img: }
    """

    student = get_student_by_id(student_id) 
    flashed_message = "There was a problem updating your profile"

    if 'profile_about' in new_profile_data:
        if student.profile_about != new_profile_data['profile_about']:
            student.profile_about = new_profile_data['profile_about']
            flashed_message = "Profile updated."
    
    if 'profile_img' in new_profile_data:
        new_image = new_profile_data['profile_img']

        if new_image and allowed_file(new_image.filename):
            encoded_img = base64.b64encode(new_image.read()).decode()
            filetype = new_image.filename.rsplit('.', 1)[1].lower()
            img_data = f'data:image/{filetype};base64,{encoded_img}'
            database.mongo.db.users.update_one({'_id':student.id},
                    {'$set':
                        {
                    'profile_image': img_data
                        }
                    })

            flashed_message = "Profile updated."

    return flashed_message
