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
                    "forename":"Chris",
                    "surname":"Hayden",
                    "profile_about":"me",
                    "profile_image":"no",
                    "subjects":{
                        "spanish":{
                            "speaking":{
                                "grade":10
                                }
                            }
                        }
                    })

    def tearDown(self):
        database.mongo.db.users.drop()
    
    def get_user_object(self):
        cursor = database.mongo.db.users.find_one({"forename":"Chris"})
        user = User(cursor['_id'],
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
        expected = {"spanish":{"speaking":{"grade":10}}}
        self.assertEqual(expected,user.subjects)

    def test_can_add_course_to_existing_subject(self):
        user = self.get_user_object()
        new_course = {"spanish":{"listening":{"grade":25}}} 
        expected = {"spanish":
                        {
                        "listening":{"grade":25},
                        "speaking":{"grade":10},
                        },
                   }

        user.add_course(new_course)
        self.assertEqual(user.subjects,expected)

    def test_can_add_course_and_new_subject(self):
        user = self.get_user_object()
        new_course = {"english":{"writing":{"grade":25}}} 
        expected = {"english":
                        {
                            "writing": {"grade":25 }
                        },
                    "spanish":
                        {
                        "speaking":{"grade":10},
                        },
                   }

        user.add_course(new_course)
        self.assertEqual(user.subjects,expected)

    def test_can_edit_existing_subject_course(self):
        user = self.get_user_object()
        updated_course = {"spanish":{"speaking":{"grade":25}}} 
        user.add_course(updated_course)
        self.assertEqual(user.subjects,updated_course)


    def test_can_delete_course_keep_subject(self):
        user = self.get_user_object()
        new_course = {"spanish":{"listening":{"grade":25}}} 
        user.add_course(new_course)
        value = user.delete_course("spanish","speaking")
        self.assertTrue(value)

    def test_can_delete_course_delete_subject(self):
        user = self.get_user_object()
        value = user.delete_course("spanish","speaking")

        with self.subTest():
            self.assertTrue(value)

        with self.subTest():
            subject = user.subjects
            self.assertEqual({ },subject)
