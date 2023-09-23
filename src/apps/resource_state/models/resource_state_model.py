from django.db import models
from ...core.behaviors import Authorable, Timestampable
class ResourceState(Authorable, Timestampable):
    resource_state = models.CharField(max_length=20)
