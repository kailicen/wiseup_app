from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from .models import Question, Answer, Resource
from .forms import QuestionForm, AnswerForm
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import View, ListView, DetailView, CreateView, UpdateView, DeleteView


class QuestionListView(ListView):
    model = Question
    template_name = 'wiseup/home.html'
    context_object_name = 'questions'
    paginate_by = 10

    def get_queryset(self):
        queryset = Question.objects.all()
        if self.request.GET.get("search"):
            input = self.request.GET.get("search")
            queryset = Question.objects.filter(content__icontains=input)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_term'] = self.request.GET.get("search").lower
        return context



class UserQuestionListView(ListView):
    model = Question
    template_name = 'wiseup/user_questions.html'
    context_object_name = 'questions'
    paginate_by = 10

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Question.objects.filter(user=user).order_by('-date')

    def get_context_data(self, **kwargs):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        context = super().get_context_data(**kwargs)
        context['user'] = user
        context['answers'] = Answer.objects.filter(user=user).order_by('-date')
        context['owner'] = self.request.user
        return context


class UserAnswerListView(ListView):
    model = Answer
    template_name = 'wiseup/user_answers.html'
    context_object_name = 'answers'
    paginate_by = 7

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Answer.objects.filter(user=user).order_by('-date')

    def get_context_data(self, **kwargs):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        context = super().get_context_data(**kwargs)
        context['questions'] = Question.objects.filter(user=user).order_by('-date')
        context['user'] = user
        context['owner'] = self.request.user
        return context


class QuestionDetailView(DetailView):
    model = Question


class QuestionCreateView(LoginRequiredMixin, CreateView):
    form_class = QuestionForm
    model = Question
    template_name = 'wiseup/create_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class AnswerCreateView(LoginRequiredMixin, CreateView):
    form_class = AnswerForm
    model = Answer
    template_name = 'wiseup/create_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.question = Question.objects.get(pk=self.kwargs['pk'])
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['question'] = Question.objects.get(pk=self.kwargs['pk'])
        return context


class QuestionUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    form_class = QuestionForm
    model = Question
    template_name = 'wiseup/update_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        question = self.get_object()
        if self.request.user == question.user:
            return True
        return False


class AnswerUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    form_class = AnswerForm
    model = Answer
    template_name = 'wiseup/update_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        answer = self.get_object()
        if self.request.user == answer.user:
            return True
        return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        answer = self.get_object()
        context['question'] = answer.question
        return context


class QuestionDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Question
    success_url = '/'

    def test_func(self):
        question = self.get_object()
        if self.request.user == question.user:
            return True
        return False


class AnswerDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Answer

    def test_func(self):
        answer = self.get_object()
        if self.request.user == answer.user:
            return True
        return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        answer = self.get_object()
        context['question'] = answer.question
        return context
    
    def get_success_url(self):
        return reverse_lazy('question-detail', kwargs={'pk':self.get_object().question.id})


def resources(request):
    return render(request, 'wiseup/resources.html')

def questions(request):
    return render(request, 'me/questions.html')

def answers(request):
    return render(request, 'me/answers.html')
