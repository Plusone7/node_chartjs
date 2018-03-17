
cd into a directory where you’d like to store your code:

```python 
$ django-admin startproject mysite
```
will create a mysite directory in your current directory

---

```python 
$ python manage.py runserver
```

Now that the server’s running, visit http://127.0.0.1:8000/ 
with your Web browser. You’ll see a “Welcome to Django” page, in pleasant, light-blue pastel. 
It worked!

---
### Changing the port

this command starts the server on port 8080:

```python 
$ python manage.py runserver 8080

```
To create your app, 
make sure you’re in the same directory as manage.py and type this command:

```python
$ python manage.py startapp polls
```
That’ll create a directory polls

---

### Write your first view:
Open the file ```polls/views.py``` and put the following Python code in it:

```python
from django.http import HttpResponse

def index(request):
return HttpResponse("Hello, world. You're at the polls index.")
```
This is the simplest view possible in Django

To call the view, we need to map it to a URL - and for this we need a URLconf.
To create a URLconf in the polls directory, create a file called urls.py.

In the ```polls/urls.py``` file include the following code:

```python
from django.conf.urls import url

from . import views

urlpatterns = [
url(r'^$', views.index, name='index'),
]
```

The next step is to point the root URLconf at the polls.urls module.

In ```mysite/urls.py,``` 
add an import for``` django.conf.urls.include``` and insert an ```include()``` in the ```urlpatterns``` list


```python

from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
url(r'^polls/', include('polls.urls')),
url(r'^admin/', admin.site.urls),
]
```

```python
$ python manage.py runserver
```
Go to http://localhost:8000/polls/ in your browser, 
and you should see the text “Hello, world. You’re at the polls index.”, which you defined in the index view.


<https://docs.djangoproject.com/en/1.11/intro/tutorial01/>

---

### Database setup

open up ```mysite/settings.py ```
It’s a normal Python module with module-level variables representing Django settings.

```python
$ python manage.py migrate
```
The ```migrate``` command looks at the``` INSTALLED_APPS``` setting and creates any necessary database tables according to the database settings in your ```mysite/settings.py file```

---
### Creating models



Edit the polls/models.py file so it looks like this:
```python
from django.db import models

class Question(models.Model):
question_text = models.CharField(max_length=200)
pub_date = models.DateTimeField('date published')

class Choice(models.Model):
question = models.ForeignKey(Question, on_delete=models.CASCADE)
choice_text = models.CharField(max_length=200)
votes = models.IntegerField(default=0)
```

---

### Activating models

With it, Django is able to:
*Create a database schema (CREATE TABLE statements) for this app.
*Create a Python database-access API for accessing Question and Choice objects.
But first we need to tell our project that the polls app is installed.

To include the app in our project, we need to add a reference to its configuration class in the ```INSTALLED_APPS setting```. The ```PollsConfig``` class is in the ```polls/apps.py``` file, so its dotted path is ```'polls.apps.PollsConfig'```. 
Edit the ```mysite/settings.py``` file and add that dotted path to the ```INSTALLED_APPS``` setting.

```python
INSTALLED_APPS = [
'polls.apps.PollsConfig',
'django.contrib.admin',
'django.contrib.auth',
'django.contrib.contenttypes',
'django.contrib.sessions',
'django.contrib.messages',
'django.contrib.staticfiles',
]
```

Now Django knows to include the polls app. Let’s run another command:

```python
$ python manage.py makemigrations polls
```

You should see something similar to the following:
```
Migrations for 'polls':
polls/migrations/0001_initial.py:
- Create model Choice
- Create model Question
- Add field question to choice
```

By running ```makemigrations```, you’re telling Django that you’ve made some changes to your models and that you’d like the changes to be stored as a migration.

There’s a command that will run the migrations for you and manage your database schema automatically  
that’s called ```migrate```, and we’ll come to it in a moment
but first, let’s see what SQL that migration would run. 
The ```sqlmigrate``` command takes migration names and returns their SQL:

Now, run migrate again to create those model tables in your database:
```python
$ python manage.py migrate
```
Read the``` django-admin documentation ```for full information on what the manage.py utility can do.

---

### Playing with the API

```python
$ python manage.py shell
```




















