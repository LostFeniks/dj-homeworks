from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters as drf_filters

from .models import Advertisement
from .serializers import AdvertisementSerializer
from .permissions import IsOwnerOrReadCreateOnly
from .filters import AdvertisementFilter

class AdvertisementViewSet(viewsets.ModelViewSet):
    queryset = Advertisement.objects.all().order_by('-created_at')
    serializer_class = AdvertisementSerializer
    permission_classes = [IsOwnerOrReadCreateOnly]  # класс сам разрешает POST для auth пользователей
    filter_backends = [DjangoFilterBackend, drf_filters.OrderingFilter, drf_filters.SearchFilter]
    filterset_class = AdvertisementFilter
    ordering_fields = ['created_at', 'updated_at']
    search_fields = ['title', 'description']

    def get_permissions(self):
        # Для создания требуем аутентификацию
        if self.action == 'create':
            # Создавать могут только авторизованные пользователи
            return [IsAuthenticated()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            # Изменять или удалять может только автор
            return [IsOwnerOrReadCreateOnly()]
            # Для всех остальных действий (list, retrieve) - доступно всем
        return [permissions.AllowAny()]

    def perform_create(self, serializer):
        user = self.request.user
        open_ads_count = Advertisement.objects.filter(creator=user, status='OPEN').count()
        if open_ads_count >= 10:
            raise permissions.PermissionDenied("У вас не может быть больше 10 открытых объявлений.")
        serializer.save(creator=user)

    def destroy(self, request, *args, **kwargs):
        advertisement = self.get_object()
        if advertisement.creator != request.user:
            return Response(
                {"error": "Нельзя удалить чужое объявление."},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().destroy(request, *args, **kwargs)
