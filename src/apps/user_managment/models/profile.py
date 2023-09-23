from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import ArrayField
from django.apps import apps
from django.contrib.auth.models import AbstractUser
from ...resource_state.models import ResourceState 
from apps.core.behaviors import Authorable, Timestampable

User = get_user_model()

class Profile(Timestampable, Authorable):
    """Profile"""


    civility = models.IntegerField(default=1, null=True)
    phone = models.CharField(max_length=12, null=True, blank=True)
    second_phone = models.CharField(max_length=12, null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.RESTRICT, related_name='profile')
    is_deleted = models.BooleanField(default=False, null=True)
    
    
    other_emails = ArrayField(models.EmailField(max_length = 50, null=True, blank = True, default="email@example.com"), null = True)
    
    # timetracking needed fields
    user_dob = models.DateField(null=True)
    user_city = models.CharField(max_length=50, null=True, default="Gafsa")
    user_postal_code = models.IntegerField(null=True, default=2100)
    user_country = models.CharField(max_length=50, null=True, default="Tunisie")
    tjm = models.DecimalField(decimal_places=2, max_digits=3, null=True, default=1.2)
    devise = models.CharField(max_length=50, null=True, default="euro")
    mobility = models.CharField(max_length=50, null=True, default="anywhere")
    # business_unit = models.ForeignKey('legal_agency.BusinessUnit', on_delete=models.CASCADE, null=True)
    user_state = models.ForeignKey(ResourceState, on_delete = models.PROTECT, null=True)
    is_manager = models.BooleanField(default=False, null=True)
    
    

    

    

    class Meta:
        permissions = [
            ("activate_profile", "Can activate Profile"),
            ("soft_delete_profile", "Can Delete Profile"),
            ("undelete_profile", "Can UnDelete Profile"),
        ]

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"