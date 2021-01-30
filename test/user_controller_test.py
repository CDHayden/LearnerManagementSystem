import unittest
import io
from unittest.mock import patch, Mock, mock_open
import mongomock 
from bson.objectid import ObjectId

from lms import create_app
import database
from lms.models.user_model import User
from lms.controllers.user_controller import (get_user_by_id, 
create_user_from_cursor, allowed_file, update_user_profile)


class TestUserController(unittest.TestCase):
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

    def test_can_create_user_from_cursor(self):
        cursor = database.mongo.db.users.find_one({"forename":"Chris"})
        user = create_user_from_cursor(cursor)
        self.assertIsInstance(user,User)

    def test_can_create_user_from_cursor_fails(self):
        cursor = database.mongo.db.users.find_one({"forename":"Bob"})
        user = create_user_from_cursor(cursor)
        self.assertEqual({},user)


    def test_can_get_user_by_id(self):
        user = get_user_by_id(ObjectId(b'123456789abc'))
        self.assertIsInstance(user,User)
        
    def test_can_get_user_by_id_fails(self):
        test_id = ObjectId(b'testStudent2')
        user = get_user_by_id(test_id)
        self.assertEqual({},user)

    def test_allowed_file(self):
        result = allowed_file("test.mp3")
        self.assertFalse(result)

    def test_allowed_file_fails(self):
        result = allowed_file("test.png")
        self.assertTrue(result)

    def test_update_user_profile_only_change_about(self):
        data = {'profile_about':'new about'}
        value = update_user_profile(ObjectId(b'123456789abc'),data) 
        user = get_user_by_id(ObjectId(b'123456789abc')) 

        #check the profile was updated
        with self.subTest():
            self.assertEqual(("Profile updated.","alert-success"),value)

        #check the profile_about was changed
        with self.subTest():
            self.assertEqual('new about', user.profile_about)

        #check the profile_image was not changed
        with self.subTest():
            self.assertEqual('no',user.profile_image)

    def test_update_user_profile_only_change_image(self):
        # Info on mocking files and file reads taken from:
        # https://docs.python.org/3/library/unittest.mock.html#mocking-the-builtin-open-used-as-a-context-manager
        def read():
            return b'test'

        data = {'profile_img': Mock(filename="test.png",read=read)}

        expected_img_return = 'data:image/png;base64,dGVzdA=='

        with patch('builtins.open', mock_open(read_data=b'test')):
            value = update_user_profile(ObjectId(b'123456789abc'),data) 

        user = get_user_by_id(ObjectId(b'123456789abc')) 

        #check the profile was updated
        with self.subTest():
            self.assertEqual(("Profile updated.","alert-success"),value)

        #check the profile_image was changed
        with self.subTest():
            self.assertEqual(expected_img_return,user.profile_image)

        #check the profile_about was not changed
        with self.subTest():
            self.assertEqual('me', user.profile_about)

