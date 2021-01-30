from bson.objectid import ObjectId

import database

class User:
    """ 
    A class used to represent a user

    """

    def __init__(self,
                 id,
                 username,
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
            The ObjectId for this user
        username: str
            Username of the user
        forename: str
            Forename of the user
        surname : str
            Surname of the user
        profile_about : str
            The about text written on the user's profile
        profile_image : str
            Base64 encoded string for the user's profile image
        Subjects : List[object]
            A list of course objects for each course the user is 
            enrolled on.
        """

        self._id = ObjectId(id)
        self._username = username
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
    def username(self):
        return self._username

    @property
    def forename(self):
        return self._forename

    @forename.setter
    def forename(self, value):
        self._forename = value
        database.mongo.db.users.update_one(self._filter, {"$set": {'forename':
            value}})

    @property
    def surname(self):
        return self._surname

    @surname.setter
    def surname(self, value):
        self._surname = value
        database.mongo.db.users.update_one(self._filter, {"$set": {'surname':
            value}})

    @property
    def profile_about(self):
        return self._profile_about

    @profile_about.setter
    def profile_about(self, value):
        self._profile_about = value
        database.mongo.db.users.update_one(self._filter, {"$set": {'profile_about':
            value}})

    @property
    def profile_image(self):
        return self._profile_image

    @profile_image.setter
    def profile_image(self, value):
        self._profile_img = value
        database.mongo.db.users.update_one(self._filter, {"$set": {'profile_image':
            value}})

    @property
    def subjects(self):
        return self._subjects


    def add_course(self, new_course):
        """ Adds a new course to the list of courses studied by this
        user

        Parameters
        ----------
        new_course : dict
        {subject:str,course:str,grade:int}
        """
        for subject in self._subjects:
            #If the subject and course already exist, update the grade
            if subject['subject'] == new_course['subject']:
                if subject['course'] == new_course['course']:
                    subject['grade'] = new_course['grade']
                    database.mongo.db.users.update_one(
                            self._filter, 
                            {"$set":
                                {"subjects.$[elem].grade":new_course['grade']}},
                                array_filters = [ 
                                    {
                                    "elem.subject":new_course['subject'],
                                     "elem.course":new_course['course']
                                     }
                                    ]
                            )
                    return
        
        #If we reach here,the course and subject are new so add
        #the new object
        database.mongo.db.users.update_one(self._filter,
                {'$addToSet': {'subjects':new_course}})
    
        self._subjects.append(new_course)

    def delete_course(self, subject_name, course_name):
        """Deletes a course from the list of courses studied by
        this user (if found)

        Parameters
        ----------
        subject_name: str
        Subject the course belongs too

        course_name: str

        Returns
        -------
        True if deleted
        False if not deleted
        """

        if subject_name in self._subjects.keys():
            courses = self._subjects[subject_name].keys()
            if course_name in courses:
                if len(courses) == 1:
                    #last course in subject so delete the whole
                    #subject
                    del self._subjects[subject_name]
                else:
                    #just delete the course
                    del self._subjects[subject_name][course_name]
                database.mongo.db.users.update_one(self._filter, {"$set":{'subjects':
                    self._subjects}})
                return True
        return False
