import csv
import os
from django.core.management.base import BaseCommand
from phones.models import Phone
from django.utils.text import slugify

class Command(BaseCommand):
    help = 'Импорт телефонов из CSV файла'
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        # путь к файлу phones.csv
        file_path = os.path.join(os.path.dirname(__file__), 'phones.csv')
        file_path = os.path.abspath(file_path)

        print('📁 CSV path:', file_path)

        with open(file_path, newline='', encoding='utf-8-sig') as csvfile:
            # Указываем правильный разделитель
            reader = csv.DictReader(csvfile, delimiter=';')

            # Выводим заголовки для проверки
            print('📄 CSV headers:', reader.fieldnames)

            for row in reader:
                # убираем пробелы вокруг ключей и значений
                row = {k.strip(): v.strip() for k, v in row.items()}

                phone = Phone(
                    id=row['id'],
                    name=row['name'],
                    image=row['image'],
                    price=row['price'],
                    release_date=row['release_date'],
                    lte_exists=row['lte_exists'],
                    slug=slugify(row['name']),
                )
                phone.save()

        self.stdout.write(self.style.SUCCESS('✅ Импорт телефонов успешно завершён!'))
