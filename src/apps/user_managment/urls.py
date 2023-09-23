from django.urls import path

from . import views as core_views


urlpatterns = [

    # profile routes
    path(r'users/', core_views.UserListCreateAPIView.as_view()),
    path(r'users/admins/', core_views.DisplayAdminUsers.as_view()),
    path(r'users/all', core_views.ALLUserListAPIView.as_view()),
    path(r'users/cps', core_views.ALLCPSListAPIView.as_view()),
    path(r'user/<int:pk>', core_views.UserRetrieveUpdateAPIView.as_view()),
    path(r'user/<int:pk>/activate', core_views.UserActivateAPIView.as_view()),
    path(r'user/<int:pk>/deactivate', core_views.UserDeactivateAPIView.as_view()),
    path(r'user/<int:pk>/delete', core_views.UserDeleteAPIView.as_view()),
    path(r'user/<int:pk>/undelete', core_views.UserUnDeleteAPIView.as_view()),

    path(r'users/activate', core_views.UserActivateAPIView.as_view()),
    path(r'users/deactivate', core_views.UserDeactivateAPIView.as_view()),
    path(r'users/delete', core_views.UserDeleteAPIView.as_view()),
    path(r'users/undelete', core_views.UserUnDeleteAPIView.as_view()),

    path(r'myself', core_views.MyProfileRetrieveUpdateAPIView.as_view()),
    path(r'myself/reset-password',
         core_views.MyProfileUpdatePasswordAPIView.as_view()),

    # Groups/Permissions routes
    path(r'groups', core_views.GroupListCreateAPIView.as_view()),
    path(r'groups/all', core_views.ALLGroupListAPIView.as_view()),
    path(r'group/<int:pk>', core_views.GroupRetrieveUpdateDestroyAPIView.as_view()),

    # Permissions routes
    path(r'permissions', core_views.PermissionListAPIView.as_view()),

    # managers
    path(r'manager', core_views.ManagerAPIView.as_view()),
    path(r'group/show/<int:pk>/', core_views.GroupRetrieveAPIView.as_view()),




    # testing new api

]
