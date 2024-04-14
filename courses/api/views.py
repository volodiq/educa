from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.authentication import BasicAuthentication
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action

from .permissions import IsEnrolled
from courses.models import Course, Subject
from .serializers import CourseSerializer, SubjectSerializer, CourseWithContentsSerializer


class CourseViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    @action(methods=["get"], detail=True, serializer_class=CourseWithContentsSerializer, authentication_classes=[BasicAuthentication], permission_classes=[IsAuthenticated, IsEnrolled])
    def contents(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class SubjectListView(ListAPIView):
    serializer_class = SubjectSerializer
    queryset = Subject.objects.all()


class SubjectDetailView(RetrieveAPIView):
    serializer_class = SubjectSerializer
    queryset = Subject.objects.all()


class CourseEnrollView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, course_pk, format=None):
        course = get_object_or_404(Course, pk=course_pk)
        course.students.add(request.user)
        return Response({"enrolled": True})


