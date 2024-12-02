from django import forms
from django.contrib.auth.models import User
from .models import Recipe
from .models import Category

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'description', 'steps', 'cooking_time', 'image', 'categories']

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password', 'email']

class RecipeSearchForm(forms.Form):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=False)
