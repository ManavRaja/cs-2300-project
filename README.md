# cs-2300-project

<img src="recipe_site/main_app/static/top_left_logo-remove-bg.png" alt="My Image" width="300" />

# **Nom Nom**, your one-stop shop for a customized meal prep experience!
This website was created using Django and it is a meal prep website where users can create and store their own custom recipes and own custom weekly meal plans

## Installation Instructions
After cloning the repository, make sure you install all necessary dependencies by running
```
pip install -r requirements.txt
```

Then, change into the django project directory by running
```
cd recipe_site
```

Then, create a .enf file in the same directory as the settings.py file, create a variable called "DB_PASSWORD". Set it equal to "local-dev" if you want to use the built in sqlite file. Set it to your actual db password if you want to use Postgres and then change the other connecton settings in the settings.py file.

Then, to set up the database, run these 2 commands to create tables in your database.
```
python3 manage.py makemigrations
python3 manage.py migrate
```

Then, to start the Django webserver run the following command while in the `recipe_site` directory
```
python manage.py runserver
```

This will start a webserver on your local machine at localhost.
Then, you will be able to view and test the features of this web app.
