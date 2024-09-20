import datetime

from django.utils import timezone

today = timezone.now().date()

# Calculate the Monday of the current week
monday = today - datetime.timedelta(days=today.weekday())
print(monday)