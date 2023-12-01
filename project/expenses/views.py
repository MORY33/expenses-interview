from django.views.generic.list import ListView
from django.db.models import Count

from .forms import ExpenseSearchForm
from .models import Expense, Category
from .reports import summary_per_category, summary_total, summary_per_year_month


class ExpenseListView(ListView):
    model = Expense
    paginate_by = 5

    def get_queryset(self):
        """ Filter and return queryset depending on input data"""
        queryset = super().get_queryset()
        form = self.get_search_form()

        if form.is_valid():
            queryset = self.apply_filters(queryset, form)
            queryset = self.apply_sorting(queryset, form.cleaned_data.get('sort_by'))

        return queryset

    def get_search_form(self):
        return ExpenseSearchForm(self.request.GET or None)

    @staticmethod
    def apply_filters(queryset, form):
        """ Apply filters depending on diff options"""
        name = form.cleaned_data.get('name', '').strip()
        if name:
            queryset = queryset.filter(name__icontains=name)

        date_from = form.cleaned_data.get('date_from')
        date_to = form.cleaned_data.get('date_to')
        if date_from and date_to:
            queryset = queryset.filter(date__range=[date_from, date_to])
        elif date_from:
            queryset = queryset.filter(date__gte=date_from)
        elif date_to:
            queryset = queryset.filter(date__lte=date_to)

        categories = form.cleaned_data.get('categories')
        if categories:
            queryset = queryset.filter(category__in=categories)

        return queryset

    @staticmethod
    def apply_sorting(queryset, sort_by):
        sort_options = {
            'date_asc': 'date',
            'date_desc': '-date',
            'category_asc': 'category__name',
            'category_desc': '-category__name',
        }
        return queryset.order_by(sort_options.get(sort_by, 'date'))  # default sorting when not choosen

    def get_context_data(self, **kwargs):
        """ Build context """
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()
        context['form'] = self.get_search_form()
        context['summary_per_category'] = summary_per_category(queryset)
        context['total_amount'] = summary_total(queryset)
        context['summary_per_year_month'] = summary_per_year_month(queryset)
        return context

class CategoryListView(ListView):
    model = Category
    paginate_by = 5

    def get_queryset(self):
        return Category.objects.annotate(expenses_count=Count('expense'))