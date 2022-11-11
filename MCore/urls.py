from django.urls import path
from . import views

urlpatterns = [
    path('follow', views.follow, name='follow'),
    path('search/', views.SearchEngineView.as_view(), name='search-view'),
    path('users/<str:pk>/',views.UserProfileView.as_view(), name="user-detail-view"),
    path('like-post', views.like_post, name='like-post'),

]