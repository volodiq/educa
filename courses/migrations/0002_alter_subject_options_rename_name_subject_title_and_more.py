# Generated by Django 5.0.4 on 2024-04-06 06:37

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("courses", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="subject",
            options={"ordering": ["title"]},
        ),
        migrations.RenameField(
            model_name="subject",
            old_name="name",
            new_name="title",
        ),
        migrations.CreateModel(
            name="Course",
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
                (
                    "title",
                    models.CharField(max_length=200, verbose_name="Название курса"),
                ),
                ("slug", models.SlugField(max_length=200, verbose_name="Slug курса")),
                ("overview", models.TextField(verbose_name="Описание курса")),
                ("created", models.DateTimeField(auto_now_add=True)),
                (
                    "owner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="courses_created",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Создатель курса",
                    ),
                ),
                (
                    "subject",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="courses",
                        to="courses.subject",
                        verbose_name="Предметы курса",
                    ),
                ),
            ],
            options={
                "ordering": ["-created"],
            },
        ),
        migrations.CreateModel(
            name="Module",
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
                (
                    "title",
                    models.CharField(max_length=200, verbose_name="Заголовок модуля"),
                ),
                ("description", models.TextField(verbose_name="Описание модуля")),
                (
                    "course",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="modules",
                        to="courses.course",
                        verbose_name="Курс модуля",
                    ),
                ),
            ],
        ),
    ]
