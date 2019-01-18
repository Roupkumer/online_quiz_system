from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, DetailView, ListView,UpdateView
from .form import *
from django.contrib.auth import authenticate, login
from django.utils import timezone


def home(request):
    if request.user.is_authenticated:
        if request.user.is_teacher:
            user = Teacher.objects.get(name=request.user.name)
            return render(request, 'home.html', {'t': user})
        elif request.user.is_student:
            user = Student.objects.get(name=request.user.name)
            return render(request, 'home.html', {'stu': user})
    else:
        return render(request, 'home.html', {})


def teacher_signup(request):
    if request.method == 'POST':
        form = TeacherSignUpForm(request.POST, request.FILES or None)
        if form.is_valid():
            teacher = form.save(commit=False)
            teacher.is_teacher = True
            teacher.save()

            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']

            # authenticate user then login
            user = authenticate(email=email, password=password)
            login(request, user)

            return redirect('home')
        else:
            return render(request,'signup.html', {'form': form})
    else:
        form = TeacherSignUpForm()
        return render(request, 'signup.html', {'form': form})


def student_signup(request):
    if request.method == 'POST':
        form = StudentSignUpForm(request.POST, request.FILES or None)
        if form.is_valid():
            student = form.save(commit=False)
            student.is_student = True
            student.save()

            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']

            # authenticate user then login
            user = authenticate(email=email, password=password)
            login(request, user)
            return redirect('home')
        else:
            return render(request,'signup.html', {'form': form})
    else:
        form = StudentSignUpForm()
        return render(request, 'signup.html', {'form': form})


class AllStudent(ListView):
    model = Student
    template_name = 'accounts/all_student.html'
    context_object_name = 'stu'


class AllTeacher(ListView):
    model = Teacher
    template_name = 'accounts/all_teacher.html'
    context_object_name = 'teacher'


class TeacherProfile(DetailView):
    model = Teacher
    template_name = 'accounts/teacher_profile.html'
    context_object_name = 't'


class StudentProfile(DetailView):
    model = Student
    template_name = 'accounts/student_profile.html'
    context_object_name = 's'


class TeacherUpdate(UpdateView):
    model = Teacher
    fields = ['name','email','image','courses']
    template_name = 'accounts/update.html'
    success_url = reverse_lazy('home')


class StudentUpdate(UpdateView):
    model = Student
    fields = ['name', 'email', 'course_teacher', 'image', 'class_roll', 'exam_roll', 'registration_no', 'batch', 'year']
    template_name = 'accounts/update.html'
    success_url = reverse_lazy('home')


def add_notice(request, teacher_id):
    t = get_object_or_404(Teacher, pk=teacher_id)
    if request.method == "POST":
        form = NoticeForm(request.POST)
        if form.is_valid():
            print("form..")
            notice = form.save(commit=False)
            notice.teacher = t
            notice.save()
            print(notice.start_time)
            #return redirect('home')
            return redirect('home')
    else:
        form = NoticeForm()
        return render(request, 'accounts/add_notice_ques_ch.html', {'form': form})


def notice_detail(request, teacher_id, notice_id):
    n = get_object_or_404(Notice, pk=notice_id)

    for q in n.question_set.all():
        print(q.question_name)
    return render(request, 'accounts/notice_detail.html', {'n': n, 'tid': teacher_id, 'nid': notice_id})


def add_question(request, teacher_id, notice_id):
    n = get_object_or_404(Notice, pk=notice_id)
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            ques = form.save(commit=False)
            ques.notice = n
            ques.save()
            return redirect('accounts:notice_detail', teacher_id, notice_id)
    else:
        form = QuestionForm()
        return render(request, 'accounts/add_notice_ques_ch.html', {'form': form})


def ques_detail(request, teacher_id, notice_id, ques_id):
    q = get_object_or_404(Question, pk=ques_id)
    return render(request, 'accounts/question_detail.html',
                  {'q': q, 'tid': teacher_id, 'nid': notice_id, 'qid': ques_id})


def add_choice(request, teacher_id, notice_id, ques_id):
    q = get_object_or_404(Question, pk=ques_id)
    print('testing..')
    print(q.question_name)
    for c in q.choice_set.all():
        print(c.choice_text)
    if request.method == "POST":
        form = ChoiceForm(request.POST)
        if form.is_valid():
            choice = form.save(commit=False)
            choice.question = q
            choice.save()
            return redirect('accounts:ques_detail', teacher_id, notice_id, ques_id)
    else:
        form = ChoiceForm()
        return render(request, 'accounts/add_notice_ques_ch.html', {'form': form})


def ques_paper(request, teacher_id, notice_id):
    notice = get_object_or_404(Notice, pk=notice_id)
    now = timezone.now()
    end_t = notice.end_time
    start_t = notice.start_time
    delay = []
    pro = []
    over = ''
    processing = ''
    de = ''
    al_exam = ''
    user = Student.objects.get(name=request.user.name)
    for r in notice.result_set.all():
        if r.name == user.name:
            al_exam = "Already Completed Exam"
    if now > end_t:
        over = 'Exam Over'
    elif start_t < now and now < end_t:
        processing = "Exam Processing..."
        pro = [end_t.strftime("%m"), end_t.strftime("%d"), end_t.strftime("%H"), end_t.strftime("%M"),
               end_t.strftime("%S")]
    elif now < start_t:
        de = "Exam Delayed"
        delay = [start_t.strftime("%m"), start_t.strftime("%d"), start_t.strftime("%H"), start_t.strftime("%M"),
                 start_t.strftime("%S")]
        print(start_t)

    context = {
        'notice': notice, 'delay': delay, 'over': over, 'pro': pro, 'p': processing, 'de': de, 'tid':teacher_id,'nid':notice_id,'al':al_exam
    }
    return render(request, 'accounts/question_paper.html', context)


def savedata(request, teacher_id, notice_id):

    notice = get_object_or_404(Notice, pk=notice_id)
    user = Student.objects.get(name=request.user.name)

    aclist = []
    ans = []

    for question in notice.question_set.all():
        name = 'choice' + question.question_name
        if name in request.POST:
            choice = question.choice_set.get(pk=request.POST[name])
            ans.append(choice.id)

        for choice in question.choice_set.all():
            if choice.answer >= 1:
                aclist.append(choice.id)

    print(aclist)
    print(ans)

    ac = len(set(aclist) & set(ans))

    print(ac)

    t = len(aclist)
    r = Result()
    r.notice = notice
    r.name = user.name
    r.class_roll = user.class_roll
    r.exam_roll = user.exam_roll
    r.total = t
    r.ac = ac
    r.wrong = t - ac
    r.marks = ac
    r.save()

    print(r.name)

    return redirect('home')


def result(request, teacher_id, notice_id):
    notice = get_object_or_404(Notice, pk=notice_id)
    r = notice.result_set.all()

    return render(request, 'accounts/result.html', {'res': r})