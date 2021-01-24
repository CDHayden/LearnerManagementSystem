import base64
from flask import current_app

from ..models.student_model import Student
from database import mongo


def create_student_from_cursor(cursor):
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

    if mongo.db.users.count_documents({'forename': name,
                                       'surname': surname}) > 0:

        return list(map(create_student_from_cursor,
                        mongo.db.users.find({'forename': name,
                                                 'surname': surname})
                        ))

    else:
        raise NameError(f"Student {name} {surname} could not be found.")

def get_course_grade(student, course_name):
    """Return student's grade for course_name"""
    grade = student['courses'].get(course_name).get('grade')
    return (course_name,grade)

def get_course_subject(course_name):
    """Return the subject that course belongs to"""
    selected_course = mongo.db.courses.find_one({'name': course_name})
    return selected_course['subject']

def get_subjects_courses(student, course="all"):
    """Return a dict of subjects and their courses for given student

    Keyword arguements:
    student -- The student you want subject and course information of
    subject -- Specific courses from a single subject. Default is all.
    """
    # subjects_courses = {}
    # for course_name in student.courses.keys():
        # selected_subject = get_course_subject(course_name)
        # if subject == "all" or subject == selected_subject:
            # if selected_subject not in subjects_courses:
                # subjects_courses[selected_subject] = []
            # subjects_courses[selected_subject].append(course_name)

    return student.courses.keys()

def get_average_grade(grades):
    """Return an average for a list of numbers"""
    avg = sum(grades) / len(grades)
    return avg

def allowed_file(filename):
    """Checks if the filename provided is permitted 

    Permitted if it contains a '.' and the file extension is listed
    in the ALLOWED_EXTENSIONS in the .env file
    """

    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in \
        current_app.config['ALLOWED_EXTENSIONS']

def update_student_profile(student_name,new_profile_data):
    student = get_student_by_name(student_name)[0]
    flashed_message = ""

    if student.profile_about != new_profile_data['profile_about']:
        mongo.db.users.update_one({'_id':student.id}, {'$set':{
                'profile_about': new_profile_data['profile_about']
            }})
        if not flashed_message:
            flashed_message = "Profile updated."

    new_image = new_profile_data['profile_img']

    if new_image and allowed_file(new_image.filename):
        encoded_img = base64.b64encode(new_image.read()).decode()
        filetype = new_image.filename.rsplit('.', 1)[1].lower()
        img_data = f'data:image/{filetype};base64,{encoded_img}'
        mongo.db.users.update_one({'_id':student.id}, {'$set':{
                'profile_image': img_data
            }})

        if not flashed_message:
            flashed_message = "Profile updated."

    return flashed_message

def load_subject_content(student_name, subject):
    pass

def load_course_content(student_name, course):
    pass

