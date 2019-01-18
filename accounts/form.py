from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Teacher, Student, Course, Notice, Question, Choice, Result

class TeacherSignUpForm(UserCreationForm):
    class Meta:
        model = Teacher
        fields = ('name', 'email', 'courses', 'image', 'password1', 'password2')


class StudentSignUpForm(UserCreationForm):
    class Meta:
        model = Student
        fields = ('name','email','course_teacher','image','class_roll','exam_roll','registration_no','batch','year', 'password1', 'password2')


class AddCourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = '__all__'


class NoticeForm(forms.ModelForm):
    class Meta:
        model = Notice
        fields = ['title','start_time', 'end_time']


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question_name']


class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['choice_text', 'answer']
