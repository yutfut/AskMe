from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('hot/', views.hot, name='hot'),
    path('ask/', views.ask, name='ask'),
    path('question/<int:pk>/', views.question, name='question'),
    path('tag/<str:tag>/', views.tag, name='tag'),
    path('settings/', views.settings, name='settings'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
