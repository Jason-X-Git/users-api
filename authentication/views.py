from authentication.serializers import CustomUserSerializer, CustomPermissionSerializer
from authentication.models import CustomUser, CustomPermission
from rest_framework import routers, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.permissions import AllowAny


@api_view(['GET'])
@permission_classes([AllowAny])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'permissions': reverse('permission-list', request=request, format=format),
    })


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.select_related('custom_permission').all()
    serializer_class = CustomUserSerializer


class CustomPermissionViewSet(viewsets.ModelViewSet):
    queryset = CustomPermission.objects.all()
    serializer_class = CustomPermissionSerializer
