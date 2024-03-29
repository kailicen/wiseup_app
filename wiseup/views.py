from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from .models import Question, Answer
from .forms import QuestionForm, AnswerForm
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import View, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db.models import Q
from django.contrib import messages


class QuestionListView(ListView):
    model = Question
    template_name = 'wiseup/home.html'
    context_object_name = 'questions'
    paginate_by = 15

    def get_queryset(self):
        if self.request.user.is_authenticated: 
            user = self.request.user
            if user.profile.if_private == True:
                queryset = Question.objects.exclude(user=user)
            else:
                queryset = Question.objects.all()
        else:
            queryset = Question.objects.all()
        if self.request.GET.get("search"):
            input = self.request.GET.get("search")
            
            queryset = Question.objects.filter(content__icontains=input)
            if not queryset:
                messages.info(self.request, f'No results. Please enter another search term')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_term'] = self.request.GET.get("search")
        return context



class UserQuestionListView(ListView):
    model = Question
    template_name = 'wiseup/user_questions.html'
    context_object_name = 'questions'
    paginate_by = 15

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        queryset = Question.objects.filter(user=user).order_by('-date')
        if self.request.GET.get("search"):
            input = self.request.GET.get("search")
            queryset = Question.objects.filter(user=user, content__icontains=input).order_by('-date')
            if not queryset:
                messages.info(self.request, f'No results. Please enter another search term')
        return queryset

    def get_context_data(self, **kwargs):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        context = super().get_context_data(**kwargs)
        context['display_user'] = user
        context['total_answer_count'] = Answer.objects.filter(user=user).count()
        context['total_question_count'] = Question.objects.filter(user=user).count()
        context['login_user'] = self.request.user
        context['search_term'] = self.request.GET.get("search")
        return context


class UserAnswerListView(ListView):
    model = Answer
    template_name = 'wiseup/user_answers.html'
    context_object_name = 'answers'
    paginate_by = 7

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        queryset = Answer.objects.filter(user=user).order_by('-date')
        if self.request.GET.get("search"):
            input = self.request.GET.get("search")
            queryset = Answer.objects.filter(Q(user=user) & Q(content__icontains=input) | Q(question__content__icontains=input)).order_by('-date')
            if not queryset:
                messages.info(self.request, f'No results. Please enter another search term')
        return queryset

    def get_context_data(self, **kwargs):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        context = super().get_context_data(**kwargs)
        context['questions'] = Question.objects.filter(user=user).order_by('-date')
        context['total_answer_count'] = Answer.objects.filter(user=user).count()
        context['total_question_count'] = Question.objects.filter(user=user).count()
        context['display_user'] = user
        context['login_user'] = self.request.user
        context['search_term'] = self.request.GET.get("search")
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


def about(request):
    return render(request, 'wiseup/about.html')
