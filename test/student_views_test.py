import unittest
import io
from unittest.mock import patch
import mongomock 
from bson.objectid import ObjectId

from lms import create_app
import database
from lms.models.student_model import Student


class TestStudentViews(unittest.TestCase):
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
        database.mongo.db.users.insert_one( { "_id":ObjectId(b'testStudent1'),
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
    
    def test_student_index(self):
        response = self.app.get('/student/')
        self.assertEqual(response.status_code, 200)

    def test_student_update_profile(self):
        update = {'profile_about':'new about'}
        response = self.app.post('/student/update_profile',
                data=update) 

        with self.subTest():
            self.assertEqual(response.status_code,302)

        with self.subTest():
            student = database.mongo.db.users.find_one({'forename':'Chris'})
            self.assertEqual('new about',student['profile_about'])

    def test_student_get_courses(self):
        # Help with session mocking: 
        #https://stackoverflow.com/questions/36509662/python-mock-testing-to-mock-session
        with self.app.session_transaction() as sess:
            sess['user'] = str(ObjectId(b'testStudent1'))
        response = self.app.get('/student/courses')
        self.assertEqual(response.status_code,200)

    def test_student_load_course_content(self):
        with self.app.session_transaction() as sess:
            sess['user'] = str(ObjectId(b'testStudent1'))

        send =  {'subject':'spanish','course':'speaking'}
        response = self.app.post('/student/_load_course_content',
                json=send)

        expected = {'grade':10}
        self.assertEqual(response.get_json(),expected)

    def test_student_load_subject_content(self):
        with self.app.session_transaction() as sess:
            sess['user'] = str(ObjectId(b'testStudent1'))

        send = { 'subject':'spanish'}
        response = self.app.post('/student/_load_subject_content', 
                json=send)
        expected = {'num_courses':1,'avg_grade':10}
        
        self.assertEqual(response.get_json(), expected)
