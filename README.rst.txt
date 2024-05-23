============
firstproject
============

firstproject is a Django app where we can add objects with field name and description. we can view the added objects in the /model/ page.

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "main" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...,
        "main",
    ]

2. Include the main URLconf in your project urls.py like this::

    path('',include("main.urls")),

3. Run ``python manage.py migrate`` to create the models.

4. Start the development server and visit the models page to view the objects. 

5. visit the homepage to view the "Django project" text.

