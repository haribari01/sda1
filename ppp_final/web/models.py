from django.db import models

class Evaluation(models.Model):
    order = models.PositiveIntegerField("발표순서")
    name = models.CharField("이름", max_length=50)
    topic = models.CharField("주제", max_length=100)
    report = models.CharField("1장보고서", max_length=200, blank=True)
    rating = models.PositiveIntegerField("평점", default=0)
    score = models.CharField("점수", max_length=10, blank=True)
    best = models.BooleanField("Best", default=False)
    suspected_gpt = models.BooleanField("GPT 의심", default=False)

    def __str__(self):
        return f"{self.order} {self.name}"
