from django.contrib import admin
from .models import Article, Tag, Scope
from django.forms import BaseInlineFormSet
from django.core.exceptions import ValidationError

class ScopeInline(admin.TabularInline):
    model = Scope
    extra = 1

class ScopeInlineFormset(BaseInlineFormSet):
    def clean(self):
        super().clean()

        main_count = 0
        for form in self.forms:
            # Пропускаем удалённые формы
            if not hasattr(form, 'cleaned_data') or form.cleaned_data.get('DELETE', False):
                continue
            if form.cleaned_data.get('is_main'):
                main_count += 1

        if main_count == 0:
            raise ValidationError('Должен быть выбран ровно один основной раздел.')
        elif main_count > 1:
            raise ValidationError('Основной раздел может быть только один.')

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [ScopeInline]

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ["name"]
