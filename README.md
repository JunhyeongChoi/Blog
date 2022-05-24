# blog
> 게시글 작성, 삭제, 댓글, 로그인/로그아웃 기능을 보유한 간단한 블로그

* [Blog 객체 생성](#Blog-객체-생성)

* [생성된 객체 확인하기](#생성된-객체-확인하기)

* [Blog 글 작성](#Blog-글-작성)

* [Blog 글들을 화면에 띄우기](#Blog-글들을-화면에-띄우기)

* [제목을 눌렀을 때 본문 보기](#제목을-눌렀을-때-본문-보기)

* [파일 업로드 구현](#파일-업로드-구현)

* [파일 업로드를 사용자에게도 보이기](#파일-업로드를-사용자에게도-보이기)

* [사진파일도 사용자 화면에 보이기](#사진파일도-사용자-화면에-보이기)

* [댓글 구현](#댓글-구현)

* [로그인 구현](#로그인-구현)

* [로그아웃 구현](#로그아웃-구현)

<br>

# Blog 객체 생성
```
class Blog(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
```
* 위 코드를 models.py에 작성하고 변경사항 파일을 생성하기 위해 아래 명령을 실행

* admin 사이트에서 Blog 글을 작성할 수 있는데 글 제목을 title field로 하려면 __str__을 정의한다.
```
python manage.py makemigrations
```
* 변경사항을 반영하기 위해 아래 명령을 실행
```
python manage.py migrate
```

<br>

# 생성된 객체 확인하기 
* Django는 admin 사이트에서 만든 model을 직접 확인할 수 있다.
```
from .models import Blog

admin.site.register(Blog)
```
* 위 코드를 admin.py에 작성하면 admin 사이트에서 Blog 객체를 확인할 수 있다.

<br>

# Blog 글 작성
## Django에서 사용자 입력을 받는 방법
1. HTML Form 이용
2. Django Form 이용
3. Django modelForm 이용

<br>

# 1. HTML Form 이용
* 글 작성 화면 HTML
```
<form action="{% url 'create' %}" method="POST">
    {% csrf_token %}
    <div>
        <label for="title">제목</label><br>
        <input type="text" name="title" id="title">
    </div>
    <div>
        <label for="body">본문</label><br>
        <textarea name="body" id="body" cols="30" rows="10"></textarea>
    </div>
    <input type="submit" value="글 생성하기">
</form>
```
* POST 방식으로 보낼 때는 보안 문제를 해결하기 위해 {% csrf_token %} 를 명시해야 함

## 블로그 글을 저장해주는 함수 (views.py)
```
from django.shortcuts import render, redirect
from .models import Blog
from django.utils import timezone  # 현재 시각

# 블로그 글을 저장해주는 함수
def create(request):
    if request.method == 'POST':  # 요청의 method가 POST라면
        post = Blog()
        post.title = request.POST['title']  # title 필드에 POST요청으로 들어온 요청안에 body안에 있는 내용
        post.body = request.POST['body']
        post.date = timezone.now
        post.save()  # 모델 객체를 데이터베이스에 저장
    return redirect('home')  # home 함수안 index.html로 다시 돌아감
```
* create함수는 어떠한 HTML을 보여주지 않으므로 요청을 보내고 특정 HTML로 다시 redirect 해야한다. (redirect도 import)

<br>

# 2. Django Form 이용
* Application 폴더안에 Django Form을 담을 수 있는 forms.py 생성

```
from django import forms
from .models import Blog

class BlogForm(forms.Form):
    # 입력받고자 하는 값들
    title = forms.CharField()
    body = forms.CharField(widget=forms.Textarea)
```
* Form을 정의할 수 있는 forms.py을 생성하고 class로써 자동으로 만들 Form을 정의

* Django의 Form을 이용해 BlogForm 생성

* django에서는 widget 을 사용하여 html input 태그를 생성한다.

* widget=forms.Textarea는 body를 textarea로 만들었기 때문에 더 넓은 문자열로 입력을 받기 위해 사용
![form](https://user-images.githubusercontent.com/103200144/169693816-77dfdf42-9bab-4efb-a746-d0bf4952218f.png)


## views.py
```
from django.shortcuts import render, redirect
from .models import Blog
from .forms import BlogForm

# Django Form을 이용해서 입력 값을 받는 함수
# Django Form은 GET, POST 요청 둘 다 처리가 가능
def formcreate(request):
    if request.method == 'POST':
        # 입력내용을 DB에 저장
        form = BlogForm(request.POST)
        if form.is_valid():  # form에 저장한 값이 유효하다면
            # DB에 저장
            post = Blog()
            post.title = form.cleaned_data['title']
            post.body = form.cleaned_data['body']
            post.save()
            return redirect('home')
    else:  # GET 요청
        # 글 작성 HTML 가져다줌
        form = BlogForm()
        return render(request, 'form_create.html', {'form':form})
```
* 위 함수는 GET, POST 요청 둘 다 처리가 가능하다.

* 글 작성 HTML을 갖다주고(GET) 글을 DB에 저장하는(POST) 기능을 다 수행한다.

* if form.is_valid(): 는 앞서 BlogForm 필드들을 Char로 정의했는데 이 형식에 맞지 않는 유효하지 않는 값이 들어올 수도 있으므로 유효한 값만 DB에 저장한다.

* render()의 세 번째 인자로 views.py내의 데이터를 HTML에 넘겨줄 수 있다. 반드시 딕셔너리 자료형으로 넘겨주어야 한다.

* render()의 세 번째 인자로 넘겨준 데이터는 HTML에서 {{ 데이터 }} 로 표현할 수 있다. ( 위에선 form이므로 {{ form }} )

* 파일 업로드까지 한다면 form = BlogForm(request.POST, request.FILES) 로 작성하면 된다.

## 글 작성 페이지 HTML (form_create.html)
```
<h1>Django Form을 이용한 새 글 작성 페이지</h1>
<form action="" method="POST">
    {% csrf_token %}
    <table>
        {{ form.as_table }}
    </table>
    <input type="submit" value="새 글 생성하기">
</form>
```
* {{ form.as_p }} -> p태그가 form을 감싼 것처럼 보임
* 
* {{ form.as_table }} -> table태그가 form을 감싼 것처럼 보임

<br>

# 3. Model Form 이용
* 위의 방법들은 views.py에 실시간으로 객체를 생성해서 입력된 값을 하나하나 넣어주었다.

* Model Form은 Form 자체가 Model을 기반으로 만들어졌기 때문에 더 간편하게 설계할 수 있다.

* (Django Form에서는 Blog 모델 객체를 post변수에 저장해서 사용)

## forms.py에 class로 정의
```
from django import forms
from .models import Blog

class BlogModelForm(forms.ModelForm):
    class Meta:
        model = Blog
        # fields = '__all__'  Blog의 모든 필드
        fields = ['title', 'body']
```

## views.py
```
# Model Form을 이용해서 입력 값을 받는 함수
def modelformcreate(request):
    if request.method == 'POST':
        # 입력내용을 DB에 저장
        form = BlogModelForm(request.POST)
        if form.is_valid():  # form에 저장한 값이 유효하다면
            # DB에 저장
            form.save()
            return redirect('home')
    else:  # GET 요청
        # 글 작성 HTML 가져다줌
        form = BlogModelForm()
        return render(request, 'form_create.html', {'form':form})
```
* views.py의 model = Blog 로 인해 form.save()만으로도 입력된 값을 저장할 수 있다.

* Model Form에서는 form 자체가 모델기반이기 때문에 save()를 사용할 수 있다.

* Django Form에서는 form이 모델기반이 아니기 때문에 save()를 사용하면 에러가 발생한다.

<br>

# Blog 글들을 화면에 띄우기
```
def home(request):
    # 글 모두 띄우기
    posts = Blog.objects.all()  # Blog 객체들을 모조리 가지고 옴

    return render(request, 'index.html', {'posts':posts})  # posts를 index.html에서 활용할 수 있다.
```
```
<h1>My Simple Blog</h1>

{{ posts }}
```
## 결과
![q](https://user-images.githubusercontent.com/103200144/169695842-2ce51ded-e0f9-4d8f-b6bb-89943cfb9cab.png)
* 쿼리셋으로 렌더링 되어 아직 원하는 형태의 모습이 아니다.

## QuerySet
* 데이터베이스로부터 전달받은 객체 목록

```
<h1>My Simple Blog</h1>

{% for post in posts %}
    <h3>제목 : {{ post.title }}</h3>
    <h3>작성날짜 : {{ post.date }}</h3>
{% endfor %}
```
* 위처럼 템플릿 언어의 for문으로 posts의 내용 하나하나를 담아와 찍어주어야 한다.

## 필터
* views.py
```
def home(request):
    # 글 모두 띄우기
    # posts = Blog.objects.all()
    posts = Blog.objects.filter().order_by('-date')
    return render(request, 'index.html', {'posts':posts})
```
* Blog.objects.all()는 그냥 모조리 가지고 온다.
* Blog.objects.filter().order_by('-date') -> date를 기준 내림차순으로 정렬해 가지고 온다. (최근글부터 보이게 됨)

<br>

# 제목을 눌렀을 때 본문 보기
## Primary Key

* Blog 모델에서 Primary Key를 지정해주지 않았기 때문에 Django는 id라고 하는 숨겨진 Primary Key를 넣어준다.

* 이 id는 Blog 객체마다 만들어진 순서에 따라 숫자가 부여된다. (처음 만들어진 Blog 객체는 1)

```
{% for post in posts %}
    <a href=""><h3>{{ post.title }}</h3></a>
    <h3>{{ post.date }}</h3>
    django가 자동으로 만든 Primary Key : {{ post.id }}
{% endfor %}
```
* 실제로 이렇게 확인해보면 Primary Key가 보이게 된다.

* 이 Primary Key를 이용한다. ( 웹주소/detail/primary key => 웹주소/detail/1, 웹주소/detail/2 ... )

# 구현
## index.html 코드 수정
```
<a href="{% url 'detail' post.id %}"><h3>{{ post.title }}</h3></a>
```
* 제목을 눌렀을 때 detail이라고 하는 name을 가지고 있는 url에 이동함과 동시에 post.id 정보도 같이 detail path로 넘어가게 된다.

## urls.py에 아래 코드를 추가
```
path('detail/<int:blog_id>', views.detail, name='detail')
```
* 위 코드는 넘어온 post.id 값은 정수 형태를 띄는데 그 정수를 blog_id라는 변수에 담아서 views.detail 함수에 넘겨준다는 의미이다.

## views.py에서 detail 함수 정의
```
def detail(request, blog_id):
    # blog_id 번째 글을 DB로부터 가지고와 detail.html로 띄워줌
    blog_detail = get_object_or_404(Blog, pk=blog_id)
    return render(request, 'detail.html', {'blog_detail':blog_detail})
```
* django.shortcuts로부터 get_object_or_404를 import 해주어야 한다.

* 위 함수는 pk값을 이용해 특정 모델 객체 하나만 가지고 올 수 있다. 없다면 404

* 앞서 blog_id 변수를 넘겨 받았으므로 인자는 두 개이다.

## detail.html
````
<h1>제목</h1>
{{ blog_detail.title }}

<h2>날짜</h2>
{{ blog_detail.date }}

<h3>본문</h3>
{{ blog_detail.body }}
````

<br>

# 파일 업로드 구현
* settings.py 맨 아래에 다음과 같은 설정을 해주어야 한다.
```
import os

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
```
* MEDIA_ROOT는 파일이 업로드 되었을 때 그 파일이 저장되는 경로
* MEDIA_URL은 파일이 업로드 되었을 때 그 파일에 접근할 수 있는 URL경로

## url.py 
```
from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```
* media 파일을 접근할 수 있는 url도 추가해준다

## Blog 모델에 photo 필드 추가
```
photo = models.ImageField(blank=True, null=True, upload_to='blog_photo')
```
* blank=True, null=True는 비어있는 값을 줘도 된다는 의미 (파일을 올려도 되고 안올려도 됨)

* upload_to='blog_photo'는 MEDIA_ROOT의 경로 폴더안에 blog_photo라는 폴더를 생성하고 그 안에 photo가 추가될 때마다 파일을 저장하겠다는 의미

## photo 필드를 추가했으므로 아래 명령어 수행
```
python manage.py makemigrations
```
```
python manage.py migrate
```
* DB에 변경사항 반영

* admin 사이트에 파일 업로드가 적용되었다

# 파일 업로드를 사용자에게도 보이기
* form_create.html
```
<form action="" method="POST" enctype="multipart/form-data"> 
    {% csrf_token %}
    <table>
        {{ form.as_table }}
    </table>
    <input type="submit" value="새 글 생성하기">
</form>
```
* 파일 업로드을 업로드하기 위해서는 enctype을 위처럼 지정해주어야 함

## views.py 수정
```
if request.method == 'POST' or request.method == 'FILES':
        # 입력내용을 DB에 저장
        form = BlogModelForm(request.POST, request.FILES)
```
* 위 코드처럼 FILES에 관련된 내용을 추가해주어야 한다.

# 사진파일도 사용자 화면에 보이기
## detail.html
```
<!-- photo 데이터가 존재한다면 -->
{% if blog_detail.photo %}  
    {{ blog_detail.photo }}
{% endif %}
```
* 위처럼 코드를 작성하면 사진이 뜨지 않고 사진이 저장된 위치만 뜬다.

## blog_detail.photo.url로 사진 전체 경로를 이용해 띄울 수 있다.
```
<!-- photo 데이터가 존재한다면 -->
{% if blog_detail.photo %}  
    <img src="{{ blog_detail.photo.url }}" alt="">
{% endif %}
```
* blog_detail.photo.path를 한다면 실제 내 컴퓨터상에 저장되어 있는 사진의 경로가 나와 보안에 취약하므로 사용하지 않는다.

# 댓글 구현
## Comment class 
```
class comment(models.Model):
    comment = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now_add=True)
```

* 위와 같이만 코드를 작성한다면 아래 사진과 같이 어떤 게시글에 댓글이 달린지 모를 것이다.

![화면 캡처 2022-05-23 003909](https://user-images.githubusercontent.com/103200144/169703670-257ff18c-8916-4f28-80e2-5931433ab7be.png)

* 따라서 어떤 게시글에 달린 댓글인지를 알아야 한다. -> Blog 객체를 참조하는 FK(Foreign Key)를 만들어주어야 한다.

```
class comment(models.Model):
    comment = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Blog, on_delete=models.CASCADE)
```
* on_delete=CASCADE는 post가 참조하는 대상이 삭제된다면 그 게시글을 참조하고 있는 comment 객체도 삭제된다는 의미

## admin 사이트에서 관리할 수 있도록 아래 코드 추가 (admin.py)
```
admin.site.register(Comment)
```

## forms.py (Model Form)
```
class CommentModelForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']
```

## views.py의 detail 함수 수정 및 추가
```
comment_form = CommentModelForm()

return render(request, 'detail.html', {'blog_detail':blog_detail, 'comment_form':comment_form})
```

## detail.html에 댓글 추가
```
<h3>댓글</h3>
<form method="POST" action="{% url 'create_comment' blog_detail.id %}">
    {% csrf_token %}
    {{ comment_form }}
    <input type="submit">
</form>
```

## urls.py에 추가
```
path('create_comment/<int:blog_id>', views.create_comment, name='create_comment')
```

## create_comment 함수 구현
```
def create_comment(request, blog_id):
    filled_form = CommentModelForm(request.POST)

    if filled_form.is_valid():
        finished_form = filled_form.save(commit=False) 
        finished_form.post = get_object_or_404(Blog, pk=blog_id)  # 어떤 게시글에 댓글이 달렸는지에 대한 정보도 저장
        finished_form.save()

    return render('detail', blog_id)  # blog_id 값을 가지고 있는 detail url로 이동
```
* commit=False는 filled_form을 아직 저장하지말고 대기하라는 의미

## 댓글 목록 추가 (detail.html)
```
{% for comment in blog_detail.comment_set.all %}
    <p>{{ comment }} - ( {{ comment.date }} )</p>
    <hr>
{% endfor %}
```
* blog_detail.comment_set.all은 blog_detail 객체안에 달려있는 (참조하고 있는) comment 집합을 모두 가지고 오라는 의미

# 로그인 구현

## 로그인/로그아웃은 앱을 따로 생성해서 관리하는게 효율적이다.
```
python manage.py startapp accounts
```

## url.py
```
from accounts import views as accounts_views
from blogapp import views
```

* views까지만 쓴다면 views가 두 개이므로 다른 이름을 설정한다.

* 이 방식보다 include로 url을 계층적으로 관리하는 것이 더 효율적이다.

## login 함수 정의
* 이 함수는 POST 요청이 들어오면 login처리, GET 요청이 들어오면 login form을 담고 있는 login.html을 띄워주는 역할

#### views.py
```
from django.shortcuts import redirect, render
from django.contrib import auth
from django.contrib.auth.models import User

def login(request):
    if request.method == 'POST':
        userid = request.POST['username']
        pwd = request.POST['password']
        user = auth.authenticate(request, username=userid, password=pwd)
        if user != None:
            auth.login(request, user)
            return redirect('home')
        else:  # 없는 계정이라면
            return render(request, 'login.html') 
    else:
        return render(request, 'login.html')
```

### Django에서는 로그인/로그아웃을 쉽게 구현할 수 있는 내장 기능이 있다.

```
from django.contrib.auth.models import User
``` 
* django는 models.py에 등록하지 않아도 User라는 객체를 가지고 있다.
```
python manage.py createsuperuser
```
* 위 명령으로 관리자 계정을 만들 수 있었는데 이 계정 정보도 User 객체가 관리

```
from django.contrib import auth
```
* auth는 DB에 이미 있는 유저인지 아닌지 확인해 주는 기능, 로그인/로그아웃 기능 등 여러가지 기능을 보유하고 있다.
```
user = auth.authenticate(request, username=userid, password=pwd)
```
* authenticate는 DB에 이미 있는 유저인지 아닌지 확인한다.

* 이미 있는 유저라면 그 User 객체를 반환하고 없다면 None 반환

```
auth.login(request, user)
```
* user 객체로 로그인한다.

## 로그인이 되었는지 확인
```
{% if user.is_authenticated %}
안녕하세요. {{ user.username }}님

{% else %}
아직 로그인 되지 않았습니다.

{% endif %}
```
* index.html로 로그인이 된 사용자가 request를 보냈다면 블록안 코드 실행

* index.html은 home이므로 사이트에 접속하는 것이 request

### 관리자 계정은 여러 개 만들 수 있으므로 하나 더 만들고 로그인 기능 확인 <br>
![화면 캡처 2022-05-24 152110](https://user-images.githubusercontent.com/103200144/169962604-e48fa514-ac99-46cf-ab0e-f29710b8b818.png)
![화면 캡처 2022-05-24 152135](https://user-images.githubusercontent.com/103200144/169962624-c171eb02-9b97-4304-81b4-937c0cbc0ef4.png)
![화면 캡처 2022-05-24 152147](https://user-images.githubusercontent.com/103200144/169962646-3bda7cad-57ab-4ca2-9973-45c1572e7948.png)

## 로그인 한 상태에서만 새 글 작성 보이기
```
{% if user.is_authenticated %}
<a href="{% url 'modelformcreate' %}">새 글 작성</a><br>
{% endif %}
```

# 로그아웃 구현
```
{% if user.is_authenticated %}
안녕하세요. {{ user.username }}님
<h2><a href="{% url 'logout' %}">로그아웃</a></h2>

{% else %}
아직 로그인 되지 않았습니다.
<h2><a href="{% url 'login' %}">로그인</a></h2>

{% endif %}
```
* 로그인이 된 상태면 로그아웃을 보이고 아니라면 로그인 보이기

## url 추가
```
path('logout/', accounts_views.login, name='logout'),
```

## views.py에 logout 함수 구현
```
def logout(request):
    auth.logout(request)
    return redirect('home')
```

### 로그아웃 기능 확인

* 로그인 된 상태 <br>

![화면 캡처 2022-05-24 153144](https://user-images.githubusercontent.com/103200144/169963987-0a93a187-888f-487f-92e6-c292e2f9d559.png)
* 로그아웃을 누른 후 로그인이 안된 상태 <br>

![화면 캡처 2022-05-24 153153](https://user-images.githubusercontent.com/103200144/169964018-dd965786-9a13-4024-a6cf-ed4010355ce0.png)

## 추가
```
LOGIN_REDIRECTION_URL = "/"
```
* settings.py에 위 코드를 추가하면 로그인을 성공했을 때 / (home) 로 redirect한다.

* views.py에 작성한 redirect와 기능은 동일하다
