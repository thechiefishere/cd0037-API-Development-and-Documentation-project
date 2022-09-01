import os
import unittest
import json
from urllib import response
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import random
import string

from flaskr import create_app
from models import setup_db, Question, Category


load_dotenv()
database_name = os.getenv('DB_TEST_NAME')
database_user = os.getenv('DB_USER')
database_password = os.getenv('DB_PASSWORD')
database_host = os.getenv('DB_HOST')
database_path = 'postgresql://{}:{}@{}/{}'.format(
    database_user, database_password, database_host, database_name)


def generate_user():
    """Generate a user object"""
    digits = random.choices(string.digits, k=3)
    letters = random.choices(string.ascii_uppercase, k=7)
    sample = random.sample(digits + letters, 10)
    sample1 = random.sample(digits + letters, 10)

    username = ''.join(sample)
    password = ''.join(sample1)
    return {
        'username': username,
        'password': password
    }


def generate_question():
    """Generate a question object"""
    letters = random.choices(string.ascii_uppercase, k=80)
    question = random.sample(letters, 50)
    answer = random.sample(letters, 10)
    difficulty = random.randint(1, 5)
    category = random.randint(1, 6)

    return {
        'question': ''.join(question),
        'answer': ''.join(answer),
        'category': category,
        'difficulty': difficulty
    }


def add_user(self):
    """Add new user to database"""
    user = generate_user()
    response = self.client().post('/users', json=user)
    data = json.loads(response.data)

    return {
        'user': user,
        'response': response,
        'data': data
    }


def add_question(self):
    """Add new quesion to database"""
    question = generate_question()
    response = self.client().post('/questions', json=question)
    data = json.loads(response.data)

    return {
        'user': question,
        'response': response,
        'data': data
    }


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = database_name
        self.database_path = 'postgresql://{}:{}@{}/{}'.format(
            database_user, database_password, database_host, self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        self.category = {
            'type': "Science"
        }

        self.user = {
            'username': 'John',
            'password': 'secret'
        }

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_a_add_new_category(self):
        response = self.client().post('/categories', json=self.category)

        self.assertEqual(response.status_code, 200)

    def test_ab_adding_category_with_wrong_data(self):
        response = self.client().post('/categories', json={'types': 'Science'})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad Request')

    def test_b_getting_all_categories(self):
        response = self.client().get('/categories')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(data['categories']))

    def test_c_method_not_allowed_on_categories(self):
        response = self.client().patch('/categories')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Method Not Allowed')

    def test_cd_adding_new_question(self):
        question = add_question(self)

        self.assertEqual(question['response'].status_code, 200)
        self.assertTrue(question['data']['question_id'])

    def test_d_adding_with_wrong_data(self):
        response = self.client().post(
            '/questions',
            json={
                'question': 'What is your name',
                'answer': 'Ladipo'})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad Request')

    def test_f_get_all_questions(self):
        response = self.client().get('/questions')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['current_category'])

    def test_g_getting_invalid_questions_page(self):
        response = self.client().get('/questions?page=1000')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found')

    def test_h_searching_question(self):
        response = self.client().post(
            '/questions/search', json={'searchTerm': 'What'})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['current_category'])

    def test_i_searching_question_with_wrong_key(self):
        response = self.client().post(
            '/questions', json={'search_term': 'What'})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad Request')

    def test_j_getting_questions_by_categories(self):
        response = self.client().get('/categories/1/questions')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['current_category'])

    def test_k_not_found_error_for_getting_questions_by_categories(self):
        response = self.client().get('/categories/1000/questions')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found')

    def test_l_get_quiz(self):
        response = self.client().post(
            '/quizzes',
            json={
                'quiz_category': {
                    'id': 1,
                    'type': 'Science'},
                'previous_questions': [
                    4,
                    3,
                    23]})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['question'])

    def test_m_get_quiz_bad_request(self):
        response = self.client().post(
            '/quizzes',
            json={
                'quiz_category': {
                    'id': 1,
                    'type': 'Science'},
                'previousQuestions': [
                    1,
                    3,
                    23]})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad Request')

    def test_n_adding_new_user(self):
        user = add_user(self)

        self.assertEqual(user['response'].status_code, 200)
        self.assertEqual(user['data']['username'],
                         user['user']['username'])
        self.assertTrue(user['data']['token'])

    def test_o_adding_already_added_user(self):
        user = add_user(self)

        response = self.client().post(
            '/users', json={'username': user['data']['username'], 'password': 'secret'})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad Request')

    def test_p_user_login(self):
        user = add_user(self)

        response = self.client().post(
            '/users/login', json={'username': user['data']['username'], 'password': user['user']['password']})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['username'], user['data']['username'])
        self.assertTrue(data['token'])

    def test_q_user_wrong_password(self):
        user = add_user(self)

        response = self.client().post(
            '/users/login', json={'username': user['data']['username'], 'password': 'seet'})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unauthorized')

    def test_t_update_user_score(self):
        user = add_user(self)
        question = add_question(self)

        response_from_login = self.client().post(
            '/users/login', json=user['user'])
        response_data = json.loads(response_from_login.data)
        user_token = response_data['token']

        response = self.client().patch(
            f'/users/{user["data"]["username"]}',
            json={
                'question_id': question['data']['question_id']},
            headers={
                'Authorization': f"Bearer {user_token}"})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['username'])
        self.assertTrue(data['score'])

    def test_u_update_score_with_invalid_token(self):
        response = self.client().patch('/users/jbaba', json={'question_id': 23}, headers={
            'Authorization': f"Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImpiYWJhIiwiZXhwIjoxNjYxNzU1NzEwfQ.2gGXfrEQZPd1HFtORbhyTjUWdgC-LCEh_RjvxzTWc9N"})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unauthorized')

    def test_v_getting_a_user(self):
        user = add_user(self)
        response = self.client().get(f'/users/{user["data"]["username"]}',
                                     headers={'Authorization': f"Bearer {user['data']['token']}"})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['username'])
        self.assertEqual(len(data['answered_questions']), 0)

    def test_w_getting_user_with_invalid_token(self):
        response = self.client().get(
            '/users/jbaba',
            headers={
                'Authorization': f"Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImpiYWJhIiwiZXhwIjoxNjYxNzU1NzEwfQ.2gGXfrEQZPd1HFtORbhyTjUWdgC-LCEh_RjvxzTWc9N"})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unauthorized')

    def test_y_deleting_question(self):
        question = add_question(self)

        response = self.client().delete(
            f'/questions/{question["data"]["question_id"]}')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['deleted_question_id'],
                         question['data']['question_id'])

    def test_z_deleting_invalid_question(self):
        response = self.client().delete('/questions/1000')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
