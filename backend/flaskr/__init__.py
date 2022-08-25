from calendar import c
import os
from urllib import response
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from werkzeug.exceptions import HTTPException

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def make_categories_object():
    categories = Category.query.all()
    formatted_categories = [category.format() for category in categories]
    result = dict()
    for category in formatted_categories:
        result[category['id']] = category['type']
        
    return result

def paginate_questions(questions, page=1):
    page_start = (page - 1) * QUESTIONS_PER_PAGE
    page_end = page_start + QUESTIONS_PER_PAGE
    
    format_questions = [question.format() for question in questions]
    questions_on_page = format_questions[page_start:page_end]
    
    return questions_on_page

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
        page = request.args.get('page', 1, type=int)
        try:
            questions = Question.query.order_by(Question.id).all()
            paginated_questions = paginate_questions(questions, page)
            if len(paginated_questions) == 0:
                abort(404)
            current_category = Category.query.first().format()['type']
            
            return jsonify({
                'questions': paginated_questions,
                'totalQuestions': len(questions),
                'currentCategory': current_category,
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
    @app.route('/questions', methods={'POST'})
    def post_new_question():
        body = request.get_json()
        expected_body_keys = ['question', 'answer', 'category', 'difficulty']
        for key in expected_body_keys:
            if key not in body:
                abort(400)
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
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """

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

    return app

