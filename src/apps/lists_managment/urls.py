from django.urls import path

from . import views

urlpatterns = [

    # lists urls
    path(r'lists', views.ListCreateAPIView.as_view()),
    path(r'lists/<int:pk>', views.ListRetrieveUpdateAPIView.as_view()),
    path(r'lists/all', views.AllListsListAPIView.as_view()),
    path(r'lists/<int:pk>/delete', views.ListDeleteAPIView.as_view()),
    
    # option urls
    path(r'options/', views.OptionCreateAPIView.as_view()),
    path(r'options/<int:pk>', views.OptionRetrieveUpdateAPIView.as_view()),
    path(r'options/list', views.AllOptionsBylistList.as_view()),

]
