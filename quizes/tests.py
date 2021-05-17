import random
from django.http import response
from django.test import TestCase, SimpleTestCase, client, testcases
from django.contrib.auth.models import User
from django.urls import reverse, resolve
from quizes.views import QuizListView, quiz_view,quiz_data_view,save_quiz_view,final_results_page
from questions.models import Question, Answer
from results.models import Result
from quizes.models import Quiz
from django.db import models


# Create your tests here.


class ViewTests(TestCase):
    def setUp(self):
        self.question_response = [{'What is the soup':'Hot and sour'},{'Where is pyramid located':'India'},{'Where is Taj mahal located':'India'}]
        self.user = User.objects.create_superuser(
            username="admin",
            password="adminadmin",
            email="admin@example.com")
        self.quiz1 = Quiz.objects.create(
            name = 'Food',
            topic = 'Savoury',
            number_of_questions = '1',
            time = '2',
            required_score_to_pass = '70',
            difficulty = 'easy'
        )
        self.question1 = Question.objects.create(
            text = 'What is the soup',
            quiz= self.quiz1,
            created = models.DateTimeField(auto_now_add=True)
        )

        self.answer1 = Answer.objects.create(
            text = 'Hot and sour',
            correct = True,
            question = self.question1,
            created = models.DateTimeField(auto_now_add=True)     
             )

        self.answer2 = Answer.objects.create(
            text = 'Noodles',
            correct = False,
            question = self.question1,
            created = models.DateTimeField(auto_now_add=True)     
             )

        self.quiz2 = Quiz.objects.create(
            name = 'Travel',
            topic = 'Locations',
            number_of_questions = '2',
            time = '2',
            required_score_to_pass = '70',
            difficulty = 'easy'
        )
        self.question2 = Question.objects.create(
            text = 'Where is pyramid located',
            quiz= self.quiz2,
            created = models.DateTimeField(auto_now_add=True)
        )

        self.answer3 = Answer.objects.create(
            text = 'India',
            correct = False,
            question = self.question2,
            created = models.DateTimeField(auto_now_add=True)     
             )

        self.answer4 = Answer.objects.create(
            text = 'Egypt',
            correct = True,
            question = self.question2,
            created = models.DateTimeField(auto_now_add=True)     
             )

        self.question3 = Question.objects.create(
            text = 'Where is Taj mahal located',
            quiz= self.quiz2,
            created = models.DateTimeField(auto_now_add=True)
        )

        self.answer5 = Answer.objects.create(
            text = 'India',
            correct = True,
            question = self.question3,
            created = models.DateTimeField(auto_now_add=True)     
             )

        self.answer6 = Answer.objects.create(
            text = 'America',
            correct = False,
            question = self.question3,
            created = models.DateTimeField(auto_now_add=True)     
             )


        
        self.quiz_no = Quiz.objects.all().count()
        self.quiz_selector = random.randint(1,self.quiz_no)
        self.quiz_list_selected = [self.quiz1,self.quiz2]
        self.quiz_view_url = reverse('quizes:quiz-view', args=[self.quiz_selector])
        self.quiz_data_view_url = reverse('quizes:quiz_data_view', args=[self.quiz_selector])
        self.save_data_view_url = reverse('quizes:save-view', args=[self.quiz_selector])
        self.final_result_view_url = reverse('quizes:final-result', args=[self.quiz_selector])

        print('no_of_quiz',self.quiz_no)
       
    

    def test_quiz_list_view(self):
        self.client.force_login(self.user)
        response = self.client.get('/')
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response,'quizes/main.html')

    def test_quiz_view(self):
        self.client.force_login(self.user)
        response = self.client.get(self.quiz_view_url)
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response,'quizes/quiz.html')


    def test_quiz_data_view(self):
        self.client.force_login(self.user)
        response = self.client.get(self.quiz_data_view_url)
        self.assertEquals(response.status_code,200)

    def test_save_data_view(self):
        self.save_data_view_data = self.question_response[self.quiz_selector]
        response = self.client.post(self.save_data_view_url,
        {'data' : self.save_data_view_data }
        )
        self.assertEquals(response.status_code,302)


    def test_final_result_page(self):
        self.timer_data = {'minutes':2 ,'seconds':10}
        response = self.client.post(self.final_result_view_url,
        {'data' : self.timer_data})
        self.assertEquals(response.status_code,302)


        


class UrlTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(
            username="admin",
            password="adminadmin",
            email="admin@example.com")
    
    def test_url_is_resolved(self):
        url = reverse('quizes:main-view')
        print(resolve(url))
        self.assertEquals(resolve(url).func.view_class, QuizListView)

    def test_quiz_view_url(self):
        url = reverse('quizes:quiz-view', args=[1])
        self.assertEquals(resolve(url).func, quiz_view)

    def test_quiz_data_view_url(self):
        url = reverse('quizes:quiz_data_view', args=[1])
        self.assertEquals(resolve(url).func, quiz_data_view)

    def test_save_data_view_url(self):
        url = reverse('quizes:save-view', args=[1])
        self.assertEquals(resolve(url).func, save_quiz_view)

    def test_final_result_view_url(self):
        url = reverse('quizes:final-result', args=[1])
        self.assertEquals(resolve(url).func, final_results_page)


class ModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(
            username="admin",
            password="adminadmin",
            email="admin@example.com")

        self.quiz1 = Quiz.objects.create(
                name = 'Food',
                topic = 'Savoury',
                number_of_questions = 1,
                time = '2',
                required_score_to_pass = '70',
                difficulty = 'easy'
            )
        self.question1 = Question.objects.create(
                text = 'What is the soup',
                quiz= self.quiz1,
                created = models.DateTimeField(auto_now_add=True)
            )

        self.answer1 = Answer.objects.create(
                text = 'Hot and sour',
                correct = True,
                question = self.question1,
                created = models.DateTimeField(auto_now_add=True)     
                )

        self.answer2 = Answer.objects.create(
                text = 'Noodles',
                correct = False,
                question = self.question1,
                created = models.DateTimeField(auto_now_add=True)     
                )

        self.quiz2 = Quiz.objects.create(
                name = 'Travel',
                topic = 'Locations',
                number_of_questions = 2,
                time = '2',
                required_score_to_pass = '70',
                difficulty = 'easy'
            )
        self.question2 = Question.objects.create(
                text = 'Where is pyramid located',
                quiz= self.quiz2,
                created = models.DateTimeField(auto_now_add=True)
            )

        self.answer3 = Answer.objects.create(
                text = 'India',
                correct = False,
                question = self.question2,
                created = models.DateTimeField(auto_now_add=True)     
                )

        self.answer4 = Answer.objects.create(
                text = 'Egypt',
                correct = True,
                question = self.question2,
                created = models.DateTimeField(auto_now_add=True)     
                )

        self.question3 = Question.objects.create(
                text = 'Where is Taj mahal located',
                quiz= self.quiz2,
                created = models.DateTimeField(auto_now_add=True)
            )

        self.answer5 = Answer.objects.create(
                text = 'India',
                correct = True,
                question = self.question3,
                created = models.DateTimeField(auto_now_add=True)     
                )

        self.answer6 = Answer.objects.create(
                text = 'America',
                correct = False,
                question = self.question3,
                created = models.DateTimeField(auto_now_add=True)     
                )

        self.quiz_no = Quiz.objects.all().count()
        self.quiz_selector = random.randint(1,self.quiz_no)
        self.quiz_list = [self.quiz1, self.quiz2]


    def test_model_quiz(self):
        self.quiz_object = Quiz.objects.get(pk = self.quiz_selector)
        self.questions_in_quiz = self.quiz_object.number_of_questions
        self.no_of_questions_in_a_quiz1 = self.quiz1.get_questions()
        self.no_of_questions_in_a_quiz2 = self.quiz2.get_questions()
        self.assertEquals(self.questions_in_quiz,self.quiz_list[self.quiz_selector-1].number_of_questions)
        self.assertEquals(len(self.no_of_questions_in_a_quiz1),1)
        self.assertEquals(len(self.no_of_questions_in_a_quiz2),2)

    def test_model_questions(self):
        self.question4 = Question.objects.create(
                text = 'oriental cuisine?',
                quiz= self.quiz1,
                created = models.DateTimeField(auto_now_add=True)
            )
        
        self.question5 = Question.objects.create(
                text = 'Paris has?',
                quiz= self.quiz2,
                created = models.DateTimeField(auto_now_add=True)
            )
        
        if self.quiz_selector == 1:
            self.no_of_questions = Question.objects.filter(quiz = self.quiz1).count()
            self.assertEquals(self.no_of_questions,2)
        else:
            self.no_of_questions = Question.objects.filter(quiz = self.quiz2).count()
            self.assertEquals(self.no_of_questions,3)

    def test_model_answer(self):
        self.answer6 = Answer.objects.create(
                text = 'India',
                correct = True,
                question = self.question2,
                created = models.DateTimeField(auto_now_add=True)     
                )

        self.answer7 = Answer.objects.create(
                text = 'America',
                correct = False,
                question = self.question3,
                created = models.DateTimeField(auto_now_add=True)     
                )
        
        self.no_of_answers_after_creating1 = Answer.objects.filter(question = self.question2).count()
        self.no_of_answers_after_creating2 = Answer.objects.filter(question = self.question3).count()
        self.to_check_true_or_false = Answer.objects.filter(correct = True, question = self.question2).count()
        self.assertEquals(self.no_of_answers_after_creating1,3)
        self.assertEquals(self.no_of_answers_after_creating2,3)
        self.assertEquals(self.to_check_true_or_false,2)

    def test_model_result(self):
        self.result1 = Result.objects.create(
            quiz = self.quiz1,
            user = self.user,
            score = 30,
            answers_selected = 'some string of answer responses'
        )

        self.assertEquals(self.result1.user,self.user)
        self.assertEquals(self.result1.quiz,self.quiz1)


    







