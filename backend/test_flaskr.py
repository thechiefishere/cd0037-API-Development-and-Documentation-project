import os
import unittest
import json
from urllib import response
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}:{}@{}/{}".format('student', 'student', 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
            
        self.new_question = {
            'question': 'What food never gets spoilt',
            'answer': 'Honey',
            'category': 1,
            'difficulty': 3
        }
        
        self.new_user = {
            'username': 'Laide',
            'password': 'laidesecret'
        }
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_getting_all_categories(self):
        response = self.client().get('/categories')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(data['categories']))
        
    def test_method_not_allowed_on_categories(self):
        response = self.client().post('/categories')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Method Not Allowed')
        
    def test_get_all_questions(self):
        response = self.client().get('/questions')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['current_category'])
        
    def test_getting_invalid_questions_page(self):
        response = self.client().get('/questions?page=1000')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found')
        
    # def test_deleting_question(self):
    #     response = self.client().delete('/questions/25')
    #     data = json.loads(response.data)
        
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(data['id'], 25)
        
    def test_deleting_invalid_question(self):
        response = self.client().delete('/questions/1000')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found')
        
    # def test_adding_new_question(self):
    #     response = self.client().post('/questions', json=self.new_question)
        
    #     self.assertEqual(response.status_code, 200)
        
    def test_adding_with_wrong_data(self):
        response = self.client().post('/questions', json={'question': 'What is your name', 'answer': 'Ladipo'})
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad Request')
        
    def test_searching_question(self):
        response = self.client().post('/questions', json={'searchTerm': 'What'})
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['current_category'])
        
    def test_searching_question_with_wrong_key(self):
        response = self.client().post('/questions', json={'search_term': 'What'})
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad Request')
        
    def test_getting_questions_by_categories(self):
        response = self.client().get('/categories/2/questions')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['current_category'])
        
    def test_not_found_error_for_getting_questions_by_categories(self):
        response = self.client().get('/categories/1000/questions')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found')
        
    def test_get_quiz(self):
        response = self.client().post('/quizzes', json={'quiz_category': {'id': 4, 'type': 'History'}, 'previous_questions': [1, 3, 23]})
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['question'])
        
    def test_get_quiz_bad_request(self):
        response = self.client().post('/quizzes', json={'quiz_category': {'id': 4, 'type': 'History'}, 'previousQuestions': [1, 3, 23]})
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad Request')
        
    # def test_adding_new_user(self):
    #     response = self.client().post('/users', json=self.new_user)
    #     data = json.loads(response.data)
        
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(data['id'], 7)
    #     self.assertEqual(data['username'], 'Laide')
    #     self.assertTrue(data['token'])
        
    def test_adding_already_added_user(self):
        response = self.client().post('/users', json={'username': 'jbaba', 'password': 'secret'})
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad Request')
        
    def test_user_login(self):
        response = self.client().post('/users/login', json={'username': 'jbaba', 'password':'secret'})
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['username'], 'jbaba')
        self.assertTrue(data['token'])
        
    def test_user_wrong_password(self):
        response = self.client().post('/users/login', json={'username': 'jbaba', 'password':'seet'})
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unauthorized')

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()