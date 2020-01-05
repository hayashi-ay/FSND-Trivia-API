# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Trivia API Reference

### Error Handling
Errors are returned as JSON objects in the following format and the corresponding error code.
```
{
  "message": "The requested URL was not found on the server. 
}
```

The API will return three error when requests fail.
 - 404: Resource Not Found
 - 422: Not Processable
 - 500: Somenthing Went Wrong

### Endpoints
#### GET /questions
 - get questions based on request
 - results are paginated in groups of 10

| Name | Data Type | Required / Optional | Description |
|:--|:--|:--|:--|
| page | int | Optional | Page Number. Default is 1. |
| category_id | int | Optional | If not provided, questions of all categories are returned. |
| search_term | string | Optional | Search Term (e.g. "movie", "medicine"). |
#### POST /questions
 - create a new question

| Name | Data Type | Required / Optional | Description |
|:--|:--|:--|:--|
| question | string | Required | The text of a question. |
| answer | string | Required | The answer of a question. |
| difficulty | int | Required | The difficulty of a question. |
| category | int | Required | The category ID of a question. |
#### DELETE /questions/{question_id}
 - delete question using a question ID
#### GET /categories
 - get all categories
#### POST /quizzes
 - get questions to play the quiz
 - questions are randomly returned

| Name | Data Type | Required / Optional | Description |
|:--|:--|:--|:--|
| previous_questions | list(int) | Required | List of previous question IDs. |
| category_id | id | Optional | If not provided, questions are returned from  all categories. |




## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
