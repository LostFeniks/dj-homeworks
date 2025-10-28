from rest_framework import permissions

class IsOwnerOrReadCreateOnly(permissions.BasePermission):
    """
    - Просмотр (GET, HEAD, OPTIONS) — всем.
    - Создание (POST) — только аутентифицированным.
    - Обновление/удаление (PUT/PATCH/DELETE) — только автору объявления.
    """

    def has_permission(self, request, view):
        # Разрешаем просмотр всем
        if request.method in permissions.SAFE_METHODS:
            return True
        # Создавать могут только авторизованные пользователи
        if request.method == 'POST':
            return request.user and request.user.is_authenticated
        # Остальные методы разрешим только на уровне объекта
        return True

    def has_object_permission(self, request, view, obj):
        # Просмотр всем
        if request.method in permissions.SAFE_METHODS:
            return True
        # Изменять и удалять может только автор
        return obj.creator == request.user
