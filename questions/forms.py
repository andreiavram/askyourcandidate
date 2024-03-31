from django_recaptcha.fields import ReCaptchaField
from django.conf import settings
from django.core.exceptions import ValidationError
from django.forms import ModelForm, CharField, Textarea
from django_recaptcha.widgets import ReCaptchaV3, ReCaptchaV2Checkbox

from questions.models import CandidateAnswer, Question
from utils.oncr_client import ONCRClient


class QuestionForm(ModelForm):
    class Meta:
        fields = ['text', 'owner_oncr_id']
        model = Question

    text = CharField(required=True, widget=Textarea, label="Intrebarea")
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)

    def __init__(self, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)
        self.oncr_data = {}

    def clean_owner_oncr_id(self):
        # client = ONCRClient(user=settings.ONCR_USER, password=settings.ONCR_PASSWORD)
        # client.do_login()
        import requests
        baseURL = 'https://membri.scout.ro'
        searchURL = '/api/v1/search-user/'

        headers = {"API-Token": settings.ORGO_APIKEY}
        try:
            users = requests.get("{}{}{}".format(baseURL, searchURL, self.cleaned_data["owner_oncr_id"].upper()), headers=headers)
            detailURL = users.json()[0].get("@id")

            data = requests.get("{}{}".format(baseURL, detailURL), headers=headers)
            groupURL = data.json().get("localCenter").get("@id")

            group = requests.get("{}{}".format(baseURL, groupURL), headers=headers)
            self.oncr_data = {
                "fullName": data.json().get("fullName"),
                "groupName": " ".join((data.json().get("localCenter").get("name"), group.json().get("town").get("name")))
            }

        except Exception:
            raise ValidationError("Nu am gasit un membru cu acest ID")

        return self.cleaned_data['owner_oncr_id']

class CandidateAnswerForm(ModelForm):
    class Meta:
        model = CandidateAnswer
        exclude = ["candidate", "question", "timestamp"]
