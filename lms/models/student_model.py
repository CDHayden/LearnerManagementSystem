from typing import TypedDict, List, Tuple
from bson.objectid import ObjectId

from database import mongo
from .courses import Attendance, Course


class Student:
    def __init__(self,
                 id: str,
                 forename: str,
                 surname: str,
                 profile_about: str,
                 profile_image: str,
                 courses: List[Course]
                 ) -> None:
        self.__id = ObjectId(id)
        self._forename: str = forename
        self._surname: str = surname
        self._profile_about: str = profile_about
        self._profile_image: str = profile_image
        self._courses = courses

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
    def profile_img(self) -> str:
        return self._profile_image

    @profile_img.setter
    def profile_img(self, value: str) -> None:
        self._profile_img = value

    @property
    def courses(self) -> Course:
        return self._courses
