# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from django.contrib.admin import ModelAdmin

from questions.models import Candidate, CandidateAnswer, Question


class CandidateAdmin(ModelAdmin):
    list_display = ['name', 'email', 'oncr_id']


class QuestionAdmin(ModelAdmin):
    list_filter = ['approval_status']
    list_display = ['text', 'owner_oncr_id', 'owner_name', 'owner_affiliation', 'approval_status']


class CandidateAnswerAdmin(ModelAdmin):
    list_display = ['question', 'candidate', 'timestamp', 'text']
    list_filter = ['question', 'candidate']


admin.site.register(Candidate, CandidateAdmin)
admin.site.register(CandidateAnswer, CandidateAnswerAdmin)
admin.site.register(Question, QuestionAdmin)