

### Create django project

```bash
$ django-admin.py startproject mydjango .
```

`django-admin.py`是一個可以創專案的腳本

接下來會看到資料目錄：

```
mydjango
├───manage.py
└───mysite
        settings.py
        urls.py
        wsgi.py
        __init__.py
```

`manage.py`用來管理django網站的腳本
`settings.py`包含網站中的各種設定

### Run web server 

```
python3 manage.py runserver
```

到`http://127.0.0.1:8000/`就可以看到建好的web server了！

如果8000port已經使用了，可以後面加上你要的`port`：
```
python3 manage.py runserver 3000
```
就可以看到：
Starting development server at http://127.0.0.1:3000/

### Start app

我們start一個叫`blog`的app

```
django-admin startapp blog
```

### Setting

在`settings.py`檔案中`Application definition`新增剛剛start的app`blog`

```python
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'blog',
]
```

在`models.py`
```python
from django.db import models
from django.core.urlresolvers import reverse
# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255,unique = True)
    summary = models.CharField(max_length=300)
    content = models.TextField()
    published = models.BooleanField(default = True)
    created = models.DateTimeField(auto_now_add=True)
    # Sub class Meta
    class Meta:
        ordering =['-created'] # sort this based on the date 
        def __unicolde__(self): # order for the posts to work
            return u'%s' %self.title #u'-> unicode
    def get_absolute_url(self):
        return reverse('blog.views.post',args=[self.slug])

```
儲存後
```
python3 ./manage.py migrate
```

### Create super user

```
python3 ./manage.py createsuperuser
```
Run Server
```
python3 ./manage.py runserver 
```
到 `http://127.0.0.1:8000/admin/` 登入後就可以看到Django administration頁面了。

### Admin 

到`admin.py`

```python
from django.contrib import admin
from .models import Post # @models.py
# post model
admin.site.register(Post)
```

migrate
```
python3 ./manage.py migrate
```
看到：
```
 No migrations to apply.
 Your models have changes that are not yet reflected in a migration, and so won't be applied.
 Run 'manage.py makemigrations' to make new migrations, and then re-run 'manage.py migrate' to apply them.
```

```
python3 ./manage.py makemigrations
python3 ./manage.py migrate
```
接著Run server
```
python3 ./manage.py runserver 
```

可以看到在admin畫面中多了`Post` 
點進去Post可以看到我們剛剛創建的`title`,`slug`,`summary`,`content`等欄位了！

### Creat Views

`urls.py`

```python
from django.conf.urls import url
from django.contrib import admin
from blog import views as blog_views
urlpatterns = [
    # define two routers (post,index)
    url(r'^post/$',blog_views.post),
    url(r'^$',blog_views.index),
    url(r'^admin/', admin.site.urls),
]
```

`views.py`

```python
from django.shortcuts import render
from django.http import HttpResponse
def index(request):
    return HttpResponse("Hey there.")
def post(request):
    return HttpResponse("I am a single post page")
```

接著Run server
```
python3 ./manage.py runserver 
```
到 `http://127.0.0.1:8000/` 與 `http://127.0.0.1:8000/post` 就可以看到頁面了！

### Templates

在blog底下建立一個`templates`資料夾，並建立一個HTML `index.html`

```html
<!DOCTYPE html>
<body>
    <h3>hello world ! plusone!</h3>
</body>
</html>
```
更改 `views.py`的`index` function
```python
def index(request):
    return render(request,'index.html',{})
```

在網頁上就可以看到:
`
hello world ! plusone!
`
### Dymanic template data
在`views.py`內import `models.py`在view內新增剛剛建立的Post class

```python
from .models import Post # @models.py
```
新增 posts變數存放Post.object

```python
def index(request):
    posts = Post.objects.all() 
    return render(request,'index.html',{'posts':posts})
```
`index.html`

```html
<!DOCTYPE html>
<body>
    <h2>hello world ! plusone!</h2>
    {% for post in posts %}
        <div>
            <h3><a href="/post/{{post.slug}}">{{post.title}}</a></h3>
            <h4>{{post.summary}}</h4>
            <p>{{post.content}}</p>
        </div>
    {% endfor %}
</body>
</html>
```

### Single post page

