from django import forms
from .models import Expense, Category
from django.forms.widgets import SelectDateWidget
from datetime import datetime


class ExpenseSearchForm(forms.ModelForm):
    current_year = datetime.now().year
    start_year = 2000
    date_from = forms.DateField(
        required=False,
        widget=SelectDateWidget(years=range(start_year, current_year + 1))
    )
    date_to = forms.DateField(
        required=False,
        widget=SelectDateWidget(years=range(start_year, current_year + 1))
    )
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )
    sort_by = forms.ChoiceField(choices=[
        ('date_asc', 'Date Ascending'),
        ('date_desc', 'Date Descending'),
        ('category_asc', 'Category Ascending'),
        ('category_desc', 'Category Descending')
    ], required=False)

    class Meta:
        model = Expense
        fields = ('name', 'date_from', 'date_to', 'categories', 'sort_by')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].required = False
