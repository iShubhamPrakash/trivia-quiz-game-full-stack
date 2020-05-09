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

## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```


## Summary of major tasks done

1. Used Flask-CORS to enable cross-domain requests and set response headers.
2. Created an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint returns a list of questions, number of total questions, current category, categories.
3. Created an endpoint to handle GET requests for all available categories.
4. Created an endpoint to DELETE question using a question ID.
5. Created an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score.
6. Created a POST endpoint to get questions based on category.
7. Created a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question.
8. Created a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions.
9. Created error handlers for all expected errors including 400, 404, 422 and 500.

## API Reference

### Base URL
Currently this application is only hosted locally. The backend is hosted at http://127.0.0.1:5000/

### Authentication:
This version does not require authentication or API keys.

### Error Handling

Errors are returned as JSON in the following format:
```
{
    "success": False,
    "error": 400,
    "message": "bad request"
}
```

List of possible errors returned by the API:

400 – bad request
404 – resource not found
422 – unprocessable

## API Endpoints

#### GET /test

* General: This is  an endpoint to quickly test if the server is up and running.
* Returns a string.

* Sample: `curl http://127.0.0.1:5000/test`<br>

```
  Hello world. server is up and running...
```

#### GET /categories

* General: Returns a list categories.
* Sample: `curl http://127.0.0.1:5000/categories`<br>

        {
            "categories": {
                "1": "Science",
                "2": "Art",
                "3": "Geography",
                "4": "History",
                "5": "Entertainment",
                "6": "Sports"
            },
            "success": true
        }



#### GET /questions

* General:
  * Returns a list questions.
  * Results are paginated in groups of 10.
  * Also returns list of categories and total number of questions.
* Sample: `curl http://127.0.0.1:5000/questions`<br>
```
    {
        "categories": {
            "1": "Science",
            "2": "Art",
            "3": "Geography",
            "4": "History",
            "5": "Entertainment",
            "6": "Sports"
        },
        "questions": [
            {
                "answer": "Colorado, New Mexico, Arizona, Utah",
                "category": 3,
                "difficulty": 3,
                "id": 164,
                "question": "Which four states make up the 4 Corners region of the US?"
            },
            ...(total 10 items)
        ],
        "success": true,
        "total_questions": 23
    }
```

#### DELETE /questions/\<int:id\>

* General:
  * Deletes a question by id using url parameters.
  * Returns the id of deleted question upon success.
* Sample: `curl http://127.0.0.1:5000/questions/6 -X DELETE`<br>

```
  {
      "deleted": 6,
      "success": true
  }
```


#### POST /questions

* General:
  * Creates a new question using JSON request parameters.
  * Returns id of the newly created question
* Sample: `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{
            "question": "Where is the capital of India?",
            "answer": "Delhi",
            "difficulty": 1,
            "category": "3"
        }'`
        <br>
```
  {
      "created": 24,
      "success": true,
  }
```

#### POST /questions/search

* General:
  * Searches for questions using search term in JSON request parameters.
  * Returns JSON object with paginated matching questions.
* Sample: `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"searchTerm": "which"}'` <br>
```
  {
    "questions": [
        {
            "answer": "Agra",
            "category": 3,
            "difficulty": 2,
            "id": 15,
            "question": "The Taj Mahal is located in which Indian city?"
        },
        {
            "answer": "Escher",
            "category": 2,
            "difficulty": 1,
            "id": 16,
            "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
        },
        {
            "answer": "Jackson Pollock",
            "category": 2,
            "difficulty": 2,
            "id": 19,
            "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
        },
    ],
    "success": true,
    "total_questions": 3
  }
```


#### GET /categories/\<int:id\>/questions

* General:
  * Gets questions by category id using url parameters.
  * Returns JSON object with paginated matching questions.
* Sample: `curl http://127.0.0.1:5000/categories/1/questions`<br>
```
{
  "current_category": "Science",
  "questions": [
    {
        "answer": "The Liver",
        "category": 1,
        "difficulty": 4,
        "id": 20,
        "question": "What is the heaviest organ in the human body?"
    },
    {
        "answer": "Alexander Fleming",
        "category": 1,
        "difficulty": 3,
        "id": 21,
        "question": "Who discovered penicillin?"
    },
    {
        "answer": "Blood",
        "category": 1,
        "difficulty": 4,
        "id": 22,
        "question": "Hematology is a branch of medicine involving the study of what?"
    }
  ],
  "success": true,
  "total_questions": 23
}
```

#### POST /quizzes

* General:
  * Allows users to play the quiz game.
  * Uses JSON request parameters of category and previous questions.
  * Returns JSON object with random question not among previous questions.
* Sample: `curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"previous_questions": [20, 21],
                                            "quiz_category": {"type": "Science", "id": "23"}}'`<br>
```
  {
    "question": {
      "answer": "Shubham Prakash is the best",
      "category": 1,
      "difficulty": 4,
      "id": 23,
      "question": "Who is the best?"
    },
    "success": true
  }
```
