from django import forms

SORT_CHOICES = [
    ('asc', 'По возростанию цены'),
    ('desc', 'По убыванию цены'),
]


class ProductFilterForm(forms.Form):
    sort_by = forms.ChoiceField(choices=SORT_CHOICES, required=False, label='Фильтр')
