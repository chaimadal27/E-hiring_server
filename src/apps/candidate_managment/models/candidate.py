# django lib
from django.db import models
from django.conf import settings
from django.contrib.postgres.fields import ArrayField
# custom lib
from apps.core.behaviors import Authorable, Timestampable
from apps.core.models import User
from apps.referentiel_managment.models import School,Company



class Candidate(Authorable, Timestampable):
    """Candidate"""
    # part1
    source=models.IntegerField(null=True, blank=True)
    rating=models.IntegerField(null=True, blank=True)
    linkedin_link=models.CharField(max_length=200, null=True, blank=True)
    key_words= ArrayField(models.CharField(max_length=200,blank=True),blank=True,null=True)
    civility=models.IntegerField(null=True, blank=True)
    first_name_fr = models.CharField(max_length=50, null=True, blank=True)
    # first_name_ar = models.CharField(max_length=50, null=True, blank=True)
    last_name_fr = models.CharField(max_length=50, null=True, blank=True)
    # last_name_ar = models.CharField(max_length=50, null=True, blank=True)
    status=models.IntegerField(choices=settings.STATUS_CANDIDATE, default=settings.NEW_STATUS, null=True,blank=True)
    email = models.EmailField(blank=False, null=False,unique=True)
    birth_date = models.DateField(blank=True, null=True)
    first_phone = models.CharField(max_length=30, blank=True, null=True)
    second_phone= models.CharField(max_length=30, blank=True, null=True)
    # photo = models.ImageField(upload_to="Candidate/photo", blank=True, null=True)
    address = models.CharField(max_length=300, blank=True, null=True)
    postal_code=models.IntegerField(null=True, blank=True)
    city = models.CharField(max_length=200, blank=True, null=True)
    country = models.CharField(max_length=300, blank=True, null=True)
    family_situation=models.IntegerField(null=True, blank=True)

    # part2
    education_level=models.IntegerField(null=True, blank=True)
    school=models.ForeignKey(School, on_delete=models.RESTRICT,null=True,blank=True)
    speciality=models.IntegerField(null=True, blank=True)
    function=models.IntegerField(null=True, blank=True)
    first_employment_date=models.DateField(blank=True, null=True)
    seniority=models.IntegerField(null=True, blank=True)
    current_employer=models.ForeignKey(Company, on_delete=models.RESTRICT,blank=True,null=True)
    contract_type=models.IntegerField(null=True, blank=True)
    current_salary=models.IntegerField(null=True, blank=True)
    current_devise=models.IntegerField(null=True, blank=True)
    current_benefits=models.TextField(null=True, blank=True)
    desired_salary=models.IntegerField(null=True, blank=True)
    desired_devise = models.IntegerField(null=True, blank=True)
    disponibility = models.IntegerField(null=True, blank=True)
    years_of_experience= models.IntegerField(null=True, blank=True)
    mobility = models.IntegerField(null=True, blank=True)
    comment=models.TextField(null=True, blank=True)

    # Foreign Keys
    user = models.ForeignKey(User, on_delete=models.RESTRICT, blank=True, null=True)

    def __str__(self):
        return f"{self.first_name_fr} {self.last_name_fr}"