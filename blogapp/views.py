from django.shortcuts import render, redirect, get_object_or_404
from .models import Blog
from django.utils import timezone
from .forms import BlogForm, BlogModelForm, CommentModelForm

def home(request):
    # 글 모두 띄우기
    # posts = Blog.objects.all()
    posts = Blog.objects.filter().order_by('-date')
    return render(request, 'index.html', {'posts':posts})

# 블로그 글 작성 HTML을 보여주는 함수
def new(request):
    return render(request, 'new.html')

# 블로그 글을 저장해주는 함수
def create(request):
    if request.method == 'POST':  # 요청의 method가 POST라면
        post = Blog()
        post.title = request.POST['title']
        post.body = request.POST['body']
        post.date = timezone.now
        post.save()
    return redirect('home')

# Django Form을 이용해서 입력 값을 받는 함수
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

# Model Form을 이용해서 입력 값을 받는 함수
def modelformcreate(request):
    if request.method == 'POST' or request.method == 'FILES':
        # 입력내용을 DB에 저장
        form = BlogModelForm(request.POST, request.FILES)
        if form.is_valid():  # form에 저장한 값이 유효하다면
            # DB에 저장
            form.save()
            return redirect('home')
    else:  # GET 요청
        # 글 작성 HTML 가져다줌
        form = BlogModelForm()
        return render(request, 'form_create.html', {'form':form})

def detail(request, blog_id):
    # blog_id 번째 글을 DB로부터 가지고와 detail.html로 띄워줌
    blog_detail = get_object_or_404(Blog, pk=blog_id)

    comment_form = CommentModelForm()

    return render(request, 'detail.html', {'blog_detail':blog_detail, 'comment_form':comment_form})

def create_comment(request, blog_id):
    filled_form = CommentModelForm(request.POST)

    if filled_form.is_valid():
        finished_form = filled_form.save(commit=False) 
        finished_form.post = get_object_or_404(Blog, pk=blog_id)  # 어떤 게시글에 댓글이 달렸는지에 대한 정보도 저장
        finished_form.save()

    return redirect('detail', blog_id)  # blog_id 값을 가지고 있는 detail url로 이동