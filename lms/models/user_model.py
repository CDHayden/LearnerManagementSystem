from bson.objectid import ObjectId

import database

class User:
    """ 
    A class used to represent a user

    """

    def __init__(self,
                 _id,
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

        self._id = ObjectId(_id)
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
        database.mongo.db.users.update_one(self._filter, {"$set": {"forename":
            value}})

    @property
    def surname(self):
        return self._surname

    @surname.setter
    def surname(self, value):
        self._surname = value
        database.mongo.db.users.update_one(self._filter, {"$set": {"surname":
            value}})

    @property
    def profile_about(self):
        return self._profile_about

    @profile_about.setter
    def profile_about(self, value):
        self._profile_about = value
        database.mongo.db.users.update_one(self._filter, {"$set": {"profile_about":
            value}})

    @property
    def profile_image(self):
        return self._profile_image

    @profile_image.setter
    def profile_image(self, value):
        self._profile_img = value
        database.mongo.db.users.update_one(self._filter, {"$set": {"profile_image":
            value}})

    @property
    def subjects(self):
        return self._subjects


    def add_course(self,subject,course,grade):
        """ Adds a new course to the list of courses studied by this
        user

        Parameters
        ----------
        new_course : dict
        {subject:str,course:str,grade:int}
        """
        for current_subject in self._subjects:
            subject_name = current_subject.get("subject")
            course_name = current_subject.get("course")

            #If the subject and course already exist, update the grade
            if subject_name == subject:
                if course_name == course:
                    current_subject["grade"] = grade 
                    database.mongo.db.users.update_one(
                            self._filter,
                            {"$set":
                                {"subjects.$[elem].grade":grade}},
                                array_filters = [
                                    {
                                    "elem.subject":subject,
                                    "elem.course":course
                                     }
                                    ]
                            )
                    return
        
        #If we reach here,the course and subject are new so add
        #the new object
        new_course = {'subject':subject,'course':course,'grade':grade}
        database.mongo.db.users.update_one(self._filter,
                {"$addToSet": {"subjects":new_course}})
    
        self._subjects.append(new_course)

    def delete_course(self, subject,course):
        """Deletes a course from the list of courses studied by
        this user (if found)

        Parameters
        ----------
        subject:str
        course:str

        Returns
        -------
        True if deleted
        False if not deleted
        """
        update = database.mongo.db.users.update_one(
                    self._filter,
                    {"$pull":
                        {
                            "subjects":
                            {"subject":subject,
                                "course":course}
                            }
                        }
                    )
        if update.modified_count > 0:
           self._subjects = database.mongo.db.users.find_one(
                   self._filter, {"subjects":1,"_id":0})['subjects']
           return True
        return False

    def get_subject_content(self,subject_name):
        """
        Returns an overview of a subject for a user

        Parameters
        ----------
        user_id : str
        ID of the user to use
        subject_name : str
        Name of the subject we want to overview of

        Return
        ------
        Empty dictionary on error.
        On success: {'avg_grade':float, 'num_courses': int}
        """
        pipeline = [
                    { "$match": self._filter },
                    {"$unwind": "$subjects"},
                    { "$match": {"subjects.subject": subject_name}},
                    {"$group":
                        {
                            "_id":"$subjects.subject",
                            "courses": {
                                "$addToSet": "$subjects.course"
                                        },
                            "avg_grade": { "$avg":"$subjects.grade"}
                        }
                    } ]
        results = list( database.mongo.db.users.aggregate(pipeline) )
        subject_content = {}
        if results:
            subject_content.update({'avg_grade':results[0]['avg_grade'],
                'num_courses':len(results[0]['courses'])})
        return subject_content

    def get_course_content(self,subject_name,course_name):
        """
        Returns an overview of a course for a user

        Parameters
        ----------
        course_name : str
        Name of the course we want to overview of

        Return
        ------
        Empty dictionary on error.
        On success: {'grade':int}
        """
        course_content = {}
        for subject in self._subjects:
            if subject['subject'] == subject_name \
            and subject['course'] == course_name:
                course_content.update({'grade':subject['grade']})
                break

        return course_content 
