# TRIVIA

Trivia api is a game api where you can fetch questions based on any category to
create a "trivial game".
You can fetch for all the questions, you can as well fetch for a single
question by providing the 'id' of the question.
Each question returns the question, answer to the question, the category
the question belongs to, and the rating of the question.
You can design a frontend of your choice to consume the data coming from
the api or you can use the frontend provided with the api.

## Getting Started

### Pre-requisites and Local Development

Developers using this project should already have Python3, pip and node
installed on their local machines.

### Backend

From the backend folder run pip install requirements.txt. All required
packages are included in the requirements file.

To run the application run the following commands:

```
    export FLASK_APP=flaskr
    export FLASK_ENV=development
    flask run
```

These commands put the application in development and directs our application
to use the **init**.py file in our flaskr folder. Working in development mode
shows an interactive debugger in the console and restarts the server whenever
changes are made. If running locally on Windows, look for the commands in the
[Flask documentation](https://flask.palletsprojects.com/en/2.2.x/).

The application is run on http://127.0.0.1:5000/ by default and is a proxy in the frontend configuration.

### Tests

In order to run tests navigate to the backend folder and run the following commands:

    dropdb trivia_test
    createdb trivia_test
    psql trivia_test < questions.psql
    python test_flaskr.py

The first time you run the tests, omit the dropdb command.
All tests are kept in that file and should be maintained as updates are made to app functionality.

## API Reference

### Getting Started

- Base Url: At present this api is hosted locally. The backend app is hosted at the default, http://127.0.0.1:5000/, which is set as a proxy in the frontend configuration.
- Authentication: The Api does not require authentication of any sort.

### Errors

Errors are returned in json format. The errors are returned with their respective error codes to elaborate on what type of error it is.
Example error code is showed below:

    {
        'success': False,
        'error': 404,
        'message': 'Not Found'
    }

The API will return one of the following errors if something goes wrong.

- 400: Bad Request
- 404: Resource Not Found
- 422: Not Processable
- 405: Method Not Allowed

### EndPoints

#### Get all questions

```http
  GET /questions
```

- General:  
  Returns a list of question objects, current category and total number of
  questions. Results are paginated in groups of 10. Include a request argument
  to choose page number, starting from 1.
- curl http://127.0.0.1:5000/questions
- Sample Response:

```
  {
     "questions": [
        {
            "answer": "Apollo 13",
            "category": 5,
            "difficulty": 4,
            "id": 2,
            "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
        },
        {
            "answer": "Tom Cruise",
            "category": 5,
            "difficulty": 4,
            "id": 4,
            "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
        },
        {
            "answer": "Maya Angelou",
            "category": 4,
            "difficulty": 2,
            "id": 5,
            "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
        },
        {
            "answer": "Edward Scissorhands",
            "category": 5,
            "difficulty": 3,
            "id": 6,
            "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
        },
        {
            "answer": "Muhammad Ali",
            "category": 4,
            "difficulty": 1,
            "id": 9,
            "question": "What boxer's original name is Cassius Clay?"
        },
        {
            "answer": "Brazil",
            "category": 6,
            "difficulty": 3,
            "id": 10,
            "question": "Which is the only team to play in every soccer World Cup tournament?"
        },
        {
            "answer": "Uruguay",
            "category": 6,
            "difficulty": 4,
            "id": 11,
            "question": "Which country won the first ever soccer World Cup in 1930?"
        },
        {
            "answer": "George Washington Carver",
            "category": 4,
            "difficulty": 2,
            "id": 12,
            "question": "Who invented Peanut Butter?"
        },
        {
            "answer": "Lake Victoria",
            "category": 3,
            "difficulty": 2,
            "id": 13,
            "question": "What is the largest lake in Africa?"
        },
        {
            "answer": "The Palace of Versailles",
            "category": 3,
            "difficulty": 3,
            "id": 14,
            "question": "In which royal palace would you find the Hall of Mirrors?"
        }
    ],
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    },
    "current_category": "Science",
    "total_questions": 20
}
```

#### Post a question

```
  POST /questions
```

- General:  
  Creates a new question using the submitted question, answer, category and
  difficulty. Returns an empty object.
- curl http://127.0.0.1:5000/questions?page=3 -X POST
  -H "Content-Type: application/json"
  -d '{"question":"How are you doing", "answer":"22", "rating":"1", "category":"3"}'

#### Delete a question by id

```
  DELETE /questions/{id}
```

- General:  
  Deletes the question of the given ID if it exists. Returns the id of the
  deleted question.
- curl -X DELETE http://127.0.0.1:5000/questions/35?page=2
- Sample Response:

```
{
    "id": 16
}
```

#### Get all categories

    GET /categories

- General:  
  Returns an object with key 'categories' and value containing an object
  containing all the categories keys and values.
- curl http://127.0.0.1:5000/categories
- Sample Response:

```
{
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    }
}
```

#### Search for question

```
POST /questions
```

- General:  
  Takes a search term in the post body and returns all the questions that
  have the search term as their substring, total_questions and the current_category.
- curl -X POST http://127.0.0.1:5000/questions?page=1 -H "Content-Type: application/json" -d '{"searchTerm": "What"}'
- Sample Response:

```
{
  "current_category": "History",
  "questions": [
    {
      "answer": "Muhammad Ali",
      "category": 4,
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
    },
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    },
    {
      "answer": "Lake Victoria",
      "category": 3,
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?"
    },
    {
      "answer": "Mona Lisa",
      "category": 2,
      "difficulty": 3,
      "id": 17,
      "question": "La Giaconda is better known as what?"
    },
    {
      "answer": "The Liver",
      "category": 1,
      "difficulty": 4,
      "id": 20,
      "question": "What is the heaviest organ in the human body?"
    },
    {
      "answer": "Blood",
      "category": 1,
      "difficulty": 4,
      "id": 22,
      "question": "Hematology is a branch of medicine involving the study of what?"
    }
  ],
  "total_questions": 8
}
```

#### Get all questions belonging to a category

    GET /categories/{id}/questions

- General:
  This endpoint returns all the questions belonging to the category labelled by
  id. It returns an object containig a list of questions, total_questions
  and the current category.
- curl http://127.0.0.1:5000/categories/1/questions
- Sample Response:

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
    },
    {
      "answer": "I don't think so",
      "category": 1,
      "difficulty": 1,
      "id": 32,
      "question": "Can we meet by 7?"
    }
  ],
  "total_questions": 4
}
```

## Authors

- John Toriola
- Udacity Team

## Acknowledgements

I am extremely grateful to everyone that has participated in my journey as a software developer.
Thanks and God bless you.
