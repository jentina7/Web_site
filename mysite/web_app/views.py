from rest_framework.response import Response
from rest_framework import viewsets, generics, status
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import *
from .serializers import *
from .pagination import CustomPagination
from django_filters.rest_framework import DjangoFilterBackend
from .permission import CheckOwner


class RegisterView(generics.CreateAPIView):
    serializer_class = UserSerializers
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CustomLoginView(TokenObtainPairView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception:
            return Response({"detail": "Неверные учетные данные"}, status=status.HTTP_401_UNAUTHORIZED)

        user = serializer.validated_data
        return Response(serializer.data, status= status.HTTP_200_OK)


class UserProfileListViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileListSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['username']


class UserProfileDetailViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileDetailSerializer

    def get_queryset(self):
        return UserProfile.objects.filter(username=self.request.user.username)


class FollowerViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowerSerializer
    # permission_classes = [IsAuthenticatedOrReadOnly]


class FollowingViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowingSerializer
    # permission_classes = [IsAuthenticatedOrReadOnly]


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['hashtag']
    ordering_fields = ['created_at']


class PostLikeViewSet(viewsets.ModelViewSet):
    queryset = PostLike.objects.all()
    serializer_class = PostLikesSerializer
    # permission_classes = [IsAuthenticatedOrReadOnly]


class PostProfileViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostProfileSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['hashtag']
    ordering_fields = ['created_at']
    # permission_classes = [CheckOwner]


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    # permission_classes = [CheckOwner]


class CommentLikeViewSet(viewsets.ModelViewSet):
    queryset = CommentLike.objects.all()
    serializer_class = CommentLikeSerializer
    # permission_classes = [IsAuthenticatedOrReadOnly]


class StoryViewSet(viewsets.ModelViewSet):
    queryset = Story.objects.all()
    serializer_class = StorySerializer
    # permission_classes = [IsAuthenticated, CheckOwner]


class SaveViewSet(viewsets.ModelViewSet):
    queryset = Save.objects.all()
    serializer_class = SaveSerializer
    # permission_classes = [IsAuthenticated, CheckOwner]


class SaveItemViewSet(viewsets.ModelViewSet):
    queryset = SaveItem.objects.all()
    serializer_class = SaveItemSerializer
    # permission_classes = [IsAuthenticated]