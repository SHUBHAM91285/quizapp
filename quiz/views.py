from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from account.models import Profile
from django.contrib import messages
from .models import Quiz,Category
from django.db.models import Q
from quiz.models import QuizSubmission

# Create your views here.
@login_required(login_url='login')
def all_quiz_view(request):
    user_object = User.objects.get(username=request.user)
    user_profile = Profile.objects.get(user=user_object)

    quizzes = Quiz.objects.all().order_by('-created_at')
    categories = Category.objects.all()
    context = {'user_profile':user_profile,'quizzes':quizzes,'categories':categories}
    return render(request,'allquiz.html',context)

@login_required(login_url='login')
def search_view(request,category):
    user_object = User.objects.get(username=request.user)
    user_profile = Profile.objects.get(user=user_object)

    #search by search bar
    if request.GET.get('q') != None:
        q= request.GET.get('q')
        query = Q(title__icontains=q)|Q(description__icontains=q)
        quizzes = Quiz.objects.filter(query).order_by('-created_at')
    #search by category bar
    elif category != " ":
        quizzes = Quiz.objects.filter(category__name=category).order_by('-created_at')
    else:
        quizzes = Quiz.objects.all().order_by('-created_at')
    categories = Category.objects.all()
    context = {'user_profile':user_profile,'quizzes':quizzes,'categories':categories}
    return render(request,'allquiz.html',context)

@login_required(login_url='login')
def quiz_view(request,quiz_id):
    user_object = User.objects.get(username=request.user)
    user_profile = Profile.objects.get(user=user_object)

    quiz = Quiz.objects.filter(id=quiz_id).first()
    total_questions = quiz.question_set.all().count()
    if request.method == "POST":
        score = int(request.POST.get('score',0))
        if QuizSubmission.objects.filter(user=request.user,quiz=quiz).exists():
            messages.success(request,f"This time you got {score} out of {total_questions}")
            return redirect('quiz',quiz_id)
        
        submission = QuizSubmission(user=request.user,quiz=quiz,score=score)
        submission.save()
        messages.success(request,f"Quiz submitted successfully.Your score is {score} out of {total_questions}")
        return redirect('quiz',quiz_id)

    if quiz != None:
        context = {'user_profile':user_profile,'quiz':quiz}
    else:
        return redirect('all_quiz')
    return render(request,'quiz.html',context)