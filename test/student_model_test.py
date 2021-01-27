import unittest
import io
from unittest.mock import patch, Mock, mock_open
import mongomock 
from bson.objectid import ObjectId

from lms import create_app
import database
from lms.models.student_model import Student


class TestStudentModel(unittest.TestCase):
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
                    "_id":ObjectId(b'testStudent1'),
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
    
    def get_student_object(self):
        cursor = database.mongo.db.users.find_one({"forename":"Chris"})
        student = Student(cursor['_id'],
                        cursor['forename'],
                        cursor['surname'],
                        cursor['profile_about'],
                        cursor['profile_image'],
                        cursor['subjects']
                        )
        return student

    def test_can_create_student_object(self):
        self.assertIsInstance(self.get_student_object(), Student)
            

    def test_can_get_forename(self):
        student = self.get_student_object()
        expected = "Chris"
        self.assertEqual(expected,student.forename)

    def test_can_get_surname(self):
        student = self.get_student_object()
        expected = "Hayden"
        self.assertEqual(expected,student.surname)

    def test_can_get_profile_about(self):
        student = self.get_student_object()
        expected = "me"
        self.assertEqual(expected,student.profile_about)

    def test_can_get_profile_image(self):
        student = self.get_student_object()
        expected = "no"
        self.assertEqual(expected,student.profile_image)

    def test_can_get_subjects(self):
        student = self.get_student_object()
        expected = {"spanish":{"speaking":{"grade":10}}}
        self.assertEqual(expected,student.subjects)

    def test_can_add_course_to_existing_subject(self):
        student = self.get_student_object()
        new_course = {"spanish":{"listening":{"grade":25}}} 
        expected = {"spanish":
                        {
                        "listening":{"grade":25},
                        "speaking":{"grade":10},
                        },
                   }

        student.add_course(new_course)
        self.assertEqual(student.subjects,expected)

    def test_can_add_course_and_new_subject(self):
        student = self.get_student_object()
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

        student.add_course(new_course)
        self.assertEqual(student.subjects,expected)

    def test_can_edit_existing_subject_course(self):
        student = self.get_student_object()
        updated_course = {"spanish":{"speaking":{"grade":25}}} 
        student.add_course(updated_course)
        self.assertEqual(student.subjects,updated_course)


    def test_can_delete_course_keep_subject(self):
        student = self.get_student_object()
        new_course = {"spanish":{"listening":{"grade":25}}} 
        student.add_course(new_course)
        value = student.delete_course("spanish","speaking")
        self.assertTrue(value)

    def test_can_delete_course_delete_subject(self):
        student = self.get_student_object()
        value = student.delete_course("spanish","speaking")

        with self.subTest():
            self.assertTrue(value)

        with self.subTest():
            subject = student.subjects
            self.assertEqual({ },subject)
