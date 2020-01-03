import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
import sys
from models import setup_db, rollback_db, close_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''

  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''

  @app.route('/categories')
  def categories():
    data = Category.query.all()

    categories = {}
    for category in data:
      categories[category.id] = category.type

    return jsonify({
      'categories': categories
    })

  @app.route('/questions')
  def questions():
    page = request.args.get('page', 1, type=int)
    offset = QUESTIONS_PER_PAGE * ( page - 1 )

    data = Question.query.order_by(Question.id).limit(QUESTIONS_PER_PAGE).offset(offset)
    questions = list( map( lambda x: x.format(), data ) )

    data = Category.query.order_by(Category.id).all()
    categories = {}
    for category in data:
      categories[category.id] = category.type

    if len(questions) == 0:
      abort(404)

    return jsonify({
      'questions': questions,
      'totalQuestions': Question.query.count(),
      'categories': categories,
      'currentCategory': None
    })

  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''

  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''

  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''

  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''


  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''

  @app.errorhandler(404)
  @app.errorhandler(500)
  def error_handler(error):
    return jsonify({
      'message': error.description
    }), error.code
  
  return app

    