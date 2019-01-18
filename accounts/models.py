from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    username = models.CharField(max_length=50, null=True, blank=True)
    name = models.CharField(max_length=100, blank=False, null=False)
    email = models.EmailField(max_length=100, unique=True)
    image = models.ImageField(blank=True, null=True)
    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = []


class Course(models.Model):
    course_name = models.CharField(max_length=100, blank=False, null=False)
    course_code = models.CharField(max_length=10, blank=False, null=False)

    def __str__(self):
        return self.course_name


class Teacher(User, models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='teacher')
    courses = models.ManyToManyField(Course, related_name='Course')

    def __str__(self):
        return self.name


years = (('11', '1st Year 1st Semester'), ('12', '1st Year 2nd Semester'),
         ('21', '2nd Year 1st Semester'), ('22', '2nd Year 2nd Semester'),
         ('31', '3rd Year 1st Semester'), ('32', '3rd Year 2nd Semester'),
         ('41', '4th Year 1st Semester'), ('42', '4th Year 2nd Semester'),
         ('51', 'Masters 1st Semester'), ('52', 'Masters 2nd Semester'),)


class Student(User, models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='student')
    course_teacher = models.ManyToManyField(Teacher, related_name='Course_Teacher')
    class_roll = models.IntegerField(default=1, blank=False, null=False)
    exam_roll = models.IntegerField(default=123456, blank=False, null=False)
    registration_no = models.IntegerField(default=12345, blank=False, null=False, unique=True)
    batch = models.IntegerField(default=23, blank=False, null=False)
    year = models.CharField(max_length=50, choices=years, default='11')

    def __str__(self):
        return self.name


class Notice(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, null=False, blank=False)
    published_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    start_time = models.DateTimeField(default=timezone.now, null=False, blank=False)
    end_time = models.DateTimeField(default=timezone.now, null=False, blank=False)

    class Meta:
        ordering = ['-published_date']

    def __str__(self):
        return self.title


class Question(models.Model):
    notice = models.ForeignKey(Notice, on_delete=models.CASCADE)
    question_name = models.CharField(max_length=200, null=False, blank=False)

    def __str__(self):
        return self.question_name


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=100, null=False, blank=False)
    answer = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text


class Result(models.Model):
    notice = models.ForeignKey(Notice, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    class_roll = models.IntegerField(default=0)
    exam_roll = models.IntegerField(default=0)
    total = models.IntegerField(default=0)
    ac = models.IntegerField(default=0)
    wrong = models.IntegerField(default=0)
    marks = models.IntegerField(default=0)

    def __str__(self):
        return self.name
