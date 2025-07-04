# Generated by Django 5.2.2 on 2025-06-10 05:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Evaluation",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("order", models.PositiveIntegerField(verbose_name="발표순서")),
                ("name", models.CharField(max_length=50, verbose_name="이름")),
                ("topic", models.CharField(max_length=100, verbose_name="주제")),
                (
                    "report",
                    models.CharField(
                        blank=True, max_length=200, verbose_name="1장보고서"
                    ),
                ),
                ("rating", models.PositiveIntegerField(default=0, verbose_name="평점")),
                (
                    "score",
                    models.CharField(blank=True, max_length=10, verbose_name="점수"),
                ),
                ("best", models.BooleanField(default=False, verbose_name="Best")),
                (
                    "suspected_gpt",
                    models.BooleanField(default=False, verbose_name="GPT 의심"),
                ),
            ],
        ),
    ]
