from rest_framework.permissions import BasePermission


class IsEnrolled(BasePermission):
    """Разрешает доступ, если студент зачислен на курс"""

    def has_object_permission(self, request, view, obj):
        return obj.students.filter(id=request.user.id).exists()
