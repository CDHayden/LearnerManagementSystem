from typing import TypedDict, List, Tuple
from bson.objectid import ObjectId

from database import mongo
from .courses import Attendance, Course


class Student:
    """ 
    A class used to represent a student

    """

    def __init__(self,
                 id: str,
                 forename: str,
                 surname: str,
                 profile_about: str,
                 profile_image: str,
                 courses: List[Course]
                 ) -> None:
        """ 
        Parameters
        ----------
        id : str
            The ObjectId for this student
        forename: str
            Forename of the student
        surname : str
            Surname of the student
        profile_about : str
            The about text written on the student's profile
        profile_image : str
            Base64 encoded string for the student's profile image
        Courses : List[course]
            A list of course objects for each course the student is 
            enrolled on.
        """

        self._id = ObjectId(id)
        self._forename: str = forename
        self._surname: str = surname
        self._profile_about: str = profile_about
        self._profile_image: str = profile_image
        self._courses = courses

    @property
    def id(self) -> ObjectId:
        return self._id

    @property
    def forename(self) -> str:
        return self._forename

    @forename.setter
    def forename(self, value: str) -> None:
        self._forename = value

    @property
    def surname(self) -> str:
        return self._surname

    @surname.setter
    def surname(self, value: str) -> None:
        self._surname = value

    @property
    def profile_about(self) -> str:
        return self._profile_about

    @profile_about.setter
    def profile_about(self, value: str) -> None:
        self._profile_about = value

    @property
    def profile_image(self) -> str:
        return self._profile_image

    @profile_image.setter
    def profile_image(self, value: str) -> None:
        self._profile_img = value

    @property
    def courses(self) -> Course:
        return self._courses