`views.py` 新增 `render_to_response ` ,` get_object_or_404 `和 `print(slug)`
```python
from django.shortcuts import render,render_to_response, get_object_or_404
from django.http import HttpResponse
from .models import Post # @models.py
def index(request):
    posts = Post.objects.all() 
    return render(request,'index.html',{'posts':posts})

def post(request,slug):
    print(slug)
    return render_to_response('post.html',{
        'post':get_object_or_404(Post,slug=slug) # Post class 
        # will match the slug find the post return it to the template in 'post'
})
```
`urls.py`新增`(.*)`在url(r'^post/',blog_views.post),內

```python
from django.conf.urls import url
from django.contrib import admin
from blog import views as blog_views
urlpatterns = [
    # define two routers (post,index)
    url(r'^post/(.*)$',blog_views.post),
    url(r'^$',blog_views.index),
    url(r'^admin/', admin.site.urls),
]
```
新增一個 `post.html`在templates目錄
```html
<a href="/"><-back to index</a><br><br>
<h3>{{post.title}}</h3>
<div>
    {{post.content}}
</div>
```

### Inplementing bootstrap3

安裝django-bootstrap3
```
pip install django-bootstrap3
```
在`settiings.py`新增bootstrap
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'blog',
    'bootstrap3',
]
```

`index.html`匯入bootstrap3
```html
{% load bootstrap3 %}
{% bootstrap_css %}
{% bootstrap_javascript %}
```
接著就可以看到網頁字體改變了！


### Static file

在`settings.py`內我們可以看到下面有一行
```python
STATIC_URL = '/static/'
```
現在我們建立一個`static`目錄
在`static`底下建立一個`css`目錄
在`css`目錄底下建立一個`style.css`檔案

style.css
```css
body{
 background-color:#bababf !important;
 #this is not going to be overidden    
}
```

`index.html`新增程式碼
```html
{% load static %}
<link rel="stylesheet" type="text/css" href="{% static 'css/style.css' %}">
```
就可以看到body顏色改變了！

### Template inheritance 

新增一個`base.html`在`template`目錄下
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    {% load static %}
    <link rel="stylesheet" type="text/css" href="{% static 'css/style.css' %}">
    {% load bootstrap3 %}
    {% bootstrap_css %}
    {% bootstrap_javascript %}
    <title>{% block title %} Mysite {% endblock %}</title>
</head>
<body>
    <nav class="navbar navbar-default">
        <div class="container-fluid">
            <div class="navbar-header">
                <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#bs-example-navbar-collapse-1"
                    aria-expanded="false">
                    <span class="sr-only">Toggle navigation</span>
                    <span class="icon-bar"></span>
                    <span class="icon-bar"></span>
                    <span class="icon-bar"></span>
                </button>
                <a class="navbar-brand" href="#">mysite</a>
            </div>
            <div class="collapse navbar-collapse" id="bs-example-navbar-collapse-1">
                <ul class="nav navbar-nav">
                    <li class="active"><a href="/">HOME<span class="sr-only">(current)</span></a></li>
                    <li><a href="#">Random Post</a></li>
                    <li><a href="#">My Profile</a></li>
                    <li><a href="#">Settings</a></li>
                </ul>
            </div>
        </div>
    </nav>
    <div id="content">
    {% block content %}
        This is fallback text
    {% endblock %}
    </div>
</body>
</html>
```

修改`index.html`檔案
```html
{% extends 'base.html'%}
<body>
    {% block content %}
        <h2>hello world ! plusone!</h2>
        {% for post in posts %}
            <div>
                <h3><a href="/post/{{post.slug}}">{{post.title}}</a></h3>
                <h4>{{post.summary}}</h4>
                <p>{{post.content}}</p>
            </div>
        {% endfor %}
    {% endblock %}
</body>
</html>
```
修改`post.html`檔案
```html
{% extends 'base.html'%}
    {% block content %}
    {% block title %} Mysite: {{ post.title }}{% endblock %}
    <a href="/"><-back to index</a><br><br>
    <h3>{{post.title}}</h3>
    <div>
        {{post.content}}
    </div>
{% endblock %}
```

### Post Images

`settings.py`下新增`
```python
STATIC_URL = '/static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR,'media/')
```

`models.py`下新增程式碼
```python
image = models.ImageFied(upload_to = 'img')
```



