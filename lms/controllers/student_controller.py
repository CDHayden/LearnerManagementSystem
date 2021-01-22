from typing import List, Union

from ..models.student_model import Student
from database import mongo


def create_student_from_cursor(cursor) -> Student:
    s = Student(cursor['_id'],
                cursor['forename'],
                cursor['surname'],
                cursor['profile_about'],
                cursor['profile_image'],
                cursor['classes'])
    return s


#Accepts get_student_by_name("Bob Loblaw") and get_student_by_name("Bob", "Loblaw")
def get_student_by_name(name: str, surname: str = None) -> Union[Student,List[Student]]:
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
