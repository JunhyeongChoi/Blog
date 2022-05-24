from django.contrib import admin
from django.urls import path
from accounts import views as accounts_views
from blogapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),

    # HTML Form을 이용해 블로그 객체 생성
    path('new/', views.new, name='new'),
    path('create/', views.create, name='create'),

    # Django Form을 이용해 블로그 객체 생성
    path('formcreate/', views.formcreate, name='formcreate'),

    # Model Form을 이용해 블로그 객체 생성
    path('modelformcreate/', views.modelformcreate, name='modelformcreate'),

    path('detail/<int:blog_id>', views.detail, name='detail'),

    path('create_comment/<int:blog_id>', views.create_comment, name='create_comment'),

    path('login/', accounts_views.login, name='login'),
    path('logout/', accounts_views.logout, name='logout'),
] 

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)