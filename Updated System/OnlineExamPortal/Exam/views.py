import datetime

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ChoiceFormSet, ExamForm, QuestionForm
from .models import Choice, Exam, Question, Result, User
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages

def signup_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        email = request.POST["email"]
        if User.objects.filter(username=username).exists():
            error_message = "Username already exists"
        else:
            user = User.objects.create_user(
                username=username, password=password, email=email
            )
            user.save()
            return redirect("login")
    else:
        error_message = None

    return render(request, "login.html", {"error_message": error_message})


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(user_dashboard)  # Replace with your desired URL
        else:
            error_message = "Invalid username or password"
    else:
        error_message = None

    return render(request, "login.html", {"error_message": error_message})


@login_required(login_url="/exam/login")
def display_exam(request, exam_id):
    exam = get_object_or_404(Exam, pk=exam_id)
    questions = Question.objects.filter(exam=exam)
    question_forms = []

    for question in questions:
        form = QuestionForm(instance=question)
        choice_formset = ChoiceFormSet(instance=question)
        question_forms.append((form, choice_formset))

    context = {
        "exam": exam,
        "question_forms": question_forms,
    }
    print(context)
    return render(request, "create_exam.html", context)


@login_required(login_url="/exam/login")
def submit_exam(request, exam_id):
    exam = get_object_or_404(Exam, pk=exam_id)
    questions = Question.objects.filter(exam=exam)
    selected_choices = []
    if request.method == "POST":
        cnt = 1
        for question in questions:
            choice_id = request.POST.get("question_{}".format(cnt))
            if choice_id:
                choice = Choice.objects.get(pk=choice_id, question_id=question.pk)
                selected_choices.append(choice.text)
            cnt += 1
        request.session["selected_choices"] = selected_choices
    return redirect("exam_results", exam_id=exam_id)


@login_required(login_url="/exam/login")
def exam_results(request, exam_id):
    exam = get_object_or_404(Exam, pk=exam_id)
    questions = Question.objects.filter(exam=exam)
    selected_choices = request.session.get("selected_choices", [])
    # Get correct answers
    correct_answers = []
    for question in questions:
        correct_choice = Choice.objects.filter(
            question=question, is_correct=True
        ).first()
        if correct_choice:
            correct_answers.append(correct_choice.text)
    questions = Question.objects.select_related("exam").filter(exam_id=exam)
    total_questions = len(questions)
    score = 0
    total_marks = 0
    for i in range(len(questions)):
        total_marks += questions[i].marks
        if selected_choices[i].lower() == correct_answers[i].lower():
            score += questions[i].marks

    context = {
        "exam": exam,
        "result": f"Your Score is {score} out of {total_marks} ",
    }
    Result.objects.create(
        user=request.user,
        exam=exam,
        score=score,
        exam_total=total_marks,
        submission_time=datetime.datetime.now(),
    )
    return render(request, "exam_results.html", context)

@login_required(login_url="/exam/login")
def available_exam(request):
    exams = Exam.objects.all()
    print(exams)
    return render(request, "exam_page.html", {"exams": exams})

@login_required(login_url="/exam/login")
def user_dashboard(request):
    return render(request, "user_dashboard.html")

@login_required(login_url="/exam/login")
def previous_scores(request):
    results = Result.objects.filter(user=request.user).order_by("-id")
    return render(request, "previous_exam_score.html", {"results": results})

@login_required(login_url="/exam/login")
def profile_page(request):
    results = User.objects.get(username=request.user.username)
    return render(request, "profile_page.html", {"results": results})

@login_required(login_url='/exam/login')
def change_credentials(request):
    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_username = request.POST['new_username']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        user = User.objects.get(username=request.user.username)

        if user.check_password(current_password):
            if new_username != user.username:
                user.username = new_username
            if new_password:
                if new_password == confirm_password:
                    user.set_password(new_password)
                else:
                    messages.error(request, 'New password and confirm password do not match.')
                    return redirect('change_credentials')
            user.save()
            update_session_auth_hash(request, user)  # Update session with new password
            messages.success(request, 'Username and password successfully changed.')
            return redirect('profile')
        else:
            messages.error(request, 'Incorrect current password.')
            return redirect('change_credentials')

    return render(request, 'change_credentials.html')