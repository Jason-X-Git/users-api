from authentication.views import CustomUserViewSet, CustomPermissionViewSet, api_root
from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path, include

user_list = CustomUserViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

user_detail = CustomUserViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

permission_list = CustomPermissionViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

permission_detail = CustomPermissionViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

urlpatterns = format_suffix_patterns([
    path('', api_root),
    path('permissions/', permission_list, name='permission-list'),
    path('permissions/<int:pk>/', permission_detail, name='permission-detail'),
    path('users/', user_list, name='user-list'),
    path('users/<int:pk>/', user_detail, name='user-detail')
])
