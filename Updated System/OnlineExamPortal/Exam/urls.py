# from rest_framework_simplejwt import views as jwt_views
from django.urls import include, path
from django.contrib.auth import views as auth_views

from .views import *

urlpatterns = [
    path('login/', login_view, name='login'),
    path('signup/', signup_view, name='signup'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('create/<int:exam_id>/', display_exam, name='display_exam'),
    path('create/<int:exam_id>/submit/', submit_exam, name='submit_exam'),
    path('create/<int:exam_id>/results/', exam_results, name='exam_results'),
    path('available_exam', available_exam, name='available_exams'),
    path('user_dashboard', user_dashboard, name='available_exams'),
    path('previous_exam_result', previous_scores, name='previous_scores'),
    path('profile_page', profile_page, name='profile_page'),
    path('change_credentials', change_credentials, name='change_credentials'),
]
