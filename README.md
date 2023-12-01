# Binghamton Quiz


## Description

This a Django Based Quiz Application which uses HTML/CSS for frontend and Django for Backend which uses postgresql as database

## Setup

### Prerequisites

- Python 3.x
- Django

### Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/lakshwanth-prasad/bing-quiz.git
    cd your-django-project
    ```

2. Create a virtual environment (optional but recommended):

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. Install dependencies:

    ```bash
	pip install -r pip install psycopg2
    pip install -r pip install matplotlib
	
    ```

4. Run migrations:

    ```bash
    python manage.py migrate
    ```

5. Create a superuser (Mandatory for Teacher):

    ```bash
    python manage.py createsuperuser
    ```

6. Run the development server:

    ```bash
    python manage.py runserver
    ```

The Django project will be accessible at [http://localhost:8000/](http://localhost:8000/).

## Usage

Accessing the App:

Provide the URL to access the app (e.g., http://localhost:8000).
Navigating the App:

Detail the steps to navigate the app, including how to:
Login in - Using Credentials
Access the quiz dashboard - Available courses
View and Take Quiz - According to the topics
Participate in a quiz
View Individual Results

## Contributing

If you'd like to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Create a new pull request.



