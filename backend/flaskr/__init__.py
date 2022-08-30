from calendar import c
import os
from unicodedata import category
from urllib import response
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from werkzeug.exceptions import HTTPException
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from dotenv import load_dotenv

from models import setup_db, Question, Category, User, db

QUESTIONS_PER_PAGE = 10
load_dotenv()

def make_categories_object():
    categories = Category.query.all()
    formatted_categories = [category.format() for category in categories]
    result = dict()
    for category in formatted_categories:
        result[category['id']] = category['type']
        
    return result

def paginate_questions(questions, request):
    page = request.args.get('page', 1, type=int)
    page_start = (page - 1) * QUESTIONS_PER_PAGE
    page_end = page_start + QUESTIONS_PER_PAGE
    
    format_questions = [question.format() for question in questions]
    questions_on_page = format_questions[page_start:page_end]
    
    return questions_on_page

def unused_ids(all_ids, previous_ids):
    unused = []
    for id in all_ids:
        if id not in previous_ids:
            unused.append(id)
            
    return unused

def get_token(user):
    timeLimit= datetime.datetime.utcnow() + datetime.timedelta(minutes=50)
    token = jwt.encode({'username': user['username'], 'exp': timeLimit}, os.getenv('SECRET_KEY'))
    
    return token

def is_correct_password(hashed_password, inputted_password):
    is_valid = check_password_hash(hashed_password, inputted_password)
    
    return is_valid

