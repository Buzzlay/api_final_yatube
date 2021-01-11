from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, filters, mixins
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly
)

from .models import Post, Group
from .serializers import (
    PostSerializer,
    CommentSerializer,
    FollowSerializer,
    GroupSerializer
)
from .permissions import IsAuthorOrReadOnlyPermission


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthorOrReadOnlyPermission]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ('group',)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrReadOnlyPermission]

    def perform_create(self, serializer):
        post = get_object_or_404(
            Post,
            id=self.kwargs.get('post_id')
        )
        serializer.save(
            author=self.request.user,
            post=post,
        )

    def get_queryset(self):
        post = get_object_or_404(
            Post,
            id=self.kwargs.get('post_id')
        )
        return post.comments.all()


class MixinViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    ...


class FollowViewSet(MixinViewSet):
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filterset_fields = ('following', )
    search_fields = ('following__username', 'user__username')

    def get_queryset(self):
        return self.request.user.following.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class GroupViewSet(MixinViewSet):
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Group.objects.all()
