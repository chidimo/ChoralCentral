# Somtochukwu (join me in praising the Lord)

A music sharing site


Output pdf
-----------

https://docs.djangoproject.com/en/1.11/howto/outputting-pdf/

https://github.com/nigma/django-easy-pdf/tree/v0.2.0-dev1

Added this ::
    <script type="text/javascript" src="/media/js/admin/RelatedObjectLookups.js"></script>
to my base template

For google chrome, download chromedriver from `here <https://chromedriver.storage.googleapis.com/index.html?path=2.27/>`_
Put it in the same directory as geckodriver, in Scripts directory


## Including django addanother

Add `django_addanother` to INSTALLED_APPS in settings

modify forms.py
-----------------
Add widgets for each field we wish to use popup


modify base.html
--------------------

Put this ::

    {% load static %}
    <script src="{% static 'admin/js/vendor/jquery/jquery.js' %}"></script>
    {{ form.media }}

in the head section of base template


## Correctly customizing User model

Follow this `guide <https://docs.djangoproject.com/en/1.11/topics/auth/customizing/#extending-the-existing-user-model>_`

Each time you create a custom user model you have to create the following too.
1. Custom user model manager
2. Custom UserCreationForm
3. Custom UserChangeForm
4. Custome UserAdmin form

Always create a custom user model when starting a project
Point AUTH_USER_MODEL to custom User before creating any migrations
or running manage.py migrate for the first time

1. Do this ::

    from django.contrib.auth.models import AbstractUser
    class CustomUserModelName(AbstractUser):
        first_name = models.CharField(max_length=30)
        last_name = models.CharField(max_length=30)
        username = models.CharField(max_length=30, unique=True)
        email = models.EmailField(max_length=50, unique=True)
        USERNAME_FIELD = 'email' # set email field for authentication
        REQUIRED_FIELDS = ["first_name", "last_name", "username"]

2. Add this line at end of settings.py file ::

    AUTH_USER_MODEL = 'appname.CustomUserModelName'

3. To use CustomUserModel in a model definition (ForeignKey or ManyToMany) ::

    settings.AUTH_USER_MODEL

4. To use this model anywhere else do the following ::

    from django.contrib.auth import get_user_model
    User = get_user_model()
    Then crete user object

### Order of operations when using custom user model ::

    python manage.py makemigrations appname
    python manage.py migrate appname
    # the above two steps create the table for storing custom users
    python manage.py migrate
    python manage.py createsuperuser


forms
---------
https://github.com/etianen/django-reversion


## play midi

https://stackoverflow.com/questions/5662293/how-to-play-a-midi-file-in-html

https://stackoverflow.com/questions/18172136/how-to-play-wav-file-in-all-browser-with-django#18172397

## last seen

https://stackoverflow.com/questions/2440603/django-last-login-attribute-in-auth-user-model#2441147

## sessions

https://docs.djangoproject.com/en/1.11/topics/http/sessions/


"login if you wish to like this song" redirects to a non-existent page.


## scaling

https://djangobook.com/scaling-django/

https://stackoverflow.com/questions/886221/does-django-scale?rq=1

https://blog.disqus.com/scaling-django-to-8-billion-page-views


## thumbnail
-----------
https://github.com/thumbor/thumbor

https://github.com/jazzband/sorl-thumbnail

form fields
https://github.com/jazzband/django-widget-tweaks

Search
----------
I'm going with Haystack and Solr
django search and solango no longer under active dev

<solr `https://archive.apache.org/dist/lucene/solr/4.10.4/`>_

http://haystacksearch.org/

https://stackoverflow.com/questions/2461322/how-to-implement-full-text-search-in-django#2461501

http://django-haystack.readthedocs.io/en/v2.5.0/tutorial.html

https://qbox.io/blog/how-to-elasticsearch-python-django-part1

http://www.chrisumbel.com/article/django_solr

http://www.opencrowd.com/blog/post/elasticsearch-django-tutorial/

http://bookofstranger.com/elastic-search-wih-django-haystack-for-search-functionality/

https://stackoverflow.com/questions/17761974/implementing-universal-search-in-a-django-application

http://www.nitinh.com/2009/10/implementing-search-in-django-site-using-haystack-and-xapian-whoosh/


## Dumping model data

Dump data to be used for test purposes ::

    python manage.py dumpdata ModelName --indent 4 > filename.json
    python manage.py dumpdata ModelName --natural-foreign --indent 4 > filename.json

During test run, place a list of fixture files at the begining of the class ::

    fixtures = ["list of fixture files"]


git checkout -b branchname
git push --set-upstream origin branchname


## Coloring

https://designschool.canva.com/blog/website-color-schemes/

https://www.dtelepathy.com/blog/inspiration/beautiful-color-palettes-for-your-next-web-project

http://www.colorzilla.com/chrome/

https://chrome.google.com/webstore/detail/colorpick-eyedropper/ohcpnigalekghcmgcdcenkpelffpdolg?hl=en-US&utm_source=chrome-ntp-launcher

wrap in html for visualstudiocode
-------------------------------------
https://marketplace.visualstudio.com/items?itemName=bradgashler.htmltagwrap

Virtual environment in pythonanywhere

mkvirtualenv myvirtualenv --python=/usr/bin/python3.6
