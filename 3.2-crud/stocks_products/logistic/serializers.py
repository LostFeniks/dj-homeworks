from rest_framework import serializers
from .models import Product, Stock, StockProduct


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'description']


class ProductPositionSerializer(serializers.ModelSerializer):
    # Сериализатор для позиции продукта на складе
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = StockProduct
        fields = ['product', 'quantity', 'price']


class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True)

    class Meta:
        model = Stock
        fields = ['id', 'address', 'positions']

    def create(self, validated_data):
        # достаем связанные данные для других таблиц
        positions = validated_data.pop('positions')

        # создаем склад
        stock = super().create(validated_data)

        # заполняем связанную таблицу StockProduct
        for position in positions:
            StockProduct.objects.create(stock=stock, **position)

        return stock

    def update(self, instance, validated_data):
        # достаем связанные данные для других таблиц
        positions = validated_data.pop('positions')

        # обновляем сам склад
        stock = super().update(instance, validated_data)

        # обновляем связанные позиции
        for position in positions:
            product = position.get('product')
            defaults = {
                'quantity': position.get('quantity'),
                'price': position.get('price'),
            }

            # update_or_create — обновляет, если запись есть, иначе создаёт
            StockProduct.objects.update_or_create(
                stock=stock,
                product=product,
                defaults=defaults
            )

        return stock
