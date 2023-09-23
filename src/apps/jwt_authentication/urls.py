from django.urls import path

from . import views as core_views

urlpatterns = [
    # auth routes
    path(r'auth/login', core_views.JWTLoginView.as_view()),

    path(r'auth/reset-request', core_views.ForgotPasswordAPIView.as_view()),
    path(r'auth/check-reset-token/<str:token>', core_views.ForgotPasswordAPIView.as_view()),
    path(r'auth/reset', core_views.ResetPasswordAPIView.as_view())
]
