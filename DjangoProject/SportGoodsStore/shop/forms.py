from django import forms

from .models import Rating, Comment, Wishlist

SORT_CHOICES = [
    ('asc', 'По возростанию цены'),
    ('desc', 'По убыванию цены'),
    ('rating_asc', 'По возрастанию рейтинга'),
    ('rating_desc', 'По убыванию рейтинга'),
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

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.product = kwargs.pop('product', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        if self.user and self.product:
            if Comment.objects.filter(use=self.user, product=self.product).exists():
                raise forms.ValidationError('Вы уже оставили комментарий к этому продукту.')
            return cleaned_data


class WishlistForm(forms.ModelForm):
    class Meta:
        model = Wishlist
        fields = ['product']
