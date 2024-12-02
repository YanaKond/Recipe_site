from django.shortcuts import render, get_object_or_404, redirect
from .forms import UserRegistrationForm
from django.contrib.auth import login
from .models import Recipe
from .forms import RecipeForm
from django.contrib.auth.decorators import login_required
from .forms import RecipeSearchForm

def index(request):
    if request.GET.get('my_recipes'):
        recipes = Recipe.objects.filter(author=request.user)
    else:
        recipes = Recipe.objects.all()

    return render(request, 'recipes/index.html', {'recipes': recipes})

def recipe_detail(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    return render(request, 'recipes/recipe_detail.html', {'recipe': recipe})

@login_required
def my_recipes(request):
    if request.user.is_authenticated:
        recipes = Recipe.objects.filter(author=request.user)
    else:
        recipes = []

    return render(request, 'recipes/my_recipes.html', {'recipes': recipes})


@login_required
def add_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            form.save_m2m()
            return redirect('recipe_detail', pk=recipe.pk)
    else:
        form = RecipeForm()
    return render(request, 'recipes/recipe_form.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def edit_recipe(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)

    if recipe.author != request.user:
        return redirect('my_recipes')

    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        if form.is_valid():
            form.save()
            return redirect('recipe_detail', pk=recipe.pk)
    else:
        form = RecipeForm(instance=recipe)

    return render(request, 'recipes/recipe_form.html', {'form': form})

