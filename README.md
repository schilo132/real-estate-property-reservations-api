# Real Estate Property Reservations API
This project consists of Django REST APIs for a real estate property reservations system which currently consists of three types of database entities:
- Property
- Announcement
- Reservation

Every Announcement instance is associated with only one Property instance and every Reservation instance is associated with only one Announcement instance. The APIs should not allow deleting Announcement instances or editing Reservation instances. Additional checks are in place to prevent a new Reservation instance from going over the number of remaining vacancies for its associated property, also checking for other Reservation instances with coinciding check-in/check-out dates. See the table below for relevant API usage information (searches may be refined according to field by using the `Filters` button at the top right of the API screens).

**Important: After the initial setup, head to http://127.0.0.1:8000/admin and login with your superuser credentials to authenticate before using the API.**

| URL | HTTP Method  | Action | 
|---|---|---|
| /admin/ |   | Admin panel |
| /properties/ | GET | Search list of Property instances |
| /properties/ | POST | Add new Property instance |
| /properties/{id} | GET | Search Property instance by ID |
| /properties/{id} | PUT | Edit Property instance by ID |
| /properties/{id} | DELETE | Delete Property instance by ID |
| /advertisements/ | GET | Search list of Advertisement instances |
| /advertisements/ | POST | Add new Advertisement instance |
| /advertisements/{id}  | GET | Search Advertisement instance by ID |
| /advertisements/{id} | PUT | Edit Advertisement instance by ID  |
| /reservations/ | GET | Search list of Reservation instances |
| /reservations/ | POST | Add new Reservation instance |
| /reservations/{id} | GET  | Search Reservation instance by ID |
| /reservations/{id} | DELETE | Delete Reservation instance by ID |

### Setup

#### Linux

Run the following commands in the project's root folder to prepare the virtual environment:
- `python3 -m venv venv`
- `source venv/bin/activate`

Install the dependencies:
- `pip install -r requirements.txt`

Start the database and create a superuser:
- `python3 manage.py migrate`
- `python3 manage.py createsuperuser`

Setup the database and load the fixtures to provide initial data:
- `python3 manage.py makemigrations khanto`
- `python3 manage.py migrate`
- `python3 manage.py loaddata fixtures.json`

Start the server:
- `python3 manage.py runserver`

The API may now be accessed at http://127.0.0.1:8000/. **Go to http://127.0.0.1:8000/admin and log in with your superuser credentials to authenticate before using the API.**

### Testing

Run the following command in the project's root folder:
- `python3 manage.py test`
