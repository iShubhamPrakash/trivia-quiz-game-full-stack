import os
import unittest
import json
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
    self.database_username='postgres'
    self.database_password='shubham@123'
    self.database_path = 'postgresql://{}:{}@localhost:5432/{}'.format(self.database_username,self.database_password,self.database_name)
    setup_db(self.app, self.database_path)

    # sample question for tests
    self.new_question = {
      'question': 'Who is the best?',
      'answer': 'Shubham is the best',
      'difficulty': 3,
      'category': '3'
    }

    # binds the app to the current context
    with self.app.app_context():
      self.db = SQLAlchemy()
      self.db.init_app(self.app)
      # create all tables
      self.db.create_all()

  def tearDown(self):
    """Executed after reach test"""
    pass

# TEST 1
  def test_test(self):
    """Tests /test endpoint success"""

    # get the response
    response = self.client().get('/test')

    # verify status code
    self.assertEqual(response.status_code, 200)


# TEST 2
  def test_questions(self):
    """Tests /questions endpoint success"""

    # get response and data
    response = self.client().get('/questions')
    data = json.loads(response.data)

    # verify status code and message
    self.assertEqual(response.status_code, 200)
    self.assertEqual(data['success'], True)

    # verify that total_questions and questions return data
    self.assertTrue(data['total_questions'])
    self.assertTrue(len(data['questions']))


# TEST 3
  def test_404_if_invalid_page(self):
    """Tests /questions endpoint pagination failure 404"""

    # send request with bad page data, load response
    response = self.client().get('/questions?page=100')
    data = json.loads(response.data)

    # verify status code and message
    self.assertEqual(response.status_code, 404)
    self.assertEqual(data['success'], False)
    self.assertEqual(data['message'], 'resource not found')


# TEST 4
  def test_delete_question(self):
    """Tests question deletion success"""

    # create a new question to be deleted using the sample dictionary above
    question = Question(question=self.new_question['question'],
                        answer=self.new_question['answer'],
                        category=self.new_question['category'],
                        difficulty=self.new_question['difficulty'])
    # Add this new question to the database
    question.insert()

    # get the id of the new question
    q_id = question.id

    # get number of questions before delete
    questions_before = Question.query.all()

    # delete the question and store response
    response = self.client().delete('/questions/{}'.format(q_id))
    data = json.loads(response.data)

    # get number of questions after delete
    questions_after = Question.query.all()

    # verify if the question has been deleted
    question = Question.query.filter(Question.id == 1).one_or_none()

    # verify status code and success message
    self.assertEqual(response.status_code, 200)
    self.assertEqual(data['success'], True)

    # verify if question id matches with the deleted id
    self.assertEqual(data['deleted'], q_id)

    # verify if total no of questions reduced by 1 after delete
    self.assertTrue(len(questions_before) - len(questions_after) == 1)

    # verify if question equals None after delete
    self.assertEqual(question, None)


# TEST 5
  def test_add_new_question(self):
    """Tests add question success"""
    # get number of questions before adding new question
    questions_before = Question.query.all()

    # add a new question
    response = self.client().post('/questions', json=self.new_question)

    #load response data
    data = json.loads(response.data)

    # get number of questions after adding a new question
    questions_after = Question.query.all()

    # verify if the question has been created
    question = Question.query.filter_by(id=data['created']).one_or_none()

    # verify the status code to be 200 and success message
    self.assertEqual(response.status_code, 200)
    self.assertEqual(data['success'], True)

    # verify total question count incremented by 1 after adding a new question
    self.assertTrue(len(questions_after) - len(questions_before) == 1)

    # verify that question is not None
    self.assertIsNotNone(question)


# TEST 6
  def test_400_if_add_question_fails(self):
    """Tests add question fail send error 400"""

    # Total number of questions before post
    questions_before = Question.query.all()

    # add new question without correct json data
    response = self.client().post('/questions', json={})

    #load the response data
    data = json.loads(response.data)

    # Total number of questions after post
    questions_after = Question.query.all()

    # verify status code and success message
    self.assertEqual(response.status_code, 400)
    self.assertEqual(data['success'], False)

    # verify if total questions count after and total questions count before are equal
    self.assertTrue(len(questions_after) == len(questions_before))


# TEST 7
  def test_questions_search(self):
    """Tests questions search success"""

    # send post request with searchTerm
    response = self.client().post('/questions/search', json={'searchTerm': 'egyptians'})

    # load response data
    data = json.loads(response.data)

    # verify response status code is 200 and success message
    self.assertEqual(response.status_code, 200)
    self.assertEqual(data['success'], True)

    # verify that number of results is 1
    self.assertEqual(len(data['questions']), 1)

    # verify that id of question in response is correct
    self.assertEqual(data['questions'][0]['id'], 23)


# TEST 8
  def test_status_404_no_search_result(self):
    """Tests search questions failure 404 if no result found"""

    # send post request with search term that should fail
    response = self.client().post('/questions/search', json={'searchTerm': 'shubham@#$hf'})

    # load response data
    data = json.loads(response.data)

    # verify response status code is 404 and success message false
    self.assertEqual(response.status_code, 404)
    self.assertEqual(data['success'], False)
    self.assertEqual(data['message'], 'resource not found')


# TEST 9
  def test_questions_by_category(self):
    """Tests fetching questions by category success"""

    # send request with category id 1 for science
    response = self.client().get('/categories/1/questions')

    # load response data
    data = json.loads(response.data)

    # verify response status code to be 200 and success message to be true
    self.assertEqual(response.status_code, 200)
    self.assertEqual(data['success'], True)

    # verify that questions are returned
    self.assertNotEqual(len(data['questions']), 0)

    # verify that current category returned is science
    self.assertEqual(data['current_category'], 'Science')


# TEST 10
  def test_status_404_if_questions_by_category_fails(self):
    """Tests 404 error when getting questions by category fails"""

    # send request with category id 23
    response = self.client().get('/categories/23/questions')

    # load response data
    data = json.loads(response.data)

    # verify response status code to be 404 and sucecess message to be true
    self.assertEqual(response.status_code, 404)
    self.assertEqual(data['success'], False)
    self.assertEqual(data['message'], 'resource not found')


# TEST 11
  def test_play_quizz_game(self):
    """Tests playing quizz game success"""

    # send post request with category and previous questions
    response = self.client().post('/quizzes',json={'previous_questions': [20, 21],
                                  'quiz_category': {'type': 'Science', 'id': '1'}})

    # load response data
    data = json.loads(response.data)

    # verify response status code to be 200 and success message to be true
    self.assertEqual(response.status_code, 200)
    self.assertEqual(data['success'], True)

    # verify that a question is returned
    self.assertTrue(data['question'])

    # verify that the question returned is in correct category
    self.assertEqual(data['question']['category'], 1)

    # verify that question returned is not on previous q list
    self.assertNotEqual(data['question']['id'], 20)
    self.assertNotEqual(data['question']['id'], 21)


# TEST 12
  def test_play_quiz_fails(self):
    """Tests playing quiz game failure send error 422"""

    # send a post request without a correct json data
    response = self.client().post('/quizzes', json={})

    # load response data
    data = json.loads(response.data)

    # verify if the response status code is 422 and sucess message is false
    self.assertEqual(response.status_code, 422)
    self.assertEqual(data['success'], False)
    self.assertEqual(data['message'], 'unprocessable')


# Make the tests conveniently executable
if __name__ == "__main__":
  unittest.main()
