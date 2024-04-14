from django.urls import include, path
from rest_framework import routers

from .views import (CourseEnrollView, CourseViewSet, SubjectDetailView,
                    SubjectListView)

router = routers.DefaultRouter()
router.register("courses", CourseViewSet)

app_name = "courses"

urlpatterns = [
    path("subjects/", SubjectListView.as_view(), name="subject_list"),
    path("subject/<int:pk>/", SubjectDetailView.as_view(), name="subject_detail"),
    path(
        "course/<int:course_pk>/enroll/",
        CourseEnrollView.as_view(),
        name="course_enroll",
    ),
    # API
    path("", include(router.urls)),
]
