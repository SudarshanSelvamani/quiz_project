from django.urls import path
from .views import (QuizListView,quiz_view, quiz_data_view,save_quiz_view,register_page,login_page,logout_user,final_results_page)

app_name = 'quizes'

urlpatterns = [
    
    path('register/',register_page,name='register'),
    path('login/',login_page,name='login'),
    path('logout/',logout_user,name='logout'),
    path('',QuizListView.as_view(),name='main-view'),
    path('<pk>/',quiz_view,name = 'quiz-view'),
    path('<pk>/data/',quiz_data_view,name = 'quiz_data_view'),
    path('<pk>/save/',save_quiz_view,name = 'save-view'),
    path('<pk>/result/',final_results_page,name='final-result'),
]