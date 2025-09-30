from django.shortcuts import render
from django.http import HttpResponse

DATA = {
    'omlet': {'яйца, шт': 2, 'молоко, л': 0.1, 'соль, ч.л.': 0.5},
    'pasta': {'макароны, г': 300, 'сыр, г': 50},
}

def recipe_view(request, recipe_name):
    servings = request.GET.get('servings', 1)
    try:
        servings = int(servings)
        if servings < 1:
            servings = 1
    except ValueError:
        servings = 1

    recipe = DATA.get(recipe_name)
    if not recipe:
        return HttpResponse("Рецепт не найден", status=404)

    adjusted_recipe = {k: v * servings for k, v in recipe.items()}
    return render(request, 'calculator/recipe.html', {'recipe': adjusted_recipe})
