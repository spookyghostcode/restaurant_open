# Restaurants API

This API currently has a single use: Querying for open restaurants given a specific date and time. The initial data is seeded in via a provided CSV file.

## Running the API

### Local
You may choose to use a Virtual Environment to run this API (as is recommended)
Once you have set that up, run:

``pip install -r requirements.txt``

Once that is finished, run the following command, which will seed a SQLite DB with the data in "restaurants.csv":

``python manage.py migrate``

And then, to spin up the API, run:

``python manage.py runserver``

### Docker
If you would like to use docker instead, simply run:

`docker compose up --build`

which should run the application on port 8000

## Using the API
Once the API is up and running, you can send a GET request to the server formatted as such:

``restaurant_list/?datetime=Jul 2 2024 11:30am``

and the server will return a list of open restaurants

## Running the Tests

If you have completed the pip installation steps, then you should be able to run the tests by running the command:

``pytest --ds=restaurant_open.settings``
