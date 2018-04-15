from django.conf.urls import url

from questions.views import QuestionList, AskQuestion, QuestionDetail, CandidateDetail, CandidateAnswerQuestion, \
    CandidateList, CandidateRedirect, DespreSite

urlpatterns = [
    url(r'^$', QuestionList.as_view(), name="index"),
    url(r'question/ask/$', AskQuestion.as_view(), name="question_ask"),
    url(r'question/(?P<pk>\d+)/$', QuestionDetail.as_view(), name="question_detail"),
    url(r'candidate/(?P<pk>\d+)/$', CandidateDetail.as_view(), name="candidate_detail"),
    url(r'candidate/$', CandidateList.as_view(), name="candidate_list"),
    url(r'candidate/own/$', CandidateRedirect.as_view(), name="candidate_redirect"),
    url(r'question/(?P<pk>\d+)/answer/$', CandidateAnswerQuestion.as_view(), name="question_answer"),
    url(r'despre/$', DespreSite.as_view(), name="despre"),
]
