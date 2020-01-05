import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy import func, and_
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
    # pagination
    page = request.args.get('page', 1, type=int)
    offset = QUESTIONS_PER_PAGE * ( page - 1 )

    # dynamically constructing filters
    filters = []
    category_id = request.args.get('category_id', None, type=int)
    if category_id:
      filters.append( Question.category == category_id )
    search_term = request.args.get('search_term', None, type=str)
    if search_term:
      filters.append( Question.question.ilike( '%{}%'.format( search_term ) ) )

    data = Question.query.filter(and_(*filters)).order_by(Question.id).limit(QUESTIONS_PER_PAGE).offset(offset)
    questions = list( map( lambda x: x.format(), data ) )

    data = Category.query.order_by(Category.id).all()
    categories = {}
    for category in data:
      categories[category.id] = category.type

    if len(questions) == 0:
      abort(404)

    return jsonify({
      'questions': questions,
      'total_questions': Question.query.filter(and_(*filters)).count(),
      'categories': categories,
      'current_category': category_id
    })

  @app.route('/questions/<int:question_id>', methods=['DELETE'])
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

  @app.route('/quizzes', methods=['POST'])
  def quizzes():
    body = request.get_json()

    # dynamically constructing filters
    filters = []
    previous_questions = body['previous_questions']
    if len(previous_questions):
      filters.append( Question.id.notin_(previous_questions) )
    category_id = body.get('category_id', None)
    if category_id:
      filters.append( Question.category == int(category_id) )

    question = Question.query.filter(and_(*filters)).order_by(func.random()).first()
    if question:
      question = question.format()

    return jsonify({
          'question': question
        }), 200

  @app.errorhandler(404)
  @app.errorhandler(422)
  @app.errorhandler(500)
  def error_handler(error):
    return jsonify({
      'message': error.description
    }), error.code
  
  return app