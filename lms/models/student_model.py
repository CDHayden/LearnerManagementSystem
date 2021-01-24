
from bson.objectid import ObjectId

from database import mongo

class Student:
    """ 
    A class used to represent a student

    """

    def __init__(self,
                 id,
                 forename,
                 surname,
                 profile_about,
                 profile_image,
                 subjects
                 ): 
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
        Subjects : List[object]
            A list of course objects for each course the student is 
            enrolled on.
        """

        self._id = ObjectId(id)
        self._forename = forename
        self._surname = surname
        self._profile_about = profile_about
        self._profile_image = profile_image
        self._subjects = subjects
        self._filter = {"_id":self._id}

    @property
    def id(self):
        return self._id

    @property
    def forename(self):
        return self._forename

    @forename.setter
    def forename(self, value):
        self._forename = value
        mongo.db.users.update_one(self._filter, {"$set": {forename:
            value}})

    @property
    def surname(self):
        return self._surname

    @surname.setter
    def surname(self, value):
        self._surname = value
        mongo.db.users.update_one(self._filter, {"$set": {surname:
            value}})

    @property
    def profile_about(self):
        return self._profile_about

    @profile_about.setter
    def profile_about(self, value):
        self._profile_about = value
        mongo.db.users.update_one(self._filter, {"$set": {profile_about:
            value}})

    @property
    def profile_image(self):
        return self._profile_image

    @profile_image.setter
    def profile_image(self, value):
        self._profile_img = value

    @property
    def subjects(self):
        return self._subjects
