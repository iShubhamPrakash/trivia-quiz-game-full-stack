import os
import sys
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category
# print("Hello")
# print(sys.path)

QUESTIONS_PER_PAGE = 10

# A function which will return paginated question
def paginate_questions(total_questions, page):
  start = (page - 1) * QUESTIONS_PER_PAGE
  end = start + QUESTIONS_PER_PAGE
  # Generating list of formatted questions
  questions = [question.format() for question in total_questions]
  question_set = questions[start:end]

  return question_set

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)

  '''
    Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs             DONE
  '''
  cors = CORS(app)

  '''
  '''
  @app.after_request
  def after_request(response):
      response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
      response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
      return response

  @app.route('/test')
  def test():
    return 'Hello world. server is up and running...'

  '''
  Create an endpoint to handle GET requests
  for all available categories.
  '''
  @app.route('/categories')
  def get_categories():
    # get all categories from the database
    all_categories = Category.query.all()
    categories = {}
    for category in all_categories:
        categories[category.id] = category.type

    # abort 404 if no categories found
    if (len(categories) == 0):
        abort(404)

    # return data to the frontend
    return jsonify({
        'success': True,
        'categories': categories
    })

  '''
  Create an endpoint to handle GET requests for questions,
  including pagination (every 10 questions).
  This endpoint should return a list of questions,
  number of total questions, current category, categories.

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions.
  '''
  @app.route('/questions')
  def get_questions():
    # Get the page value from the query parameter
    page = request.args.get('page', 1, type=int)
    # get all te question from the database
    all_questions= Question.query.all()
    total_questions= len(all_questions)
    # Create a set of questions based on the page no
    question_set= paginate_questions(all_questions,page)

    # get all categories
    all_categories = Category.query.all()
    categories = {}
    for category in all_categories:
        categories[category.id] = category.type

    # abort if no questions
    if (len(question_set) == 0):
        abort(404)

    # return data to the client
    return jsonify({
        'success': True,
        'questions': question_set,
        'total_questions': total_questions,
        'categories': categories
    })


  '''
  Create an endpoint to DELETE question using a question ID.

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page.
  '''

  @app.route('/questions/<int:id>', methods=['DELETE'])
  def delete_question(id):
    try:
      # get the question by id
      question = Question.query.filter_by(id=id).one_or_none()

      # abort 404 if no question is found
      if question is None:
          abort(404)

      # deleting the question
      question.delete()

      # return a success response to the client
      return jsonify({
          'success': True,
          'deleted': id
      })
    # Error handeling
    except:
      abort(422)

  '''
  Create an endpoint to POST a new question,
  which will require the question and answer text,
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab,
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.
  '''
  @app.route('/questions', methods=['POST'])
  def post_question():
    body = request.get_json()
    # Data validation in request body
    if not ('question' in body and 'answer' in body and 'difficulty' in body and 'category' in body):
      abort(400)

    new_question = body.get('question').strip()
    new_answer = body.get('answer').strip()
    new_difficulty = body.get('difficulty')
    new_category = body.get('category')

    # Validate if question and answers is not empty
    if not (new_question and new_answer):
      abort(400)

    try:
      # Create a new question entry in the database
      question = Question(question=new_question, answer=new_answer,category=new_category, difficulty=new_difficulty,)
      question.insert()

      # return data to the client
      return jsonify({
        'success': True,
        'created': question.id
      })

    except:
      abort(422)

  '''
  Create a POST endpoint to get questions based on a search term.
  It should return any questions for whom the search term
  is a substring of the question.

  TEST: Search by any phrase. The questions list will update to include
  only question that include that string within their question.
  Try using the word "title" to start.
  '''
  @app.route('/questions/search', methods=['POST'])
  def search_questions():
    body = request.get_json()
    search_term = body.get('searchTerm', None)

    # abort if searchTerm is empty
    if not search_term:
      abort(404)

    # Search questions in the database
    search_results = Question.query.filter(
        Question.question.ilike(f'%{search_term}%')).all()

     # Abort 404 if no results found in the database
    if (len(search_results) == 0):
      abort(404)

    # Format the search result
    questions=[question.format() for question in search_results]

    # Send response to the client
    return jsonify({
      'success': True,
      'questions': questions,
      'total_questions': len(search_results),
      'current_category': None
    })

  '''
  Create a GET endpoint to get questions based on category.

  TEST: In the "List" tab / main screen, clicking on one of the
  categories in the left column will cause only questions of that
  category to be shown.
  '''
  @app.route('/categories/<int:id>/questions')
  def get_questions_by_category(id):
    # get the category by id from the database
    category = Category.query.filter_by(id=id).one_or_none()

    # abort 404 if category not found
    if (category is None):
      abort(404)

    # get filtered question from the database
    all_questions = Question.query.filter_by(category=category.id).all()
    questions= [question.format() for question in all_questions]

    # return the results to the client
    return jsonify({
      'success': True,
      'questions': questions,
      'total_questions': len(all_questions),
      'current_category': category.type
    })

  '''
  Create a POST endpoint to get questions to play the quiz.
  This endpoint should take category and previous question parameters
  and return a random questions within the given category,
  if provided, and that is not one of the previous questions.

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not.
  '''
  @app.route('/quizzes', methods=['POST'])
  def start_quiz():
    try:
      body = request.get_json()
      # validate if body contains required fields
      if not ('quiz_category' in body and 'previous_questions' in body):
        abort(400)

      category = body.get('quiz_category')
      previous_questions = body.get('previous_questions')

      # To make sure no question is repeated and everytime a new question is shown to the user
      if category['type'] == 'click':
        available_questions = Question.query.filter(
            Question.id.notin_((previous_questions))).all()
      else:
        available_questions = Question.query.filter_by(
            category=category['id']).filter(Question.id.notin_((previous_questions))).all()

      # Generate a random index between range 0 and the length of available_questions
      random_index=random.randrange(0, len(available_questions))

      # take a random question
      if len(available_questions) > 0:
        new_question = available_questions[random_index].format()
      else:
        new_question=None

      # Return response to the client
      return jsonify({
        'success': True,
        'question': new_question
      })
    except:
      abort(422)

  '''
  Create error handlers for all expected errors
  including 404 and 422.
  '''
  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      "success": False,
      "error": 400,
      "message": "bad request"
    }), 400

  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      "success": False,
      "error": 404,
      "message": "resource not found"
    }), 404

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      "success": False,
      "error": 422,
      "message": "unprocessable"
    }), 422

  return app
