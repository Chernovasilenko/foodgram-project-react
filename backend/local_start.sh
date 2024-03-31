#!/bin/bash

python manage.py load_ingredients
python manage.py load_tags
python manage.py addsuperuser

python manage.py runserver