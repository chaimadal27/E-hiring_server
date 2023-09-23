from django.db import models
from ...user_managment.models import Profile
from ..models.activity import Activity
from ..models.activity_type import ActivityType
from ...core.behaviors import Authorable, Timestampable


class Sheet(Authorable, Timestampable):
    coef = models.DecimalField(decimal_places=2, max_digits=2)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, null=True)
    date = models.DateTimeField(null=True)
    is_validated = models.BooleanField(default=False, null=True)
    
    
    class Meta:
        permissions = [
            ('validate_sheet', 'Can validate timesheet'),
            ('invalidate_sheet', 'Can invalidate timesheet')
        ]
