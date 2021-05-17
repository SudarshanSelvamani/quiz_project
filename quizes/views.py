from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views import generic
from .models import Quiz
from django.views.generic import ListView
from django.http import JsonResponse
from questions.models import Question, Answer
from results.models import Result,TempResultToStoreBetweenRequests
from django.contrib.auth import authenticate, login, logout
from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.


def register_page(request): #register page rendering
    user = request.user
    if user.is_authenticated:
        return redirect('quizes:main-view')
    form = CreateUserForm                 #for creating custom form
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():                         
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account created successfully for '+user)
            return redirect('quizes:login')
    context = {'form':form}
    return render(request, 'quizes/register.html',context)

def login_page(request):    #login page rendering
    user = request.user
    if user.is_authenticated:
        return redirect('quizes:main-view')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username = username, password = password)
        if user is not None:
            login(request, user)
            return redirect('quizes:main-view')
        else:
            messages.info(request, 'Username or Password is incorrect')
            
    context = {}
    return render(request, 'quizes/login.html',context)

def logout_user(request):  #logout page rendering
    logout(request)
    return redirect('quizes:login')


class QuizListView(LoginRequiredMixin,ListView):   #To list all the quiz available in homepage
    login_url = '/login/'
    model = Quiz
    template_name = 'quizes/main.html'
    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super(QuizListView,self).get_context_data(**kwargs) 
        context['user']= user
        return context  


@login_required(login_url='/login')
def quiz_view(request,pk):                      
    user = request.user 
    session_id = request.session.session_key                        
    TempResultToStoreBetweenRequests.objects.filter(user=user, session_id = session_id).delete()
    quiz = Quiz.objects.get(pk = pk)
    return render(request, 'quizes/quiz.html',{'obj':quiz})

@login_required(login_url='/login')
def quiz_data_view(request, pk):
# the quiz.js handles the get request for this view, takes all the the question which is already randomised to the front end. no matter how many questions are in a quiz, only the specified no of questions are shown to the user
    quiz = Quiz.objects.get(pk = pk)
    question = []
    for q in quiz.get_questions():
        answers = []
        for a in q.get_answers():
            answers.append(a.text)
        question.append({str(q):answers})

    return JsonResponse({'data':question,
        'time':quiz.time})


@login_required(login_url='/login')
def save_quiz_view(request, pk):
#this view involves checking the response given by the user.
    user = request.user
    session_id = request.session.session_key

    score = 0
    questions = []
    if request.is_ajax():
        data = request.POST   #we need to transform querydict to normal data, That is why data_ is declared
        data_ = dict(data.lists())
        data_.pop('csrfmiddlewaretoken')
        for k in data_.keys():
            question = Question.objects.get(text = k)
            questions.append(question)
        
        results = []
        correct_answer = None

        for q in questions:
            a_selected = request.POST.get(q.text)
            
            question_answers = Answer.objects.filter(question=q)
            for a in question_answers:
                if a_selected == a.text:
                    if a.correct:
                        score = 1
                        correct_answer = a.text
                        break
                else:
                    if a.correct:           
                        correct_answer = a.text
            results.append({str(q):{'correct_answer':correct_answer,'answered':a_selected}})
            TempResultToStoreBetweenRequests.objects.create(question_tracker = str(q),user=user,session_id =session_id,correct_answer_tracker= correct_answer,answered_tracker = a_selected, score_tracker = score)
            
        
            
    return JsonResponse({'results':results})


@login_required(login_url='/login')
def final_results_page(request,pk):
# this view handles the final results and create a record on resuts table
    correct_answers_and_answered = []
    score = 0
    user = request.user
    session_id = request.session.session_key
    string_answer = ''
    message =''
    score_and_answers = TempResultToStoreBetweenRequests.objects.filter(user=user, session_id = session_id)
    for obj in score_and_answers:
        dict_of_reponses = {obj.question_tracker:{'correct_answer':obj.correct_answer_tracker,'answered':obj.answered_tracker}}
        score += obj.score_tracker
        correct_answers_and_answered.append(dict_of_reponses)
        
    quiz = Quiz.objects.get(pk = pk)
    multiplier = 100/quiz.number_of_questions
    percent_score = score*multiplier
    if percent_score >= quiz.required_score_to_pass:
        message = 'Congratulations, you passed'
    else:
        message = 'Sorry, try again'


    if request.is_ajax():
        if request.method == 'POST':
            timer_data = request.POST
     
        timer_data_ = dict(timer_data.lists())
        timer_data_str = str(timer_data_['minutes'][0])+':'+str(timer_data_['seconds'][0])

        for question in correct_answers_and_answered:
            for question_name in question.keys():
                string_answer += question[question_name]['answered']
                string_answer += '@#$%'
        
        final_data = {'pk':pk,'quizname':quiz.name,'timerData':timer_data_str,'score':score,'answerSel':correct_answers_and_answered,'percent':round(percent_score,2),'message':message}

        result_update(quiz,user,round(percent_score,2),string_answer,session_id)

    return JsonResponse(final_data)

def result_update(quiz,user,percent_score,string_answer, session_id):
# To create a record on the result table and flush the data on TempResultToStoreBetweenRequests
    Result.objects.create(quiz=quiz,user=user,score=percent_score,answers_selected = string_answer)
    TempResultToStoreBetweenRequests.objects.filter(user=user, session_id = session_id).delete()
    return





