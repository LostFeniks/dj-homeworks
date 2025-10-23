from django.shortcuts import render

from articles.models import Article


def articles_list(request):
    template = 'articles/news.html'
    articles = Article.objects.prefetch_related('scopes__tag').all()
    context = {
        'object_list': articles,
    }


    return render(request, template, context)
