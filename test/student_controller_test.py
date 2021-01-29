import unittest
import io
from unittest.mock import patch, Mock, mock_open
import mongomock 
from bson.objectid import ObjectId

from lms import create_app
import database
from lms.models.user_model import User
from lms.controllers.student_controller import (get_student_by_id, 
create_student_from_cursor, get_subject_content, allowed_file,
update_student_profile)


class TestStudentController(unittest.TestCase):
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

    def test_can_create_student_from_cursor(self):
        cursor = database.mongo.db.users.find_one({"forename":"Chris"})
        student = create_student_from_cursor(cursor)
        self.assertIsInstance(student,User)

    def test_can_create_student_from_cursor_fails(self):
        cursor = database.mongo.db.users.find_one({"forename":"Bob"})
        student = create_student_from_cursor(cursor)
        self.assertEqual({},student)


    def test_can_get_student_by_id(self):
        student = get_student_by_id(ObjectId(b'testStudent1'))
        self.assertIsInstance(student,User)
        
    def test_can_get_student_by_id_fails(self):
        test_id = ObjectId(b'testStudent2')
        student = get_student_by_id(test_id)
        self.assertEqual({},student)

    def test_can_get_subject_content(self):
        expected = {'avg_grade': 10.0, 'num_courses': 1}
        value = get_subject_content(ObjectId(b'testStudent1'),"spanish")
        self.assertEqual(expected,value)

    def test_can_get_subject_content_fails(self):
        expected = {}
        value = get_subject_content(ObjectId(b'testStudent1'),"Wrong")
        self.assertEqual(expected,value)

    def test_allowed_file(self):
        result = allowed_file("test.mp3")
        self.assertFalse(result)

    def test_allowed_file_fails(self):
        result = allowed_file("test.png")
        self.assertTrue(result)

    def test_update_student_profile_only_change_about(self):
        data = {'profile_about':'new about'}
        value = update_student_profile(ObjectId(b'testStudent1'),data) 
        student = get_student_by_id(ObjectId(b'testStudent1')) 

        #check the profile was updated
        with self.subTest():
            self.assertEqual("Profile updated.",value)

        #check the profile_about was changed
        with self.subTest():
            self.assertEqual('new about', student.profile_about)

        #check the profile_image was not changed
        with self.subTest():
            self.assertEqual('no',student.profile_image)

    def test_update_student_profile_only_change_image(self):

        # Info on mocking files and file reads taken from:
        # https://docs.python.org/3/library/unittest.mock.html#mocking-the-builtin-open-used-as-a-context-manager
        def read():
            return b'test'

        data = {'profile_img': Mock(filename="test.png",read=read)}

        expected_img_return = 'data:image/png;base64,dGVzdA=='

        with patch('builtins.open', mock_open(read_data=b'test')):
            value = update_student_profile(ObjectId(b'testStudent1'),data) 

        student = get_student_by_id(ObjectId(b'testStudent1')) 

        #check the profile was updated
        with self.subTest():
            self.assertEqual("Profile updated.",value)

        #check the profile_image was changed
        with self.subTest():
            self.assertEqual(expected_img_return,student.profile_image)

        #check the profile_about was not changed
        with self.subTest():
            self.assertEqual('me', student.profile_about)