def validate_token(auth):
    if auth is None or auth.find('Bearer ') == -1:
        abort(401)
    token = auth.split(' ')[1]
    try:
        decoded_token = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=["HS256"])
        if decoded_token is None:
            abort(401)
    except:
        abort(401)
    
    # return decoded_token

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    CORS(app, resources={r"/*": {"origins": "*"}})

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type: application/json')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, DELETE, PATCH, OPTION')
        
        return response

    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route('/categories')
    def get_all_categories():
        try:
            result = make_categories_object()
                        
            return jsonify({
                'categories': result
            })
        except:
            abort(404)
        

    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    @app.route('/questions')
    def get_all_questions():
        try:
            questions = Question.query.order_by(Question.id).all()
            paginated_questions = paginate_questions(questions, request)
            if len(paginated_questions) == 0:
                abort(404)
            current_category = Category.query.first().format()['type']
            
            return jsonify({
                'questions': paginated_questions,
                'total_questions': len(questions),
                'current_category': current_category,
                'categories': make_categories_object()
            })      
        except:
            abort(404)
            
    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route('/questions/<int:id>', methods={'DELETE'})
    def delete_a_question(id):
        try:
            question = Question.query.filter_by(id=id).first()
            if question is None:
                return abort(404)
            
            question.delete()
            
            return jsonify({
                'id': id
            })
        except Exception as e:
            if isinstance(e, HTTPException):
                abort(e.code)    
            abort(422)

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    
    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    
    @app.route('/questions', methods={'POST'})
    def post_new_question():
        body = request.get_json()
        question_post = False
        search_post = False
        if 'searchTerm' in body:
            search_post = True
        
        if not(search_post):
            expected_body_keys = ['question', 'answer', 'category', 'difficulty']
            keys_in_body = 0
            for key in expected_body_keys:
                if key in body:
                    keys_in_body = keys_in_body + 1
            if keys_in_body == 4:
                question_post = True
                
        if not(question_post) and not(search_post):
            abort(400)
            
        if search_post:
            try:
                questions_with_search_term = Question.query.filter(Question.question.ilike('%' + body['searchTerm'] + '%')).all()
                paginated_questions = paginate_questions(questions_with_search_term, request)
                if len(questions_with_search_term) == 0:
                    return jsonify({
                    'questions': [],
                    'total_questions': 0,
                    'current_category': ""
                })
                category_id = paginated_questions[0]['category']
                category = Category.query.filter_by(id=category_id).first().format()
                
                return jsonify({
                    'questions': paginated_questions,
                    'total_questions': len(questions_with_search_term),
                    'current_category': category['type']
                })
            except Exception as e:
                if isinstance(e, HTTPException):
                    abort(e.code)
                abort(422)
        
        if question_post:     
            try:
                question = Question(question=body['question'], answer=body['answer'], difficulty=body['difficulty'], category=body['category'])
                if not question:
                    abort(422)
                question.insert()
                
                return jsonify({})
            except Exception as e:
                if isinstance(e, HTTPException):
                    abort(e.code)
                abort(422)

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route('/categories/<int:id>/questions')
    def get_questions_by_categories(id):
        try:
            questions = Question.query.filter_by(category=str(id)).all()
            if len(questions) == 0:
                abort(404)
                
            paginated_questions = paginate_questions(questions, request)
            category_id = paginated_questions[0]['category']
            category = Category.query.filter_by(id=str(category_id)).first().format()
            
            return jsonify({
                'questions': paginated_questions,
                'total_questions': len(questions),
                'current_category': category['type']
            })
        except Exception as e:
            if isinstance(e, HTTPException):
                abort(e.code)
            abort(422)
            

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    @app.route('/quizzes', methods=['POST'])
    def get_quiz():
        body = request.get_json()
        if 'quiz_category' not in body or 'previous_questions' not in body:
            abort(400)
        category_id = body['quiz_category']['id']
        previous_questions = body['previous_questions']
        
        try:
            category = Category.query.filter_by(id=category_id).first()
            if category is None and category_id != 0:
                abort(404)
            category_questions = []
            if category_id == 0:
                category_questions = Question.query.all()
            else:
                category_questions = Question.query.filter_by(category=str(category_id)).all()
            formatted_questions_ids = [question.format()['id'] for question in category_questions]
            unused = unused_ids(formatted_questions_ids, previous_questions)
            random_id = random.choice(unused)
            question = Question.query.filter_by(id=random_id).first().format()
            
            return jsonify({
                'question': question
            })
            
        except Exception as e:
            if isinstance(e, HTTPException):
                abort(e.code)
            abort(404)
            
    
    @app.route('/users', methods=['POST'])
    def add_new_user():
        body = request.get_json()
        if 'username' not in body or 'password' not in body:
            abort(400)
        try:
            user = User.query.filter_by(username=body['username']).first()
            if user:
                abort(400)
            hashed_password = generate_password_hash(body['password'])
            user = User(username=body['username'], password=hashed_password)
            if user is None:
                abort(422)
            user.insert()
            
            formatted_user = user.format()
            
            return jsonify({
                'id': formatted_user['id'],
                'username': formatted_user['username'],
                'score': formatted_user['score'],
                'token': get_token(formatted_user)
            })
        except Exception as e:
            if isinstance(e, HTTPException):
                abort(e.code)
            abort(422)
            
            
    @app.route('/users/login', methods=['POST'])
    def login():
        body = request.get_json()
        if 'username' not in body or 'password' not in body:
            abort(400)
        try:
            user = User.query.filter_by(username=body['username']).first().format()
            if user is None:
                abort(401)
            is_password_correct = is_correct_password(user['password'], body['password'])
            if not(is_password_correct):
                abort(401)
            
            return jsonify({
                'id': user['id'],
                'username': user['username'],
                'score': user['score'],
                'token': get_token(user)
            })
        except Exception as e:
            if isinstance(e, HTTPException):
                abort(e.code)
            abort(422)
            
            
    @app.route('/users/<string:username>', methods=['PATCH'])
    def update_user_score(username):
        auth = request.headers['AUTHORIZATION']
        validate_token(auth)
        body = request.get_json()
        if 'question_id' not in body:
            abort(400)
            
        try:
            user = User.query.filter_by(username=username).first()
            question = Question.query.filter_by(id=body['question_id']).first()
            if user is None or question is None:
                abort(400)
                
            formatted_user = user.format()
            if question not in user.questions:
                user.score = formatted_user['score'] + 1
                user.questions.append(question)
                user.update()
                            
            return jsonify({
                'username': formatted_user['username'],
                'score': user.score
            })
        except Exception as e:
            if isinstance(e, HTTPException):
                abort(e.code)
            abort(422)
            
            
    @app.route('/users/<string:username>')
    def get_user(username):
        auth = request.headers['AUTHORIZATION']
        validate_token(auth)
        
        try:
            # user = User.query.join(Question).filter(User.username==username).first()
            user = db.session.query(User).filter(User.username==username).first()
            questions = user.questions
            formated_questions = [question.format() for question in questions]
            if user is None:
                abort(404)
            return jsonify({
                'username': user.username,
                'score': user.score,
                'answered_questions':formated_questions
            })
        except Exception as e:
            if isinstance(e, HTTPException):
                abort(e.code)
            abort(404)

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(400)
    def not_found_error(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'Bad Request'
        }), 400
        
    @app.errorhandler(404)
    def not_found_error(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'Resource Not Found'
        }), 404
        
    @app.errorhandler(405)
    def method_not_allowed_method(error):
        return jsonify({
            'success': False,
            'error': 405,
            'message': 'Method Not Allowed'
        }), 405
        
    @app.errorhandler(422)
    def unprocessed(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'Unprocessed'
        }), 422
        
    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({
            'success': False,
            'error': 401,
            'message': 'Unauthorized'
        }), 401

    return app

