import unittest
import io
from unittest.mock import patch, Mock, mock_open
import mongomock 
from bson.objectid import ObjectId

from lms import create_app
import database
from lms.models.user_model import User


class TestUserModel(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.patcher = patch('flask_pymongo.MongoClient',
                mongomock.MongoClient)
        cls.patcher.start()
        cls.app = create_app("mongodb://localhost:27017/mydatabase").test_client()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.patcher.stop()
        pass

    def setUp(self):
        database.mongo.db.users.insert_one( {
                    "_id":ObjectId(b'123456789abc'),
                    "username":"chayden",
                    "forename":"Chris",
                    "surname":"Hayden",
                    "profile_about":"me",
                    "profile_image":"no",
                    "subjects":[
                        {"subject":"spanish", 
                         "course":"speaking",
                         "grade":10}
                        ]
                    })

    def tearDown(self):
        database.mongo.db.users.drop()
    
    def get_user_object(self):
        cursor = database.mongo.db.users.find_one({"forename":"Chris"})
        user = User(cursor['_id'],
                        cursor['username'],
                        cursor['forename'],
                        cursor['surname'],
                        cursor['profile_about'],
                        cursor['profile_image'],
                        cursor['subjects']
                        )
        return user

    def test_can_create_user_object(self):
        self.assertIsInstance(self.get_user_object(), User)
            

    def test_can_get_forename(self):
        user = self.get_user_object()
        expected = "Chris"
        self.assertEqual(expected,user.forename)

    def test_can_get_surname(self):
        user = self.get_user_object()
        expected = "Hayden"
        self.assertEqual(expected,user.surname)

    def test_can_get_profile_about(self):
        user = self.get_user_object()
        expected = "me"
        self.assertEqual(expected,user.profile_about)

    def test_can_get_profile_image(self):
        user = self.get_user_object()
        expected = "no"
        self.assertEqual(expected,user.profile_image)

    def test_can_get_subjects(self):
        user = self.get_user_object()
        expected = [{"subject":"spanish","course":"speaking","grade":10}]
        self.assertEqual(expected,user.subjects)

    def test_can_add_course_to_existing_subject(self):
        user = self.get_user_object()
        subject = "spanish"
        course = "listening"
        grade = 25
        expected = [
                {"subject":"spanish","course":"speaking","grade":10},
                {"subject":subject,"course":course,"grade":grade}
                ]

        user.add_course(subject,course,grade)
        self.assertEqual(user.subjects,expected)

    def test_can_add_course_and_new_subject(self):
        user = self.get_user_object()
        subject = 'english'
        course = 'writing'
        grade = 25

        expected = [
                {"subject":"spanish", "course":"speaking", "grade":10},
                {"subject":subject,"course":course,"grade":grade}
                ]

        user.add_course(subject, course, grade)
        self.assertEqual(user.subjects,expected)

    @unittest.skip("mongomock does not support array_filters")
    def test_can_edit_existing_subject_course(self):
        user = self.get_user_object()
        subject = 'spanish'
        course = 'speaking'
        grade = 100
        user.add_course(subject,course,grade)
        value = user.get_course_content(subject,course)
        self.assertEqual(value.grade,grade)


    def test_can_delete_course_keep_subject(self):
        user = self.get_user_object()
        subject = "spanish"
        course = "listening"
        grade = 25
        user.add_course(subject,course,grade)
        value = user.delete_course("spanish","speaking")
        self.assertTrue(value)

    def test_can_delete_course_delete_subject(self):
        user = self.get_user_object()
        value = user.delete_course("spanish","speaking")

        with self.subTest():
            self.assertTrue(value)

        with self.subTest():
            subject = user.subjects
            self.assertEqual([ ],subject)
