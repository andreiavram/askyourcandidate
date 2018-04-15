from django.forms import ModelForm, CharField, Textarea

from questions.models import CandidateAnswer, Question


class QuestionForm(ModelForm):
    class Meta:
        fields = ['text', 'owner_oncr_id']
        model = Question

    text = CharField(required=True, widget=Textarea, label="Intrebarea")


class CandidateAnswerForm(ModelForm):
    class Meta:
        model = CandidateAnswer
        exclude = ["candidate", "question", "timestamp"]
