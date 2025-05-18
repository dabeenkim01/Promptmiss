from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    객체의 작성자만 수정/삭제 가능하고, 읽기는 누구나 가능함
    """

    def has_object_permission(self, request, view, obj):
        # SAFE_METHODS: GET, HEAD, OPTIONS 요청은 모두 허용
        if request.method in permissions.SAFE_METHODS:
            return True

        # 그 외 요청은 객체의 작성자와 요청자가 같아야 허용
        return obj.user == request.user