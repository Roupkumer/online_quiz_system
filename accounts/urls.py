from django.urls import path
from .views import *

app_name = 'accounts'
urlpatterns = [
    path('signup/student/', student_signup, name='student_s'),
    path('signup/teacher/', teacher_signup, name='teacher_s'),

    path('teacher/<int:pk>/', TeacherProfile.as_view(), name='teacher_p'),
    path('student/<int:pk>/', StudentProfile.as_view(), name='student_p'),

    path('teacher/<int:pk>/update/', TeacherUpdate.as_view(), name='teacher_up'),
    path('student/<int:pk>/update/', StudentUpdate.as_view(), name='student_up'),

    path('students/all/', AllStudent.as_view(), name='all_s'),
    path('teachers/all/', AllTeacher.as_view(), name='all_t'),

    path('teacher/<int:teacher_id>/add/', add_notice, name='add_notice'),
    path('teacher/<int:teacher_id>/notice/<int:notice_id>/detail/', notice_detail, name='notice_detail'),

    path('teacher/<int:teacher_id>/notice/<int:notice_id>/question/add/', add_question, name='add_question'),
    path('teacher/<int:teacher_id>/notice/<int:notice_id>/ques/<int:ques_id>/detail/', ques_detail, name='ques_detail'),

    path('teacher/<int:teacher_id>/notice/<int:notice_id>/ques/<int:ques_id>/choice/add/', add_choice,
         name='add_choice'),

    path('teacher/<int:teacher_id>/notice/<int:notice_id>/questionpaper/', ques_paper, name='ques_paper'),

    path('teacher/<int:teacher_id>/notice/<int:notice_id>/save/', savedata, name='savedata'),
    path('teacher/<int:teacher_id>/notice/<int:notice_id>/result/', result, name='result'),
]
