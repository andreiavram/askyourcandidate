# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponseRedirect, Http404, HttpResponseForbidden
# Create your views here.
from django.urls import reverse
from django.views.generic import ListView, DetailView, UpdateView, CreateView, RedirectView, TemplateView

from questions.forms import QuestionForm, CandidateAnswerForm
from questions.models import Question, Candidate, CandidateAnswer
from django.contrib import messages


class QuestionList(ListView):
    template_name = "questions/question_list.html"
    model = Question

    def dispatch(self, request, *args, **kwargs):
        self.list_type = int(self.request.GET.get("list_type", Question.APPROVED))
        return super(QuestionList, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return super(QuestionList, self).get_queryset().filter(approval_status=self.list_type).order_by("timestamp")

    def get_context_data(self, **kwargs):
        data = super(QuestionList, self).get_context_data(**kwargs)
        data['rejected_count'] = Question.objects.filter(approval_status=Question.DECLINED).count()
        data['pending_count'] = Question.objects.filter(approval_status=Question.PENDING).count()
        data['approved_count'] = Question.objects.filter(approval_status=Question.APPROVED).count()

        data['list_type'] = self.list_type
        return data


class CandidateList(ListView):
    template_name = "questions/candidate_list.html"
    model = Candidate


class QuestionDetail(DetailView):
    template_name = "questions/question_detail.html"
    model = Question

    def get_queryset(self):
        return super(QuestionDetail, self).get_queryset().filter(approval_status=Question.APPROVED).order_by("timestamp")

    def get_context_data(self, **kwargs):
        data = super(QuestionDetail, self).get_context_data(**kwargs)
        candidates = Candidate.objects.all()
        answers_dict = {a.candidate_id: a for a in CandidateAnswer.objects.filter(question=self.object)}
        qa = {c: answers_dict.get(c.id) for c in candidates}
        data["qa"] = qa
        return data


class CandidateDetail(DetailView):
    template_name = "questions/candidate_detail.html"
    model = Candidate

    def get_context_data(self, **kwargs):
        data = super(CandidateDetail, self).get_context_data(**kwargs)
        questions = Question.objects.filter(approval_status=Question.APPROVED).order_by("timestamp")
        answers_dict = {a.question_id: a for a in CandidateAnswer.objects.filter(candidate=self.object)}
        qa = {q: answers_dict.get(q.id) for q in questions}
        data["qa"] = qa
        return data


class CandidateAnswerQuestion(UserPassesTestMixin, UpdateView):
    template_name = "questions/answer_form.html"
    model = CandidateAnswer
    form_class = CandidateAnswerForm

    def test_func(self):
        return self.request.user.candidate is not None

    def get_object(self, queryset=None):
        try:
            pk = self.kwargs.get(self.pk_url_kwarg)
            try:
                self.question = Question.objects.get(pk=pk)
                self.object, created = CandidateAnswer.objects.get_or_create(question=self.question, candidate=self.request.user.candidate)
                return self.object
            except Question.DoesNotExist:
                raise Http404("Question does not exists")
        except AttributeError:
            return None

    def form_valid(self, form):
        self.object = form.save(commit=True)
        messages.success(self.request, "Raspunsul tau a fost salvat!")
        return HttpResponseRedirect(reverse("questions:candidate_detail", kwargs={"pk": self.object.candidate_id}))

    def get_context_data(self, **kwargs):
        data = super(CandidateAnswerQuestion, self).get_context_data(**kwargs)
        data['question'] = self.question
        return data


class AskQuestion(CreateView):
    template_name = "questions/question_form.html"
    model = Question
    form_class = QuestionForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.approval_status = False
        self.object.save()
        messages.success(self.request, "Intrebarea ta a fost salvata si a mers spre aprobare")
        return HttpResponseRedirect(reverse("questions:index"))


class CandidateRedirect(UserPassesTestMixin, RedirectView):
    def test_func(self):
        return self.request.user.candidate is not None

    def get_redirect_url(self, *args, **kwargs):
        return reverse("questions:candidate_detail", kwargs={"pk": self.request.user.candidate.pk})


class DespreSite(TemplateView):
    template_name = "questions/despre.html"