from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from api.views import PostViewSet, CommentViewSet, FollowViewSet, GroupViewSet

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]


router = DefaultRouter()
router.register(
    r'posts',
    PostViewSet,
    basename='post'
)
router.register(
    r'posts/(?P<post_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)
router.register(
    r'follow',
    FollowViewSet,
    basename='follows'
)
router.register(
    r'group',
    GroupViewSet,
    basename='groups'
)

urlpatterns += [
    path('v1/api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('v1/', include(router.urls)),
]
