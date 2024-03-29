from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models


# Create your models here.


class Question(models.Model):
    PENDING = 0
    APPROVED = 1
    DECLINED = 2

    STATUS_INTREBARE = (
        (PENDING, 'In asteptare'),
        (APPROVED, 'Aprobata'),
        (DECLINED, 'Respinsa'),
    )
    text = models.CharField(max_length=2048, verbose_name="Intrebarea")
    timestamp = models.DateTimeField(auto_now_add=True)
    owner_oncr_id = models.CharField(max_length=255, verbose_name="ONCR ID", help_text="Dacă nu îți cunoști ONCR ID-ul, întreabă-ți liderul sau șeful de Centru Local. Completând acest câmp îți dai acordul ca numele și Centrul tău Local să fie afișate public, alături de întrebarea ta.")

    owner_name = models.CharField(max_length=255, null=True, blank=True)
    owner_affiliation = models.CharField(max_length=1024, null=True, blank=True)

    approval_status = models.SmallIntegerField(default=PENDING, choices=STATUS_INTREBARE)
    rejection_reason = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.text


class Candidate(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    oncr_id = models.CharField(max_length=20)
    pdf_link = models.URLField()
    motivation = models.TextField()

    photo = models.ImageField(upload_to="img")
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    order = models.IntegerField(default=1)

    class Meta:
        ordering = ["order", ]

    def __str__(self):
        return self.name


class CandidateAnswer(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, models.CASCADE)

    timestamp = models.DateTimeField(auto_now=True)
    text = models.TextField(verbose_name="Raspunsul tau")

    class Meta:
        unique_together = ['candidate', 'question']

    def __str__(self):
        return "[{}] {}".format(self.candidate, self.text)
