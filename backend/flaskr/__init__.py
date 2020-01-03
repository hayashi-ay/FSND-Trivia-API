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

  CORS(app)

  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
    return response

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
      'total_questions': Question.query.count(),
      'categories': categories,
      'current_category': None
    })

  @app.route('/questions/<question_id>', methods=['DELETE'])
  def delete_questions(question_id):
    question = Question.query.filter_by(id=question_id).one_or_none()

    if question is None:
      abort(422)

    error = False
    try:
      question.delete()
    except:
      error = True
      rollback_db()
      print( sys.exc_info() )
    finally:
      close_db()
      if error:
        abort(500)
      else:
        return jsonify({
          'message': 'Deleted'
        }), 200

  @app.route('/questions', methods=['POST'])
  def create_questions():
    error = False
    try:
      body = request.get_json()
      question = Question( body['question'], body['answer'], body['difficulty'], body['category'] )
      question.insert()
    except:
      error = True
      rollback_db()
      print( sys.exc_info() )
    finally:
      close_db()
      if error:
        abort(500)
      else:
        return jsonify({
          'message': 'Created'
        }), 201

  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''

  @app.route('/categories/<int:category_id>/questions')
  def questions_by_category(category_id):
    data = Question.query.filter_by(category=category_id).order_by(Question.id)
    questions = list( map( lambda x: x.format(), data ) )

    if len(questions) == 0:
      abort(404)

    return jsonify({
      'questions': questions,
      'total_questions': Question.query.filter_by(category=category_id).count(),
      'current_category': category_id
    })


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
  @app.errorhandler(422)
  @app.errorhandler(500)
  def error_handler(error):
    return jsonify({
      'message': error.description
    }), error.code
  
  return app

    