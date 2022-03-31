from django import forms
from .models import Question, Answer
from django.utils.translation import gettext_lazy as _


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['content']
        labels = {
            'content': _('Write down your question...'),
        }
        widgets = {
            'content': forms.Textarea(attrs={'cols': 100, 'rows': 3}),
        }
        

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['content']
        labels = {
            'content': _('What\'s your answer...'),
        }
        widgets = {
            'content': forms.Textarea(attrs={'cols': 100, 'rows': 18}),
        }