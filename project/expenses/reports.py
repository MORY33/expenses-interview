from collections import OrderedDict

from django.db.models import Sum, Value, functions as F
from django.db.models.functions import Coalesce


def summary_per_category(queryset):
    return OrderedDict(sorted(
        queryset
        .annotate(category_name=Coalesce('category__name', Value('-')))
        .order_by()
        .values('category_name')
        .annotate(s=Sum('amount'))
        .values_list('category_name', 's')
    ))


def summary_per_year_month(queryset):
    annotated_queryset = queryset.annotate(
        year=F.ExtractYear('date'),
        month=F.ExtractMonth('date')
    )
    aggregated_data = annotated_queryset.values('year', 'month').annotate(
        total=Sum('amount')
    ).order_by('year', 'month')
    summary = OrderedDict()
    for entry in aggregated_data:
        year_month = (entry['year'], entry['month'])
        summary[year_month] = entry['total']

    return summary


def summary_total(queryset):
    total = queryset.aggregate(total_amount=Sum('amount'))['total_amount']
    return total if total is not None else 0
