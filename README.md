# Hexrestapi - introduction and installation 

Hi! 
hexrestapi is an application that allows you to upload any image in JPG or PNG format via HTTP request, which is converted into a thumbnail of a size depending on the user's plan. There are 3 types of plans: Basic, Premium, Enterprise 

1. users that have "Basic" plan after uploading an image get: 
- a link to a thumbnail that's 200px in height

2. users that have "Premium" plan get:
- a link to a thumbnail that's 200px in height
- a link to a thumbnail that's 400px in height
- a link to the originally uploaded image

3. users that have "Enterprise" plan get
- a link to a thumbnail that's 200px in height
- a link to a thumbnail that's 400px in height
- a link to the originally uploaded image
- ability to fetch a link that expires after a number of seconds (user can specify any number between 300 and 30000)


In addition, the API gives the admin the ability to create arbitrary plans with the following things configurable:
- arbitrary thumbnail sizes
- presence of the link to the originally uploaded file
- ability to generate expiring links



## Run project

The first thing to do is upload source files or to clone the repository:

```sh
$ mkdir hexrestapi
$ cd hexrestapi #move here source files or clone git respiratory
$ git clone https://github.com/.../ 
```

Create a virtual environment to install dependencies in and activate it:
(I assume you have python installed)

```sh
$ python venv venv
$ source venv/bin/activate #for Windows user type "venv/Scripts/activate
```

Then install the dependencies:
(If u want to install project localy use `requirements-dev.txt`)

```sh
(venv)$ pip install -r requirements-dev.txt
```
Note the `(venv)` in front of the prompt. This indicates that this terminal
session operates in a virtual environment set up by `python venv`.

Once `pip` has finished downloading the dependencies:
```sh
(venv)$ cd hexrestapi
(venv)$ python manage.py runserver
```
Create super user(admin):
```sh
(venv)$ python manage.py createsuperuser
```

And navigate to `http://127.0.0.1:8000/admin/`, to create users and user plans.

Users can view their images and upload new ones at `http://127.0.0.1:8000/images/`

User permissions(plans) must be set manually in django-admin, each user automatically has a Basic plan(if created)
