from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.template.loader import render_to_string

from .fields import OrderField


class Subject(models.Model):
    title = models.CharField("Имя предмета", max_length=200)
    slug = models.SlugField("Slug предмета", max_length=200)

    class Meta:
        ordering = ["title"]

    def __str__(self) -> str:
        return self.title


class Course(models.Model):
    owner = models.ForeignKey(
        User,
        related_name="courses_created",
        verbose_name="Создатель курса",
        on_delete=models.CASCADE,
    )
    subject = models.ForeignKey(
        Subject,
        related_name="courses",
        verbose_name="Предметы курса",
        on_delete=models.CASCADE,
    )
    title = models.CharField("Название курса", max_length=200)
    slug = models.SlugField("Slug курса", max_length=200)
    overview = models.TextField("Описание курса")
    created = models.DateTimeField(auto_now_add=True)
    students = models.ManyToManyField(User, related_name="courses_joined", blank=True)

    class Meta:
        ordering = ["-created"]

    def __str__(self) -> str:
        return self.title


class Module(models.Model):
    course = models.ForeignKey(
        Course,
        related_name="modules",
        verbose_name="Курс модуля",
        on_delete=models.CASCADE,
    )
    title = models.CharField("Заголовок модуля", max_length=200)
    description = models.TextField("Описание модуля", blank=True)
    order = OrderField(blank=True, for_fields=["course"])  # type: ignore

    class Meta:  # type: ignore
        ordering = ["order"]

    def __str__(self) -> str:
        return f"{self.order} {self.course}"


class Content(models.Model):
    module = models.ForeignKey(
        Module,
        related_name="contents",
        verbose_name="Контент в модуле",
        on_delete=models.CASCADE,
    )

    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        limit_choices_to={"model__in": ("text, video, file, image")},
    )
    object_id = models.PositiveIntegerField()
    order = OrderField(blank=True, for_fields=["module"])  # type: ignore

    item = GenericForeignKey("content_type", "object_id")

    class Meta:  # type: ignore
        ordering = ["order"]


class BaseItem(models.Model):
    owner = models.ForeignKey(
        User,
        related_name="%(class)s_related",
        verbose_name="Автор элемента",
        on_delete=models.CASCADE,
    )
    title = models.CharField("Название элемента", max_length=250)
    created = models.DateTimeField("Дата добавления элемента", auto_now_add=True)
    updated = models.DateTimeField("Дата обновления элемента", auto_now=True)

    class Meta:  # type: ignore
        abstract = True

    def __str__(self) -> str:
        return self.title

    def render(self):
        return render_to_string(
            f"courses/content/{self._meta.model_name}.html", {"item": self}
        )


class Text(BaseItem):
    content = models.TextField("Текст")


class File(BaseItem):
    content = models.FileField("Файл", upload_to="files")


class Image(BaseItem):
    content = models.ImageField("Изображение", upload_to="images")


class Video(BaseItem):
    content = models.URLField("URL видео")
