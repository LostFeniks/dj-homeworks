from django.contrib.auth.models import User
from rest_framework import serializers

from advertisements.models import Advertisement


class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name',)


class AdvertisementSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(read_only=True)
    """Serializer для объявления."""

    creator = UserSerializer(
        read_only=True,
    )

    class Meta:
        model = Advertisement
        fields = ('id', 'title', 'description', 'creator',
                  'status', 'created_at', )

    def create(self, validated_data):
        """Метод для создания"""
        request = self.context.get('request')
        validated_data['author'] = request.user
        return super().create(validated_data)

    def validate(self, data):
        """Метод для валидации. Вызывается при создании и обновлении."""

        request = self.context.get('request')
        user = getattr(request, 'user', None)

        if user is None or not user.is_authenticated:
            return data


        new_status = data.get('status', None)
        if self.instance is None:
            status_to_check = new_status or Advertisement.Status.OPEN
            if status_to_check == Advertisement.Status.OPEN:
                open_ads_count = Advertisement.objects.filter(author=user, status=Advertisement.Status.OPEN).count()
                if open_ads_count >= 10:
                    raise serializers.ValidationError("Нельзя создать более 10 открытых объявлений.")
        else:
            if new_status == Advertisement.Status.OPEN and self.instance.status != Advertisement.Status.OPEN:
                open_ads_count = Advertisement.objects.filter(author=user, status=Advertisement.Status.OPEN).exclude(
                    pk=self.instance.pk).count()
                if open_ads_count >= 10:
                    raise serializers.ValidationError("Нельзя иметь более 10 открытых объявлений.")
        return data
