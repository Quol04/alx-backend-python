import django_filters
from .models import Message

class MessageFilter(django_filters.FilterSet):
    """
    Filters for Message model:
    - Filter by participant (sender or receiver)
    - Filter by date range
    """
    user = django_filters.NumberFilter(field_name="sender__id")
    conversation = django_filters.NumberFilter(field_name="conversation__id")
    start_date = django_filters.DateTimeFilter(field_name="created_at", lookup_expr='gte')
    end_date = django_filters.DateTimeFilter(field_name="created_at", lookup_expr='lte')

    class Meta:
        model = Message
        fields = ['user', 'conversation', 'start_date', 'end_date']
