from django.db import models
from django.utils.text import slugify


class Phone(models.Model):
    id = models.AutoField(primary_key=True)  # Основной ключ
    name = models.CharField(max_length=100, verbose_name='Название')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    image = models.URLField(max_length=200, verbose_name='Изображение')
    release_date = models.DateField(verbose_name='Дата выхода')
    lte_exists = models.BooleanField(default=False, verbose_name='Поддержка LTE')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='Слаг')

    def save(self, *args, **kwargs):
        # slug формируется каждый раз из name
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
