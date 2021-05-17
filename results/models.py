from django.db import models
from quizes.models import Quiz
from django.contrib.auth.models import User


# Create your models here.


class Result(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.FloatField()
    answers_selected = models.CharField(max_length=200)

    def __str__(self):
        return str(self.user.username+' got '+str(self.score)+'% in '+self.quiz.name)

class TempResultToStoreBetweenRequests(models.Model):
    question_tracker = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE,null= True)
    session_id = models.CharField(max_length = 200, null=True)
    correct_answer_tracker = models.CharField(max_length = 120)
    answered_tracker = models.CharField(max_length=120)
    score_tracker = models.IntegerField()

    def __str__(self):
        return str(self.user.username+' chose '+str(self.answered_tracker)+' for '+self.question_tracker)
    