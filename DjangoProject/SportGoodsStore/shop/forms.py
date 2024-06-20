from django import forms

from .models import Rating, Comment

SORT_CHOICES = [
    ('asc', 'По возростанию цены'),
    ('desc', 'По убыванию цены'),
]


class ProductFilterForm(forms.Form):
    sort_by = forms.ChoiceField(choices=SORT_CHOICES, required=False, label='Фильтр')


class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['score']
        widgets = {
            'score': forms.RadioSelect(choices=[(i, i) for i in range(1, 6)]),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'placeholder': 'Напишите ваш комментарий здесь...',
                'rows': 4,
                'cols': 50,
                'style': 'resize:vertical;'
            }),
        }