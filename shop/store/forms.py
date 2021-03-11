from django import forms

from store.models import Products


class PostForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = ["title", "author_name", "description", "pages_count"]