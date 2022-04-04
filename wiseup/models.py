from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Question(models.Model):
    content = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return self.content
    
    def get_absolute_url(self):
        return reverse('question-detail', kwargs={'pk': self.pk})

class Answer(models.Model):
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return "%s - %s" % (self.question, self.user)

    def get_absolute_url(self):
        return reverse('question-detail', kwargs={'pk': self.question.id})